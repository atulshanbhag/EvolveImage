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

    # test gene
    g = Gene(target_image.size)

    # test save working fine
    print("Initial save", g.save())

    # test blank image
    img = Image.new("RGB", target_image.size, (255, 255, 255))
    # test fitness value with blank, working fine
    fitness(target_image, img)

    # test number of cpu cores
    print("multiprocessing count =", multiprocessing.cpu_count())

    # test load and save feature using jsonpickle
    with open("logs.txt", 'w+') as f:
        f.write(jsonpickle.encode(g.save()))

        f.seek(0)
        d = jsonpickle.decode(f.read())

    print("Final save", d)
    g.load(d)
    print(g)

    # canvas = ImageDraw.Draw(img)
    # print(canvas)

    # im = np.array(target_image)
    # print(im.shape)


if __name__ == "__main__":
    run()
