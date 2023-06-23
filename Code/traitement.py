'''
 Name : Elowan
 Creation : 23-06-2023 10:35:11
 Last modified : 23-06-2023 14:00:21
'''

from json import dump, load
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import os

from Models import Figure, FIGURES
from Terrain import Field, Case, SIZE_GRILLE

from main import POPULATION_NUMBER
from Genetic import NUMBER_OF_CHROMOSOME_TO_KEEP

def unserializeJson(filename):
    """
    Take a json file and return a dict following this structure :
    {
        athlete : {
            xp,
            FigureFav
        },
        field : [[Case, Case], [Case, Case]],
        dataGenerations : [
            {
                genes : [[(x,y), Figure, tick],],
                fitness,
                age,
                size,
            }
        ]
    }
    """
    with open(filename, "r") as file:
        data = load(file)

        parsed_data = {
            "athlete": {
                "xp": data["athlete"]["xp"],
                "FigureFav": Figure.getFigureById(data["athlete"]["FigureFav"])
            },
            "field": [],
            "dataGenerations": []
        }

        for lines in data["field"]:
            parsed_line = []
            for case in lines:
                parsed_line.append(Case.getCaseById(case))
            
            parsed_data["field"].append(parsed_line)

        for generation in data["dataGenerations"]:
            parsed_generation = {
                "genes": [],
                "fitness": generation["fitness"],
                "age": generation["age"],
                "size": generation["size"]
            }

            for gene in generation["genes"]:
                parsed_gene = []
                parsed_gene.append(((gene[0][0], gene[0][1]), Figure.getFigureById(gene[1]), gene[2]))
                
                parsed_generation["genes"].append(parsed_gene)

            parsed_data["dataGenerations"].append(parsed_generation)

        return parsed_data
    
if __name__ == "__main__":
    filename = "5xp_frontflip_1"

    # Récupère les données
    data = unserializeJson("data/{}.json".format(filename))

    # Création des dossiers
    if not os.path.exists("traitement"):
        os.mkdir("traitement")

    if not os.path.exists("traitement/{}_images".format(filename)):
        os.mkdir("traitement/{}_images".format(filename))
        
    
    ### Histogramme des figures les plus utilisées
    # Comptage le nombre de fois que chaque figure est utilisée
    count = {}
    for generation in data["dataGenerations"]:
        for gene in generation["genes"]:
            for combo in gene:
                if str(combo[1]) in count:
                    count[str(combo[1])] += 1
                else:
                    count[str(combo[1])] = 1

    # Ramène les valeurs sous forme de fréquence
    list_figures = []
    list_count = []
    for key, value in count.items():
        list_figures.append(key)
        list_count.append(value)

    list_figures = np.array(list_figures)
    list_count = np.array(list_count)

    list_count = list_count/list_count.sum()

    name = "Fréquence des figures les plus utilisées"
    characteristics = "{}xp, {}, {} générations, {} individus/génération".format(
        data["athlete"]["xp"], data["athlete"]["FigureFav"], 
        len(data["dataGenerations"]), POPULATION_NUMBER
    )

    # Affichage de l'histogramme
    plt.bar(list_figures, list_count)
    plt.suptitle(name)
    plt.xlabel("Figures")
    plt.ylabel("Fréquence")
    plt.title(characteristics)

    # Sauvegarde
    plt.savefig("traitement/{}_images/freq.png".format(filename))
    plt.close()
    
    ### Evolution de la fitness au cours des générations
    list_fitness = []
    for generation in data["dataGenerations"]:
        list_fitness.append(generation["fitness"])
        
    list_fitness = np.array(list_fitness)

    name = "Evolution de la fitness au cours des générations"
    characteristics = "{}xp, {}, {} générations, {} individus/génération".format(
        data["athlete"]["xp"], data["athlete"]["FigureFav"],
        len(data["dataGenerations"]), POPULATION_NUMBER
    )

    # Affichage de la courbe
    plt.plot(list_fitness)
    plt.xlabel("Nb générations")
    plt.ylabel("Score")
    plt.suptitle(name)
    plt.title(characteristics)

    # Sauvegarde
    plt.savefig("traitement/{}_images/evol_fitness.png".format(filename))
    plt.close()
    
    ### Utilisation des cases au cours des générations
    cases = [[0 for _ in range(SIZE_GRILLE)] for _ in range(SIZE_GRILLE)]

    # Comptage du nombre de fois que chaque case est utilisée
    for generation in data["dataGenerations"]:
        for gene in generation["genes"]:
            for combo in gene:
                cases[combo[0][0]][combo[0][1]] += 1

    # Récupération la case la plus utilisée
    max_case = max(case for line in cases for case in line)

    # Ramène les valeurs à une fréquence d'utilisation
    for i in range(len(cases)):
        for j in range(len(cases[i])):
            cases[i][j] = cases[i][j]/max_case

    # Création de la matrice d'utilisation des cases
    freq_matrice = np.zeros((len(cases), len(cases[0])))
    for i in range(len(cases)):
        for j in range(len(cases[i])):
            freq_matrice[i][j] = cases[i][j]

    # Creation d'une matrice représentant le mobilier du terrain
    terrain_matrice = np.zeros((len(data["field"]), len(data["field"][0])))
    for i in range(len(data["field"])):
        for j in range(len(data["field"][i])):
            terrain_matrice[i][j] = data["field"][i][j].id

    # Affichage des deux matrices
    plt.subplot(1, 2, 1)
    plt.matshow(freq_matrice, cmap=plt.get_cmap('OrRd'), vmin=0, vmax=1, fignum=False)
    plt.colorbar(ax=plt.gca(), fraction=0.046, pad=0.04)
    plt.title("Utilisation des cases au cours\ndes générations")

    plt.subplot(1, 2, 2, aspect='equal')
    plt.matshow(terrain_matrice, cmap=plt.get_cmap('gray'), fignum=False)

    # Création de la légende
    empty_patch = mpatches.Patch(color='black', label='Case vide')
    wall_patch = mpatches.Patch(color='grey', label='Case mur')
    hole_patch = mpatches.Patch(color='white', label='Case trou')
    plt.legend(handles=[empty_patch, wall_patch, hole_patch])

    plt.title("Mobilier du terrain")

    # Marges
    plt.subplots_adjust(bottom=0.1, right=1.5, top=0.9)

    # Sauvegarde
    plt.savefig("traitement/{}_images/cases.png".format(filename), bbox_inches='tight',dpi=100)
    plt.close()