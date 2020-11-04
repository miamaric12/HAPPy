import numpy as np
from skimage.color import rgb2grey
from skimage.io import imread

def image(image_path, transpose):
    """
    Import and Transpose an image.
    
    Parameters
    ----------
    image_path: str
        Path to the image, excluding extension, including name
    transpose: Boolean Value
        Whether the image needs to be rotated so that radial hydrides are in the vertical direction
        If True: Image will be transposed
        If False: Image will not be transposed
        
    Output
    -------
    original_image
        The transposed/imported image to be analysed
    """

    original_image = imread(image_path)
    original_image = rgb2grey(original_image)
    
    if transpose == True:
        original_image = np.transpose(original_image)
        
    return original_image