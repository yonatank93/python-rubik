colors = ["y", "b", "r", "g", "o", "w"]

# Color combinations of corners and edges
corner_triplets = ["rby", "boy", "ogy", "gry", "brw", "rgw", "gow", "obw"]
edge_doublets = ["yb", "yr", "yg", "yo", "ob", "br", "rg", "go", "ow", "bw", "rw", "gw"]
# Indices to extract the elements of the cube
# Centers: top, left, front, right, back, bottom
center_indices = [4, 13, 22, 31, 40, 49]
# Corners: top-back-left, top-back-right, top-fron-left, top-front-right,
# bottom-front-left, bottom-front-right, bottom-back-left, bottom-back-right
corner_indices = [
    [9, 38, 0],
    [28, 27, 2],
    [18, 11, 6],
    [27, 20, 8],
    [17, 24, 45],
    [26, 33, 47],
    [44, 15, 51],
    [35, 42, 53],
]
# Edges: top-back, top-left, top-right, top-front,
# back-left, left-front, front-right, right-back,
# bottom-front, bottom-left, bottom-right, bottom-back
edge_indices = [
    [1, 37],
    [3, 10],
    [5, 28],
    [7, 19],
    [41, 12],
    [14, 21],
    [23, 30],
    [32, 39],
    [25, 46],
    [16, 48],
    [34, 50],
    [43, 52],
]

bottom_locs = ["bottom-front", "bottom-left", "bottom-right", "bottom-back"]


def are_cyclic_equivalent(set1, set2):
    """Check if 2 sets (or in this case are strings) are cyclic permutation of each other.
    We will also use this to check if a subset of a string is potentially from a cyclic
    permutation of the other set.

    For example, if we compare "rgb" and "brg", the function should return True. So as if
    we compare "rgb" and "gb".
    """
    # Set the reference set
    if len(set1) >= len(set2):
        ref_set = set1
        set_ask = set2
    else:
        ref_set = set2
        set_ask = set1
    equivalent = set_ask in ref_set + ref_set
    return equivalent


def infer_bottom_center(faces_no_bottom):
    # First, get all the known center colors
    known_centers = [faces_no_bottom[ii] for ii in center_indices[:-1]]
    # Then, just find the missing color (this is an easy job)
    missing_center = list(set(colors) - set(known_centers))[0]
    return missing_center


def infer_bottom_corners(faces_no_bottom):
    # First, get the colors of the bottom face corners that we know
    bottom_known_corners = []
    for idx in corner_indices[4:]:
        bottom_known_corners.append("".join([str(faces_no_bottom)[ii] for ii in idx[:2]]))

    # Then, find the missing colors
    missing_corner_colors_bottom = []
    corner_triplets_copy = corner_triplets.copy()  # Make a copy so we can remove stuffs
    for member in bottom_known_corners:
        for candidate in corner_triplets_copy:
            # We compare each doublet of known colors with the corner triplets
            if are_cyclic_equivalent(member, candidate):
                # Found the correct triplets, get the missing color
                missing_color = candidate
                # Find the missing color by removing known colors from the triplets
                for col in member:
                    missing_color = missing_color.replace(col, "")
                missing_corner_colors_bottom.append(missing_color)
                # Remove the corner we just found from the candidate to speed up the next
                # search
                corner_triplets_copy.remove(candidate)
                break
    return missing_corner_colors_bottom


def infer_bottom_edges(faces_no_bottom):
    # First, let's look at what complete edges we have so far in the cube
    known_edges = []
    for idx in edge_indices[:-4]:  # Exclude the bottom face
        known_edges.append("".join([faces_no_bottom[ii] for ii in idx]))
    # From this information, let's list the missing edges
    missing_edges = edge_doublets.copy()  # So we can remove stuffs[]
    for edge in known_edges:
        for candidate in missing_edges:
            if are_cyclic_equivalent(edge, candidate):
                missing_edges.remove(candidate)
                break
    # Then, let's list the color of the bottom edges that we know
    bottom_known_edges = []
    for idx in edge_indices[-4:]:
        bottom_known_edges.append(str(faces_no_bottom)[idx[0]])

    # Finally, let's do the search
    missing_edge_colors_bottom = ["", "", "", ""]
    while len(missing_edges) > 0:
        state_changed = False
        for ii, edge in enumerate(bottom_known_edges):
            if missing_edge_colors_bottom[ii] == "":
                # What possibility do we have?
                poss = [edge in elem for elem in missing_edges]
                if sum(poss) == 1:  # There is only 1 option, that must be it.
                    correct_edge = missing_edges[poss.index(True)]
                    # Remove this corner from the list of missing corner, since we have
                    # found it
                    missing_edges.remove(correct_edge)
                    # Get the missing color
                    missing_edge_colors_bottom[ii] = correct_edge.replace(edge, "")
                    state_changed = True
            else:
                continue

        if not state_changed:
            # Request for input from user
            idx_req = missing_edge_colors_bottom.index("")
            print("Cannot infer further")
            while True:
                add_input = input(f"Please input color of {bottom_locs[idx_req]}: ")
                if add_input in colors:
                    break
                else:
                    print("Please input one of", colors)
            # Update the missing edge colors information
            missing_edge_colors_bottom[idx_req] = add_input
            # Remove this new edge from the missing edges list
            correct_edge = bottom_known_edges[idx_req] + add_input
            if correct_edge in missing_edges:
                missing_edges.remove(correct_edge)
            else:
                missing_edges.remove(correct_edge[::-1])
    return missing_edge_colors_bottom
