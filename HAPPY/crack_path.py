import numpy as np
from scipy import ndimage
from skimage.graph import route_through_array, MCP_Flexible, MCP_Geometric
from skimage.transform import rescale
from scipy.ndimage.morphology import binary_dilation
from skimage.graph import MCP_Flexible


#so here we are creating a new class that is based off MCP flex allowing us to change the functions in it
class My_MCP(MCP_Flexible):   #has a set of functions and variables 

    def __init__(self, costs, offsets=None, fully_connected=True, distance_weight=0):
        self.distance_weight = distance_weight
        super().__init__(
                costs, offsets=offsets, fully_connected=fully_connected
                )     # Based on the skimage.graph MCP_Flexible class

    def travel_cost(self, old_cost, new_cost, offset_length):
        my_cost = new_cost + (self.distance_weight*offset_length)
        return my_cost


def det_crack_path(
        thres,
        crop_threshold,
        num_runs,
        kernel_size,
        distance_weight=0,
        ):
    """Determine possible crack paths in the micrograph.

    Parameters
    ----------
    thres: array
        thesholded image to look at
    crop_threshold: array
        calculated during thresholding, array of true and false values
    num_runs: int
        number of crack paths to determine
    kernel_size: int
        Once a crack is found, all future paths must be at least kernel_size
        away from it.
    distance_weight : float
        Crack paths should follow hydrides but only up to a point: they should
        also be short. This weight determines how much the "shortness"
        consideration should count compared to the hydride. Higher weight =>
        shorter paths.

    Returns
    -------
    edist: array
        min euclidean distace from the hydride to the matrix
    path_list:
        list of possible crack paths
    cost_list: list
        list of cost values for each crack path
    """

    # Use distance away from a hydride as a path to route through
    edist = ndimage.morphology.distance_transform_edt(thres == 0)
    edist = rescale(edist, (1, 1))

    # Add a row of zeros on the top and bottom and set cost=0 outside tube
    edist[0, :] = 0
    edist[-1, :] = 0
    edist = np.where(crop_threshold, 0, edist)

    # Make a empty list to store paths and costs
    path_list = []
    cost_list = []

    nrows, ncols = edist.shape

    for _ in np.arange(num_runs):
        # Coordinates and cost corresponding to path

        m = My_MCP(edist, fully_connected=True, distance_weight=distance_weight)
        # if distance_weight==0, this should behave the same as
        # m = MCP_Geometric(edist, fully_connected=True)
        # every coordinate on the top row is a possible start point
        starts = np.stack((np.zeros(ncols), np.arange(ncols)), axis=1)
        # every coordinate on tho bottom row is a possible end point
        ends = np.stack((np.full(ncols, nrows - 1), np.arange(ncols)), axis=1)
        costs, traceback_array = m.find_costs(starts, ends, find_all_ends=False)
        end_column = np.argmin(costs[-1, :])
        path = np.array(m.traceback((-1, end_column)))
        cost = costs[-1, end_column]

        # old code that we imitated manually with classes above:
        # path, cost = route_through_array(edist, [0, 0], [-1, -1])
        
        # Boolean array based on coordinates, True is on path
        path_array = np.zeros(np.shape(edist), dtype=bool)
        for coord in path:
            path_array[coord[0], coord[1]] = True

        # Take away points outside of crop, make coord array and append to list
        path_array_cropped = np.logical_and(path_array, ~crop_threshold)
        path_coords = np.transpose(np.nonzero(path_array_cropped))
        path_list.append(np.array(path_coords))
        cost_list.append(cost)

        # Filtering path based on kernel size, so that the next run will take
        # a different path
        filter_array = binary_dilation(
            path_array_cropped, iterations=kernel_size
        )
        edist = np.where(filter_array, np.inf, edist)
        edist = np.where(crop_threshold, 0, edist)

    edist = ndimage.morphology.distance_transform_edt(thres == 0)
    edist = rescale(edist, (1, 1))

    return edist, path_list, cost_list
