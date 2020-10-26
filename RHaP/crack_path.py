import numpy as np
from scipy import ndimage
from skimage.graph import route_through_array
from skimage.transform import rescale, resize, downscale_local_mean

def det_crack_path(thres,crop_threshold,num_runs,kernel_size):
    """
    Determine Possible Crack Paths in the micrograph
    
    Parameters
    ----------
    thres: array
        thesholded image to look at
    crop_threshold: array
        calculated during thresholding, array of true and false values
    num_runs int
        number of crack paths to determine

        
    
    Output
    -------
    Edist: array
        min euclidean distace from the hydride to the matrix
    path_list:
        list of possible crack paths
    cost_list: list
        list of cost values for each crack path



    """
  
    edist = ndimage.morphology.distance_transform_edt(thres==0)
    edist = rescale(edist,(1,1))

    #add a row of zeros on the top and bottom 
    edist[0,:]=0
    edist[-1,:]=0

    #make a empty list to store paths and costs
    path_list = []; cost_list = [];

    for run in np.arange(num_runs):
        path, cost = route_through_array(edist,[0,0],[-1,-1])
        path=np.array(path)

        path_coord_list = []

        # Filtering the path
        for coord in path:
            #if coord[0] != 0:       #remove the top row
            #    if coord[0]!= edist.shape[0]-1:       #remove the bottom row
            if crop_threshold[coord[0], coord[1]] == False:      #if the threshold region is fale then apend the path
                path_coord_list.append(coord)

                #to search for a different path next time, change current path to np.inf
                #also make surrounding coords np.inf too
                for j in [1, kernel_size]:
                    for i in [[0,0], [j,0], [0,j], [-j,0], [0,-j], [j,j], [-j,-j], [j,-j], [-j,j]]:
                        if coord[0]+i[0] >=0 and coord[0]+i[0] <edist.shape[0] and coord[1]+i[1] >=0 and coord[1]+i[1]<edist.shape[1]:
                            edist[coord[0]+i[0], coord[1]+i[1]] = np.inf

        path_list.append(np.array(path_coord_list))
        cost_list.append(cost)

      
    edist = ndimage.morphology.distance_transform_edt(thres==0)
    edist = rescale(edist,(1,1))


    return edist, path_list, cost_list
