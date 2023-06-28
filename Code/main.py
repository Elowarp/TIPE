'''
 Name : Elowan
 Creation : 02-06-2023 10:59:30
 Last modified : 28-06-2023 22:56:55
'''
from random import seed, randint, choices
import numpy as np
import datetime

from Terrain import Field, Figure, FIGURES, CASES
from Models import Athlete
from Game import Game
from Genetic import GeneticAlgorithm, Chromosome

seed(2207) # Pour avoir des résultats reproductibles

#########
# Algorithme glouton
#########

# A faire

#########
# Algorithme génétique
#########

POPULATION_NUMBER = 200     # Nombre d'individus dans la population
MUTATION_RATE = 5           # Taux de mutation en pourcentage

def weighted_random(mn, mx, mnweight, mxweight):
    """
    Exécute un random entre mn et mx avec une probabilité de mnweight
    d'avoir la plus basse valeur et mxweight d'avoir la plus haute valeur
    """
    return choices(range(mn, mx+1), \
      weights=np.linspace(mnweight,mxweight,(mx-mn)+1))[0]

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
        score["presentation"] = randint(0, 2)

        # Calcule du flow
        # Compte le nb de fois qu'on s'est arreté
        score["flow"] = 3 - tricks.count(FIGURES["do_nothing"])

        # Calcule de la connection
        score["connection"] = weighted_random(0, 2, 10, 1)

        # Calcule des parts
        # Compte le nb de cases différentes utilisées
        score["parts"] = len(set([field.getCase(combo[0]).id
                                    for combo in self.athlete.combos]))
        
        # Calcule des types
        score["types"] = randint(0, 2)

        # Calcule des tricks
        # Calcule des points accordés par les tricks
        # Majoré par 5
        score["tricks"] = sum([trick.complexity
                                for trick in tricks])
        if score["tricks"] > 5:
            score["tricks"] = 5

        # Calcule du placement
        score["placement"] = randint(1, 3)

        # Calcule du temps
        score["time"] = weighted_random(0, 2, 10, 1)

        # Calcule de la variété
        # Ajoute 0.5 pts a chaque figure de complexité > 2
        # (Donc que le trick n'est pas ds la catégorie de parkour classique)
        score["variety"] = sum([trick.complexity/2
                                for trick in tricks
                                if trick.complexity > 2])
        
        if score["variety"] > 3:
            score["variety"] = 3
        
        # Calcule de la technique
        # Ajout de 2 points max coefficienté par l'xp de l'athlète
        score["technique"] = 2*self.athlete.xp/10

        self.fitness = sum(score.values())
        return self.fitness
    
    def __repr__(self) -> str:
        return "AthleteID {} de score {} d'age {} et de taille {} : \n{}".format(
            self.athlete.id, self.fitness, self.age, self.size, self.athlete)
    
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
    print([x.fitness for x in population[:10]])
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
            index = randint(0, len(athlete.combos)-1)
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
    print(evalPop[0].athlete, evalPop[0].fitness)

def termination(population:list) -> bool:
    """
    Condition d'arrêt de l'algorithme génétique
    (Pour l'instant, on s'arrête quand le meilleur athlète a un score de 3000)

    Params:
        population (AthleteChromosome list): liste des athlètes

    Returns:
        (bool): True si l'algorithme doit s'arrêter, False sinon
    """
    return maxInfos["maxAge"] > 5000

if __name__ == "__main__":
    ### Creation de la population

    # Chronométrage
    start_time = datetime.datetime.now()
    
    # POPULATION_NUMBER de fois le meme athlete 
    population = [AthleteChromosome(Athlete(10, FIGURES["frontflip"])) 
    
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
        getBestAthlete(population)
        evalPop = evaluate(population)

        # Mise a jour du score max des athlètes
        # et le temps depuis quand c'est le max
        if evalPop[0].fitness > maxInfos["maxFitness"]:
            maxInfos["maxFitness"] = evalPop[0].fitness
            maxInfos["maxAge"] = 1

        else:
            maxInfos["maxAge"] += 1

    parkourGenetic.run(iteration=iterate, callback=getBestAthlete)

    print("\nMeilleur athlète : {}".format(evaluate(parkourGenetic.population)[0]))
    print("Temps d'execution : {}".format(datetime.datetime.now() - start_time))