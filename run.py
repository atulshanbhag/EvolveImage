""" Evolve an image using an Genetic Algorithm
using circles for fitting.
"""
import os
import multiprocessing
from utils import *
from chromosome import Chromosome


def run(cores, so=None):
    """ Genetic Algorithm run here.
    Stores the image results in RESULTS
    directory, after every SAVE_PER_GEN
    generations .
    """

    # Load image.
    target_image = load_image()

    RESULTS = "results"
    # Make RESULTS directory, if not exists.
    if not os.path.exists(RESULTS):
        os.mkdir(RESULTS)

    # Logs file, in RESULTS directory.
    f = file(os.path.join(RESULTS, "logs.txt"), "a")

    target = target_image
    generation = 1
    INIT_GENES = 50
    parent = Chromosome(target.size, INIT_GENES)

    # Load Save file from function parameter.
    if so is not None:
        generation = parent.load(so)

    prev_fitness = 0
    curr_fitness = fitness(parent.draw(), target)

    p = multiprocessing.Pool(cores)
    SAVE_PER_GEN = 50

    while True:

        print("Generation {0} Score {1}".format(
            generation, curr_fitness))
        f.write("Generation {0} Score {1}\n".format(
            generation, curr_fitness))

        if generation % SAVE_PER_GEN == 0:
            parent.draw().save(os.path.join(
                RESULTS, "{}.png".format(generation)))

        generation += 1
        prev_fitness = curr_fitness

        children = [parent, ]
        new_fitness = [curr_fitness, ]


if __name__ == "__main__":
    run()
