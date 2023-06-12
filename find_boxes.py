import numpy as np
import cv2
from PIL import Image
import matplotlib
import matplotlib.pyplot as plt
import warnings
import time
import tensorflow as tf
import sys
sys.path.append("models/resdearch/object_detection") #add path to built object_detection lib  
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as viz_utils
import pathlib
import csv
import sys
import os
import pandas as pd

def load_model(PATH_TO_SAVED_MODEL):
    """
    Load saved model from input directory 
    """
    print('Loading model...', end='')

    start_time = time.time()
    # Load saved model and build the detection function
    detect_fn = tf.saved_model.load(PATH_TO_SAVED_MODEL)

    end_time = time.time()
    elapsed_time = end_time - start_time

    print('Done! Took {} seconds'.format(elapsed_time))

    return detect_fn

def load_category(PATH_TO_LABELS):
    """
    Load index labels from label map
    """
    category_index = label_map_util.create_category_index_from_labelmap(PATH_TO_LABELS,
                                                                        use_display_name=True)
    return category_index 

def load_image_into_numpy_array(path):
    """Load an image from file into a numpy array.

    Puts image into numpy array to feed into tensorflow graph.
    Note that by convention we put it into a numpy array with shape
    (height, width, channels), where channels=3 for RGB.

    Args:
      path: the file path to the image

    Returns:
      uint8 numpy array with shape (img_height, img_width, 3)
    """
    return cv2.imread(str(path))

def remove_overlap(boxes_positions,boxes_scores):

    boxes_passing_OR = [ True for x in range(len(boxes_scores)) ]
    
    for i1,b1 in enumerate(boxes_positions):
        b1_size = (b1[2]-b1[0])*(b1[3]-b1[1])
        for i2,b2 in enumerate(boxes_positions[i1+1:]):
            i2=i1+i2+1
            b2_size = (b2[2]-b2[0])*(b2[3]-b2[1])
            overlap=0
            dx = min(b1[2], b2[2]) - max(b1[0], b2[0])
            dy = min(b1[3], b2[3]) - max(b1[1], b2[1])
            if (dx>=0) and (dy>=0):
                overlap = dx*dy
                if (overlap/b1_size > 0.5 or overlap/b2_size > 0.5):
                    #print("overalp {}-{}".format(i1,i2))
                    #print("        scores {}-{}".format(boxes_scores[i1],boxes_scores[i2]))
                    if (boxes_scores[i1] > boxes_scores[i2]):
                        boxes_passing_OR[i2] = False
                    else:
                        boxes_passing_OR[i1] = False

    return boxes_passing_OR          
                      
                    

def process_images(IMAGE_PATH,
                   PATH_TO_MODEL_DIR,
                   LABEL_FILENAME,
                   PATH_TO_LABELS,
                   PATH_TO_SAVED_MODEL,
                   SCALE=1.7654):
    """Process image to derive boundry areas around RoIs

    Args:
        IMAGE_PATH
        PATH_TO_MODEL_DIR
        LABEL_FILENAME
        PATH_TO_LABELS
        PATH_TO_SAVED_MODEL
        SCALE

    Returns:
      uint8 numpy array with shape (img_height, img_width, 3)
    """
    #load saved model
    detect_fn = load_model(PATH_TO_SAVED_MODEL)
    #load saved labels from map
    category_index = load_category(PATH_TO_LABELS)

    # make good boxes dictionary
    good_boxes={}
    num_good_boxes=0
    for idx, image_path in enumerate(IMAGE_PATH):
        print ('Running inference for {}... '.format(image_path))
        image_np = load_image_into_numpy_array(image_path)
        # The input needs to be a tensor, convert it using `tf.convert_to_tensor`.
        input_tensor = tf.convert_to_tensor(image_np)
        # The model expects a batch of images, so add an axis with `tf.newaxis`.
        input_tensor = input_tensor[tf.newaxis, ...]

        detections = detect_fn(input_tensor)

        # All outputs are batches tensors.
        # Convert to numpy arrays, and take index [0] to remove the batch dimension.
        # We're only interested in the first num_detections.
        num_detections = int(detections.pop('num_detections'))

        detections = {key: value[0, :num_detections].numpy()
                   for key, value in detections.items()}
        detections['num_detections'] = num_detections
    
        # detection_classes should be ints.
        detections['detection_classes'] = detections['detection_classes'].astype(np.int64)
    
        image_np_with_detections = image_np.copy()
    

        #threshold value to accept
        threshold = 0.02

        #  retrieve good boxes #
        print ("Searches for good boxes...",end='')
        ind = detections['detection_scores'] > threshold
        # perform overlap removal procedure # 
        boxes_passing_OR = remove_overlap(detections['detection_boxes'],
                                              detections['detection_scores'])
        for p in range(len(detections['detection_scores'])):
            if ( ind[p] and  boxes_passing_OR[p] ):
                ind[p] = True
            else:
                ind[p] = False
        
        ## making image with detections ##
        viz_utils.visualize_boxes_and_labels_on_image_array(
            image_np_with_detections,
            detections['detection_boxes'][ind],
            detections['detection_classes'][ind],
            detections['detection_scores'][ind],
            category_index,
            use_normalized_coordinates=True,
            max_boxes_to_draw=200,
            min_score_thresh=threshold,
            agnostic_mode=False)

        ## saving image ##
        plt.figure(figsize=(image_np_with_detections.shape[0]/72, image_np_with_detections.shape[1]/72), dpi=72,frameon=False)
        NAME=os.path.basename(image_path)
        NAME=NAME[:NAME.find('.')]
        print('Saving figure to : output/images/{}...'.format(NAME),end='')
        plt.imshow(image_np_with_detections)
        plt.savefig("output/images/"+NAME+".png")
        print('Done')

        #appending good box info to dictionary ##        
        num_good_boxes+=sum(ind)
        
        for v in range(sum(ind)):
            good_boxes.setdefault('image_name',[]).append( NAME  ) 
            good_boxes.setdefault('path_to_image_dir',[]).append(  image_path  ) 
            good_boxes.setdefault('path_to_model',[]).append(   PATH_TO_MODEL_DIR ) 
            good_boxes.setdefault('label_filename',[]).append(  LABEL_FILENAME  ) 
            good_boxes.setdefault('path_to_label_dir',[]).append(  PATH_TO_LABELS  ) 
            good_boxes.setdefault('path_to_saved_model',[]).append(  PATH_TO_SAVED_MODEL  )
            good_boxes.setdefault('image_size',[]).append([image_np_with_detections.shape[0],image_np_with_detections.shape[1]])
            good_boxes.setdefault('scale',[]).append(  SCALE  ) 
        for key, values in detections.items():
            if not isinstance(detections[key],int):
                for v in values[ind]:   
                    good_boxes.setdefault(key,[]).append( v )
                    
            
           
    print ("found {}".format(num_good_boxes))
    return good_boxes

def store_box_info(data_dict,
                   fpath="output/files/",
                   fname="saving_private_boxes_multi.csv"):
    csv_file = fpath+fname
    try:
        fat_bear = pd.DataFrame.from_dict(data_dict)
        fat_bear.to_csv(csv_file)
    except IOError:
        print("I/O error")


###  MAIN FUCTION BEGINS HERE ####

def main(argv):
    IMAGE_PATH=[pathlib.Path("input/images/20000X_0043.jpeg"),
                pathlib.Path("input/images/663 20m_100kV_20kX_0017.jpg"),
                pathlib.Path("input/images/663 20m_100kV_20kX_0092.jpg"),
                pathlib.Path("input/images/663 20m_100kV_20kX_0040.jpg")]
    
    PATH_TO_MODEL_DIR="trained_models/my_faster_rcnn_resnet50_1024x1024_multiclass_steps6k/"

    LABEL_FILENAME="label_map_multiclass.pbtxt"
    
    PATH_TO_LABELS="trained_models/annotations/"+LABEL_FILENAME

    PATH_TO_SAVED_MODEL = PATH_TO_MODEL_DIR + "saved_model"

    SCALE = 1.7654 # pix/nm

    good_boxes = process_images(IMAGE_PATH,
                               PATH_TO_MODEL_DIR,
                               LABEL_FILENAME,
                               PATH_TO_LABELS,
                               PATH_TO_SAVED_MODEL,
                               SCALE)
   
    store_box_info(good_boxes)

    return

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#    
if __name__ == "__main__":
    main(sys.argv[1:])
    
    
