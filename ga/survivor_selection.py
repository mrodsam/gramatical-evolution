from ga.params import POPULATION_SIZE


def age_based_replacement(offspring, population):
    """
    Selección de supervivientes generacional con elitismo.

    La descendencia sustituye a la población anterior. Si el individuo con mejor fitness de la población anterior es
    mejor que el mejor de la población actual, sustituye al peor individuo de la descendencia y se mantiene en la
    población.

    :param offspring: individuos que forman la descendencia
    :param population: población actual
    :return: nueva población
    """
    offspring.sort(reverse=True)
    offspring[-1] = max(max(population), offspring[0])

    return offspring


def fitness_based_replacement(offspring, population):
    """
    Selección de supervivientes basada en su valor de adaptación.

    Se genera un menor número de descendientes que el tamaño de la población y estos sustituyen a los individuos con
    peor fitness de la población.

    :param offspring: individuos que forman la descendencia
    :param population: población actual
    :return: nueva población
    """
    population.sort(reverse=True)
    population = population[:len(population)-len(offspring)]
    population.extend(offspring)

    return population


def mu_lambda_selection(offspring, population):
    """
    Esquema de selección de supervivientes (mu, lambda).

    Se generan lambda descendientes y, de entre ellos, los mu mejores forman la nueva población.

    :param offspring: individuos que forman la descendencia.
    :param population: población actual
    :return: nueva población
    """
    offspring.sort(reverse=True)
    offspring = offspring[:POPULATION_SIZE]

    return offspring


def check_lifetime(population):
    """
    Comprobación del tiempo de vida restante de cada individuo.

    En caso de que el tiempo de vida de un individuo sea 0, este se elimina de la población.
    Se utiliza este método en caso de usar tamaño de población autoadaptativo.

    :param population: población actual
    :return: nueva población
    """
    for index, individual in enumerate(population):
        if individual.lifetime <= 0.:
            population.pop(index)
    population.sort(reverse=True)

    return population
