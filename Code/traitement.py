'''
 Name : Elowan
 Creation : 23-06-2023 10:35:11
 Last modified : 26-04-2024 16:54:41
'''

from json import dump, load
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.patches as mpatches
from matplotlib.transforms import Bbox
import matplotlib as mpl
import os
import datetime
import logging

from Models import Figure, FIGURES
from Terrain import Case
from Chromosome import from_string_to_combos

from consts import SIZE_X, SIZE_Y, NUMBER_OF_CHROMOSOME_TO_KEEP,\
    POPULATIONS, PROBS_M, PROBS_C, INITIAL_POSITION,\
    MAX_TICK_COUNT, ITERATION_NUMBER, TICK_INTERVAL

def unserializeJson(filename):
    """
    Take a json file and return a dict following this structure :
    {
        athlete : {
            xp,
        },
        field : {
            case: [[Case, Case], [Case, Case]],
            width
            height
            },
        dataGenerations : [
            {
                genes : "xxyyii",
                fitness,
                age,
                size,
            }
        ]
        meta : {
            is_success
        }
    }
    """
    with open(filename, "r") as file:
        data = load(file)

        parsed_data = {
            "athlete": {
                "xp": data["athlete"]["xp"],
            },
            "field": {
                "cases": [],
                "width": data["field"]["width"],
                "height": data["field"]["height"]
            },
            "meta": {
                "is_success": data["metaInfo"]["is_success"],
                "crossover_prob": data["metaInfo"]["crossover_prob"],
                "mutation_prob": data["metaInfo"]["mutation_prob"],
                "population_size": data["metaInfo"]["population_size"],
                "terminaison_age": data["metaInfo"]["terminaison_age"],
            },
            "dataGenerations": []
        }

        for lines in data["field"]["cases"]:
            parsed_line = []
            for case in lines:
                parsed_line.append(Case.getCaseById(case))
            
            parsed_data["field"]["cases"].append(parsed_line)

        
        for generation in data["dataGenerations"]:
            # Récupération de la fitness détaillée
            parsed_generation = {
                "genes": [],
                "fitness": generation["f"],
                "age": generation["a"],
                "size": generation["s"]
            }
            
            parsed_generation["genes"] = from_string_to_combos(generation["g"])
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
            if str(gene[1]) in count:
                count[str(gene[1])] += 1
            else:
                count[str(gene[1])] = 1

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
    list_fitness = np.array(list_fitness)


    # Fait une liste de la moyenne des fitness par génération
    list_fitness_moy = [sum(list_fitness[i:i+NUMBER_OF_CHROMOSOME_TO_KEEP])
                    /NUMBER_OF_CHROMOSOME_TO_KEEP
                    for i in range(0, len(list_fitness), NUMBER_OF_CHROMOSOME_TO_KEEP)]
    
    list_fitness_moy = np.array(list_fitness_moy)
    logging.debug("Evolution de la fitness au cours des générations créée !\n")
    
    ### Utilisation des cases au cours des générations
    logging.debug("Création de l'utilisation des cases au cours des générations...")
    cases = [[0 for _ in range(data["field"]["height"])] 
             for _ in range(data["field"]["width"])]

    # Comptage du nombre de fois que chaque case est utilisée
    for generation in data["dataGenerations"]:
        for gene in generation["genes"]:
            cases[gene[0][1]][gene[0][0]] += 1

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
        "is_success": data["meta"]["is_success"],
        "crossover_prob": data["meta"]["crossover_prob"],
        "mutation_prob": data["meta"]["mutation_prob"],
        "population_size": data["meta"]["population_size"],
        "terminaison_age": data["meta"]["terminaison_age"],
    }

def analyseFolder(foldername):
    """
    Analyse tous les fichiers d'un dossier en concaténant les données
    """    
    # Récupération des noms des fichiers
    filenames = [f for f in os.listdir(foldername) if os.path.isfile(os.path.join(foldername, f))]

    filenames.sort(key=lambda x : int(x.split(".")[0]))

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
        "performance": 0,
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
        data["performance"] += 1 if file_data["is_success"] else 0

        # Variables invariantes face aux excécutions de l'algorithme
        data["terrain_matrice"] = file_data["terrain_matrice"]
        data["figures"] = file_data["figures"]
        data["count"] = file_data["count"]
        data["athlete"] = file_data["athlete"]

        # Valeurs sans cohérence face aux exécutions
        data["population_size"] = -1
        data["crossover_prob"] = -1
        data["mutation_prob"] = -1
        data["terminaison_age"] = -1

        # Meilleur athlète
        if file_data["best_athlete"]["fitness"] > data["best_athlete"]["fitness"]:
            data["best_athlete"] = file_data["best_athlete"]

        count += 1
        logging.info("Analyse de {} terminée ({}%)".format(filename,
            round((count/file_number)*100, 2)))

    # Moyenne des données
    data["freq_matrice"] /= len(filenames)
    data["nb_generations"] /= len(filenames)
    data["performance"] /= len(filenames)

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


def makeEvolFitnessImg(list_fitness, nb_executions=1):
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
                            
    plt.legend()


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
        plt.text(best_athlete["genes"][i][0][0] + 0.5, 
                 best_athlete["genes"][i][0][1] + 0.5,
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
    plt.subplots_adjust(right=1.2, bottom=-0.8) 

    # Sauvegarde
    plt.savefig("traitement/{}_images/cases.png".format(filename), 
                bbox_inches=Bbox([[0, -4], [9, 5]]),dpi=100)
    plt.close()

def makeFreqImg(list_figures, list_count, nb_executions=1):
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
    
    plt.tight_layout()
    plt.savefig("traitement/{}_images/constantes.png".format(filename), dpi=100)
    plt.close()
    

def createStats(path=None, data=None):
    """
    Crée les images statistiques à partir d'un fichier ou de données fournies.
    
    Args:
        path (str, optional): Le chemin du fichier à analyser. 
            Si non spécifié, les données doivent être fournies.
        data (dict, optional): Les données à analyser. 
            Si non spécifié, le fichier sera analysé en utilisant le chemin spécifié.
    
    Returns:
        None: Cette fonction ne retourne aucune valeur.
    """
    if path is None and data is None:
        logging.error("Veuillez entrer un nom de fichier ou des données à analyser.")
        return
    
    # Chronométrage du programme
    start_time = datetime.datetime.now()
    
    # Récupération des données
    if data is None:
        data = analyse(path)

    # Création du dossier de sauvegarde
    filename = path.split("data/")[-1] # Nom du fichier sans la partie "data/"
    os.makedirs("traitement/{}_images".format(filename), exist_ok=True)

    logging.info("Traitement des données...")

    # Création des images
    makeEvolFitnessImg(data["fitness"],data["nb_executions"])
    makeFreqImg(data["figures"], data["count"], data["nb_executions"])
    
    perf = " performance {}%".format(round(data["performance"]*100,2)) if "performance" in data.keys() \
        else " succès ? {}".format(data["is_success"])

    name = "{}xp, {} générations/exécution en moy, {} individus/génération ({} exécutions)"\
        .format(
            data["athlete"]["xp"], 
            round(data["nb_generations"]), data["population_size"],
            data["nb_executions"]
        )
    
    name += "\n" + perf
    
    plt.suptitle(name)
    plt.subplots_adjust(bottom=0.1, left=-0.2, right=1.3, top=0.85, hspace=2)
    
    plt.savefig("traitement/{}_images/freq&fitness.png".format(filename),
                bbox_inches=Bbox([[-2, -1.3], [9, 5]]),dpi=100)
    plt.close()
    
    constListImage(filename=filename, const_dict={
        "ATHLETE_XP": data["athlete"]["xp"],
        "CROSSOVER_PROB": data["crossover_prob"],
        "MUTATION_PROB": data["mutation_prob"],
        "POPULATION_SIZE": data["population_size"],
        "NUMBER_OF_CHROMOSOME_TO_KEEP": 
                min(NUMBER_OF_CHROMOSOME_TO_KEEP, data["population_size"]-1),
        "TERMINAISON_AGE": data["terminaison_age"],
        "INITIAL_POSITION": INITIAL_POSITION,
        "MAX_TICK_COUNT": MAX_TICK_COUNT,
        "ITERATION_NUMBER": ITERATION_NUMBER,
        "SIZE_X": SIZE_X,
        "SIZE_Y": SIZE_Y,
        "TICK_INTERVAL": TICK_INTERVAL,
        "MAX_FITNESS_GOTTEN": data["best_athlete"]["fitness"],
    })

    makeCasesImg(data["freq_matrice"], data["terrain_matrice"], 
                 data["best_athlete"], filename)

    logging.info("Traitement terminé (en {})!\n".format(
        datetime.datetime.now()-start_time))
    
def analyseStudy(foldername):
    """
    Analyse et création des images pour la comparaison avec l'étude
    """
    
    dataFolder = "data/"+foldername

    # Récupération des noms des fichiers
    filenames = [f for f in os.listdir(dataFolder) 
                 if os.path.isfile(os.path.join(dataFolder, f))]
    filenames.sort(key=lambda x : int(x.split(".")[0]))

    # Construction du dictionnaire : 
    # perfs = {
    #   p_c-p_m-population_size : [0, 1, 1, 0] 
    #       (0 pour un échec, 1 pour un succès)
    #       Longueur = Nombre d'executions
    # }
    # 
    perfs = {}

    def pc_pmToString(file_data):
        pc = file_data["crossover_prob"]
        pm = file_data["mutation_prob"]
        popu = file_data["population_size"]
        return "{}-{}-{}".format(pc, pm, popu)

    # Analyse de chaque fichier
    count = 0
    for filename in filenames:
        # Analyse du fichier
        file_data = analyse(os.path.join(dataFolder, filename))
        
        category = pc_pmToString(file_data)
        if category not in perfs:
            perfs[category] = []

        perfs[category].append(1 if file_data["is_success"] else 0)

        count += 1
        logging.info("Analyse de {} terminée ({}%)".format(filename,
            round((count/len(filenames))*100, 2)))
    
    # Construction du dictionnaire :
    # perfsFinales = {
    #     "pc-pm": [float]
    # }
    perfsFinales = {}

    for pc, pm in zip(PROBS_C, PROBS_M):
        perfsFinales["{}|{}".format(pc, pm)] = []
        for popu in POPULATIONS:
            perf = 0
            for success in perfs["{}-{}-{}".format(pc, pm, popu)]:
                perf += success
            perf /= ITERATION_NUMBER

            perfsFinales["{}|{}".format(pc, pm)].append(perf)

    # Affichage des différentes courbes
    for key, value in perfsFinales.items():
        pc, pm = key.split("|")

        plt.plot(POPULATIONS, value, label="p_c = {}; p_m = {}/l".format(pc, pm))

    # Sauvegarde du tableau final
    saveDir = "traitement/study/{}".format(foldername)
    os.makedirs(saveDir, exist_ok=True)

    plt.legend(prop={'size': 10})
    plt.xlabel("Taille de la population")
    plt.ylabel("Performances")
    plt.ylim((0, 1))
    plt.xscale('log')
    ax = plt.gca()
    ax.xaxis.set_major_formatter(mticker.ScalarFormatter())
    ax.set_xticks([2, 10, 100, 500, 1000, 2000])
    plt.xlim((2, 2000))
    plt.savefig("{}/performances.png".format(saveDir), dpi=100)
    plt.close()

    logging.info("Fichier sauvegardé : {}/performances.png".format(
        saveDir
    ))


if __name__ == "__main__":
    # Afficher les logs dans un fichier
    logging.basicConfig(level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%d-%m-%Y %H:%M:%S',
                    filename='logs/Traitement - {}.txt'.format(
                                            datetime.datetime.now().strftime(
                                                "%d-%m-%Y %H:%M:%S"
                                            )),
                    filemode='w')
    
    # Affichage dans la console
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)
    
    # folder = "8xp/27-03-2024 11h32m49s/"
    # data = analyseFolder("data/" + folder)
    # createStats(path=folder+"/all", data=data)

    analyseStudy("8xp/18-04-2024 16h37m18s")
