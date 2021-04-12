import math
import random
import itertools
from ga.params import FIX_LENGTH, OFFSPRING_SIZE, POPULATION_SIZE, MAX_GENOME_LENGTH, GENERATIONS, VARIABLE_POPULATION_SIZE, MIN_LIFETIME, MAX_LIFETIME, ETA, SELF_ADAPTATION, FITNESS_BASED_REPLACEMENT, UNIFORM_CROSSOVER, AGE_BASED_REPLACEMENT
from ga.individual import Individual
from ga.parent_selection import tournament_selection
from ga.recombination import one_point_crossover, uniform_crossover
from ga.mutation import random_resetting
from ga.survivor_selection import fitness_based_replacement, age_based_replacement, mu_lambda_selection, check_lifetime
from ga.duplication import duplication
from ga.fitness import fitness_function, phenotypeToExpression, average_fitness
from ga.local_search import local_search


def initialization():
    """
    Inicialización de la población: se crean POPULATION_SIZE individuos con una longitud de genoma aleatoria entre 1 y MAX_GENOME_LENGTH.

    :return: Población inicial
    """
    if FIX_LENGTH:
        return [Individual(None, MAX_GENOME_LENGTH) for _ in range(POPULATION_SIZE)]
    else:
        return [Individual(None, random.randint(1, MAX_GENOME_LENGTH)) for _ in range(POPULATION_SIZE)]


def define_model():
    """
    Según los parámetros especificados se asigna un operador de recombinación y un método de selección de supervivientes.

    :return: Funciones escogidas para recombinación y selección de supervivientes
    """
    if UNIFORM_CROSSOVER:
        crossover = uniform_crossover
    else:
        crossover = one_point_crossover

    if AGE_BASED_REPLACEMENT:
        survivor_selection = age_based_replacement
    elif SELF_ADAPTATION:
        survivor_selection = mu_lambda_selection
    elif VARIABLE_POPULATION_SIZE or FITNESS_BASED_REPLACEMENT:
        survivor_selection = fitness_based_replacement
    else:
        survivor_selection = age_based_replacement

    return crossover, survivor_selection


def search(population, grammar):
    """
    Ejecución del algoritmo de búsqueda, en este caso un algoritmo genético.

    :param population: Población inicial
    :param grammar: Objeto con la gramática BNF especificada y métodos necesarios para generar el fenotipo de un individuo
    :return: Individuo con mejor fitness de la población tras completar la búsqueda,
            número de generaciones necesarias hasta encontrar una solución,
            lista con los fitness de los mejores individuos de cada generación,
            número de evaluaciones de fitness realizadas durante las búsquedas locales en cada generación
    """

    # Evaluación del fitness de la población inicial
    evaluate_fitness(population, grammar)

    # Cálculo del tiempo de vida de la población inicial
    if VARIABLE_POPULATION_SIZE:
        compute_lifetime(population)

    # Almacenamiento del mejor individuo de la población inicial
    best_individual = max(population)
    population.sort(reverse=True)

    first = True
    gens_to_sol = 0

    best_individuals = []
    total_local_evaluations = 0
    # Se escogen los operadores de cruce y selección de supervivientes según los parámetros definidos
    crossover, survivor_selection = define_model()
    # Ejecución del algoritmo de búsqueda durante un número GENERATIONS de generaciones
    for generation in range(0, GENERATIONS):
        population, best_individual, local_evaluations = search_step(population, grammar, generation, crossover, survivor_selection)
        best_individuals.append(best_individual.fitness)
        # Si se alcanza una solución, se guarda el número de evaluaciones realizadas durante la búsqueda local y la
        # generación en la que se ha obtenido.
        if first and best_individual.hits == 51:
            total_local_evaluations += local_evaluations
            gens_to_sol = generation
            first = False

    return best_individual, gens_to_sol, best_individuals, total_local_evaluations


def search_step(population, grammar, generation, crossover, survivor_selection):
    """
    Ejecución de cada generación de la búsqueda.

    :param population: Población inicial
    :param grammar: Objeto con la gramática BNF especificada y métodos necesarios para generar el fenotipo de un individuo
    :param generation: Número de la generación actual
    :param crossover: Método seleccionado para realizar la recombinación
    :param survivor_selection: Método seleccionado para realizar la selección de supervivientes
    :return: nueva población generada tras aplicar el proceso de búsqueda,
            individuo con mejor fitness de la población,
            número de evaluaciones de fitness realizadas durante el proceso de búsqueda local
    """

    # Selección de padres
    mating_pool = tournament_selection(population)

    # Recombinación
    offspring = []
    while len(offspring) < OFFSPRING_SIZE:
        offspring.extend(crossover(*random.sample(mating_pool, 2), generation))

    # Mutación
    offspring = list(map(random_resetting, offspring, itertools.repeat(generation, len(offspring))))

    # Duplicación
    offspring = list(map(duplication, offspring))

    # Evaluación del fitness de la descendencia
    evaluate_fitness(offspring, grammar)

    # Búsqueda local
    offspring, local_evaluations = local_search(offspring, grammar)

    # Cálculo del tiempo de vida de la descendencia
    if VARIABLE_POPULATION_SIZE:
        compute_lifetime(offspring)

    # Selección de supervivientes
    population = survivor_selection(offspring, population)

    # Decremento del tiempo de vida de la población y eliminación de individuos a los que se le haya terminado
    if VARIABLE_POPULATION_SIZE:
        population = decrease_lifetime(population)
        population = check_lifetime(population)

    return population, max(population), local_evaluations


def evaluate_fitness(population, grammar):
    """
    Cálculo del fitness de cada individuo de la población.

    :param population: Población actual
    :param grammar: Objeto con la gramática BNF especificada y métodos necesarios para generar el fenotipo de un individuo

    """
    for individual in population:
        individual.phenotype = grammar.decode(individual.genome)
        if individual.phenotype is not None:
            individual.fitness, individual.hits = fitness_function(phenotypeToExpression(individual.phenotype))
        # En caso de que el individuo sea inválido y no se realice reparación, se le asigna un fitness infinito
        else:
            individual.fitness = math.inf


def compute_lifetime(population):
    """
    Cálculo del tiempo de vida inicial de cada individuo (en caso de utilizar tamaño de población variable).

    :param population: Individuos de los que se desea calcular el tiempo de vida.

    """
    population.sort(reverse=True)
    avg_fitness = average_fitness(population)
    best_fitness = max(population).fitness
    worst_fitness = min(population).fitness

    for individual in population:
        if individual.fitness == math.inf:
            individual.lifetime = 1.0
        # Bi-linear allocation
        if avg_fitness <= individual.fitness:
            try:
                individual.lifetime = MIN_LIFETIME + ETA * ((worst_fitness - individual.fitness)/(worst_fitness - avg_fitness))
            except ZeroDivisionError:
                individual.lifetime = MAX_LIFETIME

        elif avg_fitness > individual.fitness:
            individual.lifetime = 0.5 * (MIN_LIFETIME + MAX_LIFETIME) + ETA * ((avg_fitness - individual.fitness)/(avg_fitness - best_fitness))


def decrease_lifetime(population):
    """
    Disminución en una unidad del tiempo de vida de cada individuo de la población tras cada generación.

    No se disminuye el tiempo de vida del individuo con mejor fitness.
    :param population: Población actual
    :return: Población actualizada
    """
    population.sort(reverse=True)
    for ind in population[1:]:
        ind.lifetime -= 1

    return population
