import numpy as np
import copy
from scipy import ndimage
from skimage.morphology import remove_small_objects


def nan_gaussian(image, sigma):
    """
    Apply a gaussian filter to an array with nans.
    
    Parameters
    ----------
    image: 
        an array with nans
    sigma: int
        σ is the standard deviation of the Gaussian distribution
    
    Output
    -------
    gauss
        
    """

    nan_msk = np.isnan(image)
    loss = np.zeros(image.shape)
    loss[nan_msk] = 1
    loss = ndimage.gaussian_filter(loss, sigma=sigma, mode='constant', cval=1)
    gauss = image.copy()
    gauss[nan_msk] = 0
    gauss = ndimage.gaussian_filter(gauss, sigma=sigma, mode='constant', cval=0)
    gauss[nan_msk] = np.nan
    gauss += loss * image

    return gauss

def minimize_grain_contrast(image,sigma): 
    gaussian_blur = nan_gaussian(image, sigma = sigma)
    removedGrains = image/gaussian_blur
    
    return(removedGrains)

def simple_threshold(image,crop_threshold,threshold,small_grains):
    """
    Threshold the image, where the hydrides are identified to be white and the matrix is black
    
    Parameters
    ----------
    removed_grains: arr
        image to threshold
    theshold: int/float
        threshold level
    small_grains: int/float
        size of features to be removed and not thresholded
    crop_threshold: array
        array of true false so that thresholding is only performed within this region
        
    
    Output
    -------
    thres_disp:
        The thresholded image
        
    """
    thres = image < threshold
    thres = remove_small_objects(thres, min_size=small_grains)


    thres_disp = copy.deepcopy(thres)
    thres_disp = np.array(thres_disp)*1.0
    thres_disp[crop_threshold] = np.nan
           
    return thres_disp

