from random import randint
import logging
from utils import weighted_random

from Terrain import FIGURES
from Models import Athlete
from Game import Game
from Genetic import Chromosome
from consts import POPULATION_NUMBER, MUTATION_RATE, TERMINAISON_AGE,\
    INITIAL_POSITION, MUTATION_RATE, NUMBER_OF_CHROMOSOME_TO_KEEP

import json
import os
import logging

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

        self.detailedFitness = {
            "execution": {
                "safety": 3,
                "flow": 0,
                "mastery": 0,
            },
            "composition": {
                "use_of_space": 0,
                "use_of_obstacles": 0,
                "connection": 0,
            },
            "difficulty": {
                "variety": 0,
                "single_trick": 0,
                "whole_run": 0,
            },
        }

        super().__init__(self.genes, self.calc_fitness(), 
                         0, len(self.genes))

    def calc_fitness(self) -> int:
        """Calcule le score de l'athlète"""
        score = self.detailedFitness

        tricks = [combo[1] for combo in self.athlete.combos]
        field = self.athlete.field
        cases = [field.getCase(combo[0]) 
            for combo in self.athlete.combos]

        # Calcul de la sureté des figures
        # On coefficiente la sureté par l'xp de l'athlète
        score["execution"]["safety"] =\
            (score["execution"]["safety"])*self.athlete.xp/10

        # Calcul du flow
        # Compte le nb de fois qu'on s'est arreté
        score["execution"]["flow"] = 3 - tricks.count(FIGURES["do_nothing"])
                        
        # Calcul de la maitrise
        # score["execution"]["mastery"] = weighted_random(0, 4, 1, 2*self.athlete.xp)
        score["execution"]["mastery"] = 4*self.athlete.xp/10

        # Calcul de l'utilisation de l'espace
        # Compte le nb de cases différentes utilisées
        
        l = []
        for case in cases:
            if case.id not in l: l.append(case.id)
        score["composition"]["use_of_obstacles"] = len(l)/3
        
        if score["composition"]["use_of_space"] > 3:
            score["composition"]["use_of_space"] = 3

        # Calcul de l'utilisation des obstacles
        # Compte le nb de types de cases différents utilisés
        l = []
        for case in cases:
            if case.name not in l: l.append(case.name)
        score["composition"]["use_of_obstacles"] = len(l)/3
        
        # Limite le score à 3
        if score["composition"]["use_of_obstacles"] > 3:
            score["composition"]["use_of_obstacles"] = 3

        # Calcul de la connexion entre les obstacles
        # score["composition"]["connection"] = weighted_random(0, 4, 1, 2*self.athlete.xp)
        score["composition"]["connection"] = 4*self.athlete.xp/10

        # Calcul de la variété
        # Ajoute 0.5 pts a chaque figure de complexité > 2
        # (Donc que le trick n'est pas ds la catégorie de parkour classique)
        score["difficulty"]["variety"] = sum([0.5
                                for trick in tricks
                                if trick.complexity > 2])
        
        if score["difficulty"]["variety"] > 3:
            score["difficulty"]["variety"] = 3

        # Calcul de la difficulté d'un trick
        # Ajoute 1 pt par trick de complexité > 3
        score["difficulty"]["single_trick"] = sum([trick.complexity
                                for trick in tricks
                                if trick.complexity > 3])
        
        if score["difficulty"]["single_trick"] > 3:
            score["difficulty"]["single_trick"] = 3

        # Calcul de la difficulté d'un run
        score["difficulty"]["whole_run"] = weighted_random(0, 4, 1, 2*self.athlete.xp)


        # Calcul du score final
        self.detailedFitness = score
        self.fitness = sum([sum(score["execution"].values()),
                            sum(score["composition"].values()),
                            sum(score["difficulty"].values())])
                            
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

def termination(population:list, maxInfos) -> bool:
    """
    Condition d'arrêt de l'algorithme génétique

    Params:
        population (AthleteChromosome list): liste des athlètes

    Returns:
        (bool): True si l'algorithme doit s'arrêter, False sinon
    """
    return maxInfos["maxAge"] > TERMINAISON_AGE

def getBestAthlete(population):
    """
    Affiche le meilleur athlète de la population

    Params:
        population (AthleteChromosome list): liste des athlètes
    """
    evalPop = evaluate(population)
    logging.debug(evalPop[0].athlete, evalPop[0].fitness)

def save(self):
    """
    Sauvegarde en Json les données de la population à chaque itération
    en plus des informations sur l'athlète original
    """
    # Formatage des données
    dataSerialized = []
    for i in range(len(self.populationOverTime)):
        for j in range(NUMBER_OF_CHROMOSOME_TO_KEEP):
            genes = self.populationOverTime[i][j].genes
            genesSerialized = []
                
            for k in range(len(genes)):
                genesSerialized.append((genes[k][0], genes[k][1].id, genes[k][2]))
                    
            dataSerialized.append({
                "genes": genesSerialized,
                "fitness": self.populationOverTime[i][j].fitness,
                "detailedFitness": self.populationOverTime[i][j].detailedFitness,
                "age": self.populationOverTime[i][j].age,
                "size": self.populationOverTime[i][j].size
            })
        
    athleteSerialized = {
        "xp": self.population[0].athlete.xp,
        "FigureFav": self.population[0].athlete.figureFav.id, 
        "InitialPosition": INITIAL_POSITION,  
    }

    metaInfoSerialized = {
        "POPULATION_NUMBER": self.population_len,
        "NUMBER_OF_CHROMOSOME_TO_KEEP": NUMBER_OF_CHROMOSOME_TO_KEEP,
        "MUTATION_RATE": MUTATION_RATE,
        "NUMBER_OF_GENERATIONS": len(self.populationOverTime)
    }
        
    fieldCases = []
    for i in range(len(self.population[0].athlete.field.grille)):
        ligne = []
        for j in range(len(self.population[0].athlete.field.grille[i])):
            caseId = self.population[0].athlete.field.grille[i][j].id
            ligne.append(caseId)

        fieldCases.append(ligne)

    fieldSerialized = {
        "cases": fieldCases,
        "width": len(self.population[0].athlete.field.grille),
        "height": len(self.population[0].athlete.field.grille[0])
    }

    data = {
        "metaInfo": metaInfoSerialized,
        "athlete": athleteSerialized,
        "field": fieldSerialized,
        "dataGenerations": dataSerialized
    }

    os.makedirs(self.dirname, exist_ok=True)

    i=0
    while os.path.exists("{}/{}.json".format(self.dirname, i)):
        i += 1
            
    self.filename = str(i)

    with open("{}/{}.json".format(self.dirname, self.filename), "w") as f:
        json.dump(data, f)

    logging.debug("Data saved in {}.json".format(self.filename))
       