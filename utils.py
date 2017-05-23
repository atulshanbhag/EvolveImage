""" Utils for Genetic Algorithm used
for evolving images.
"""

import os
import sys
import numpy as np
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


def load_image(image="monalisa.png"):
    """ Load the image file given
    filename as parameter.
    """
    # Target image location
    TARGET_LOCATION = os.path.join(os.getcwd(), image)

    # Load target image file. Error if doesn't exist.
    try:
        target_image = Image.open(TARGET_LOCATION)
    except IOError:
        print("Target image {0} not found. Must be placed as {0}".format(
            image, TARGET_LOCATION))
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


if __name__ == "__main__":
    p = Point(10, 10)
    print(p)
    c = Color(10, 10, 10, 10)
    print(c)
