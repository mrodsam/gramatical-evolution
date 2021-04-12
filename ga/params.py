# Funciones objetivo
FUNCTION, A, B, SOL = None, None, None, None
# FUNCTION, A, B, SOL = "X ** 3 + 8", 0, 5, "3 * (X ** 2)"
# FUNCTION, A, B, SOL = "(X-2)/(X+2)", 0, 5, "4 / ((X + 2) ** 2)"
# FUNCTION, A, B, SOL = "(1/5)*(X ** 2 + 1)*(X - 1)", -2, 2, "(1/5)*(3 * (X ** 2) - (2 * X) + 1)"
# FUNCTION, A, B, SOL = "-math.exp(-2 * (X ** 2) + 2)", 0, 3, "4 * X * math.exp(-2*(X ** 2) + 2)"
# FUNCTION, A, B, SOL = "(math.exp(2*X) + math.exp(-6*X))/2", 0, 2, "math.exp(2*X) - 3*math.exp(-6*X)"
# FUNCTION, A, B, SOL = "X * math.log(1 + 2*X)", 0, 5, "math.log(1+(2*X)) + (2*X)/(1 + (2*X))"
# FUNCTION, A, B, SOL = "math.exp(2*X)*math.sin(X)", -2, 2, "math.exp(2*X)*(2*math.sin(X)+math.cos(X))"

# Variables de ejecución
GENERATIONS = 200
RUNS = 10

# Tamaños
POPULATION_SIZE = 200
TOURNAMENT_SIZE = 3
OFFSPRING_SIZE = 200

# Tamaño variable de población
VARIABLE_POPULATION_SIZE = False
MIN_LIFETIME = 1
MAX_LIFETIME = 11
ETA = 0.5 * (MAX_LIFETIME - MIN_LIFETIME)

# Gramática y generación de cromosomas
CODON_SIZE = 255
FIX_LENGTH = False
MAX_GENOME_LENGTH = 20
MAX_WRAPS = 2
REPAIR = True

# Probabilidades de operadores de variación
DUPLICATION_RATE = 0.01
CROSSOVER_RATE = 0.5
MUTATION_RATE = 0.1

# Adaptación y auto-adaptación de parámetros
SELF_ADAPTATION = False # Cambiar tamaños de población y descendencia (descendencia > población)
GAMMA = 0.22
DETERMINISTIC_BASIC1 = False
DETERMINISTIC_BASIC2 = False
DETERMINISTIC = False

# Selección de supervivientes
AGE_BASED_REPLACEMENT = True # Cambiar tamaños de población y descendencia (mismo tamaño)
FITNESS_BASED_REPLACEMENT = False # Cambiar tamaños de población y descendencia (descendencia < población)

# Métodos añadidos
UNIFORM_CROSSOVER = False
DUPLICATION = False
LOCAL_SEARCH = True


