'''
 Name : Elowan
 Creation : 30-06-2023 23:57:04
 Last modified : 01-07-2023 00:00:11
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