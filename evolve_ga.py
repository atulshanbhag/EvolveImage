""" Evolve an image using an Genetic Algorithm
using circles for fitting.
"""

import os
import sys
import random
from copy import deepcopy
import multiprocessing
import jsonpickle
import numpy as np
from PIL import Image, ImageDraw


# Target image file and location.
TARGET_IMAGE_NAME = 'monalisa.png'
TARGET_LOCATION = os.getcwd() + '\{0}'.format(TARGET_IMAGE_NAME)


# Load target image file. Error if doesn't exist.
try:
    target_image = Image.open(TARGET_LOCATION)
except IOError:
    print('Target image {0} not found. Must be placed as {0}'.format(
        TARGET_NAME, TARGET_LOCATION))
    sys.exit()


TARGET_IMAGE_WIDTH = target_image.width
TARGET_IMAGE_HEIGHT = target_image.height
TARGET_IMAGE_SIZE = target_image.size


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

    # Save point object in case of interrupt.
    def save(self):
        s = {'x': self._x, 'y': self._y}
        return s

    # Load point object from saved paramter.
    def load(self, s):
        self._x = s['x']
        self._y = s['y']

    # Add 2 points
    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __eq__(self, other):
        return (self.x == other.x) and (self.y == other.y)

    def __repr__(self):
        return 'Point({0}, {1})'.format(self.x, self.y)


class Color(object):
    """ Helper class for representing a color.
    Represented as a RGB value in radix-256
    with opacity.
    """

    def __init__(self, r, g, b, alpha=0):
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

    # Save color object in case of interrupt.
    def save(self):
        s = {'r': self._r, 'g': self._g,
             'b': self._b, 'alpha': self._alpha}
        return s

    # Load color object from saved paramter.
    def load(self, s):
        self._r = s['r']
        self._g = s['g']
        self._b = s['b']
        self._alpha = s['alpha']

    def __repr__(self):
        return 'Color({0}, {1}, {2}, {3})'.format(
            self.r, self.g, self.b, self.alpha)


GENE_PARAMS = ['diameter', 'pos', 'color']


class Gene(object):
    """ Gene class representing the gene 
    in the genetic algorithm. Each gene 
    contains a circle of randomly generated 
    size and color, used for fitting the 
    image.
    """

    def __init__(self):
        # Let diameter of circle be randomly from [2, 15)
        self._diameter = random.randint(2, 15)

        # Randomly choose a pixel point in the image space.
        self._pos = Point(random.randint(0, TARGET_IMAGE_WIDTH),
                          random.randint(0, TARGET_IMAGE_HEIGHT))

        # Randomly assign color to pixel with random opacity
        self._color = Color(random.randint(0, 255), random.randint(
            0, 255), random.randint(0, 255), random.randint(0, 255))

    @property
    def diameter(self):
        return self._diameter

    @property
    def pos(self):
        return self._pos

    @property
    def color(self):
        return self._color

    def __repr__(self):
        return 'Gene( Diameter({0}), {1}, {2} )'.format(
            self.diameter, self.pos, self.color)

    def mutate(self):
        # Randomly choose the amount of mutation to be done.
        mutation_size = max(1, int(round(random.gauss(15, 4)))) // 100

        # Randomly choose the mutation type from GENE_PARAMS.
        # Options --> diameter, pos, color
        mutation_type = random.choice(GENE_PARAMS)

        if mutation_type == 'diameter':
            self._diameter = max(1, random.randint(int(
                self._diameter * (1 - mutation_size)), int(self.diameter * (1 + mutation_size))))

        elif mutation_type == 'pos':
            x = max(0, random.randint(
                int(self.pos.x * (1 - mutation_size)), int(self.pos.x * (1 + mutation_size))))
            y = max(0, random.randint(
                int(self.pos.y * (1 - mutation_size)), int(self.pos.y * (1 + mutation_size))))
            self._pos = Point(min(x, TARGET_IMAGE_SIZE[0]), min(
                y, TARGET_IMAGE_SIZE[1]))

        # mutation_type == color
        else:
            r = min(max(0, random.randint(int(self.color.r * (1 - mutation_size)),
                                          int(self.color.r * (1 + mutation_size)))), 255)
            g = min(max(0, random.randint(int(self.color.g * (1 - mutation_size)),
                                          int(self.color.g * (1 + mutation_size)))), 255)
            b = min(max(0, random.randint(int(self.color.b * (1 - mutation_size)),
                                          int(self.color.b * (1 + mutation_size)))), 255)
            alpha = min(max(0, random.randint(int(self.color.alpha * (1 - mutation_size)),
                                              int(self.color.alpha * (1 + mutation_size)))), 255)
            self._color = Color(r, g, b, alpha)

    # Save the gene in case of program interrupt.
    def save(self):
        """ Save the gene object in case 
        of the program interrupt.
        """
        s = {'diameter': self._diameter,
             'pos': self._pos,
             'color': self._color}
        return s

    # Load the saved gene.
    def load(self, s):
        """ Load the gene object from 
        save parameter
        """
        self._diameter = s['diameter']
        self._pos = s['pos']
        self._color = s['color']

if __name__ == '__main__':
    g = Gene()
    print(g.save())
