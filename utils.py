""" Utils for Genetic Hill Climbing Algorithm used
for evolving images.
"""

import sys
import numpy as np
from copy import deepcopy
from PIL import Image


class Point(object):
    """ Helper class to define a point
    in the 2d space. Used to represent
    an image pixel.
    """

    def __init__(self, x, y):
        self._x = x
        self._y = y

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    # Add 2 points
    def __add__(self, other):
        return Point(self._x + other.x, self._y + other.y)

    def __eq__(self, other):
        return (self._x == other.x) and (self._y == other.y)

    def __repr__(self):
        return "Point({0}, {1})".format(self._x, self._y)


class Color(object):
    """ Helper class for representing a color.
    Represented as a RGB value in radix-256
    with opacity.
    """

    def __init__(self, r, g, b, alpha=255):
        self._r = r
        self._g = g
        self._b = b
        self._alpha = alpha

    @property
    def r(self):
        return self._r

    @property
    def g(self):
        return self._g

    @property
    def b(self):
        return self._b

    @property
    def alpha(self):
        return self._alpha

    def __repr__(self):
        return "Color({0}, {1}, {2}, {3})".format(
            self._r, self._g, self._b, self._alpha)


def load_image(image):
    """ Load the image file given
    file location as parameter.
    """

    # Load target image file. Error if doesn't exist.
    try:
        target_image = Image.open(image).convert("RGBA")
    except IOError:
        print("Target image {0} not found. Must be placed as {1}".format(
            image, image))
        sys.exit()

    return target_image


def fitness(img1, img2):
    """ Calculate the fitness value for one
    image corresponding to another image.
    Uses Euclidean Mean Squared Error as
    fitness function. This fitness function
    decides the survival of the genes for
    upcoming generations.

    Convert images to numpy arrays for
    faster computation of fitness value.
    """

    im1 = np.array(img1, dtype=np.int16)
    im2 = np.array(img2, dtype=np.int16)

    return (np.abs(im1 - im2).mean() / 255 * 100)


def mutate_test(parent, target):
    """ Randomly mutate a chromosome
    given as parameter. Return new fitness
    value compared with target. Exit on
    KeyboardInterrupt.
    """

    try:
        child = deepcopy(parent)
        child.mutate()
        return (fitness(child.draw(), target), child)
    except KeyboardInterrupt:
        pass


def group_mutate(parent, num_child, pool, target):
    """ Return num_child children on
    mutating the parent. Run the mutations
    on mutiple cores.
    """

    results = pool.starmap(mutate_test,
                           [(parent, target) for _ in range(num_child)])
    return results
