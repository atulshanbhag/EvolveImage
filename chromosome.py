""" Class for Chromosome object. It
is a collection of Genes which correspond
to the current generation of the species
used in the Genetic Algorithm.
Selection, Reproduction, Crossover and
Mutation occur on these chromosomes, and
the fittest chromosome survive.

This class also draws the chromosome to
the canvas, and returns an image.
"""

import random
from PIL import Image, ImageDraw
from gene import Gene


class Chromosome(object):

    # By default, chromosome contains 50 genes.
    def __init__(self, size, gene_count=50):
        self._size = size
        self._gene_count = gene_count
        self._genes = [Gene(self._size) for _ in range(self._gene_count)]

    def __repr__(self):
        return "Chromosome( GeneSize({0}), GeneSet({1}) )".format(
            self._gene_count, self._genes)

    def __len__(self):
        return self._gene_count

    MUTATION_CHANCE = 0.01
    ADD_CHANCE = 0.3
    DEL_CHANCE = 0.2

    def add_gene(self):
        """ Add a new Gene to the chromosome.
        """

        if Chromosome.ADD_CHANCE < random.random():
            self._gene_count += 1
            self._genes.append(Gene(self._size))

        else:
            pass

    def del_gene(self):
        """ Delete a Gene from the geneset
        of the Chromosome.
        """

        if len(self) > 0 and Chromosome.DEL_CHANCE < random.random():
            self._gene_count -= 1
            self._genes.remove(random.choice(self._genes))

        else:
            pass

    def mutate(self):
        """ Mutation operator for the Genetic
        Algorithm. If gene count is fairly small
        mutate all the genes. Else choose a random
        subset of the genes to mutate.

        Also add and/or delete a gene from the
        chromosome randomly.
        """

        if self._gene_count < 100:
            for g in self._genes:
                if Chromosome.MUTATION_CHANCE < random.random():
                    g.mutate()

        else:
            gene_subset = random.sample(self._genes, int(
                self._gene_count * Chromosome.MUTATION_CHANCE))
            for g in gene_subset:
                g.mutate()

        self.add_gene()
        self.del_gene()

    def draw_image(self):
        """ Draw the chromosome onto an image
        and return the image. Each gene from the
        geneset is drawn on to the image.
        """

        img = Image.new("RGBA", self._size, (255, 255, 255))
        front = Image.new("RGBA", self._size)
        draw = ImageDraw.Draw(front)

        for g in self._genes:
            color = (g.color.r, g.color.g, g.color.b, g.color.alpha)
            rect = ((g.pos.x - g.diameter), (g.pos.y - g.diameter),
                    (g.pos.x + g.diameter), (g.pos.y + g.diameter))
            draw.ellipse(rect, outline=color, fill=color)

        img.paste(front, mask=front)
        return img

    def save(self):
        """ Save the Chromosome object in
        case of program interrupt.
        """
        s = {"size": self._size,
             "gene_count": self._gene_count,
             "genes": [g.save() for g in self._genes]}

        return s

    def load(self, s):
        """ Load the Chromosome from
        save passed as parameter.
        """
        self._size = s["size"]
        self._gene_count = s["gene_count"]
        self._genes = []
        for g in s["genes"]:
            new_gene = Gene(self._size)
            new_gene.load(g)
            self._genes.append(new_gene)


if __name__ == "__main__":
    c = Chromosome((150, 150), 2)
    print(c)
    C = c
    import jsonpickle
    with open("logs.txt", "w+") as f:
        f.write(jsonpickle.encode(c.save()))
        f.seek(0)
        d = f.read()
        c.load(jsonpickle.decode(d))
        print(c)
