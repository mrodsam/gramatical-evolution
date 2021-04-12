import random
from ga.individual import Individual
from ga.params import CROSSOVER_RATE, MAX_GENOME_LENGTH, GENERATIONS, DETERMINISTIC_BASIC1, DETERMINISTIC_BASIC2


def select_crossover_rate(generation):
    """
    Selección de la probabilidad de cruce según el esquema utilizado.

    Modelo determinista básico 1: en cada generación se disminuye la probabilidad de cruce.
    Modelo determinista básico 2: en cada generación se aumenta la probabilidad de cruce.
    Modelo estático: se utiliza siempre la probabilidad de cruce predefinida.

    :param generation: generación actual
    :return: probabilidad de cruce a utilizar
    """
    if DETERMINISTIC_BASIC1:
        pc = 1 - (generation/GENERATIONS)
    elif DETERMINISTIC_BASIC2:
        pc = generation/GENERATIONS
    else:
        pc = CROSSOVER_RATE

    return pc


def one_point_crossover(parent1, parent2, generation):
    """
    Recombinación realizada utilizando el método "One-point crossover".

    Se calcula un punto aleatorio en cada padre, dividiéndolo en dos secciones, y los hijos se forman uniendo
    estas secciones de forma alterna.

    :param parent1: individuo que actúa como primer padre
    :param parent2: individuo que actúa como segundo padre
    :param generation: generación actual
    :return: dos nuevos individuos (hijos)
    """

    pc = select_crossover_rate(generation)

    parent1_genome = parent1.genome
    parent2_genome = parent2.genome

    if random.random() < pc:
        while True:
            r1 = random.randint(1, len(parent1_genome))
            r2 = random.randint(1, len(parent2_genome))

            child1_genome = parent1_genome[:r1] + parent2_genome[r2:]
            child2_genome = parent2_genome[:r2] + parent1_genome[r1:]
            # Si alguno de los hijos excede la longitud máxima permitida, se vuelve a realizar el cruce
            if len(child1_genome) <= MAX_GENOME_LENGTH and len(child2_genome) <= MAX_GENOME_LENGTH:
                break
    # En caso de que el número aleatorio sea mayor que la probabilidad de cruce, los hijos se generan como copias de los
    # padres
    else:
        child1_genome = parent1_genome[:]
        child2_genome = parent2_genome[:]

    return [Individual(child1_genome, len(child1_genome)), Individual(child2_genome, len(child2_genome))]


def uniform_crossover(parent1, parent2, generation):
    """
    Recombinación realizada utilizando el método de cruce "uniforme".

    Se genera una cadena de números aleatorios, entre 0 y 1, de la misma longitud que la máxima longitud entre los dos genomas de
    los padres. Por cada uno de estos valores, si es menor que 0.5, se añade al primer hijo el codón correspondiente
    del primer padre, si es mayor que 0.5 se le añade el codón correspondiente del segundo padre. Se crea el segundo hijo
    de forma análoga.
    Puesto que la longitud de los cromosomas es variable, en caso de que se agoten los codones de alguno de los padres
    y corresponda insertar un codón de su secuencia, este simplemente se saltará y se pasará al siguiente.

    :param parent1: individuo que actúa como primer padre
    :param parent2: individuo que actúa como segundo padre
    :param generation: generación actual
    :return: dos nuevos individuos (hijos)
    """
    pc = select_crossover_rate(generation)

    child1_genome = []
    child2_genome = []

    limit = max(len(parent1.genome), len(parent2.genome))

    random_list = [random.random() for _ in range(limit)]
    if random.random() < pc:
        for i, p in enumerate(random_list):
            if p < 0.5:
                if len(parent1.genome) > i:
                    child1_genome.append(parent1.genome[i])
                if len(parent2.genome) > i:
                    child2_genome.append(parent2.genome[i])
            else:
                if len(parent2.genome) > i:
                    child1_genome.append(parent2.genome[i])
                if len(parent1.genome) > i:
                    child2_genome.append(parent1.genome[i])

    # En caso de que el número aleatorio sea mayor que la probabilidad de cruce, los hijos se generan como copias de los
    # padres
    else:
        child1_genome = parent1.genome[:]
        child2_genome = parent2.genome[:]

    return [Individual(child1_genome, len(child1_genome)), Individual(child2_genome, len(child2_genome))]
