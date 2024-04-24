'''
 Name : Elowan
 Creation : 02-06-2023 10:59:30
 Last modified : 18-04-2024 21:28:42
'''
import datetime
import logging
from multiprocessing import Process
import traceback

from chromosomeV2 import *
from Models import Athlete
from Game import Game
from Genetic import GeneticAlgorithm
from utils import computeNextOccurrence
from traitement import analyseStudy, analyseFolder, createStats
from consts import NB_EVAL_MAX, PROBS_C, PROBS_M,\
    ITERATION_NUMBER, NUMBER_OF_CHROMOSOME_TO_KEEP,\
    INITIAL_POSITION, MAX_TICK_COUNT, SIZE_X, SIZE_Y,\
    POPULATIONS

#########
# Algorithme génétique
#########

def playAllGames(population:list):
    """
    Joue toutes les parties associées aux athlètes de la population

    Params:
        population (AthleteChromosome list): liste des athlètes à faire jouer
    """
    # Supprime les anciens jeux
    Game.resetGames()

    for athleteChromosome in population:
        game = Game(athleteChromosome.athlete)
        game.play()


def logConstants(athleteLevel, seed):
    """
    Log les constantes de l'algorithme
    """
    logging.info("Seed : {}".format(seed))
    logging.debug("Iteration number : {}".format(ITERATION_NUMBER))
    logging.debug("Athlete level : {}".format(athleteLevel))
    logging.debug("Number of chromosomes to keep : {}".format(NUMBER_OF_CHROMOSOME_TO_KEEP))
    logging.debug("Initial position : {}".format(INITIAL_POSITION))
    logging.debug("Size of the field : {}".format((SIZE_X, SIZE_Y)))
    logging.debug("Max tick count : {}".format(MAX_TICK_COUNT))


def process(POPULATIONS, iteration):
    count = 0
    total = len(POPULATIONS)*len(PROBS_C)*ITERATION_NUMBER

    for population_number in POPULATIONS:
        for probs in zip(PROBS_C, PROBS_M):
            for i in range(ITERATION_NUMBER):
                count+=1
                
                logging.info("##### ITERATION {}/{} #####".format(count, total))
                logging.info("Population number : {}".format(population_number))
                logging.info("Probabilitées : Crossover = {}% Mutation = {}%"\
                            .format(probs[0]*100, probs[1]*100))
                logging.info("Terminaison age : {}".format(NB_EVAL_MAX/population_number))
                ### Creation de la population

                # Chronométrage
                start_time = datetime.datetime.now()
                
                # population_number de fois le meme athlete 
                population = [AthleteChromosome(
                                Athlete(athleteLevel)) 
                            for _ in range(population_number)]
                
                playAllGames(population)
                
                ### Algorithme génétique

                # Informations utilisées pour déterminer la terminaison
                # de l'algorithme (quand le maximum n'a pas été modifié depuis
                # un certain temps maxAge par exemple)
                infos = {
                    "maxPopulationFitness": 0,
                    "maxAge": 0,
                    "generationCount": 0,
                    "terminaison_age": NB_EVAL_MAX/population_number,
                    "start_filenumber": iteration*total,
                }

                # Crée la variable l comme dans l'étude sélectionnée
                u = randint(0, 99)/100
                l = computeNextOccurrence(u, probs[1])

                # Ajout de paramètres supplémentaires
                def term(pop): return termination(pop, infos)
                def s(pop): return save(pop, probs, population_number, infos)
                def mut(pop): return mutation(pop, l)

                def cross(pop): 
                    children = crossover(pop, probs)
                    
                    # Duplications des enfants pour generer une population entière
                    popu = []
                    for _ in range(population_number//len(children)):popu.extend(children)
                    return popu[:population_number]

                parkourGenetic = GeneticAlgorithm(population, term, evaluate, 
                                                selection, cross, mut, s,
                                                "data/{}".format(dirnameSaves))
                
                def iterate(population):
                    # getBestAthlete(population)
                    evalPop = evaluate(population)
                    infos["generationCount"] += 1

                    # Mise a jour du score max des athlètes
                    # et le temps depuis quand c'est le max
                    if evalPop[0].fitness > infos["maxPopulationFitness"]:
                        infos["maxPopulationFitness"] = evalPop[0].fitness
                        infos["maxAge"] = 1

                    else:
                        infos["maxAge"] += 1

                try:
                    parkourGenetic.run(iteration=iterate)
                    
                except Exception as e:
                    traceback.print_exc(e) 
                    logging.error("{}/{} probs:{};{} pop: {}" % 
                                  (i, ITERATION_NUMBER, probs[0], 
                                   probs[1], population_number))
                    logging.error(e)
                    break
                
                else:
                    logging.debug("\nMeilleur athlète de la dernière génération: {}".format(evaluate(parkourGenetic.population)[0]))
                    logging.info("Temps d'execution : {}".format(datetime.datetime.now() - start_time))

                    # createStats(parkourGenetic.getDirname() + "/" + 
                    #                 parkourGenetic.getFilename() + ".json")
                                        
    return parkourGenetic


if __name__ == "__main__":
    s = 1713449159 # Pour avoir des résultats reproductibles
    # s = int(datetime.datetime.now().timestamp())
    seed(s)
    
    athleteLevel = 8
    dirnameSaves = "{}xp/{}".format(athleteLevel, 
                                      datetime.datetime.now()
                                      .strftime("%d-%m-%Y %Hh%Mm%Ss"))
    
    dirs = "data/{}".format(dirnameSaves)

    # Initialisation des logs
    logging.basicConfig(level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%d-%m-%Y %H:%M:%S',
                    filename='logs/Main - {}.txt'.format(str(athleteLevel) + "xp - "
                                             + datetime.datetime.now()
                                             .strftime("%d-%m-%Y %H:%M:%S")),
                    filemode='w')
    
    # Affichage dans la console
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)

    logConstants(athleteLevel, s)


    # Multi-Processing pour accélérer le temps d'exécution
    processes = []
    init_time = datetime.datetime.now()    

    for i in range(len(POPULATIONS)):
    # for i in range(1):
        args = (POPULATIONS[i:i+1], i)
        p = Process(target=process, args=args)
        p.start()
        processes.append(p)

    for p in processes:
        p.join()
    
    # Analyse du dossier (moyenne sur toutes les itérations)
    data = analyseFolder(dirs)
    createStats(path="{}/all".format(dirs), data=data)
    
    # Dessine un graphe semblable à l'étude
    analyseStudy(dirnameSaves)
    

    logging.info("Temps d'execution total : {}".format(
        (datetime.datetime.now() - init_time)))