import random
from ga.params import CODON_SIZE, MUTATION_RATE, SELF_ADAPTATION


class Individual(object):

    def __init__(self, genome, length):
        """
        Inicialización de un individuo.

        Se calcula cada codón del individuo de forma aleatoria, salvo que se especifique una secuencia concreta.

        :param genome: secuencia de codones del individuo
        :param length: longitud de la secuencia de codones
        """
        if genome is None:
            self.genome = [random.randint(0, CODON_SIZE) for _ in range(length)]
        else:
            self.genome = genome

        self.fitness = 0
        self.phenotype = None
        self.hits = 0
        if SELF_ADAPTATION:
            self.mutation_rate = 1/len(self.genome)
        else:
            self.mutation_rate = MUTATION_RATE
        self.lifetime = 0

    def __lt__(self, other):
        return self.fitness > other.fitness

    def __str__(self):
        return "Individual: " + str(self.genome) + "; " + str(self.phenotype) + "; " + str(self.fitness) + "; " \
               + str(self.hits) + "; " + str(self.mutation_rate) + "; " + str(self.lifetime)

