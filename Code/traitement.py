'''
 Name : Elowan
 Creation : 23-06-2023 10:35:11
 Last modified : 01-07-2023 01:27:10
'''

from json import dump, load
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.transforms import Bbox
import matplotlib as mpl
import os
import datetime

from Models import Figure, FIGURES
from Terrain import Field, Case

from Genetic import NUMBER_OF_CHROMOSOME_TO_KEEP

from consts import SIZE_X, SIZE_Y, NUMBER_OF_CHROMOSOME_TO_KEEP,\
    POPULATION_NUMBER

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
            "field": {
                "cases": [],
                "width": data["field"]["width"],
                "height": data["field"]["height"]
            },
            "dataGenerations": []
        }

        for lines in data["field"]["cases"]:
            parsed_line = []
            for case in lines:
                parsed_line.append(Case.getCaseById(case))
            
            parsed_data["field"]["cases"].append(parsed_line)

        for generation in data["dataGenerations"]:
            parsed_generation = {
                "genes": [],
                "fitness": generation["fitness"],
                "age": generation["age"],
                "size": generation["size"]
            }

            for gene in generation["genes"]:
                parsed_gene = []
                parsed_gene.append(((gene[0][0], gene[0][1]), 
                                    Figure.getFigureById(gene[1]), gene[2]))
                
                parsed_generation["genes"].append(parsed_gene)

            parsed_data["dataGenerations"].append(parsed_generation)

        return parsed_data
    
def analyse(filename):
    """
    Prend en paramètre un dictionnaire généré par la fonction unserializeJson
    et renvoie un dictionnaire contenant les données analysées
    """
    print("Désérialisation du fichier {}...".format(filename))
    # Récupère les données
    data = unserializeJson(filename)

    print("Désérialisation terminée !\n")
    
    ### Histogramme des figures les plus utilisées
    print("Création de l'histogramme des figures les plus utilisées...")
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
    nb_generations = len(data["dataGenerations"])/NUMBER_OF_CHROMOSOME_TO_KEEP

    list_count = list_count/list_count.sum()

    # Tri par insertion des deux listes par ordre lexicographique croissant
    for i in range(1, len(list_figures)):
        j = i
        while j > 0 and list_figures[j-1] > list_figures[j]:
            # Swaping
            list_figures[j-1], list_figures[j] = list_figures[j], list_figures[j-1]
            list_count[j-1], list_count[j] = list_count[j], list_count[j-1]
            j -= 1

    print("Histogramme des figures utilisées créé !\n")
    
    ### Evolution de la fitness au cours des générations
    print("Création de l'évolution de la fitness au cours des générations...")
    list_fitness = []
    for generation in data["dataGenerations"]:
        list_fitness.append(generation["fitness"])

    # Fait une liste de la moyenne des fitness par génération
    list_fitness_moy = [sum(list_fitness[i:i+NUMBER_OF_CHROMOSOME_TO_KEEP])
                    /NUMBER_OF_CHROMOSOME_TO_KEEP
                    for i in range(0, len(list_fitness), NUMBER_OF_CHROMOSOME_TO_KEEP)]
    
    list_fitness = np.array(list_fitness)
    list_fitness_moy = np.array(list_fitness_moy)
    print("Evolution de la fitness au cours des générations créée !\n")
    
    ### Utilisation des cases au cours des générations
    print("Création de l'utilisation des cases au cours des générations...")
    cases = [[0 for _ in range(data["field"]["height"])] 
             for _ in range(data["field"]["width"])]

    # Comptage du nombre de fois que chaque case est utilisée
    for generation in data["dataGenerations"]:
        for gene in generation["genes"]:
            for combo in gene:
                cases[combo[0][1]][combo[0][0]] += 1

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
    terrain_matrice = np.zeros((data["field"]["width"], 
                                data["field"]["height"]))
    for i in range(data["field"]["width"]):
        for j in range(data["field"]["height"]):
            terrain_matrice[i][j] = data["field"]["cases"][i][j].id
    
    print("Utilisation des cases au cours des générations créée !\n")

    # Trouve le chemin utilisé par l'athlete avec la meilleur fitness
    best_athlete = {}
    best_fitness = 0
    for generation in data["dataGenerations"]:
        if generation["fitness"] > best_fitness:
            best_fitness = generation["fitness"] 
            best_athlete = generation

    return {
        "freq_matrice": freq_matrice,
        "terrain_matrice": terrain_matrice,
        "fitness": list_fitness,
        "fitness_moy": list_fitness_moy,
        "figures": list_figures,
        "count": list_count,
        "nb_generations": nb_generations,
        "athlete": data["athlete"],
        "best_athlete": best_athlete
    }


def makeEvolFitnessImg(athlete, nb_generations, list_fitness, list_fitness_moy,
                        best_athlete, filename):
    """
    Crée l'image de l'évolution de la fitness au cours des générations
    """
    mean_fitness = list_fitness.mean()

    name = "Evolution de la fitness au cours des générations"
    characteristics = "{}xp, {}, {} générations, {} individus/génération, max {}"\
        .format(athlete["xp"], athlete["FigureFav"],
            nb_generations, POPULATION_NUMBER, best_athlete["fitness"]
        )

    # Affichage de la courbe
    x_values = [i for i in range(0, len(list_fitness))]
    plt.plot(x_values, list_fitness, color="blue", label="Score")
    plt.xlabel("Nb d'athlètes sauvegardés par génération ({} athlètes/génération)"\
               .format(NUMBER_OF_CHROMOSOME_TO_KEEP))
    plt.ylabel("Score")
    plt.suptitle(name)
    plt.title(characteristics)

    # Affichage de la fitness maximale
    plt.axhline(y=mean_fitness, color="red", linestyle="--", 
                label="Moyenne : {}".format(round(float(mean_fitness), 2)),
                zorder = 3)

    
    x_values = [i for i in range(0, len(list_fitness), NUMBER_OF_CHROMOSOME_TO_KEEP)]
            
    plt.plot(list_fitness_moy, color="orange", label="Moyenne par génération", zorder=2)
    plt.legend()

    # Sauvegarde
    plt.savefig("traitement/{}_images/evol_fitness.png".format(filename))
    plt.close()

def makeCasesImg(freq_matrice, terrain_matrice, best_athlete, filename):
    """
    Crée l'image de l'utilisation des cases au cours des générations
    """     
    
    # Création de la figure et des axes
    ax = plt.subplot(1, 2, 1, aspect='equal')

    cmap = mpl.colormaps['OrRd']
    
    # Création des rectangles avec les valeurs de la matrice frequence
    for i in range(len(freq_matrice)):
        for j in range(len(freq_matrice[i])):
            rect = mpatches.Rectangle((j, i), 1, 1, fc=cmap(freq_matrice[i, j]), lw=2)
            ax.add_patch(rect)
   
    # Affichage du chemin de l'athlete avec la meilleur fitness avec
    # des chiffres croissants
    for i in range(len(best_athlete["genes"])):
        plt.text(best_athlete["genes"][i][0][0][0] + 0.5, 
                 best_athlete["genes"][i][0][0][1] + 0.5,
                str(i+1), color="black", ha="center", va="center")

    # Mise en forme de l'image
    max_x, max_y, diff = len(freq_matrice[0]), len(freq_matrice), 1.

    plt.title("Utilisation des cases au cours\ndes générations")
    plt.colorbar(mpl.cm.ScalarMappable(norm=mpl.colors.Normalize(vmin=0, vmax=1), cmap=cmap), ax=ax)
    ax.set_xlim(0, max_x)
    ax.set_ylim(max_y, 0)
    ax.set_xticks(np.arange(max_x))
    ax.set_yticks(np.arange(max_y))
    ax.xaxis.tick_top()
    ax.grid()


    # Création de l'affichage représentant le terrain
    ax2 = plt.subplot(1, 2, 2, aspect='equal')

    # Couleurs représentant les différents types de cases
    colors = {
        0: "black",
        1: "grey",
        2: "white"
    }

    # Création des rectangles avec les cases de la matrice terrain
    for i in range(len(terrain_matrice)):
        for j in range(len(terrain_matrice[i])):
            rect = mpatches.Rectangle((j, i), 1, 1, 
                                        fc=colors[int(terrain_matrice[i, j])],
                                        lw=2)
            ax2.add_patch(rect)

    # Création de la légende
    empty_patch = mpatches.Patch(color='black', label='Case sol')
    wall_patch = mpatches.Patch(color='grey', label='Case mur')
    hole_patch = mpatches.Patch(color='white', label='Case barre')
    
    plt.legend(handles=[empty_patch, wall_patch, hole_patch], 
               loc='center left', bbox_to_anchor=(1, 0.5))

    plt.title("Mobilier du terrain")

    ax2.set_xlim(0, max_x)
    ax2.set_ylim(max_y, 0)
    ax2.set_xticks(np.arange(max_x))
    ax2.set_yticks(np.arange(max_y))
    ax2.xaxis.tick_top()
    ax2.grid()
    
    # Marges
    plt.subplots_adjust(bottom=0.1, right=1.5, top=0.9) 

    # Sauvegarde
    plt.savefig("traitement/{}_images/cases.png".format(filename), 
                bbox_inches='tight',dpi=100)
    plt.close()

def makeFreqImg(athlete, list_figures, list_count, nb_generations, filename):
    """
    Crée l'histogramme de la fréquence des figures
    """
    name = "Fréquence des figures utilisées"
    characteristics = "{}xp, {}, {} générations, {} individus/génération"\
        .format(
            athlete["xp"], athlete["FigureFav"], 
            nb_generations, POPULATION_NUMBER
        )

    # Affichage de l'histogramme
    plt.bar(list_figures, list_count)
    plt.xticks(rotation="vertical")
    plt.suptitle(name)
    plt.xlabel("Figures")
    plt.ylabel("Fréquence")
    plt.title(characteristics)

    plt.autoscale(tight=False)

    # Sauvegarde
    plt.savefig("traitement/{}_images/freq.png".format(filename), bbox_inches=Bbox([[0, -1.3], [6.4, 5]]))
    plt.close()

def main(filename=None, data=None):
    if filename is None and data is None:
        print("Veuillez entrer un nom de fichier ou des données à analyser.")
        return
    
    # Chronométrage du programme
    start_time = datetime.datetime.now()
    
    # Récupération des données
    if data is None:
        data = analyse(filename)

    os.makedirs("traitement/{}_images".format(filename), exist_ok=True)

    print("Création des images...")

    # Création des images
    makeEvolFitnessImg(data["athlete"], data["nb_generations"],
                          data["fitness"], data["fitness_moy"], 
                          data["best_athlete"], filename)
    makeCasesImg(data["freq_matrice"], data["terrain_matrice"], data["best_athlete"], filename)
    makeFreqImg(data["athlete"], data["figures"], data["count"],
                data["nb_generations"], filename)
    
    print("Traitement terminé (en {})!\n".format(
        datetime.datetime.now()-start_time))

def analyseFolder(foldername):
    """
    Analyse tous les fichiers d'un dossier en concaténant les données
    """
    # Récupération des noms des fichiers
    filenames = [f for f in os.listdir(foldername) if os.path.isfile(os.path.join(foldername, f))]

    # Initialisation des données
    data = {
        "nb_generations": 0,
        "fitness": [],
        "fitness_moy": [],
        "freq_matrice": np.zeros((SIZE_Y, SIZE_X)),
        "terrain_matrice": np.zeros((SIZE_Y, SIZE_X)),
        "figures": [],
        "count": [],
        "best_athlete": {
            "fitness": 0,
            "genes": []
        },
        "athlete": {}
    }

    # Analyse de chaque fichier
    for filename in filenames:
        # Analyse du fichier
        file_data = analyse(os.path.join(foldername, filename))

        # Ajout des données
        data["nb_generations"] = file_data["nb_generations"]
        data["freq_matrice"] += file_data["freq_matrice"]
        data["fitness"].extend(file_data["fitness"])
        

        # Variables invariantes face aux excécutions de l'algorithme
        data["terrain_matrice"] = file_data["terrain_matrice"]
        data["figures"] = file_data["figures"]
        data["count"] = file_data["count"]
        data["athlete"] = file_data["athlete"]


        # Meilleur athlète
        if file_data["best_athlete"]["fitness"] > data["best_athlete"]["fitness"]:
            data["best_athlete"] = file_data["best_athlete"]

    # Moyenne des données
    data["fitness_moy"] = np.zeros(47000)

    data["freq_matrice"] /= len(filenames)

    # Moyenne de toutes les fitness
    for i in range(0, len(data["fitness"]), NUMBER_OF_CHROMOSOME_TO_KEEP):
        print(data["fitness"][i])
        data["fitness_moy"][i] = np.mean(data["fitness"][i:i+NUMBER_OF_CHROMOSOME_TO_KEEP])

    data["fitness"] = np.zeros(5000)
    return data

if __name__ == "__main__":
    filename = "6xp_frontflip/0"

    # main(filename)
    data = analyseFolder("data/6xp_frontflip")
    main(filename="6xp_frontflip/all", data=data)