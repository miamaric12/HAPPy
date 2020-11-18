import numpy as np
from scipy import ndimage
from skimage.transform import hough_line, hough_line_peaks
from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle
from .plot_functions import addScaleBar, addArrows


def hough_rad(
        image,
        num_peaks,
        min_distance=5,
        min_angle=5,
        val=0.25,
        scale=None,
        location=None,
        ):
    """Perform Hough Line Transfom to determine radial hydride fraction.

    Parameters
    ----------
    image : array
        input thresholded hydride image
    num_peaks : float
        number of measured peaks in one rectangle.
    min_distance : float
        minimum distance separating two parallel lines. It seems that a value
        of 5 is good
    min_angle : float
        minimum angle separating two lines it seems that a value of 5 is good
    val : float
        val is a number < 1 where, only hydrides that are at least val times
        the length of the longest hydride are measured. This helps to reduce
        noise becuase only hydrides that are significant in size are included
        in the calculation. The default value for this is 0.25, if you have
        much smaller hydride branches that you want to pick up this value can
        be reduced, but remember the noise increases as well.
    scale : float
        Scale in meters per pixel.
    location : str
        Location of scale bar i.e. 'lower right', 'upper left'

    Returns
    -------
    angle_list : array
        List of angles generated from the hough transform.
    len_list : array
        List of line lengths generated from the hough transform.
    """

    fig, axes = plt.subplots(
            ncols=2, figsize=(14, 7), sharex=True, sharey=True
            )
    ax = axes.ravel()

    # Plotting
    ax[0].imshow(image, cmap='gray')
    ax[0].set_axis_off()
    ax[0].set_title('Thresholded image', fontsize=14)
    ax[1].imshow(image, cmap='gray')
    ax[1].set_axis_off()
    ax[1].set_title('Hough Transform', fontsize=14)

    # Label image
    label, num_features = ndimage.label(image > 0.1)
    slices = ndimage.find_objects(label)

    # Loop over each slice
    len_list = []
    angle_list = []
    d_list = []
    for feature in np.arange(num_features):
        h, theta, d = hough_line(
                label[slices[feature]],
                theta=np.linspace(-np.pi/2 , np.pi/2 , 90),
                )
        threshold = val*np.amax(h)
        h_peak, angles, d_peak = hough_line_peaks(
                h,
                theta,
                d,
                threshold=threshold,
                num_peaks=num_peaks,
                min_distance=min_distance,
                min_angle=min_angle,
                )
        angle_list.append(angles)
        len_list.append(h_peak)
        d_list.append(d_peak)

        # Draw bounding box
        x0_box = np.min([slices[feature][1].stop, slices[feature][1].start])
        y0_box = np.min([slices[feature][0].stop, slices[feature][0].start])
        x1_box = np.max([slices[feature][1].stop, slices[feature][1].start])
        y1_box = np.max([slices[feature][0].stop, slices[feature][0].start])
        rect = Rectangle(
                (x0_box, y0_box),
                x1_box-x0_box,
                y1_box-y0_box,
                angle=0.0,
                ec='r',
                fill=False,
                )
        ax[1].add_artist(rect)
        # origin = np.array((0, np.abs(x1_box-x0_box)))  # never used
        for _, angle, dist in zip(h_peak, angles, d_peak):
            y0b, y1b = (
                    (dist - np.array((0, x1_box-x0_box)) * np.cos(angle))
                    / np.sin(angle)
                    )
            y0_line = y0b + y0_box
            y1_line = y1b + y0_box
            x0_line = x0_box
            x1_line = x1_box
            m = (y1_line-y0_line)/(x1_line-x0_line)

            # Fix lines which go over the edges of bounding boxes
            if y0_line < y0_box:
                x0_line = ((y0_box - y1_line) / m) + x1_line
                y0_line = y0_box
            if y0_line > y1_box:
                x0_line = ((y1_box - y1_line) / m) + x1_line
                y0_line = y1_box
            if y1_line < y0_box:
                x1_line = ((y0_box - y1_line) / m) + x1_line
                y1_line = y0_box
            if y1_line > y1_box:
                x1_line = ((y1_box - y1_line) / m) + x1_line
                y1_line = y1_box

            ax[1].plot(np.array((x0_line, x1_line)), (y0_line, y1_line), '-g')

    print('Number of detected angles: {0}'.format(len(len_list)))
    ax[1].set_xlim(0, image.shape[1])
    ax[0].set_ylim(0, image.shape[0])

    if scale is not None:
        addScaleBar(ax[1], scale, location)
    addArrows(ax[0])
    addArrows(ax[1])

    fig.tight_layout()

    return np.concatenate(angle_list), np.concatenate(len_list)


def RHF_no_weighting_factor(angle_list, len_list):
    """Calculate the Radial Hydride Fraction without any weighting factor

    Parameters
    ----------
    angle_list : array
        calculated from the Hough line transform
    len_list : array
        List of lengths generated from the hogh line transform

    Returns
    -------
    radial : float
        fraction of radial hydrides
    circumferential : float
        fraction of circumferential hydrides
    """
    radial_angles = np.logical_and(
            -np.pi / 4 <= angle_list, angle_list < np.pi / 4
            )
    radial_len = np.sum(len_list[radial_angles])
    circumferential_len = np.sum(len_list[~radial_angles])

    radial = radial_len / (radial_len + circumferential_len)
    circumferential = 1 - radial

    return radial, circumferential


def weighted_RHF_calculation(angle_list, len_list):
    """
    Weighted Radial Hydride Fraction Calculation
    
    Parameters
    ----------
    angle_list: list
        List of angles generated from the hogh line transform
    len_list: list
        List of lengths generated from the hogh line transform
   
    Returns
    -------
      RHF: float
          Weighted radial hydride fraction
    """

    deg_angle_list = np.rad2deg(angle_list)
    fi = []

    for k in deg_angle_list:
        if k >0 and k<=30: x=1
        elif k>30 and k<=50: x=0.5
        elif k>50 and k<=90: x=0
        elif k>-30 and k<=0: x=1
        elif k>-50 and k<=-30: x=0.5
        elif k>-90 and k<=-50: x=0

        fi.append(x)

    #The next step is to do the summation
    SumOfLixFi = sum(len_list * np.array(fi))
    SumOfLi = sum(len_list)

    RHF = SumOfLixFi / SumOfLi

    return RHF

