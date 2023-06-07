from utils import *

plt.rcParams['figure.figsize'] = [9, 10]



def shift_rotate_points(x,y,scale,rotation,origin,reference):
    if (isinstance(x,list)): 
        x = [ xs / scale[0] for xs in x ]
        y = [ 1-(ys / scale[1]) for ys in y ]
        xshift = x - origin[0]
        yshift = y - (1-origin[1])
        xpp = [ xp*np.cos(rotation) - yshift[j]*np.sin(rotation) for j,xp in enumerate(xshift) ]
        ypp = [ xshift[j]*np.sin(rotation) + yp*np.cos(rotation) for j,yp in enumerate(yshift) ]
        new_x = xpp + reference[0]
        new_y = ypp + reference[1]
    else:
        x = x/scale[0]
        y = y/scale[1]
        xshift = x - origin[0]
        yshift = y - (1-origin[1])
        xpp = xshift*np.cos(rotation) - yshift*np.sin(rotation)
        ypp = xshift*np.sin(rotation) + yshift*np.cos(rotation)
        new_x = xpp + reference[0]
        new_y = ypp + reference[1]
    
    #print("calc. XY",new_x,new_y)
    return new_x , new_y
    
def analyse_stored_images(csv_file):
    full_dict = csv_to_dict(csv_file)
    old_image=''

    fig1, ax1 = plt.subplots()
    fig2, ax2 = plt.subplots()
    fig3, ax3 = plt.subplots()
    fig4, ax4 = plt.subplots()

    accepted_signal=[]
    accepted=[]
    distance_between_points = []
    distance_to_reference=[]
    xlim_max = 0
    ylim_max = 0

    poly_dict={}
    
    for i,image in enumerate(full_dict['path_to_image_dir']):
        if (old_image == image or old_image==''):
            if (old_image==''):
                poly_dict[image] = [[],[]] 
            # relative position of vesticle of interest
            new_x  = full_dict['new_x'][i]
            new_y  = full_dict['new_y'][i]
            # constructing point from relative position
            # turned into real distance in nm
            p1 = Point(new_x*full_dict['scale'][i]*full_dict['image_size'][i][0],
                       new_y*full_dict['scale'][i]*full_dict['image_size'][i][1])

            
            pixel_distance = full_dict['scale'][i]*full_dict['image_size'][i]
            
            if (xlim_max <  pixel_distance[0] ):
                xlim_max =  pixel_distance[0]
            if (ylim_max <  pixel_distance[1] ):
                ylim_max =  pixel_distance[1]
            
            #finding relative positions of borders (0,1) 
            scaled_border_x ,  scaled_border_y = shift_rotate_points(full_dict['border_area_x'][i],
                                                                     full_dict['border_area_y'][i],
                                                                     scale=full_dict['image_size'][i],
                                                                     rotation=full_dict['rotation'][i],
                                                                     origin=full_dict['origin'][i],
                                                                     reference=full_dict['reference_point'][i])

            # constructing polygon from relative position
            # turned into real distance in nm?
            nm_border_x = [ v*full_dict['scale'][i]*full_dict['image_size'][i][0] for v in scaled_border_x  ]
            nm_border_y = [ v*full_dict['scale'][i]*full_dict['image_size'][i][1] for v in scaled_border_y  ]
            poly = Polygon(np.column_stack((nm_border_x,nm_border_y)))
                                            
            if (poly.contains(p1)):
                accepted.append(p1)
                if (full_dict['box_class'][i] == 1):
                    poly_dict[image][0].append(p1)
                elif (full_dict['box_class'][i] == 2):
                    poly_dict[image][1].append(p1)
        else :
            poly_dict[image] = [[],[]]
            accepted_signal.append(accepted)
            accepted=[]
            for i,p in enumerate(accepted):
                for p2 in  accepted[i:]:
                    relative_distance = p.distance(p2)
                    if relative_distance > 0:
                        distance_between_points.append(relative_distance)
        old_image=image
    
    accepted_signal.append(accepted)
    for i,p in enumerate(accepted):
        for p2 in  accepted[i:]:
            relative_distance = p.distance(p2)
            if relative_distance > 0:
                distance_between_points.append(relative_distance)
                
    accepted_signal = [item for sublist in accepted_signal for item in sublist]
    ref = Point(*np.array(full_dict['reference_point'][0])*np.array(full_dict['scale'][0]*full_dict['image_size'][0])) 
    
    for p in accepted_signal:
        ax1.plot(*p.xy,'ro')
        distance_to_reference.append(p.distance(ref))
    
    # scatter positions
    ax1.set_title('position of vesicles relative to AZ')
    ax1.plot(*ref.xy,'bo')
    ax1.set_xlim(0,xlim_max)
    ax1.set_ylim(0,ylim_max)

    # cumulative distance between points
    ax2.set_title('distance between vesicles')
    ax2.set_xlim(0,max(distance_between_points))
    n,bins,patches = ax2.hist(distance_between_points,bins=30,cumulative=True,histtype='step',density=True)
    [b.remove() for b in patches ]
    ax2.plot(bins[:-1]+0.5*(bins[1:]-bins[:-1]),n,'bo:',fillstyle='none',)

    # cumulative distance from az
    ax3.set_title('distance from AZ')
    n,bins,patches=ax3.hist(distance_to_reference,bins=30,cumulative=True,histtype='step',density=True)
    [b.remove() for b in patches ]
    ax3.plot(bins[:-1]+0.5*(bins[1:]-bins[:-1]),n,'bo:',fillstyle='none',)


    # scatter heatmap
    ax4.set_title('position of vesicles relative to AZ heatmap')
    xs=[p.x for p in accepted_signal ]
    ys=[p.y for p in accepted_signal ]
    h = ax4.hist2d(xs,ys,bins=(100,100),density=True,cmap=plt.cm.jet,range=[(0,xlim_max),(0,ylim_max)])
    cb = fig4.colorbar(h[3],ax=ax4)
    
    ax4.plot(*ref.xy,'o',color='orange')
    ax4.hlines(ref.y,0,xlim_max,colors='orange')
    ax4.vlines(ref.x,0,ylim_max,colors='orange')

    plt.show() 
    return 

    
analyse_stored_images('output/files/processed.csv')
