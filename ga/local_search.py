import copy
import random
from ga.fitness import fitness_function, phenotypeToExpression
from ga.params import CODON_SIZE


def local_search(offspring, grammar):
    """
    Método de búsqueda local.

    Se evalúa el fitness de los vecinos del mejor individuo de la descendencia, en caso de que alguno sea mejor,
    se finaliza la búsqueda y se sustituye al individuo por el nuevo.
    Los vecinos de un individuo se calculan aplicando mutación secuencialmente a cada codón del individuo.

    :param offspring: conjunto de individuos que forman la descendencia
    :param grammar: objeto con la gramática BNF especificada y métodos necesarios para generar el fenotipo de un individuo
    :return: conjunto de individuos de la descendencia,
            número de evaluaciones de fitness realizadas hasta completar la búsqueda
    """
    best = max(offspring)
    evaluations = 0

    for i in range(len(best.genome)):
        new_best = copy.deepcopy(best)
        new_best.genome[i] = random.randint(0, CODON_SIZE)
        new_best.phenotype = grammar.decode(new_best.genome)
        if new_best.phenotype is None:
            continue
        new_best.fitness, new_best.hits = fitness_function(phenotypeToExpression(new_best.phenotype))
        evaluations += 1
        if new_best.fitness < best.fitness:
            offspring.sort(reverse=True)
            offspring[0] = new_best
            break

    return offspring, evaluations

