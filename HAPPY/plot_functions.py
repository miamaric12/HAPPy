import numpy as np
from matplotlib_scalebar.scalebar import ScaleBar
from matplotlib import pyplot as plt


def addScaleBar(ax, scale, location='upper right'):
    """Add a scale bar to an axes.

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        Matplotlib axis on which to plot.
    """

    if scale:
        scalebar = ScaleBar(scale, location=location)
        ax.add_artist(scalebar)
        plt.show()


def addArrows(ax, c='r', lenx=0.04, leny=0.06, flip=False):
    """
    Add coordinate definition arrows (radial and circumferential) to an axes.
    
    Parameters
    ----------
    ax : matplotlib.axes.Axes
        Matplotlib axis to plot on 
    """

    startcoord = (0.02, 0.02)

    ax.annotate(
            "",
            xy=(startcoord[0]-0.002, startcoord[1]),
            xytext=(startcoord[0]+lenx, startcoord[1]),
            xycoords='axes fraction',
            c=c,
            arrowprops=dict(arrowstyle="<-", color=c, lw=2),
            )
    ax.annotate(
            "",
            xy=(startcoord[0], startcoord[1]-0.002),
            xytext=(startcoord[0], startcoord[1]+leny),
            xycoords='axes fraction',
            c=c,
            arrowprops=dict(arrowstyle="<-", color=c, lw=2),
            )
    positions = [(0.011, startcoord[1]+leny), (startcoord[0]+lenx, 0.01)]
    if flip:
        labels = 'CR'
    else:
        labels = 'RC'
    for label, position in zip(labels, positions):
        ax.annotate(
                label,
                xy=position,
                xycoords='axes fraction',
                fontsize=14,
                fontweight='bold',
                c=c,
                )


def plot(img, title, scale=None, location=None, ax=None):
    """Plotting an imge.
    
    Parameters
    ----------
    img : array
        Image data to be plotted
    title : str
        Title of plot.
    scale : float
        Scale in meters per pixel.
    location : str
        Location of scale bar i.e. 'lower right', 'upper left'
    """
    if ax is None:
        _, ax = plt.subplots(figsize=(10, 6))
    ax.imshow(img, cmap='gray')
    ax.set_title(title, fontsize=14)
    ax.set_axis_off()
    if scale is not None:
        addScaleBar(ax, scale=scale, location=location)
    addArrows(ax)


def plot_comparison(img1, title1, img2, title2, scale=None, location=None):
    """Plotting two images next to each other.

    Parameters
    ----------
    img1 : array
        Image data to be plotted on left.
    img2 : array
        Image data to be plotted on right.
    title1 : str
        Title of left-hand plot.
    title2 : str
        Title of right-hand plot.
    scale : float
        Scale in meters per pixel.
    location : str
        Location of scale bar i.e. 'lower right', 'upper left'
    """

    fig, (ax_a, ax_b) = plt.subplots(
            ncols=2, figsize=(14, 7), sharex=True, sharey=True
            )
    plot(img1, title1, ax=ax_a)
    plot(img2, title2, scale=scale, location=location, ax=ax_b)
    fig.tight_layout()


def plot_hist(arr):
    _, ax = plt.subplots(figsize=(8, 5))
    histogram = ax.hist(arr[~np.isnan(arr)].flatten(), bins=60, range=(0, 2))
    ax.set_title('Image Histogram', fontsize=14)
    ax.set_xlabel('Gray value', fontsize=12)
    ax.set_ylabel('Frequency', fontsize=12)

    return histogram
    