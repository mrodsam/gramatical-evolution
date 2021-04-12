import random
from ga.params import OFFSPRING_SIZE, TOURNAMENT_SIZE


def tournament_selection(population):
    """
    Selección de padres por torneo.

    Se seleccionan tantos padres como descendientes se desee generar.
    Se escogen aleatoriamente TOURNAMENT_SIZE candidatos de entre la población y el que tiene mejor fitness de entre
    ellos es seleccionado como padre.

    :param population: población actual
    :return: conjunto de individuos seleccionados como padres
    """

    mating_pool = []
    while len(mating_pool) < OFFSPRING_SIZE:
        candidates = random.sample(population, TOURNAMENT_SIZE)
        candidates.sort(reverse=True)
        mating_pool.append(candidates[0])

    return mating_pool
