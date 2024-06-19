'''
 Name : Elowan
 Creation : 30-06-2023 23:57:04
 Last modified : 21-05-2024 21:31:35
 File : utils.py
'''
import random
import numpy as np

def weighted_random(mn, mx, mnweight, mxweight):
    """
    Exécute un random entre mn et mx avec une probabilité de mnweight
    d'avoir la plus basse valeur et mxweight d'avoir la plus haute valeur
    """
    return random.choices(range(mn, mx+1), \
      weights=np.linspace(mnweight,mxweight,(mx-mn)+1))[0]

def computeNextOccurrence(u: float, pm: float)->int: 
    """
    Calcule la variable l de l'étude qui permet de réduire le 
    nombre de calcul de variable aléatoire sans changer le succés
    de l'algorithme génétique.
    """
    if pm == 0.0: return 0
    else:
        val = (1/pm)*np.log(1-u)
        return int(val)