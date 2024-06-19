'''
 Name : Elowan
 Creation : 30-06-2023 23:56:45
 Last modified : 21-05-2024 12:02:45
 File : consts.py
'''
NUMBER_OF_CHROMOSOME_TO_KEEP = 20   # Nombre de chromosomes à garder à 
                                    # chaque génération

def MAX_SCORE(xp):                  # Score théorique maximal pour un niveau
    return 15 + 15*xp/10            # d'xp donné

EPS = 0.5                           # Epsilon interval autour du score max atteignable 

INITIAL_POSITION = (7, 31)          # Position initiale de l'athlète
MAX_TICK_COUNT = 70                 # Nombre de tours(=secondes) maximum

ITERATION_NUMBER = 1               # Nombre d'itérations de l'algorithme

TICK_INTERVAL = 1                   # Interval entre 2 executions de la partie

CROSSOVER_PROB = 1                  # Probabilité de croiser deux parents
MUTATION_PROB = 0.05                # Probabilité de mutation d'un enfant

SIZE_X = 10                         # Taille du terrain
SIZE_Y = 40

# Valeurs utilisées dans l'étude
POPULATIONS = [2, 5, 10, 20, 35, 60, 100, 200, 300,
        450, 700, 1000, 1200, 1400, 1800, 2000]

# Distance en mètre maximal qu'un être humain peut parcourir en courant pendant 1s
DIST_MAX = 6

# L le nombre de variables représentant un gène 
L = 6*70

PROBS_C = [0.0, 0.0, 0.0, 0.9, 0.9] # Probabilité de croisement
PROBS_M = [0.1, 0.5, 1.0, 0.0, 0.1] # Probabilité de mutation

NB_EVAL_MAX = 45_000                # = S