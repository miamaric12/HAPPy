import numpy as np
from scipy.ndimage import gaussian_filter
from skimage.morphology import remove_small_objects


def nan_gaussian(image, sigma):
    """Apply a gaussian filter to an array with nans.

    Parameters
    ----------
    image : array
        an array with nans
    sigma : float
        σ is the standard deviation of the Gaussian distribution

    Returns
    -------
    gauss : array, same shape as `image`
        The Gaussian-filtered input image, with nan entries ignored.
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
    """Minimise grain contrast or uneven lighting.

    This is accomplished by dividing the original image
    by an image with a gaussian blur applied.

    Parameters
    ----------
    image : array
        Image to minimise grain contrast.
    sigma : float
        Sigma value for gaussian blur.

    Returns
    -------
    removed_grains : array, same shape as image
        Output image.
    """

    gaussian_blur = nan_gaussian(image, sigma=sigma)
    removed_grains = image / gaussian_blur

    return(removed_grains)


def simple_threshold(image, crop_threshold, threshold, small_obj=None):
    """Threshold the image, accounting for crop and small features.

    Hydrides are assumed to be dark (value below the threshold) in the input
    image, but are returned as bright (1.0) features in the output, and vice-
    -versa for the matrix.

    Parameters
    ----------
    removed_grains : array
        image to threshold.
    crop_threshold : array of bool
        Thresholding is only performed within regions labeled False in this
        array. Values labeled True will be set to np.nan in the output
    theshold : float
        threshold level.
    small_obj : int, optional
        size of features to be removed and not thresholded.

    Returns
    -------
    thres_disp : array of float
        The thresholded image, with 1.0 in foreground pixels, 0.0 in
        background pixels, and np.nan in cropped pixels.
    """

    thres = image < threshold
    if small_obj is not None:
        thres = remove_small_objects(thres, min_size=small_obj)

    thres_disp = thres.astype(float)  # this will copy and set True to 1.0
    thres_disp[crop_threshold] = np.nan

    return thres_disp
