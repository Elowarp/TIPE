'''
 Name : Elowan
 Creation : 23-06-2023 10:35:11
 Last modified : 27-08-2023 16:27:30
'''

from json import dump, load
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.transforms import Bbox
import matplotlib as mpl
import os
import sys
import datetime
import logging

from Models import Figure, FIGURES
from Terrain import Case

from Genetic import NUMBER_OF_CHROMOSOME_TO_KEEP

from consts import SIZE_X, SIZE_Y, NUMBER_OF_CHROMOSOME_TO_KEEP,\
    POPULATION_NUMBER, MUTATION_RATE, TERMINAISON_AGE, INITIAL_POSITION,\
    MAX_TICK_COUNT, ITERATION_NUMBER

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
    logging.debug("Désérialisation du fichier {}...".format(filename))
    # Récupère les données
    data = unserializeJson(filename)

    logging.debug("Désérialisation terminée !\n")
    
    ### Histogramme des figures les plus utilisées
    logging.debug("Création de l'histogramme des figures les plus utilisées...")
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

    for key in FIGURES.keys():
        if key not in list_figures:
            list_figures.append(key)
            list_count.append(0)

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

    logging.debug("Histogramme des figures utilisées créé !\n")
    
    ### Evolution de la fitness au cours des générations
    logging.debug("Création de l'évolution de la fitness au cours des générations...")
    list_fitness = []
    for generation in data["dataGenerations"]:
        list_fitness.append(generation["fitness"])

    # Fait une liste de la moyenne des fitness par génération
    list_fitness_moy = [sum(list_fitness[i:i+NUMBER_OF_CHROMOSOME_TO_KEEP])
                    /NUMBER_OF_CHROMOSOME_TO_KEEP
                    for i in range(0, len(list_fitness), NUMBER_OF_CHROMOSOME_TO_KEEP)]
    
    list_fitness = np.array(list_fitness)
    list_fitness_moy = np.array(list_fitness_moy)
    logging.debug("Evolution de la fitness au cours des générations créée !\n")
    
    ### Utilisation des cases au cours des générations
    logging.debug("Création de l'utilisation des cases au cours des générations...")
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
    
    logging.debug("Utilisation des cases au cours des générations créée !\n")

    # Trouve le chemin utilisé par l'athlete avec la meilleur fitness
    best_athlete = {}
    best_fitness = -1
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
        "best_athlete": best_athlete,
        "nb_executions": 1,
    }

def analyseFolder(foldername):
    """
    Analyse tous les fichiers d'un dossier en concaténant les données
    """    
    foldername = "data/"+foldername
    # Récupération des noms des fichiers
    filenames = [f for f in os.listdir(foldername) if os.path.isfile(os.path.join(foldername, f))]

    file_number = len(filenames)

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
        "athlete": {},
        "nb_executions": file_number,
    }

    fitness_temp = []

    # Analyse de chaque fichier
    count = 0
    for filename in filenames:
        # Analyse du fichier
        file_data = analyse(os.path.join(foldername, filename))

        # Ajout des données
        data["nb_generations"] += file_data["nb_generations"]
        data["freq_matrice"] += file_data["freq_matrice"]
        fitness_temp.append(file_data["fitness"])
        

        # Variables invariantes face aux excécutions de l'algorithme
        data["terrain_matrice"] = file_data["terrain_matrice"]
        data["figures"] = file_data["figures"]
        data["count"] = file_data["count"]
        data["athlete"] = file_data["athlete"]


        # Meilleur athlète
        if file_data["best_athlete"]["fitness"] > data["best_athlete"]["fitness"]:
            data["best_athlete"] = file_data["best_athlete"]

        count += 1
        logging.info("Analyse de {} terminée ({}%)".format(filename,
            round((count/file_number)*100, 2)))

    # Moyenne des données
    data["freq_matrice"] /= len(filenames)
    data["nb_generations"] /= len(filenames)

    # Moyenne de toutes les fitness par exécution
    # de l'algorithme génétique
    max_size = max(len(x) for x in fitness_temp)
    for i in range(max_size):
        moy_cur_fitness = [x[i] for x in fitness_temp if len(x) > i] 
        data["fitness"].append(sum(moy_cur_fitness)/len(moy_cur_fitness))

    data["fitness"] = np.array(data["fitness"])

    # Moyenne par génération
    data["fitness_moy"] = [sum(data["fitness"][i:i+NUMBER_OF_CHROMOSOME_TO_KEEP])
                    /NUMBER_OF_CHROMOSOME_TO_KEEP
                    for i in range(0, len(data["fitness"]), 
                                   NUMBER_OF_CHROMOSOME_TO_KEEP)]
    
    data["fitness_moy"] = np.array(data["fitness_moy"])
    
    return data


def makeEvolFitnessImg(athlete, nb_generations, list_fitness, list_fitness_moy,
                        best_athlete, filename, nb_executions=1):
    """
    Crée l'image de l'évolution de la fitness au cours des générations
    """
    plt.subplot(1, 2, 1)
    mean_fitness = list_fitness.mean()

    name = "Evolution du score au cours des générations ({} exécutions)"\
        .format(nb_executions)

    # Liste de la moyenne des fitness par génération
    fitness_moy_by_gen = [sum(list_fitness[i:i+NUMBER_OF_CHROMOSOME_TO_KEEP])
                          /NUMBER_OF_CHROMOSOME_TO_KEEP
                        for i in range(0, len(list_fitness), NUMBER_OF_CHROMOSOME_TO_KEEP)]

    # Affichage de la courbe
    plt.plot(fitness_moy_by_gen, color="blue", label="Score", linewidth=2)
    plt.xlabel("Génération ({} athlètes/génération)"\
               .format(NUMBER_OF_CHROMOSOME_TO_KEEP))
    plt.ylabel("Score")
    plt.title(name)

    # Affichage de la fitness maximale
    plt.axhline(y=mean_fitness, color="red", linestyle="--", 
                label="Moyenne : {}".format(round(float(mean_fitness), 2)),
                zorder = 3)
                
    x_values = [i for i in range(0, len(fitness_moy_by_gen))]
            
    # plt.plot(x_values, list_fitness_moy, color="orange", label="Moyenne par génération", zorder=2)
    plt.legend()

    # Sauvegarde
    # plt.savefig("traitement/{}_images/evol_fitness.png".format(filename))
    # plt.close()

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
    print(len(freq_matrice), len(freq_matrice[0]))
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
    plt.subplots_adjust(right=1.2, bottom=-0.8) 
    # plt.tight_layout()  

    # Sauvegarde
    plt.savefig("traitement/{}_images/cases.png".format(filename), 
                bbox_inches=Bbox([[0, -4], [9, 5]]),dpi=100)
    plt.close()

def makeFreqImg(athlete, list_figures, list_count, nb_generations, 
                filename, nb_executions=1):
    """
    Crée l'histogramme de la fréquence des figures
    """
    plt.subplot(1, 2, 2)
    title = "Fréquence des figures utilisées".format(nb_executions)

    # Affichage de l'histogramme
    plt.bar(list_figures, list_count)
    plt.xticks(rotation="vertical")
    plt.xlabel("Figures")
    plt.ylabel("Fréquence")
    plt.title(title)

    plt.autoscale(tight=False)

    # Sauvegarde
    # plt.savefig("traitement/{}_images/freq.png".format(filename), bbox_inches=Bbox([[0, -1.3], [6.4, 5]]))
    # plt.close()

def constListImage(filename, const_dict):
    """
    Crée l'image de la liste des constantes utilisées pour les données
    """
    plt.axis('off')

    # Converti un dictionnaire vers un tableau 2D
    const_array = []
    for key, value in const_dict.items():
        const_array.append([str(key), str(value)])
    
    table = plt.table(cellText=const_array, colLabels=["Constante", "Valeur"], loc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(8)  
    # plt.subplots_adjust(bottom=-0.18, top=1.2)
    
    plt.tight_layout()
    plt.savefig("traitement/{}_images/constantes.png".format(filename), dpi=100)
    plt.close()
    

def main(filename=None, data=None):
    if filename is None and data is None:
        logging.error("Veuillez entrer un nom de fichier ou des données à analyser.")
        return
    
    # Chronométrage du programme
    start_time = datetime.datetime.now()
    
    # Récupération des données
    if data is None:
        data = analyse("data/" + filename)

    os.makedirs("traitement/{}_images".format(filename), exist_ok=True)

    logging.info("Traitement des données...")

    # Création des images
    makeEvolFitnessImg(data["athlete"], data["nb_generations"],
                          data["fitness"], data["fitness_moy"], 
                          data["best_athlete"], filename, 
                          data["nb_executions"])
    makeFreqImg(data["athlete"], data["figures"], data["count"],
                data["nb_generations"], filename, data["nb_executions"])
    
    name = "{}xp, {}, {} générations/exécution en moy, {} individus/génération ({} exécutions)"\
        .format(
            data["athlete"]["xp"], data["athlete"]["FigureFav"], 
            data["nb_generations"], POPULATION_NUMBER,
            data["nb_executions"]
        )
    
    plt.suptitle(name)
    plt.subplots_adjust(bottom=0.1, left=-0.2, right=1.3, top=0.85, hspace=2)
    
    plt.savefig("traitement/{}_images/freq&fitness.png".format(filename),
                bbox_inches=Bbox([[-2, -1.3], [9, 5]]),dpi=100)
    plt.close()
    
    constListImage(filename=filename, const_dict={
        "ATHLETE_XP": data["athlete"]["xp"],
        "ATHLETE_FIG_FAV": data["athlete"]["FigureFav"],
        #"FIGURES": data["figures"],
        "POPULATION_NUMBER": POPULATION_NUMBER,
        "MUTATION_RATE": MUTATION_RATE,
        "NUMBER_OF_CHROMOSOME_TO_KEEP": NUMBER_OF_CHROMOSOME_TO_KEEP,
        "TERMINAISON_AGE": TERMINAISON_AGE,
        "INITIAL_POSITION": INITIAL_POSITION,
        "MAX_TICK_COUNT": MAX_TICK_COUNT,
        "ITERATION_NUMBER": ITERATION_NUMBER,
        "SIZE_X": SIZE_X,
        "SIZE_Y": SIZE_Y,
        "MAX_FITNESS": data["best_athlete"]["fitness"],
    })

    makeCasesImg(data["freq_matrice"], data["terrain_matrice"], 
                 data["best_athlete"], filename)

    logging.info("Traitement terminé (en {})!\n".format(
        datetime.datetime.now()-start_time))

if __name__ == "__main__":
    # filename = "6xp_frontflip/0.json"
    # main(filename)

    folder = "7xp_frontflip"

    # Afficher les logs dans un fichier
    logging.basicConfig(level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%d-%m-%Y %H:%M:%S',
                    filename='logs/Traitement - {}.txt'.format(
                                            str(folder)
                                            + " - "
                                            + datetime.datetime.now().strftime(
                                                "%d-%m-%Y %H:%M:%S"
                                            )),
                    filemode='w')
    
    # Affichage dans la console
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)

    data = analyseFolder(folder)
    main(filename=folder+"/all", data=data)