'''
 Name : Elowan
 Creation : 02-06-2023 10:59:30
 Last modified : 21-02-2024 08:57:15
'''
import datetime
import logging

from Terrain import FIGURES
# from chromosomeV1 import *
from chromosomeV2 import *
from Models import Athlete
from Game import Game
from Genetic import GeneticAlgorithm
import traitement
from consts import NB_EVAL_MAX, MUTATION_PROB, CROSSOVER_PROB,\
    ITERATION_NUMBER, NUMBER_OF_CHROMOSOME_TO_KEEP,\
    INITIAL_POSITION, MAX_TICK_COUNT, SIZE_X, SIZE_Y

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


def logConstants(athleteLevel):
    """
    Log les constantes de l'algorithme
    """
    # logging.debug("Population number : {}".format(POPULATION_NUMBER))
    logging.debug("Iteration number : {}".format(ITERATION_NUMBER))
    # logging.debug("Mutation probability : {}".format(MUTATION_PROB))
    # logging.debug("Crossover probability : {}".format(CROSSOVER_PROB))
    # logging.debug("Terminaison age : {}".format(TERMINAISON_AGE))
    logging.debug("Athlete level : {}".format(athleteLevel))
    logging.debug("Number of chromosomes to keep : {}".format(NUMBER_OF_CHROMOSOME_TO_KEEP))
    logging.debug("Initial position : {}".format(INITIAL_POSITION))
    logging.debug("Size of the field : {}".format((SIZE_X, SIZE_Y)))
    logging.debug("Max tick count : {}".format(MAX_TICK_COUNT))


if __name__ == "__main__":
    # seed(24) # Pour avoir des résultats reproductibles
    athleteLevel = 8
    dirnameSaves = "{}xp/{}".format(athleteLevel, 
                                      datetime.datetime.now()
                                      .strftime("%d-%m-%Y %Hh%Mm%Ss"))

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

    logConstants(athleteLevel)

    total_time = datetime.timedelta(0)

    # Probabilités utilisées dans l'étude
    POPULATIONS = [2, 5, 10, 20, 35, 60, 100, 200, 300,
        450, 700, 1000, 1400, 1800, 2000]
    PROBS_C = [0.0, 0.0, 0.0, 0.9, 0.9]
    PROBS_M = [0.1, 0.5, 1.0, 0.0, 0.1]

    # Valeurs tests
    # POPULATIONS = [200]
    # PROBS_C = [1.0]
    # PROBS_M = [0.05]
    # ITERATION_NUMBER = 4
    
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
                    "terminaison_age": NB_EVAL_MAX/population_number
                }

                # Ajout de paramètres supplémentaires
                def term(pop): return termination(pop, infos)
                def cross(pop): return crossover_ameliore(pop, probs)
                def mut(pop): return mutation(pop, probs)
                def s(pop): return save(pop, probs, population_number, infos)

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

                parkourGenetic.run(iteration=iterate)

                logging.debug("\nMeilleur athlète de la dernière génération: {}".format(evaluate(parkourGenetic.population)[0]))
                logging.info("Temps d'execution : {}".format(datetime.datetime.now() - start_time))

                traitement.main(parkourGenetic.getDirname() + "/" + 
                                parkourGenetic.getFilename() + ".json")
                        
                total_time += datetime.datetime.now() - start_time

    data = traitement.analyseFolder(parkourGenetic.getDirname())
    traitement.main(path="{}/all".format(parkourGenetic.getDirname()), data=data)
    
    logging.info("Temps d'execution total : {} pour {} itérations".format(
        total_time, ITERATION_NUMBER))