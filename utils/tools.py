from utils.libs import *

def centre_coordinates(box_coordinates):
    return [ 0.5*(box_coordinates[1]+box_coordinates[3]) , 0.5*(box_coordinates[0]+box_coordinates[2])  ]

def distance_to_box(origin_coordinates,box_coordinates):
    centre_of_box_coordinates = centre_coordinates(box_coordinates)
    vector_coordinates = [ origin_coordinates[0] , origin_coordinates[1] , centre_of_box_coordinates[0] , centre_of_box_coordinates[1] ]
    length = np.sqrt(pow(vector_coordinates[0]-vector_coordinates[2],2)+pow(vector_coordinates[1]-vector_coordinates[3],2))
    return length

def csv_to_dict(path_to_csv):
    boxes_dict = pd.read_csv(path_to_csv,sep=',')#.to_dict('series')
    
    new_dict = {}
    for key in boxes_dict:
        new_vals=[]
        #print("{} {}... ".format(key,boxes_dict[key]))
        for val in boxes_dict[key]:
            if ( isinstance(boxes_dict[key][0],str)):
                if ( '['  in boxes_dict[key][0] ):
                    new_val=[]
                    oldpos=1
                    if(',' in val):
                        seps = [ s.start()-1 for s in re.finditer(' ',val[:-1])]
                    else:
                        seps = [ s.start() for s in re.finditer(' ',val[:-1])]
                    seps.append(len(val[1:]))
                    for pos in seps:
                        try:
                            convert = float(val[oldpos:pos])
                            new_val.append(convert)
                        except:
                            pass
                        oldpos=pos+1
                    new_vals.append(new_val)
                else:
                    new_vals.append(val)
            else:
                new_vals.append(val)
                
        #print("{} {}... ".format(key,new_vals))
        new_dict[key] = np.array(new_vals)
                
    return new_dict

def update_dictionaries(old_dict,update):
    new_dict = old_dict
    for key, val in update.items():
        if ( key in old_dict):
            tmp = []   
            for v in new_dict[key].tolist():
                tmp.append(v)
            for v in val:
                tmp.append(v)

            new_dict[key] = tmp
        else:
            new_dict[key] = val
    return new_dict

