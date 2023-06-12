from utils import *
sys.setrecursionlimit(2000)

plt.rcParams['figure.figsize'] = [9, 10]


def process_images(image_name,boxes_dict):
    reference_point = [ 0.5 , 0.2 ]
    
    #img = pd.DataFrame.from_dict(boxes_dict)['path_to_image_dir'] == image_name
    img = np.array(boxes_dict['path_to_image_dir']) == image_name
    
    boxes={}
    for key, value in boxes_dict.items():
        accepted = []
        for i, val in enumerate(value):
            if (img[i]):
                accepted.append(np.array(val))
            
        boxes[key] = np.array(accepted)
        
    scale = np.array(boxes['scale'])
    classes =  np.array(boxes['detection_classes'])
    
    image_np = cv2.imread(str(image_name))
    
    f, ax = plt.subplots()
    ax.imshow(image_np)
    d = DrawingTool(image_np,boxes,ax,f)
    d.connect()
    plt.show()
            
    if (d.exclude_image):
        return {}

    origin = d.get_origin_position("relative")

        
    north_coord = d.get_north_position('relative')

    rotation  = d.getRotation(north_coord[0],
                              north_coord[1],
                              north_coord[2],
                              north_coord[3])
    
    border_x, border_y = np.split(np.array(d.border),2,axis=1)
    activeregion_x, activeregion_y = np.split(np.array(d.activeregion),2,axis=1)

    border_x = border_x.flatten()
    border_y = border_y.flatten()

    activeregion_x = activeregion_x.flatten()
    activeregion_y = activeregion_y.flatten()
    
    new_dict = {}
    for idx , box in enumerate(boxes['detection_boxes']):
        dist = distance_to_box(origin,box)
        if ( dist < d.accepted_radius('relative') ):
            pos = centre_coordinates(box)
             
            xp = pos[0] - origin[0]
            yp = (1-pos[1]) - (1-origin[1])
                
            xpp = xp*np.cos(rotation) - yp*np.sin(rotation)
            ypp = xp*np.sin(rotation) + yp*np.cos(rotation)
               
            new_x = xpp + reference_point[0]
            new_y = ypp + reference_point[1] 

            # img related info
            new_dict.setdefault('path_to_image_dir',[]).append( image_name )
            new_dict.setdefault('image_size',[]).append( np.array([ image_np.shape[1] , image_np.shape[0] ]) )
            new_dict.setdefault('scale',[]).append(scale[idx])
            # box related info
            new_dict.setdefault('detection_boxes',[]).append( np.array(box) )
            new_dict.setdefault('box_class',[]).append(classes[idx])
            new_dict.setdefault('x',[]).append( pos[0] )
            new_dict.setdefault('y',[]).append( 1-pos[1] )
            # box processed info
            new_dict.setdefault('new_x',[]).append( new_x )
            new_dict.setdefault('new_y',[]).append( new_y )
            # normalization related info
            new_dict.setdefault('origin',[]).append( np.array(origin) )
            new_dict.setdefault('north',[]).append( np.array(north_coord) )
            new_dict.setdefault('rotation',[]).append( rotation )
            new_dict.setdefault('accepted_radius',[]).append( dist )
            new_dict.setdefault('reference_point',[]).append( np.array(reference_point) )
            # border and active zone info
            new_dict.setdefault('border_area_x',[]).append( list(border_x) )
            new_dict.setdefault('border_area_y',[]).append( list(border_y) )
            new_dict.setdefault('active_zone_x',[]).append( list(activeregion_x) )
            new_dict.setdefault('active_zone_y',[]).append( list(activeregion_y) )

            #new_dict.setdefault('active_zone',[]).append( activeregion )

    return new_dict



def update_output_csv(output_name,
                      update_dict):
    
    if ( not os.path.isfile(output_name) ):
        csv_file = open(output_name,"w")
        csv_file.close()
        new_dict = {}
    else:
        if(os.stat(output_name).st_size==0):
            new_dict = {}
        else:
            new_dict = csv_to_dict(output_name)

    if (update_dict):
        if (new_dict):
            new_dict = update_dictionaries(new_dict,update_dict)
        else:
            new_dict = update_dict

        with open(output_name,'w') as f:
            writer = csv.writer(f)
            writer.writerow(new_dict.keys())
            writer.writerows(zip(*new_dict.values()))
    return new_dict


def plot_results(new_box_dict):
    fig, ax = plt.subplots(1,2)
    ax[0].set_xlim(0,1)
    ax[0].set_ylim(0,1)

    
    ax[0].scatter(np.array(new_box_dict['reference_point'])[:,0],np.array(new_box_dict['reference_point'])[:,1],color='b')
    ax[0].scatter(new_box_dict['new_x'],new_box_dict['new_y'],color='r')
    
    ax[1].hist(new_box_dict['accepted_radius'],cumulative=True,histtype='step')
    plt.show()
    return

def main_process(stored_boxes_csv,
                 processed_boxes_csv):
    boxes_dict = csv_to_dict(stored_boxes_csv)

    new_dict = update_output_csv(processed_boxes_csv,{})
    
    for image_name in sorted(set(boxes_dict['path_to_image_dir']),key=list(boxes_dict['path_to_image_dir']).index):
        print("Opening image : {}".format(image_name),end='')
        if('path_to_image_dir' in new_dict ):
            if (sum(np.array(new_dict['path_to_image_dir'])==image_name)):
                print("...skipping")
                continue
            else:
                print()
                update_dict = process_images(image_name,boxes_dict)
                if (not update_dict):
                    print("...skipping")
                    continue
                new_dict = update_output_csv(processed_boxes_csv,update_dict)
        else:
            print()
            update_dict = process_images(image_name,boxes_dict)
            new_dict = update_output_csv(processed_boxes_csv,update_dict)

    plot_results(new_dict)
    
    return 

main_process("output/files/saving_private_boxes_multi.csv",
             "output/files/processed.csv")
