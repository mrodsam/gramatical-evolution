import numpy as np
import time
from ge.grammar import Grammar
from ga.params import RUNS
from ga.genetic_algorithm import initialization, search, phenotypeToExpression
from ge.evaluation import Evaluation
import ga.params as params

if __name__ == "__main__":

    for i in range(0, 7):
        if i == 0:
            params.FUNCTION, params.A, params.B, params.SOL = "X ** 3 + 8", 0, 5, "3 * (X ** 2)"
        if i == 1:
            params.FUNCTION, params.A, params.B, params.SOL = "(X-2)/(X+2)", 0, 5, "4 / ((X + 2) ** 2)"
        if i == 2:
            params.FUNCTION, params.A, params.B, params.SOL = "(1/5)*(X ** 2 + 1)*(X - 1)", -2, 2, "(1/5)*(3 * (X ** 2) - (2 * X) + 1)"
        if i == 3:
            params.FUNCTION, params.A, params.B, params.SOL = "-math.exp(-2 * (X ** 2) + 2)", 0, 3, "4 * X * math.exp(-2*(X ** 2) + 2)"
        if i == 4:
            params.FUNCTION, params.A, params.B, params.SOL = "(math.exp(2*X) + math.exp(-6*X))/2", 0, 2, "math.exp(2*X) - 3*math.exp(-6*X)"
        if i == 5:
            params.FUNCTION, params.A, params.B, params.SOL = "X * math.log(1 + 2*X)", 0, 5, "math.log(1+(2*X)) + (2*X)/(1 + (2*X))"
        if i == 6:
            params.FUNCTION, params.A, params.B, params.SOL  = "math.exp(2*X)*math.sin(X)", -2, 2, "math.exp(2*X)*(2*math.sin(X)+math.cos(X))"

        print("Función: "+params.FUNCTION)

        # Lectura del fichero que contiene la gramática
        bnf_grammar = Grammar("grammars/derivada.bnf")
        times = []
        first = True
        progress_curves = []

        evaluation = Evaluation()

        for i in range(0, RUNS):
            start_time = time.time()
            # Inicialización de la población
            population = initialization()
            # Ejecución del algoritmo de búsqueda
            solution, generation, best_individuals, local_evaluations = search(population, bnf_grammar)
            times.append(time.time() - start_time)

            print("Resultado: " + str(solution))
            # Almacenamiento de los mejores valores de fitness de cada generación en cada ejecución
            progress_curves.append(best_individuals)
            # Suma de los mejores valores de fitness obtenidos tras cada ejecución
            evaluation.fitness_sum += solution.fitness

            if solution.hits == 51:
                if first:
                    # Almacenamiento del fenotipo de la primera solución obtenida
                    evaluation.phen_solution = phenotypeToExpression(solution.phenotype)
                    first = False
                # Contador de ejecuciones exitosas
                evaluation.successful_runs += 1
                # Contador de evaluaciones de fitness realizadas durante la búsqueda local
                evaluation.local_evaluations += local_evaluations
                # Contador de número de generaciones necesarias hasta obtener una solución
                evaluation.gens_to_sol.append(generation)

        evaluation.fitness_values = progress_curves
        # Resultado de la evaluación de la ejecución
        print(evaluation)
        print("Tiempo medio de ejecución: "+str(sum(np.asarray(times, dtype=np.float32))/len(times)))

