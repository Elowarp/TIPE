'''
 Name : Elowan
 Creation : 30-06-2023 23:56:45
 Last modified : 04-01-2024 21:48:42
'''

POPULATION_NUMBER = 200             # Nombre d'individus dans la population = N
NB_EVAL_MAX = 45_000                # = S

NUMBER_OF_CHROMOSOME_TO_KEEP = 20   # Nombre de chromosomes à garder à 
                                    # chaque génération

# TERMINAISON_AGE = 200             # Nombre de générations avant de
                                    # terminer l'algorithme = T

def MAX_SCORE(xp):                  # Score théorique maximal pour un niveau
    return 15 + 15*xp/10            # d'xp donné

EPS = 0.5                           # Epsilon interval autour du score max atteignable 

INITIAL_POSITION = (7, 31)          # Position initiale de l'athlète
MAX_TICK_COUNT = 70                 # Nombre de tours(=secondes) maximum

ITERATION_NUMBER = 50               # Nombre d'itérations de l'algorithme

TICK_INTERVAL = 1                   # Interval entre 2 executions de la partie

CROSSOVER_PROB = 1                  # Probabilité de croiser deux parents
MUTATION_PROB = 0.05                # Probabilité de mutation d'un enfant

SIZE_X = 10                         # Taille du terrain
SIZE_Y = 40