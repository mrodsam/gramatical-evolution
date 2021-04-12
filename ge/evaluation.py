import numpy as np
import math
from matplotlib import pyplot as plt
from ga.params import A, B, SOL, RUNS, POPULATION_SIZE, OFFSPRING_SIZE, SELF_ADAPTATION
import ga.params as params


class Evaluation:

    def __init__(self):
        self.successful_runs = 0
        self.aes = 0
        self.sr = 0
        self.mbf = 0
        self.fitness_sum = 0
        self.gens_to_sol = []
        self.local_evaluations = 0
        self.phen_solution = None
        self.fitness_values = None

    def computeSR(self):
        """
        Cálculo de la tasa de éxito.

        :return: tasa de éxito
        """
        self.sr = self.successful_runs / RUNS

    def computeMBF(self):
        """
        Cálculo del mejor fitness medio.

        :return: mejor fitness medio
        """
        self.mbf = self.fitness_sum/RUNS

    def computeAES(self):
        """
        Cálculo del número medio de evaluaciones hasta encontrar una solución.

        En caso de utilizar el esquema de selección de supervivientes (mu, lambda), las evaluaciones de fitness de
        cada individuo se realizan sobre el conjunto de la descendencia, por lo que se utiliza este valor para calcular
        el AES.
        Se tienen en cuenta las evaluaciones realizadas durante el proceso de búsqueda local.

        :return: número medio de evaluaciones hasta encontrar una solución
        """
        # En caso de autoadaptación se usa un esquema (mu,lambda) por lo que el número de evaluaciones de
        # fitness se calcula sobre el tamaño de la descendencia
        if SELF_ADAPTATION:
            self.aes = (sum(np.asarray(self.gens_to_sol, dtype=np.float32)) * OFFSPRING_SIZE + self.local_evaluations) / self.successful_runs
        else:
            self.aes = (sum(np.asarray(self.gens_to_sol,
                                       dtype=np.float32)) * POPULATION_SIZE + self.local_evaluations) / self.successful_runs

    def plot_g_vs_gHat(self):
        """
        Representación gráfica de la solución encontrada y la solución real al problema.

        """
        x = np.arange(params.A, params.B, 0.1)
        y = []
        y_sol = []
        for value in x:
            y.append(eval(params.SOL.replace('X', str(value))))
            y_sol.append(eval(self.phen_solution.replace('X', str(value))))

        plt.plot(x, y, 'b', x, y_sol, 'r')
        plt.legend(['g(x)', r'$\hat{g}(x)$'])
        plt.show()

    def plot_progress_curve(self):
        """
        Representación gráfica de la evolución del mejor fitness de cada generación.

        El valor de fitness se calcula realizando una media entre los mejores valores de fitness de cada generación
        obtenidos en cada ejecución.

        """
        fitness_values = np.asarray(self.fitness_values)

        y = np.mean(fitness_values, axis=0)

        x = np.arange(0, len(y), 1)
        plt.ylabel("Valor de adaptación")
        plt.xlabel("Número de generaciones")
        plt.yscale("log")
        plt.plot(x, y)
        plt.show()

    def perform_evaluation(self):
        """
        Evaluación de la ejecución realizada.

        """
        self.computeSR()
        self.computeMBF()
        if self.successful_runs > 0:
            self.computeAES()
            self.plot_g_vs_gHat()
        self.plot_progress_curve()

    def __str__(self):
        """
        Presentación de los resultados de la evaluación realizada a la ejecución.

        :return: cadena de texto con los valores de SR, MBF y AES
        """
        self.perform_evaluation()
        return "SR: {}; MBF: {}; AES: {}".format(int(self.sr*100), self.mbf, self.aes)

