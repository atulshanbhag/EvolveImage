""" Evolve an image using an Genetic Algorithm
using circles for fitting.
"""

import os
import sys
from copy import deepcopy
import multiprocessing
import jsonpickle
from PIL import Image, ImageDraw
from utils import fitness
from gene import Gene


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


def run():

    target_image = load_image()


if __name__ == "__main__":
    run()
