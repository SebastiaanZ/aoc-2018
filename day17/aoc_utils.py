import numpy as np
from collections import namedtuple


Slice = namedtuple("Slice", ["x", "y"])
Cursor = namedtuple("Cursor", ["row", "col"])
Location = namedtuple("Location", ["left", "right"])


def create_array(fn):

    axis = {"x": None, "y": None}
    x_min = y_min = np.inf
    x_max = y_max = -np.inf
    indices = []

    with open(fn) as f:
        for line in f:
            for part in line.strip().split(", "):
                splice = part[2:].split("..")
                axis[part[0]] = (int(splice[0]), int(splice[-1]))
            x_min = x_min if axis["x"][0] > x_min else axis["x"][0]
            x_max = x_max if axis["x"][1] < x_max else axis["x"][1]
            y_min = y_min if axis["y"][0] > y_min else axis["y"][0]
            y_max = y_max if axis["y"][1] < y_max else axis["y"][1]
            indices.append(Slice(**axis))

    ground = np.full((y_max+1, x_max - x_min + 3), fill_value=".", dtype=str)

    for s in indices:
        x_lower = s.x[0] - x_min + 1
        x_upper = s.x[1] - x_min + 2
        y_lower = s.y[0]
        y_upper = s.y[1] + 1
        ground[y_lower:y_upper, x_lower:x_upper] = "#"
    ground[0][500 + 1 - x_min] = "+"
    return ground, Cursor(0, 500 + 1 - x_min), y_min


def waterfall(cursor, ground):
    water_startpoint = cursor.row + 1
    find_endpoint = np.isin(ground[water_startpoint:, cursor.col], ["#", "~", "|"])
    endpoint = np.where(find_endpoint)[0]
    if endpoint.size > 0:
        water_endpoint = endpoint[0] + water_startpoint
        finite = True
    else:
        water_endpoint = ground.shape[0] + 3
        finite = False

    ground[water_startpoint:water_endpoint, cursor.col] = "|"
    if finite and ground[water_endpoint, cursor.col] == "|":
        return None

    cursor = Cursor(water_endpoint - 1, cursor.col) if finite else None
    return cursor


def spread_water(cursor, ground):
    done = False
    while not done:
        cursor, done = fill_water(cursor, ground)
    return cursor


def check_boundaries(cursor, ground):
    clay_left = np.where(ground[cursor.row, :cursor.col] == "#")[0]
    clay_right = np.where(ground[cursor.row, cursor.col:] == "#")[0]

    if clay_left.size == 0:
        left_boundary = 0
    else:
        left_boundary = clay_left.max()

    if clay_right.size == 0:
        right_boundary = ground.shape[0]
    else:
        right_boundary = clay_right.min() + cursor.col

    return Location(left_boundary, right_boundary)


def check_bottom(cursor, ground, boundary):
    left_bottom = np.isin(ground[cursor.row + 1, boundary.left:cursor.col], ["#", "~"])
    right_bottom = np.isin(ground[cursor.row + 1, cursor.col:(boundary.right+1)], ["#", "~"])

    left_closed = np.all(left_bottom)
    right_closed = np.all(right_bottom)

    left_gap = right_gap = None

    if not left_closed:
        left_gap = np.where(left_bottom == False)[0].max() + boundary.left
    if not right_closed:
        right_gap = np.where(right_bottom == False)[0].min() + cursor.col
    return Location(left_closed, right_closed), Location(left_gap, right_gap)


def fill_water(cursor, ground):
    boundary = check_boundaries(cursor, ground)
    enclosed, gap = check_bottom(cursor, ground, boundary)

    if(all(enclosed)):
        ground[cursor.row, boundary.left + 1:boundary.right] = "~"
        return Cursor(cursor.row - 1, cursor.col), False
    elif enclosed.left:
        ground[cursor.row, boundary.left+1:gap.right+1] = "|"
        return (Cursor(cursor.row, gap.right), ), True
    elif enclosed.right:
        ground[cursor.row, gap.left:boundary.right] = "|"
        return (Cursor(cursor.row, gap.left), ), True
    else:
        ground[cursor.row, gap.left:gap.right+1] = "|"
        return (Cursor(cursor.row, gap.left), Cursor(cursor.row, gap.right)), True

    raise Exception("This shouldn't happen!")
