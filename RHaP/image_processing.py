import copy
import numpy as np
from scipy.ndimage import gaussian_filter
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
    
    Returns
    -------
        gauss
    """

    nan_msk = np.isnan(image)
    loss = np.zeros(image.shape)
    loss[nan_msk] = 1
    loss = gaussian_filter(loss, sigma=sigma, mode='constant', cval=1)
    gauss = image.copy()
    gauss[nan_msk] = 0
    gauss = gaussian_filter(gauss, sigma=sigma, mode='constant', cval=0)
    gauss[nan_msk] = np.nan
    gauss += loss * image

    return gauss

def minimize_grain_contrast(image, sigma):
    """
    Minimise grain contrast or uneven lighting by dividing the original image 
    by an image with a gaussian blur applied.
    
    Parameters
    ----------
        image: 
            Image to minimise grain contrast.
        sigma: float
            Sigma value for gaussian blur.
        
    Returns
    -------
        removedGrains:
            Output image.
    """

    gaussian_blur = nan_gaussian(image, sigma = sigma)
    removedGrains = image / gaussian_blur
    
    return(removedGrains)

def simple_threshold(image, crop_threshold, threshold, small_obj=None):
    """
    Threshold the image, where the hydrides are identified to be white and the matrix is black
    
    Parameters
    ----------
        removed_grains: arr
            image to threshold
        theshold: float
            threshold level
        small_grains: int
            size of features to be removed and not thresholded
        crop_threshold: array
            array of true false so that thresholding is only performed within the region that has been previously cropped
        
    Returns
    -------
        thres_disp:
            The thresholded image
    """

    thres = image < threshold
    if small_obj is not None:
        thres = remove_small_objects(thres, min_size=small_obj)


    thres_disp = copy.deepcopy(thres)
    thres_disp = np.array(thres_disp)*1.0
    thres_disp[crop_threshold] = np.nan
           
    return thres_disp

