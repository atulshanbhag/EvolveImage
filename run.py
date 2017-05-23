""" Evolve an image using an Genetic Algorithm
using circles for fitting.
"""
import os
import sys
import multiprocessing
import jsonpickle
import utils
from chromosome import Chromosome


def run(target, cores, images=None):
    """ Genetic Algorithm run here.
    Stores the image results in RESULTS
    directory, after every SAVE_PER_GEN
    generations .
    """

    RESULTS = "results"
    # Make RESULTS directory, if not exists.
    if not os.path.exists(RESULTS):
        os.mkdir(RESULTS)

    # Logs file, in RESULTS directory.
    f = open(os.path.join(RESULTS, "logs.txt"), "a")

    generation = 1
    INIT_GENES = 50
    parent = Chromosome(target.size, INIT_GENES)

    # Load Save file from function parameter.
    if s is not None:
        generation = parent.load(jsonpickle.decode(s))

    # First generation fitness.
    score = utils.fitness(parent.draw(), target)

    # Create thread pool for each core.
    p = multiprocessing.Pool(cores)

    # Frequency of saves and number of children
    # per generation of genetic algorithm.
    SAVE_PER_GEN = 50
    CHILDS_PER_GEN = 50

    while True:

        print("Generation {0} Score {1}".format(
            generation, round(score, 5)))
        f.write("Generation {0} Score {1}\n".format(
            generation, round(score, 5)))

        # Draw the image and save it.
        # Also save the logs.
        if generation % SAVE_PER_GEN == 0:
            parent.draw().save(os.path.join(
                RESULTS, "{0}.png".format(generation)))

            save_file = open(os.path.join(
                RESULTS, "{0}.txt".format(generation)), "w")
            save_file.write(jsonpickle.encode(parent.save(generation)))
            save_file.close()

        generation += 1

        # Mutate the current parent.
        try:
            results = utils.group_mutate(parent, CHILDS_PER_GEN - 1, p, target)
        except KeyboardInterrupt:
            print("Exiting program... Bye!")
            p.close()
            return

        # Children for the next generation.
        # Includes the current parent in case
        # bad mutation.
        new_score, new_children = map(list, zip(*results))
        new_score.append(score)
        new_children.append(parent)

        # Choose the fittest child for next generation.
        fittest = min(zip(new_children, new_score), key=lambda x: x[1])
        parent, score = fittest


if __name__ == "__main__":
    cores = max(1, multiprocessing.cpu_count() - 1)
    s = None
    target_name = "white.jpg"

    if len(sys.argv) > 1:
        args = sys.argv[1:]

        for i, a in enumerate(args):

            # -t option for specifying the number of cores manually.
            if a == "-t":
                cores = int(args[i + 1])

            # -s option for specifying the saved file.

            # Example usage -->
            # >>> python run.py -s results/100.txt
            # This will run the script from the specified
            # log file.
            elif a == "-s":
                with open(args[i + 1], "r") as save:
                    s = save.read()

            # -i option for specifying the image file.
            # Has to be located in the RESULTS folder.

            # Example usage -->
            # >>> python run.py -i monalisa.png
            elif a == "-i":
                target_name = args[i + 1]

            else:
                pass

    # Load image.
    target = utils.load_image(target_name)

    run(target, cores, s)
