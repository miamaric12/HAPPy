import numpy as np
from scipy import ndimage
from skimage.graph import route_through_array
from skimage.transform import rescale, resize, downscale_local_mean

def det_crack_path(thres,crop_threshold,num_runs):
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

    path_list = []; cost_list = [];
    for run in np.arange(num_runs):
        path, cost = route_through_array(edist,[0,0],[-1,-1])
        path2=np.array(path)
        path3 = []
        for item in path2:
            if item[0] != 0:
                if item[0]!= edist.shape[0]-1:
                    if crop_threshold[item[0], item[1]] == False: #if the threshold region is fale then apend the path
                        path3.append(item)

                        edist[item[0], item[1]] = np.inf

                        for j in [1, 5]:
                            for i in [[j,0], [0,j], [-j,0], [0,-j], [j,j], [-j,-j], [j,-j], [-j,j]]:
                                edist[item[0]+i[0], item[1]+i[1]] = np.inf

        path4 = np.array(path3)
        path_list.append(path4)
        cost_list.append(cost)

      
    edist = ndimage.morphology.distance_transform_edt(thres==0)
    edist = rescale(edist,(1,1))


    return edist, path_list, cost_list
