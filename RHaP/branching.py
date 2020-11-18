import numpy as np
from skimage.morphology import skeletonize
from skan import Skeleton, summarize
import networkx as nx
import toolz as tz


def branch_classification(thres):
    """Predict the extent of branching.

    Parameters
    ----------
    thres: array
        thresholded image to be analysed

    Returns
    -------
    skel: array
        skeletonised image
    is_main: array
       whether the hydride identified is part of the main section or if it is a branch
    BLF: int/float
        branch length fraction
    """

    skeleton = skeletonize(thres)
    skel = Skeleton(skeleton, source_image=thres)
    summary = summarize(skel)

    is_main = np.zeros(summary.shape[0])
    us = summary['node-id-src']
    vs = summary['node-id-dst']
    ws = summary['branch-distance']

    edge2idx = {
        (u, v): i
        for i, (u, v) in enumerate(zip(us, vs))
    }

    edge2idx.update({
        (v, u): i
        for i, (u, v) in enumerate(zip(us, vs)) 
    })

    g = nx.Graph()

    g.add_weighted_edges_from(
        zip(us, vs, ws)
    )

    for conn in nx.connected_components(g):
        curr_val = 0
        curr_pair = None
        h = g.subgraph(conn)
        p = dict(nx.all_pairs_dijkstra_path_length(h))
        for src in p:
            for dst in p[src]:
                val = p[src][dst]
                if (val is not None
                        and np.isfinite(val)
                        and val > curr_val):
                    curr_val = val
                    curr_pair = (src, dst)
        for i, j in tz.sliding_window(
            2,
            nx.shortest_path(
                h, source=curr_pair[0], target=curr_pair[1], weight='weight'
            )
        ):
            is_main[edge2idx[(i, j)]] = 1

    summary['main'] = is_main

    # Branch Length Fraction

    total_length = np.sum(skeleton)
    trunk_length = 0
    for i in range(summary.shape[0]):
        if summary['main'][i]:
            trunk_length += summary['branch-distance'][i]

    branch_length = total_length - trunk_length
    BLF = branch_length/total_length

    return skel, is_main, BLF
