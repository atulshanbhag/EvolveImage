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


def run():
    # Target image file and location.
    TARGET_IMAGE_NAME = "monalisa.png"
    TARGET_LOCATION = os.path.join(os.getcwd(), TARGET_IMAGE_NAME)


    # Load target image file. Error if doesn't exist.
    try:
        target_image = Image.open(TARGET_LOCATION)
    except IOError:
        print("Target image {0} not found. Must be placed as {0}".format(
            TARGET_IMAGE_NAME, TARGET_LOCATION))
        sys.exit()


    TARGET_IMAGE_WIDTH = target_image.width
    TARGET_IMAGE_HEIGHT = target_image.height
    TARGET_IMAGE_SIZE = target_image.size

    # test gene
    g = Gene(TARGET_IMAGE_SIZE)

    # test save working fine
    print("Initial save", g.save())

    # test blank image
    img = Image.new("RGB", TARGET_IMAGE_SIZE, (255, 255, 255))
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

run()
