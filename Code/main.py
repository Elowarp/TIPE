'''
 Name : Elowan
 Creation : 02-06-2023 10:59:30
 Last modified : 10-08-2023 13:16:38
'''
from random import seed, randint
import datetime
import logging

from Terrain import FIGURES
from Models import Athlete
from Game import Game
from Genetic import GeneticAlgorithm, Chromosome
import traitement
from consts import POPULATION_NUMBER, MUTATION_RATE, TERMINAISON_AGE,\
    ITERATION_NUMBER, NUMBER_OF_CHROMOSOME_TO_KEEP, INITIAL_POSITION,\
    MAX_TICK_COUNT, SIZE_X, SIZE_Y

#########
# Algorithme glouton
#########

# A faire

#########
# Algorithme génétique
#########

class AthleteChromosome(Chromosome):
    """
        Classe représentant un athlète (une entitée) pour l'algorithme 
        génétique

        Params:
            athlete (Athlete): Athlète représenté par le chromosome
    """
    def __init__(self, athlete):
        self.athlete = athlete
        self.genes = athlete.combos
        super().__init__(self.genes, self.calc_fitness(), 
                         0, len(self.genes))

    def calc_fitness(self) -> int:
        """Calcule le score de l'athlète"""
        score = {
            "surete": 3,
            "presentation": 0,
            "flow": 3,
            "connection": 0,
            "parts": 0,
            "types": 0,
            "tricks": 0,
            "placement": 0,
            "time": 0,
            "variety": 0,
            "technique": 0
        }

        tricks = [ combo[1] for combo in self.athlete.combos]
        field = self.athlete.field

        # Calcule de la sureté des figures
        # On coefficiente la sureté par l'xp de l'athlète
        score["surete"] = (score["surete"])*self.athlete.xp/10
        
        # Calcule de la présentation
        # score["presentation"] = randint(0, 2)
        score["presentation"] = 2*self.athlete.xp/10

        # Calcule du flow
        # Compte le nb de fois qu'on s'est arreté
        score["flow"] = 3 - tricks.count(FIGURES["do_nothing"])

        # Calcule de la connection
        # score["connection"] = weighted_random(0, 2, 20, 1)
        score["connection"] = 2*self.athlete.xp/10

        # Calcule des parts
        # Compte le nb de cases différentes utilisées
        score["parts"] = len(set([field.getCase(combo[0]).id
                                    for combo in self.athlete.combos]))
        
        # Calcule des types
        score["types"] = randint(0, 2)
        score["types"] = 2*self.athlete.xp/10

        # Calcule des tricks
        # Calcule des points accordés par les tricks
        # Majoré par 5
        score["tricks"] = sum([trick.complexity
                                for trick in tricks])/5
        
        if score["tricks"] > 5:
            score["tricks"] = 5

        # Calcule du placement
        score["placement"] = 3*self.athlete.xp/10

        # Calcule du temps
        # score["time"] = weighted_random(0, 2, 20, 1)
        score["time"] = 2*self.athlete.xp/10

        # Calcule de la variété
        # Ajoute 0.5 pts a chaque figure de complexité > 2
        # (Donc que le trick n'est pas ds la catégorie de parkour classique)
        score["variety"] = sum([0.5
                                for trick in tricks
                                if trick.complexity > 2])
        
        if score["variety"] > 3:
            score["variety"] = 3
        
        # Calcule de la technique
        # Ajout de 2 points max coefficienté par l'xp de l'athlète
        score["technique"] = 2*self.athlete.xp/10

        self.fitness = sum(score.values())

        # Une chance pour que l'athlète se blesse
        if randint(0, 100) < 5:
            self.fitness = self.fitness - 5

        if self.fitness < 0:
            self.fitness = 0
            
        return self.fitness
    
    def __repr__(self) -> str:
        return "AthleteID {} de score {} d'age {} et de taille {} : \n{}".format(
            self.athlete.id, round(self.fitness, 2), self.age, self.size, self.athlete)
    
def evaluate(population:list) -> list:
    """
    Evaluation de la population d'athlete
    
    Params:
        population (AthleteChromosome list): liste d'athlètes

    Returns:
        population (AthleteChromosome list): liste d'athlètes triés 
            (décroissant) par score
    """
    population.sort(key=lambda x: x.calc_fitness(), reverse=True)
    return population

def selection(population:list) -> list:
    """
    Selectionne les parents de la prochaine population
    Parents = 10 premiers en score de la population actuelle

    Params:
        population (AthleteChromosome list): liste d'athlètes

    Returns:
        (AthleteChromosome list): liste d'athlètes sélectionnés
    """
    return population[:10]

def crossover(parents:list) -> list:
    """
    Crée les enfants de la prochaine population
    On choisit un parent sur 10 (modulo) pour créer un enfant
    parfaitement identique à lui

    Params:
        parents (AthleteChromosome list): liste d'athlètes

    Returns:
        children (AthleteChromosome list): liste d'athlètes enfants
    """
    children = []

    for i in range(POPULATION_NUMBER):
        # Selectionne un parent sur 10 (modulo)
        parent = parents[i % 10]
        child = Athlete(parent.athlete.xp, parent.athlete.figureFav)
        child.combos = parent.athlete.combos
        child.setField(parent.athlete.field)
        childChro = AthleteChromosome(child)
        childChro.age = parent.age + 1
        children.append(childChro)
    return children

def mutation(population:list) -> list:
    """
    Fait muter la population
    On choisit un athlète (5% de chance de le muter) et on lui change
    une figure aléatoire

    Params:
        population (AthleteChromosome list): liste d'athlètes

    Returns:
        children (AthleteChromosome list): liste d'athlètes enfants
    """
    children = []
    for athleteChromosome in population:
        # Mutation
        if randint(0, 100) < MUTATION_RATE: 
            athlete = athleteChromosome.athlete 
             
            # On supprime tous les combots à partir d'un index aléatoire
            index = randint(0, len(athlete.combos) - 1)
            athlete.combos = athlete.combos[:index]
            
            # On fait jouer l'athlète 
            Game(athlete).play()
            
        children.append(athleteChromosome)

    return children

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

def getBestAthlete(population):
    """
    Affiche le meilleur athlète de la population

    Params:
        population (AthleteChromosome list): liste des athlètes
    """
    evalPop = evaluate(population)
    logging.debug(evalPop[0].athlete, evalPop[0].fitness)

def termination(population:list) -> bool:
    """
    Condition d'arrêt de l'algorithme génétique
    (Pour l'instant, on s'arrête quand le meilleur athlète a un score de 3000)

    Params:
        population (AthleteChromosome list): liste des athlètes

    Returns:
        (bool): True si l'algorithme doit s'arrêter, False sinon
    """
    return maxInfos["maxAge"] > TERMINAISON_AGE

def logConstants(athleteLevel, athleteFigureFav):
    """
    Log les constantes de l'algorithme
    """
    logging.debug("Population number : {}".format(POPULATION_NUMBER))
    logging.debug("Iteration number : {}".format(ITERATION_NUMBER))
    logging.debug("Mutation rate : {}%".format(MUTATION_RATE))
    logging.debug("Terminaison age : {}".format(TERMINAISON_AGE))
    logging.debug("Athlete level : {}".format(athleteLevel))
    logging.debug("Athlete figure fav : {}".format(athleteFigureFav))
    logging.debug("Number of chromosomes to keep : {}".format(NUMBER_OF_CHROMOSOME_TO_KEEP))
    logging.debug("Initial position : {}".format(INITIAL_POSITION))
    logging.debug("Size of the field : {}".format((SIZE_X, SIZE_Y)))
    logging.debug("Max tick count : {}".format(MAX_TICK_COUNT))


if __name__ == "__main__":
    # seed(24) # Pour avoir des résultats reproductibles
    athleteLevel = 9
    athleteFigureFav = FIGURES["frontflip"]

    # Initialisation des logs
    logging.basicConfig(level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%d-%m-%Y %H:%M:%S',
                    filename='logs/Main - {}.txt'.format(str(athleteLevel) + "xp - "
                                             + str(athleteFigureFav) + " - "
                                             + datetime.datetime.now()
                                             .strftime("%d-%m-%Y %H:%M:%S")),
                    filemode='w')
    
    # Affichage dans la console
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)

    logConstants(athleteLevel, athleteFigureFav)

    total_time = datetime.timedelta(0)

    for i in range(ITERATION_NUMBER):
        logging.info("##### ITERATION {}/{} #####".format(i+1, ITERATION_NUMBER))
        ### Creation de la population

        # Chronométrage
        start_time = datetime.datetime.now()
        
        # POPULATION_NUMBER de fois le meme athlete 
        population = [AthleteChromosome(
                        Athlete(athleteLevel, athleteFigureFav)) 
                    for _ in range(POPULATION_NUMBER)]
        
        playAllGames(population)
        
        ### Algorithme génétique

        maxInfos = {
            "maxFitness": 0,
            "maxAge": 0,
        }

        parkourGenetic = GeneticAlgorithm(population, termination, evaluate, 
                                        selection, crossover, mutation)
        
        def iterate(population):
            # getBestAthlete(population)
            evalPop = evaluate(population)

            # Mise a jour du score max des athlètes
            # et le temps depuis quand c'est le max
            if evalPop[0].fitness > maxInfos["maxFitness"]:
                maxInfos["maxFitness"] = evalPop[0].fitness
                maxInfos["maxAge"] = 1

            else:
                maxInfos["maxAge"] += 1

        parkourGenetic.run(iteration=iterate)

        logging.debug("\nMeilleur athlète de la dernière génération: {}".format(evaluate(parkourGenetic.population)[0]))
        logging.info("Temps d'execution : {}".format(datetime.datetime.now() - start_time))

        traitement.main(parkourGenetic.getDirname() + "/" + 
                        parkourGenetic.getFilename() + ".json")
                
        total_time += datetime.datetime.now() - start_time

    data = traitement.analyseFolder(parkourGenetic.getDirname())
    traitement.main(filename="{}/all".format(parkourGenetic.getDirname()), data=data)
    
    logging.info("Temps d'execution total : {} pour {} itérations".format(
        total_time, ITERATION_NUMBER))