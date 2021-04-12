import random
import numpy as np
import copy
from ga.params import MAX_GENOME_LENGTH, DUPLICATION_RATE


def duplication(individual):
    """
    Operador de duplicación.

    Se genera un número aleatorio entre 0 y 1, en caso de que sea menor que la probabilidad de duplicación, se aplica
    este operador al individuo.

    La duplicación consiste en copiar un número aleatorio de codones del individuo, a partir de una posición aleatoria,
    antes del último codón de la cadena.

    :param individual: individuo al que se le aplica la duplicación
    :return: nuevo individuo tras haberse aplicado la duplicación
    """
    if random.random() < DUPLICATION_RATE:
        genome = copy.copy(individual.genome)
        codons2duplicate = random.randint(1, len(genome))
        start = random.randint(0, len(genome)-codons2duplicate)
        end = start+codons2duplicate
        output = np.insert(genome, -1, genome[start:end])

        if len(output) <= MAX_GENOME_LENGTH:
            individual.genome = list(output)

    return individual

