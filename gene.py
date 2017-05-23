""" Gene class representing the gene
in the genetic algorithm. Each gene
contains a circle of randomly generated
size and color, used for fitting the
image.
"""

import random
from utils import Point, Color


class Gene(object):

    def __init__(self, size):
        # Let diameter of circle be randomly from [2, 15)
        self._diameter = random.randint(2, 15)
        self._size = size
        self._width, self._height = self._size

        # Randomly choose a pixel point in the image space.
        self._pos = Point(random.randint(0, self._width),
                          random.randint(0, self._height))

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
        return "Gene( Diameter({0}), {1}, {2} )".format(
            self._diameter, self._pos, self._color)

    # Mutation type parameters.
    PARAMS = ["diameter", "pos", "color"]

    def mutate(self):
        # Randomly choose the amount of mutation to be done.
        mutation_size = max(1, int(round(random.gauss(15, 4)))) // 100

        # Randomly choose the mutation type from PARAMS.
        # Options --> diameter, pos, color
        mutation_type = random.choice(Gene.PARAMS)

        if mutation_type == "diameter":
            self._diameter = max(1, random.randint(int(
                self._diameter * (1 - mutation_size)), int(
                self._diameter * (1 + mutation_size))))

        elif mutation_type == "pos":
            x = max(0, random.randint(
                int(self._pos.x * (1 - mutation_size)), int(
                    self._pos.x * (1 + mutation_size))))
            y = max(0, random.randint(
                int(self._pos.y * (1 - mutation_size)), int(
                    self._pos.y * (1 + mutation_size))))
            self._pos = Point(min(x, self._width), min(
                y, self._height))

        # mutation_type == color
        else:
            r = min(max(0, random.randint(
                int(self._color.r * (1 - mutation_size)),
                int(self._color.r * (1 + mutation_size)))), 255)
            g = min(max(0, random.randint(
                int(self._color.g * (1 - mutation_size)),
                int(self._color.g * (1 + mutation_size)))), 255)
            b = min(max(0, random.randint(
                int(self._color.b * (1 - mutation_size)),
                int(self._color.b * (1 + mutation_size)))), 255)
            alpha = min(max(0, random.randint(
                int(self._color.alpha * (1 - mutation_size)),
                int(self._color.alpha * (1 + mutation_size)))), 255)

            self._color = Color(r, g, b, alpha)

    # Save the gene in case of program interrupt.
    def save(self):
        """Save the gene object in case
        of the program interrupt.
        """

        s = {"size": self._size,
             "diameter": self._diameter,
             "pos": self._pos,
             "color": self._color}
        return s

    # Load the saved gene.
    def load(self, s):
        """ Load the gene object from
        save parameter.
        """

        self._size = s["size"]
        self._diameter = s["diameter"]
        self._pos = s["pos"]
        self._color = s["color"]


if __name__ == "__main__":
    g = Gene((150, 150))
    print(g)
