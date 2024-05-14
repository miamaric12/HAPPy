import numpy as np
from skimage.color import rgb2gray
from skimage.io import imread


def image(image_path, transpose):
    """Import and transpose an image.

    Parameters
    ----------
    image_path: str
        Path to the image, excluding extension, including name
    transpose: bool
        Whether the image needs to be rotated so that radial hydrides are in
        the vertical direction. If True, the read array will be transposed
        before returning.

    Returns
    -------
    original_image
        The transposed/imported image to be analysed
    """

    original_image = imread(image_path, as_gray=True)

    if transpose:
        original_image = np.transpose(original_image)

    return original_image
