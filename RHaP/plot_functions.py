
from matplotlib_scalebar.scalebar import ScaleBar
from matplotlib import pyplot as plt
import numpy as np

def addScaleBar(ax):
    """
    Add a scale bar to an axes.
    Parameters
    ----------
    ax : matplotlib.axes.Axes
        Matplotlib axis to plot on 
        
    """
    if scale:
        scalebar = ScaleBar(scale)
        fig.gca().add_artist(scalebar)
        plt.show()

def addArrows(ax, c='r', lenx=0.04, leny=0.06, flip=False):
    """
    Add coordinate definition arrows (radial and circumferential) to an axes.
    
    Parameters
    ----------
    ax : matplotlib.axes.Axes
        Matplotlib axis to plot on 
  
    
    """
    startcoord = (0.02, 0.02);
    
    ax.annotate("", xy=(startcoord[0]-0.002, startcoord[1]), xytext=(startcoord[0]+lenx, startcoord[1]), xycoords = 'axes fraction', c=c, arrowprops=dict(arrowstyle="<-", color=c, lw=3))
    ax.annotate("", xy=(startcoord[0], startcoord[1]-0.002), xytext=(startcoord[0], startcoord[1]+leny), xycoords = 'axes fraction', c=c, arrowprops=dict(arrowstyle="<-", color=c, lw=3))
    if flip == False:
        ax.annotate("R", xy=(0.011, startcoord[1]+leny), xycoords = 'axes fraction', fontsize=18, fontweight='bold', c=c)
        ax.annotate("C", xy=(startcoord[0]+lenx, 0.01), xycoords = 'axes fraction', fontsize=18, fontweight='bold', c=c)
    if flip == True:
        ax.annotate("C", xy=(0.011, startcoord[1]+leny), xycoords = 'axes fraction', fontsize=18, fontweight='bold', c=c)
        ax.annotate("R", xy=(startcoord[0]+lenx, 0.01), xycoords = 'axes fraction', fontsize=18, fontweight='bold', c=c)


def plot_comparison(plot1, name_plot_1, plot2, name_plot_2):
    """
    Plotting two plots next to each other
    
    Parameters
    ----------
    plot1:
        Plot that is to be displayed first
    plot2:
        Plot that is to be displayed second
    name_plot_1: String
        Title of plot 1
    name_plot_2: String
        Title of plot 2
            
    """
    fig, (ax_a, ax_b) = plt.subplots(ncols=2, figsize=(26, 16), sharex=True, sharey=True)
    ax_a.imshow(plot1, cmap=plt.cm.gray)
    ax_a.set_title(name_plot_1, fontsize=16)
    ax_a.axis('off')
    ax_b.imshow(plot2, cmap=plt.cm.gray)
    ax_b.set_title(name_plot_2, fontsize=16)
    ax_b.axis('off')
    addArrows(ax_a)
    addArrows(ax_b)

def plot_hist(arr):
    fig, ax = plt.subplots(figsize=(10,6))
    histogram = ax.hist(arr[~np.isnan(arr)].flatten(), bins=60, range=(0,2));
    ax.set_title('Image Histogram', fontsize=16);
    ax.set_xlabel('Gray value', fontsize=14); ax.set_ylabel('Frequency', fontsize=14);

    return histogram
    