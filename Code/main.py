'''
 Name : Elowan
 Creation : 02-06-2023 10:59:30
 Last modified : 27-06-2023 21:16:16
'''
from Terrain import Field, Figure, FIGURES, CASES
from Models import Athlete
from Game import Game
from Genetic import GeneticAlgorithm, Chromosome

from random import seed, randint

seed(2207) # Pour avoir des résultats reproductibles

#########
# Algorithme glouton
#########

# A faire

#########
# Algorithme génétique
#########

POPULATION_NUMBER = 200

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
        score = 0
        for combo in self.genes:
            score += combo[1].complexity
            if combo[1] == self.athlete.figureFav:
                score += 3

        self.fitness = score
        return score
    
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
        child = Athlete(5, parent.athlete.figureFav)
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
        if randint(0, 100) < 5: 
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
    Récupère le meilleur athlète de la population

    Params:
        population (AthleteChromosome list): liste des athlètes

    Returns:
        (AthleteChromosome): le meilleur athlète
    """
    return print(evaluate(population)[0].athlete, evaluate(population)[0].fitness)

def termination(population:list) -> bool:
    """
    Condition d'arrêt de l'algorithme génétique
    (Pour l'instant, on s'arrête quand le meilleur athlète a un score de 3000)

    Params:
        population (AthleteChromosome list): liste des athlètes

    Returns:
        (bool): True si l'algorithme doit s'arrêter, False sinon
    """
    return population[0].fitness >= 102

if __name__ == "__main__":
    ### Creation de la population
    
    # POPULATION_NUMBER de fois le meme athlete 
    population = [AthleteChromosome(Athlete(5, FIGURES["frontflip"])) 
    
                  for _ in range(POPULATION_NUMBER)]
    playAllGames(population)
    
    ### Algorithme génétique

    parkourGenetic = GeneticAlgorithm(population, termination, evaluate, 
                                      selection, crossover, mutation)
    
    parkourGenetic.run(iteration=getBestAthlete, callback=getBestAthlete)

    print("\nMeilleur athlète : {}".format(parkourGenetic.population[-1]))