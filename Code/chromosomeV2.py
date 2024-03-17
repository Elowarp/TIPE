from random import randint, seed
import logging

from Terrain import FIGURES
from Models import Athlete, Figure
from Game import Game
from Genetic import Chromosome
from consts import INITIAL_POSITION, NUMBER_OF_CHROMOSOME_TO_KEEP,\
    EPS, MAX_SCORE, L

import json
import os
import logging
from Game import Game

class AthleteChromosome(Chromosome):
    """
        Classe représentant un athlète (une entitée) pour l'algorithme 
        génétique

        Params:
            athlete (Athlete): Athlète représenté par le chromosome
    """    
    def __init__(self, athlete):
        self.athlete = athlete
        self.genes = from_combo_to_string(athlete.combos)
        # self.detailedFitness = AthleteChromosome.BaseFitness
        self.detailedFitness = {}

        super().__init__(self.genes, self.calc_fitness(), 
                         0, len(self.genes))
        
    def calc_fitness(self) -> int:
        """Calcule le score de l'athlète"""
        score =  {
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
        self.genes = from_combo_to_string(self.athlete.combos)

        # Liste des figures faites
        nb_figure = len(self.genes)//6
        tricks = [Figure.figures[int(self.genes[6*i+4: 6*i+6])] 
                  for i in range(nb_figure)]
        field = self.athlete.field
        cases = [field.getCase(
            (int(self.genes[6*i:6*i+2]), int(self.genes[6*i+2: 6*i+4]))) 
            for i in range(nb_figure)]
        
        # print(tricks)
        # print(cases)

        # Calcul de la sureté des figures
        # On coefficiente la sureté par l'xp de l'athlète
        score["execution"]["safety"] =\
            (score["execution"]["safety"])*self.athlete.xp/10

        # Calcul du flow
        # Compte le nb de fois qu'on s'est arreté
        score["execution"]["flow"] = 3 - tricks.count(FIGURES["do_nothing"])
                        
        # Calcul de la maitrise
        # Max 4
        score["execution"]["mastery"] = 4*self.athlete.xp/10

        # Calcul de l'utilisation de l'espace
        # Compte le nb de cases différentes utilisées
        # Post-it : Identifiant d'une case est unique donc on ne compte que
        #           les cases visitées (dans notre liste de cases)
        # Max 3 (comme le nb de cases)
        l = []
        for case in cases:
            if case.id not in l: l.append(case.id)
        score["composition"]["use_of_space"] = len(l)


        # Calcul de l'utilisation des obstacles
        # Compte le nb de types de cases différents utilisés
        # Max 3 (comme le nb de cases)
        l = []
        for case in cases:
            if case.name not in l: l.append(case.name)
        score["composition"]["use_of_obstacles"] = len(l)

        # Calcul de la connexion entre les obstacles
        # Max 4
        score["composition"]["connection"] = 4*self.athlete.xp/10

        # Calcul de la variété
        # Ajoute 1 pts a chaque figure de complexité >= 2
        # (Donc que le trick n'est pas ds la catégorie de parkour classique)
        score["difficulty"]["variety"] = sum([1
                                for trick in tricks
                                if trick.complexity >= 2])
        
        if score["difficulty"]["variety"] > 3:
            score["difficulty"]["variety"] = 3

        # Calcul de la difficulté d'un trick
        # Ajoute 1 pt par trick de complexité >= 3
        score["difficulty"]["single_trick"] = sum([1
                                for trick in tricks
                                if trick.complexity >= 3])
        
        if score["difficulty"]["single_trick"] > 3:
            score["difficulty"]["single_trick"] = 3

        # Calcul de la difficulté d'un run
        score["difficulty"]["whole_run"] = 4*self.athlete.xp/10


        # Calcul du score final
        self.detailedFitness = score
        self.fitness = sum([sum(score["execution"].values()),
                            sum(score["composition"].values()),
                            sum(score["difficulty"].values())])

        if self.fitness < 0:
            self.fitness = 0
        
        # print(self.fitness)
        return self.fitness
    
    def __repr__(self) -> str:
        return "AthleteID {} de score {} d'age {} et de taille {} : \n{}"\
            .format(self.athlete.id, round(self.fitness, 2), 
                    self.age, self.size, self.athlete)
    
def evaluate(population:list) -> list:
    """
    Notation de chaque athlète de la population
    
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

def get_point_communs(a1, a2) -> tuple[int, int]:
    """
    Renvoie les indices où les deux athlètes sont au même point dans leur course,
    différent de (0, 0).
    Si renvoie (-1, -1) alors il n'y en a pas

    Params :
        a1 (AthleteChromosome) : Athlète
        a2 (AthleteChromosome) : Athlète

    Returns:
        int: indice 
    """
    for i in range(len(a1.combos)):
        for j in range(len(a2.combos)):
            if a1.combos[i] == a2.combos[j]: return (i, j)
    return (-1, -1)


def crossover(parents: list, probs) -> list:
    """
    Crée les enfants de la prochaine population
    On choisit 2 parents et on les on prend 2 moins communs aux deux
    chemins (s'il y a) et on échange les chemins entre ces deux points  

    Si les deux parents sont en réalité le même, on le copie tel quel.
    
    Params:
        parents (AthleteChromosome list): liste d'athlètes

    Returns:
        children (AthleteChromosome list): liste d'athlètes enfants
    """
    children = []   
    CROSSOVER_PROB, _ = probs

    for i in range(len(parents)):
        for j in range(len(parents)):
            if i!=j:
                c1, c2 = get_point_communs(parents[i].athlete, parents[j].athlete)

                # Vérification qu'il y ait au moins 2 points en commun pour
                # faire le croisement et qu'on ait bien la probabilité de le faire
                if c1 != -1 and c2 != -1\
                    and randint(0, 100)/100 < CROSSOVER_PROB:

                    # Premier enfant, avec un premier croisement des combos
                    child1 = Athlete(parents[i].athlete.xp)
                    child1.combos = parents[i].athlete.combos[:c1] +\
                                     parents[j].athlete.combos[c2:]
                    child1.setField(parents[i].athlete.field)
                    childChro1 = AthleteChromosome(child1)
                    childChro1.age = parents[i].age + 1
                    children.append(childChro1)
                    
                    # Deuxieme enfant, avec le croisement complémentaire au premier
                    child2 = Athlete(parents[j].athlete.xp)
                    child2.combos = parents[j].athlete.combos[:c2] +\
                                     parents[i].athlete.combos[c1:]
                    child2.setField(parents[j].athlete.field)
                    childChro2 = AthleteChromosome(child2)
                    childChro2.age = parents[j].age + 1
                    children.append(childChro2)
                    
            else:
                # Premier enfant, copie littérale du parent
                child = Athlete(parents[i].athlete.xp)
                child.combos = parents[i].athlete.combos
                child.setField(parents[i].athlete.field)
                
                childChro = AthleteChromosome(child)
                childChro.age = parents[i].age + 1
                children.append(childChro)

                # Second enfant, idem
                child = Athlete(parents[j].athlete.xp)
                child.combos = parents[j].athlete.combos
                child.setField(parents[j].athlete.field)
                childChro = AthleteChromosome(child)
                childChro.age = parents[j].age + 1
                children.append(childChro)

    return children

def mutation(population:list, probs) -> list:
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
    _, MUTATION_PROB = probs

    for athleteChromosome in population:
        # Mutation
        if randint(0, 100)/100 < MUTATION_PROB/L: # Divisé par L comme dit dans l'étude
            athlete = athleteChromosome.athlete 
             
            # On supprime tous les combots à partir d'un index aléatoire
            index = randint(0, len(athlete.combos) - 1)
            athlete.combos = athlete.combos[:index]
            
            # On fait jouer l'athlète 
            Game(athlete).play()
            
        children.append(athleteChromosome)

    return children

def termination(population:list, infos) -> bool:
    """
    Condition d'arrêt de l'algorithme génétique

    Params:
        population (AthleteChromosome list): liste des athlètes

    Returns:
        (bool): True si l'algorithme doit s'arrêter, False sinon
    """
    # return infos["generationCount"] > 400 or \
    #     MAX_SCORE(population[0].athlete.xp) - EPS < infos["maxPopulationFitness"]
    return infos["generationCount"] > infos["terminaison_age"] or \
        MAX_SCORE(population[0].athlete.xp) - EPS < infos["maxPopulationFitness"]

def getBestAthlete(population):
    """
    Affiche le meilleur athlète de la population

    Params:
        population (AthleteChromosome list): liste des athlètes
    """
    evalPop = evaluate(population)
    logging.debug(evalPop[0].athlete, evalPop[0].fitness)

def from_combo_to_string(combos) -> str:
    """
    Changement de représentation de la suite de combos en une chaîne de 
    caractères pour la représentation des gènes d'un chromosome

    Params:
        combos (tuple list): liste des combos sous la forme
            [((x, y), Figure, tickStarted)]

    Returns:
        str: concaténation de chaque figure codée sur 6 caractères. Par exemple
            "xxyyii" pour la figure d'identifiant i en ligne y et colonne x
            Attention : on code chaque nombre sur 2 chiffres (d'où la longueur 6)
    """
    chaine = []
    for combo in combos:
        x = combo[0][0]
        if x < 10: chaine.append("0")
        chaine.append(str(x))
        y = combo[0][1]
        if y < 10: chaine.append("0")
        chaine.append(str(y))
        i = combo[1].id
        if i < 10: chaine.append("0")
        chaine.append(str(i))
    
    return "".join(chaine)

def from_string_to_combos(genes: str) -> list:
    combos = []
    for i in range(len(genes)//6):
        combos.append(
            (
                (int(genes[6*i: 6*i+2]), int(genes[6*i+2: 6*i+4])),
                Figure.figures[int(genes[6*i+4: 6*i+6])],
                -1
            )
        )

    return combos

def is_success(population):
    """
        Vrai si le meilleur score obtenu est dans l'epsilon interval
        défini par la constante EPS et le meilleur score théorique 
        pour un niveau d'expérience donné. Faux sinon
    """
    return evaluate(population)[0].fitness >\
        MAX_SCORE(population[0].athlete.xp) - EPS

def save(self, probs, population_number, infos):
    """
    Sauvegarde en Json les données de la population à chaque itération
    en plus des informations sur l'athlète original
    """
    # Formatage des données
    dataSerialized = []
    CROSSOVER_PROB, MUTATION_PROB = probs
    for i in range(len(self.populationOverTime)):
        for j in range(min(NUMBER_OF_CHROMOSOME_TO_KEEP, population_number-1)):
            genes = from_string_to_combos(self.populationOverTime[i][j].genes)
            genesSerialized = []
                
            for k in range(len(genes)):
                # -1 pour remplacer le tick auquel la figure a été faite
                # car la modélisation par chaîne de caractère ne tient pas
                # compte de cette info
                genesSerialized.append((genes[k][0], genes[k][1].id, -1))
                    
            dataSerialized.append({
                "genes": genesSerialized,
                "fitness": self.populationOverTime[i][j].fitness,
                "detailedFitness": self.populationOverTime[i][j].detailedFitness,
                "age": self.populationOverTime[i][j].age,
                "size": self.populationOverTime[i][j].size
            })
        
    athleteSerialized = {
        "xp": self.population[0].athlete.xp,
        "InitialPosition": INITIAL_POSITION,  
    }

    metaInfoSerialized = {
        "is_success" : is_success(self.populationOverTime[-1]),
        "crossover_prob": CROSSOVER_PROB,
        "mutation_prob": MUTATION_PROB,
        "population_size": population_number,
        "terminaison_age": infos["terminaison_age"]
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

    i=infos["start_filenumber"]
    while os.path.exists("{}/{}.json".format(self.dirname, i)):
        i += 1
            
    self.filename = str(i)

    with open("{}/{}.json".format(self.dirname, self.filename), "w") as f:
        json.dump(data, f)

    logging.debug("Data saved in {}.json".format(self.filename))

if __name__ == "__main__":    
    # Vérification que les fonctions de traduction Genes <-> Combo
    # est bijective et ne change pas le score final
    
    # Initialisation d'athlètes
    population_number = 8
    population = [AthleteChromosome(Athlete(8)) 
                for _ in range(population_number)]
    
    Game.resetGames()

    for athleteChromosome in population:
        game = Game(athleteChromosome.athlete)
        game.play()

    # Genes avec un score 27 normalement
    genes = [[[7, 30], 2, -1], [[8, 31], 7, -1], [[7, 32], 1, -1], [[8, 33], 7, -1], [[8, 34], 2, -1], [[8, 35], 7, -1], [[8, 36], 5, -1], [[8, 35], 7, -1], [[9, 36], 5, -1], [[9, 37], 17, -1], [[8, 37], 2, -1], [[8, 36], 16, -1], [[7, 37], 9, -1], [[8, 38], 5, -1], [[9, 39], 5, -1], [[8, 39], 17, -1], [[7, 39], 1, -1], [[6, 38], 1, -1], [[5, 39], 10, -1], [[6, 38], 10, -1], [[6, 37], 8, -1], [[5, 38], 6, -1], [[4, 37], 2, -1], [[5, 36], 13, -1], [[6, 36], 8, -1]]
    
    # Transformation du genes sauvegardé en genes utilisable par le programme
    # (Conversion des identifiants en Figure par exemple)
    genes_2 = []
    for coords, fig, tick in genes:
        genes_2.append(((coords[0], coords[1]), Figure.getFigureById(fig), tick))

    print(from_combo_to_string(genes_2))

    s = from_combo_to_string(genes_2)
    g = from_string_to_combos(s)

    print("Echange string <-> combo bijectif (sans ticks) ? "+str(g==genes_2))
    
    # Vérification que les deux évaluations des genes ont le même score 
    population[4].athlete.combos = genes_2

    a = AthleteChromosome(population[4].athlete)
    a.calc_fitness()
    print("A-t-on égalité après deux évalutations consécutives des mêmes gènes ?")
    print(a.fitness==a.calc_fitness())