from skimage.morphology import binary_dilation
from skimage.morphology import remove_small_objects
from skimage.morphology import disk
import copy
import numpy as np

def cropImage(im, crop_bottom, crop_top, crop_left, crop_right):
    """
    Crop an image
    
    Parameters
    ----------
    im : jpg or png
        The image that is to be cropped
    crop_bottom, crop_top, crop_left, crop: int
        How many pixels to crop in each of these directions
        
    """
    if crop_bottom == 0:
        im = im[crop_top:]
    else:
        im = im[crop_top:-crop_bottom]
    if crop_right == 0:
        im = im[:, crop_left:]
    else:
        im = im[:, crop_left:-crop_right]
    
    return im

def cropping_tube(original_image,crop_param, size_param, dilation_param):
    """
    Cropping tubes of an image
      
    Parameters
      ----------
      original_image: jpg, png
          The original tubed image that needs to be cropped
      crop_param: int
          Threshold for removing the dark edges i.e., tube ends in the image
      size_param: int
          Make sure features below this size (i.e. hydrides) are not included in cropping
      dilation_param:int
          Dilate the cropped boundary by a number of pixels
      
    Output
      -------
      cropped image:
        The final cropped image
      cropped threshold:

    """
    
    crop_threshold = original_image < crop_param
    crop_threshold = remove_small_objects(crop_threshold, size_param)

    crop_threshold = binary_dilation(crop_threshold, selem=disk(dilation_param))        
    cropped_image = copy.deepcopy(original_image)
    cropped_image[crop_threshold] = np.nan

    return cropped_image, crop_threshold
