'''
 Name : Elowan
 Creation : 23-06-2023 11:42:17
 Last modified : 21-05-2024 12:02:40
 File : Chromosome.py
'''
from random import randint, seed, choice
import logging
from math import sqrt, ceil
import json
import os

from Terrain import FIGURES
from Models import Athlete, Figure
from Game import Game
from Genetic import Chromosome
from consts import INITIAL_POSITION, NUMBER_OF_CHROMOSOME_TO_KEEP,\
    EPS, MAX_SCORE, L, SIZE_X, SIZE_Y, DIST_MAX

k = 0
i = 0

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
        try:
            cases = [field.getCase(
                (int(self.genes[6*i:6*i+2]), int(self.genes[6*i+2: 6*i+4]))) 
                for i in range(nb_figure)]
        except IndexError:
            for i in range(nb_figure): 
                print((int(self.genes[6*i:6*i+2]), int(self.genes[6*i+2: 6*i+4])))
                return 0


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
    for i in range(0, len(a1.genes), 6):
        for j in range(0, len(a1.genes), 6):
            if a1.genes[i: i+6] == a2.genes[j: j+6]: return (i, j)
    return (-1, -1)

def copy_chromosome(parent):
    """
    Duplique littéralement un chromosome en augmentant son age

    Params :
        parent (AthleteChromosome) : Parent

    Returns:
        AthleteChromosome: Duplica
    """
    child = Athlete(parent.athlete.xp)
    child.combos = parent.athlete.combos
    child.setField(parent.athlete.field)
    
    childChro = AthleteChromosome(child)
    childChro.age = parent.age + 1
    return childChro

def new_children_crossover(p1, p2, cross_prob):
    """
    Renvoie deux nouveaux chromosomes enfants des deux parents p1 et p2
    selon la méthode de croisement et la probabilité de croisement cross_prob

    Params :
        p1 (AthleteChromosome) : Parent
        p2 (AthleteChromosome) : Parent

    Returns:
        (AthleteChromosome, AthleteChromosome): Les enfants 
    """
    c1, c2 = get_point_communs(p1, p2)

    if c1 != -1 and c2 != -1\
                    and randint(0, 100)/100 < cross_prob:

        # Premier enfant, avec un premier croisement des combos
        child1 = Athlete(p1.athlete.xp)
        child1.setField(p1.athlete.field)
        child1.combos = from_string_to_combos(p1.genes[:c1]+p2.genes[c2:])
        childChro1 = AthleteChromosome(child1)
                        
        # Deuxieme enfant, avec le croisement complémentaire au premier
        child2 = Athlete(p2.athlete.xp)
        child2.setField(p2.athlete.field)
        child2.combos = from_string_to_combos(p2.genes[:c2] + p1.genes[c1:])
        childChro2 = AthleteChromosome(child2)
        return childChro1, childChro2

    else:
        return copy_chromosome(p1), copy_chromosome(p2)

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
    for i in range(0, len(parents)-1, 2):
        c1, c2 = new_children_crossover(parents[i], parents[i+1],
                                            CROSSOVER_PROB)
        children.append(c1)
        children.append(c2)

    return children

def dist(x1, y1, x2, y2):
    """Calcule la distance entre 2 points dans le plan"""
    return sqrt((x2-x1)**2 + (y2-y1)**2)

def coherence_suite_etats(e1, e2, e3):
    """
    Vérifie la cohérence des l'état e2 provenant de l'état e1 et allant 
    à l'état e3 

    Params:
        e1/e2/e3 (str): String de 6 caractères représentant un état

    Returns:
        (bool): Valide ou non
    """
    x1 = int(e1[0:2])
    x2 = int(e2[0:2])
    x3 = int(e3[0:2])

    y1 = int(e1[2:4])
    y2 = int(e2[2:4])
    y3 = int(e3[2:4])

    return dist(x1, y1, x2, y2) <= DIST_MAX and dist(x2, y2, x3, y3) <= DIST_MAX

def mutation_individual(athleteChromosome: AthleteChromosome, k:int):
    """
    Mutation en place de l'athlete `athleteChromosome` passé en paramètre.
    Le caractère du gene à modifier est imposé par le paramètre `k` contenu 
    entre 0 et 419 inclus.
    """
    # k = Indice du caractère à modifier 
    # i = Indice du gene contenant la variable 
    k = k%len(athleteChromosome.genes)
    i = (k - k%6)//6

    # Etat associé au gène
    e = athleteChromosome.genes[i*6: (i+1)*6]
    
    # Positions et figure associé à l'état
    x = int(e[0:2])
    y = int(e[2:4])
    f = int(e[4:6])

    modifieur = choice([-1, 1])

    # Récupération des états précédant et succédant l'état à l'étude
    if i == 0 :
        e1 = e
    else:
        e1 = athleteChromosome.genes[(i-1)*6: i*6]

    if i >= len(athleteChromosome.genes)//6 - 1:
        e3 = e
    else:
        e3 = athleteChromosome.genes[(i+1)*6: (i+2)*6]

    has_mutated = True

    # Match sur la composante qui va être modifiée
    match (k%6)//2:
        case 0 : # Si on modifie la variable de l'abscisse
            # Le modifieur étant choisi avant le match, on vérifie que 
            # la modification apporté à l'abscisse n'enfreint aucune 
            # des conditions de bons fonctionnements comme : 
            # 0 <= x < SIZE_X et que le déplacement à cette case depuis 
            # la case précédente e1 est possible et le deplacement vers e3, 
            # assuré par le renvoie "true" de la fonction coherence_suite_etats
            e2 = from_combo_to_string(
                [((x+modifieur, y), Figure.getFigureById(f), 0)])

            if x + modifieur >= 0 and x + modifieur < SIZE_X:
                if coherence_suite_etats(e1, e2, e3):
                    x += modifieur
                    
                else:
                    if x-modifieur >= 0 :
                        e2_recovery = from_combo_to_string(
                                [((x-modifieur, y), Figure.getFigureById(f), 0)])

                        if coherence_suite_etats(e1, e2_recovery, e3): 
                            x -= modifieur

                        else: has_mutated = False

            else:
                if x-modifieur >= 0 and x-modifieur < SIZE_X:
                    e2_recovery = from_combo_to_string(
                        [((x-modifieur, y), Figure.getFigureById(f), 0)])
                        
                    if coherence_suite_etats(e1, e2_recovery, e3): 
                        x -= modifieur
                    else: has_mutated = False
                else: has_mutated = False
                    
        
        case 1: # Sensiblement la même chose que précédemment mais pour l'ordonné
            e2 = from_combo_to_string(
                [((x, y+modifieur), Figure.getFigureById(f), 0)])

            if y + modifieur >= 0 and y + modifieur < SIZE_Y:

                if coherence_suite_etats(e1, e2, e3):
                    y += modifieur

                else:
                    if y-modifieur >= 0 :
                        e2_recovery = from_combo_to_string(
                                [((x, y-modifieur), Figure.getFigureById(f), 0)])
                        
                        if coherence_suite_etats(e1, e2_recovery, e3): 
                            y -= modifieur
                        else: has_mutated = False
                    

            else:
                if y-modifieur >= 0 and y-modifieur < SIZE_Y:
                    e2_recovery = from_combo_to_string(
                        [((x, y-modifieur), Figure.getFigureById(f), 0)])
                    
                    if coherence_suite_etats(e1, e2_recovery, e3): 
                        y -= modifieur
                    else: has_mutated = False
                else: has_mutated = False

        case 2: # Cas du changement de la figure
            if f + modifieur >= len(FIGURES) or f+modifieur < 0 :
                f -= modifieur
            else:
                f += modifieur
    
    # Reconstruction du gène
    gene = athleteChromosome.genes[0: i*6] +\
            from_combo_to_string([((x, y), Figure.getFigureById(f), 0)])+\
            athleteChromosome.genes[(i+1)*6:]
    
    # Modification en place de l'athlete
    athleteChromosome.genes = gene
    athleteChromosome.athlete.combos = from_string_to_combos(gene)

    return has_mutated

def mutation(population:list, l: int) -> list:
    """
    Fait muter la `population`, en ajoutant 1 ou -1 à un gène aléatoire
    (position x, position y ou l'indentifiant de la figure) selon le dernier muté
    et du paramètre `l` (Mutation Clock operation) et la cohérence de 
    ce changement avec le modèle réel

    Params:
        population (AthleteChromosome list): liste d'athlètes
        l (int): nombre associé à une probabilité selon la 2nd étude sur les GAs

    Returns:
        population (AthleteChromosome list): liste d'athlètes enfants
                 
    """
    global k, i
    has_mutated = mutation_individual(population[i], k)

    if not has_mutated:
        i = (i+1)%len(population)
        
    else:
        k = int((k+l)%L)
        i = (i + ceil((k+l)/L))%len(population)

    return population

def termination(population:list, infos) -> bool:
    """
    Condition d'arrêt de l'algorithme génétique

    Params:
        population (AthleteChromosome list): liste des athlètes

    Returns:
        (bool): True si l'algorithme doit s'arrêter, False sinon
    """
    return infos["generationCount"] > infos["terminaison_age"] or \
        MAX_SCORE(population[0].athlete.xp) - EPS < infos["maxPopulationFitness"]

def getBestAthlete(population):
    """
    Affiche le meilleur athlète de la population

    Params:
        population (AthleteChromosome list): liste des athlètes
    """
    evalPop = evaluate(population)
    logging.info(evalPop[0])

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
    """
    Fonction réciproque de `from_combo_to_string` sans les ticks
    """
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
      
            dataSerialized.append({
                "g": self.populationOverTime[i][j].genes,
                "f": self.populationOverTime[i][j].fitness,
                "a": self.populationOverTime[i][j].age,
                "s": self.populationOverTime[i][j].size
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
    ### Tests
    seed(0)

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

    s = from_combo_to_string(genes_2)
    g = from_string_to_combos(s)

    print("Echange string <-> combo bijectif (sans ticks) ? "+str(g==genes_2))
    
    # Vérification que les deux évaluations des genes ont le même score 
    population[4].athlete.combos = genes_2

    a = AthleteChromosome(population[4].athlete)
    a.calc_fitness()
    print("A-t-on égalité après deux évalutations consécutives des mêmes gènes ? %s" % 
          (a.fitness==a.calc_fitness()))

    print()

    # Test du croisement
    print("Croisement de 073002-083107-073201 et 083107-012601-070002")
    
    a1 = AthleteChromosome(population[4].athlete)
    a2 = AthleteChromosome(population[4].athlete)

    a1.genes = "073002083107073201"
    a2.genes = "083107012601070002"

    a1.athlete.combos = from_string_to_combos(a1.genes)
    a2.athlete.combos = from_string_to_combos(a2.genes)

    l = crossover([a1, a2], (1, 1))
    
    # Tests
    t1 = l[0].genes == "073002083107012601070002"
    t2 = l[1].genes == "083107073201"


    print("Donne-t-il 073002-083107-012601-070002 et 083107-073201 ? %s" % 
          (t1 and t2))

    l = crossover(population, (0.2, 0.3))
    print("Garde-t-on la même taille de population ? %s" % 
          (len(population) == len(l)))
    
    a1.genes = "012506"
    d = mutation([a1], 0)

    print("Mutation de 012506 : %s (Valide si égal à 022506)" % d["population"][0].genes)
    print("Probs : (1, 1, 0, 0) devient (%s, %s, %s, %s)" % d["probs"])
