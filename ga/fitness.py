import math
import ga.params as params


def fitness_function(g_hat):
    """
    Función de evaluación de nivel de adaptación (fitness) de cada individuo.

    :param g_hat: fenotipo del individuo del que se desea calcular el nivel de adaptación.
    :return: valor de fitness del individuo,
            número de hits (51 hits significa que se ha alcanzado una solución)
    """
    N = 50
    h = 10 ** -5
    U = 10 ** -1
    K0 = 1
    K1 = 10
    hits = 0

    expression = []
    delta = (params.B - params.A) / N
    for i in range(0, N+1):
        try:
            f_p = (eval(params.FUNCTION.replace("X", str(params.A + i*delta + h))) - eval(params.FUNCTION.replace("X", str(params.A+i*delta))))/h
            expr = abs(f_p - eval(g_hat.replace("X", str(params.A + i * delta))))
        except (ValueError, ZeroDivisionError, OverflowError):
            # return math.inf, 0
            return 100000, 0

        if expr <= U:
            w = K0
            hits += 1
        else:
            w = K1
        expression.append(w*expr)

    return (1/(N+1))*sum(expression), hits


def phenotypeToExpression(phenotype):
    """
    Función utilizada para poder evaluar con eval() la expresión matemática que define el fenotipo de un individuo.

    :param phenotype: fenotipo de un individuo
    :return: expresión matemática válida para su ejecución
    """
    phenotype = phenotype.replace("sin", "math.sin")
    phenotype = phenotype.replace("cos", "math.cos")
    phenotype = phenotype.replace("exp", "math.exp")
    phenotype = phenotype.replace("ln", "math.log")
    phenotype = phenotype.replace("inv", "1/")

    return phenotype


def average_fitness(population):
    """
    Cálculo del fitness medio de la población.

    :param population: población de la que se desea calcular el fitness medio
    :return: media aritmética del fitness de los individuos de la población
    """
    return sum(i.fitness for i in population)/len(population)
