import random
import math
from ga.params import MUTATION_RATE, CODON_SIZE, GENERATIONS, GAMMA, SELF_ADAPTATION, DETERMINISTIC, DETERMINISTIC_BASIC1, DETERMINISTIC_BASIC2


def random_resetting(individual, generation):
    """
    Método de mutación "random resetting".

     Para cada codón del individuo se calcula un número aleatorio en el intervalo [0,1], si este es menor que la probabilidad de mutación
     se cambia el codón por un entero calculado aleatoriamente en el intervalo [0, 255]

    :param individual: individuo al que se le aplica el operador de mutación
    :param generation: número de generación actual para adaptar la probabilidad de mutación
    :return: nuevo individuo tras haberse aplicado la mutación
    """
    pm = select_mutation_rate(individual, generation)

    for i in range(len(individual.genome)):
        if random.random() < pm:
            individual.genome[i] = random.randint(0, CODON_SIZE)

    return individual


def evolve_mutation_rate(individual):
    """
    Probabilidad de mutación autoadaptativa.

    Se calcula una nueva probabilidad de mutación para el individuo que posteriormente se utiliza para mutar su genoma.

    :param individual: individuo para el que se calcula la nueva probabilidad de mutación
    :return: nueva probabilidad de mutación
    """
    new_pm = 1/(1 + ((1 - individual.mutation_rate)/individual.mutation_rate) * math.exp(GAMMA * random.random()))

    if new_pm < 1/len(individual.genome):
        new_pm = 1/len(individual.genome)

    return new_pm


def select_mutation_rate(individual, generation):
    """
    Selección de la probabilidad de mutación según el esquema utilizado.

    Modelo autoadaptativo: la probabilidad de mutación evoluciona junto al individuo.
    Modelo determinista básico 1: en cada generación se aumenta la probabilidad de mutación
    Modelo determinista básico 2: en cada generación se disminuye la probabilidad de mutación
    Modelo determinista "Bäck and Schütz": en cada generación se aplica una fórmula a la probabilidad de mutación
                                         para actualizarla
    Modelo estático: se utiliza siempre la probabilidad de mutación predefinida

    :param individual: individuo al que se le aplica la mutación
    :param generation: generación actual
    :return: probabilidad de mutación a utilizar
    """
    if SELF_ADAPTATION:
        individual.mutation_rate = evolve_mutation_rate(individual)
        pm = individual.mutation_rate

    elif DETERMINISTIC_BASIC1:
        pm = generation / GENERATIONS

    elif DETERMINISTIC_BASIC2:
        pm = 1 - (generation / GENERATIONS)

    # Determinista Back and Schutz: pm = 1/(2 + (l-2)/(T-1)*t)
    elif DETERMINISTIC:
        pm = 1 / (2 + (len(individual.genome) - 2) / (GENERATIONS - 1) * generation)

    else:
        pm = MUTATION_RATE

    return pm
