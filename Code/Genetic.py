'''
 Name : Elowan
 Creation : 08-06-2023 10:00:40
 Last modified : 12-12-2023 17:03:31
'''
import random 

class Chromosome:
    """
        Classe abstraite représentant un chromosome (une entitée) 
        de l'algorithme génétique

        Params:
            genes (Polymorphique): Variable représentant les caractéristiques 
                du Chromosome
            fitness (int): Score attribué du chromosome
            age (int): Nombre de générations du chromosome
            size (int): Taille du chromosome
    """
    def __init__(self, genes, fitness, age, size):
        self.genes = genes
        self.fitness = fitness
        self.age = age
        self.size = size

    def __repr__(self) -> str:
        return "Fitness : {}".format(self.fitness)

class GeneticAlgorithm:
    """
        Algorithme génétique adapté à un problème donné
        
        Params:
            population (Chromosome): liste de chromosomes
            termination (function): fonction qui renvoie true/false 
                selon le critère de terminaison de l'algorithme
            evaluate (function): fonction qui évalue la population
            selection (function): fonction qui sélectionne les parents
            crossover (function): fonction qui crée les enfants
            mutation (function): fonction qui fait des mutations sur eux
    """
    def __init__(self, population:list, termination, evaluate, 
                 selection, crossover, mutation, save, dirname="") -> None:
        
        # Renvoie true/false selon le critere de terminaison
        self.termination = termination

        # Fonction d'algo genetique
        self.evaluate = evaluate        # Tri la population
        self.selection = selection      # Selectionne les parents
        self.crossover = crossover      # Crée les enfants
        self.mutation = mutation        # Fait des mutations sur eux
        self.save = save

        self.population = population
        self.population_len = len(population)

        self.populationOverTime = [self.population]

        self.dirname = dirname

    def run(self, iteration=lambda x: None, callback=lambda x: None):
        """
            Execute l'algorithme génétique

            Params:
                ?iteration (function (GeneticAlgorithm): None): fonction qui s'execute à chaque itération
                    de la boucle principale (Prend en paramètre l'instance de l'algorithme génétique et
                    renvoie None)
                ?callback (function (GeneticAlgorithm): None): fonction qui s'execute à la fin de
                    l'algorithme (Prend en paramètre l'instance de l'algorithme génétique et renvoie None)
        """
        while not self.termination(self.population):
            iteration(self.population)
            self.population = self.evaluate(self.population)
            self.population = self.selection(self.population)
            self.population = self.crossover(self.population)
            self.population = self.mutation(self.population)

            # Sauvegarde des données pour la sérialisation
            self.populationOverTime.append(self.population)

        self.save(self)
        return callback(self.population) 
    
    def getFilename(self):
        return self.filename
    
    def getDirname(self):
        return self.dirname

if __name__ == "__main__":
    random.seed(22)
    
    # Test de l'algorithme génétique avec le problème OneMax
    class OneMaxChromosome(Chromosome):
        def __init__(self, genes: list):
            self.genes = genes
            super().__init__(self.genes, self.calc_fitness(), 0, len(self.genes))

        def calc_fitness(self):
            sum_gene = 0
            for i in range(len(self.genes)):
                sum_gene += int(self.genes[i])

            return sum_gene
        
        def mix(self, gene1, gene2):
            self.genes = gene1+gene2
            self.fitness = self.calc_fitness()
            self.age += 1

        def __repr__(self):
            string = ""
            for i in range(len(self.genes)):
                string += str(self.genes[i])

            return string

    def sumlist(population):
        return [chro.fitness for chro in population]

    def swap(i, j, liste):
        temp = liste[i]
        liste[i] = liste[j]
        liste[j] = temp

        return liste

    def evaluate(population):
        # Evaluation de la population
        sums = sumlist(population)

        # Sort list decreasing
        for i in range(len(sums)-1):
            max = i
            for j in range(i+1, len(sums)):
                if sums[j] >= sums[max]:
                    max = j
        
            if max != i:
                sums = swap(i, max, sums)
                population = swap(i, max, population)

        return population
    
    def selection(population):
        # Selection des parents
        # On fait des pairs de chaque element
        liste = []

        for i in range(0, len(population)-1, 2):
            liste.append((population[i], population[i+1]))

        return liste
    
    def crossover(population):
        # Creation des enfants 
        cross_point = random.randint(0, 1000)
        liste = []
        for i in range(len(population)):
            chro1 = population[i][0]
            chro2 = population[i][1]
            chro1.mix(chro1.genes[:cross_point], chro2.genes[cross_point:])
            chro2.mix(chro1.genes[:cross_point], chro2.genes[cross_point:])

            liste.append(chro1)
            liste.append(chro2)

        # print("".join([ str(x) for x in liste[0] ]))
        return liste
    
    def mutation(population):
        liste = []
        for pop in population:
            l = pop
            if random.randint(0, 100) < 5:
                random.shuffle(l.genes)

            liste.append(l)

        return liste
    
    def termination(population): 
        sums = sumlist(population)
        best = sums.index(max(sums))
        return population[best].fitness >= 1000
    
    def iteration(population):
        sums = sumlist(population)
        best = sums.index(max(sums))

        print("Current best : {}".format(population[best].fitness))

    populationChromosome = [ OneMaxChromosome([ random.randint(0, 1) 
                                               for x in range(1000) ]) 
                            for y in range(100) ]
    OneMaxProblem = GeneticAlgorithm(populationChromosome, termination, evaluate,
                            selection, crossover, mutation)
    
    OneMaxProblem.run(iteration)

    sums = sumlist(OneMaxProblem.population)
    best = sums.index(max(sums))
    print("Best overall : {}\nAge : {}".format(OneMaxProblem.population[best], OneMaxProblem.population[best].age))


