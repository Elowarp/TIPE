## 26 / 05 / 2023

> Idée de tipe : Comment optimiser ses déplacements pour gagner une compétition de parkour ?

Compétition de parkour = Obtenir le plus gros score en faisant des acrobaties en un temps réduit

Sur un parcours restreint (terrain de jeu), l’athlète se voit offrir des murs, des barres et des trous. Il doit faire toutes les acrobaties qu’il veut/peut pour gagner le plus de point, sachant que chacune d’entre elle est notée sur 10 selon sa difficulté de réalisation dans l’espace, sa complexité technique et la beauté de réalisation.

Idée de résolution de problème : On applique certains algorithmes (gloutons et sélection naturelle) pour ensuite savoir quels combos sont les meilleurs à effectuer pour maximiser ses points et ses chances de gagner.

### Modèle :
- On a un damier représentant le terrain de jeu.
- Chaque case se voit attribuer un numéro correspondant à une figure possible sur cette case (ne rien faire, avancer, palm flip, backflip, gap, cork, front flip, saut de bras, etc.).
- Chaque figure a des attributs différents (complexité technique et difficulté de réalisation dans l’espace, temps de réalisation, case de réalisation)
- L’athlète a aussi des attributs : Expérience, aisance de pratique, et figure préférée
- Les athlètes réalisent une certaine action en fonction de la case où ils sont (soit ils vont à droite soit gauche soit haut soit bas et suite à se déplacement, il effectue une figure).  

### Algorithme glouton :
On fait une génération avec un seul athlète qui a certains attributs définis, on applique l’algorithme glouton pour avoir un résultat optimal pour cet athlète (choix optimal à chaque case). On ré exécute l’algorithme pour toutes les combinaisons possibles d’attributs

### Algorithmes de sélection naturelle :
1. On génère des athlètes d’un niveau d’expérience défini (correspondant à la personne dont on veut étudier ses chances), d’aisance et de figure préférée défini au départ. On lance un certain nombre (50 sûrement, a voir avec les sources bibliographiques) d’athlètes sur le parcours, ils font leurs actions (chaque déplacement est prévu avant la génération, chemin de première génération = aléatoire) et on regarde lequel ont les meilleurs scores pour ces attributs, on prend les premiers (10), on fait des mutations sur leur parcours et on régénère, jusque obtenir un « bon » score. (TODO : Voir comment définir un bon score)
2. Idem que celui d’au dessus mais cette fois on rajoute une dose d’aléatoire dans l’emplacement de départ. But : Voir différents profils et différents parcours au lieu de voir une sorte d’algorithme de plus court chemin

### Comment noter le score :
- Pas de borne sup
- Nombre d’action (voir à ne pas mettre pour ne pas récompenser encore plus ceux qui font bcp alors que les actions sont pas folles)    
- Beauté de réalisation pour chaque action en fonction de sa difficulté, genre plus la difficulté est basse, plus la beauté est haute mais moins d’expérience il y a, moins la beauté est haute (possibilité de mettre de l’aléatoire pour pimenter la chose et si ya le temps)
- Moyenne de la complexité et difficulté de l’action

  

### Comment comparer les algorithmes :
- Diagrammes (Nombres d’actions / Score) pour les 3 algos
- Diagrammes du nombres d’actions pour expériences pour les 3 algos
- Etc

# 31/05/2023

Recherche des bibliographies :
- Genetic Algorithms in Elixir: Solve Problems Using Evolution
- Scoring : [https://www.gymnastics.sport/publicdir/rules/files/en_2022-2024%20PK%20Code%20of%20Points%20with%20changes.pdf](https://www.gymnastics.sport/publicdir/rules/files/en_2022-2024%20PK%20Code%20of%20Points%20with%20changes.pdf)

# 02/05/2023

[](https://app.mindmup.com/map/_free/2023/06/416c9280012b11ee805667c45dd8edd2)![](file:///tmp/lu29377elvmn.tmp/lu29377elvmu_tmp_c8fa242a88a97841.png) [https://app.mindmup.com/map/_free/2023/06/416c9280012b11ee805667c45dd8edd2](https://app.mindmup.com/map/_free/2023/06/416c9280012b11ee805667c45dd8edd2)

Chaque athlète on met dans un fichier json avec le nom de l’algo, le nombre d’itération de l’algo, les modifications par itération, les attributs de l’athèle

# 03/05/2023
Terrain a pour 0, 0 le coin en haut a gauche

Pseudo aléatoire : graine de 22

Changement de l’athlete
- Position en x y
- Etat de mouvement
- Un score
- La fonction de note il faudrait la bouger de lathelte vers game

Pour faire bouger l athlete sur le terrain, on note les cases adjacentes de 0 à 7 (0 = haut gauche et on tourne sens horaire) et on choisit un aléatoire parmis eux et ca sera notre prochaine case

A faire : Mettre a jour la mindmap, faire le scoring, faire des sauvegardes des états des game apres chaque fin de jeu, commencer a lire pour faire les algos et comprendre comment jdois agencer le code

# 04/06/2023

Lecture du livre genetique elixir

Différence entre exploitation et exploration, exploitation des informations déjà connus (grâce à l’hérédité notamment) et exploration de l’environnement (notion d’aléatoire)

**Crossover /** **Croisement**: Comment les algo genetique exploitent les informations disponibles dans la recherche

c’est a dire le processus de créer des nouveaux child solutions depuis les parents solutions.

The idea is that the strongest solutions have **characteristics** that make them strong. These characteristics are called **schemas,** c’est le combo de départ.

premature convergence : c’est pour ça qu’on utilise de la mutation, pour éviter de rester bloqué dans un schema

Mutation : Comment l’algorithme explore
![](file:///tmp/lu29377elvmn.tmp/lu29377elvmu_tmp_8aa53475c50d3373.png)Code : Changer les deplacements des générations futures par des variations des premieres donc il faut rajouter un champ chemin et preferer prendre le chemin à l’aléatoire complet pour eviter la premature convergence

Fitness solution : Score associé à un chromosome

Faire des constantes pour les parametres d’algorithme en mode le taux de mutation, la taille du set etc

# 09/06/2023

Chromosome : Solution à un problème

Alleles : Etapes / Constituants du problème

Un chromosome typique a :
- Genes
- Taille
- Fitness
- Age

3 choses à avoir :
- Comment tu mesures le score (fitness)
- Une facon de representer la solution (encoding, named genotype)
- Un critère de terminaison

genotype = tells what the chromosome should look like, defini le search space (interne)
phenotype = representation expressionelle des solutions

![](file:///tmp/lu29377elvmn.tmp/lu29377elvmu_tmp_5c2c5c81bcc2ded6.png)  

   
4 Formes de Genotype :
1. Binaire  
    Tableau de 0 et 1 : [0, 0, 1, 1, 0, 1, 0 ]. Chaque case represente une caractéristique, le 1 montre que le génotype l’a, te 0 montre que non. Plutot bien adapté à plusieurs problèmes
2. Permutation  
    Tableau de nombre : [5, 6, 0, 4, 0, 8]. Reponds au problème appelé Combinatorial optimization. Un problème qui cherche une facon de trier les nombres pour repondre au mieux à un problème (ex : une ville repr par un nombre, et la liste est triée de telle sorte que c’est le meilleur chemin à suivre). Problèmes : difficile de faire de la mutation ou créer des enfants en gardant son intégrité
3. Valeurs réelles  
    Tableau de valeurs réelles / string, utile dans certains problèmes mais pas utilisé majoritairement. Utilité : PRECISION
4. Arbre / Graphe  
    Grv utilisé dans la programmation génétique (faire apprendre a l’ordi a programmer tout seul). Compliqué à implementer cependant.

Problème du sac à dos : Problèmes de satisfaction de contrainte (ce qui se rapproche de ce que moi je fais, temps contraint, espace contraint)

J’ai fait la mindmap du programme pour l’instant, en plus de l’adaptation en POO de l’algorithme

[](https://framindmap.org/c/maps/1361436/edit)![](file:///tmp/lu29377elvmn.tmp/lu29377elvmu_tmp_1c9ae3aa10223a10.png) [https://framindmap.org/c/maps/1361436/edit](https://framindmap.org/c/maps/1361436/edit)

Les classes : [[Classes.canvas|Classes]]

Fonction de pénalité : Punir quand le resultat c’est pas bon
Critère de terminaison quand on ne sait pas quel est le meilleur résultat
3 façons de faire :
- Arreter d’évoluer au bout d’un certain seuil de score
- Arreter d’évoluer au bout de la n-ieme génération
- Arreter d’évoluer s’il n’y a pas d’avancement  
    Utilisation de la **température** : Plus c’est chaud plus ya d’amélioration, plus c’est froid, moins y’en a.

Recherche de comment utiliser la température (Bibliographie)

Schema : schema theorem or fundamental theorem of genetic algorithms => Explique POURQUOI les algos génétiques fonctionnent
  
Fitness fonction sont heuristiques : C’est une approximation / estimation de la réalité

Multiobjective optimisation (notre cas)

# 13/06/2023

Il faut

- Créer le système de score (à faire)
- La sauvegarde des combos (d’abord dans la classe de l’athelete (fait) et ensuite en json avec les données de la partie(à faire))
- Fonction pour faire jouer une partie entière (Fait : doOneGame(iterate, callback))
- Les fonctions pour l’algorithme génétique (fitness etc) (à faire)

# 16/06/2023
**changelog**
- Ajout des commentaires de classe pour l’algo génétique
- Ajout repr Chromosome
- Ajout calc_fitness Athlete Chromosome
- Rename doOneGame → play    
- Fix du deplacement outofbound de l’athlete
- Ajout du paramètre tick à takeAction et du tick aux combos
- Ajout du fonctionnement de l’algo génétique avec le modèle

Comment représenter un Genes ? `[(x,y), fig]` comme les combos

Génération de 100 athlètes
→ Changement chemin et de figures
→ Si changement de chemin, **on regenere aléatoirement**
→ Changement de figure aléatoire sur la case

Score (temporaire)
→ Difficulté + 2 si fig fav

**Mutation actuelle :**
On prend 5 % des athlètes, et on garde une partie de leur combo (on prend les i-eme premieres figures et on regenere la suite aléatoirement) (i choisi aléatoirement)

Premiers run de l’algo : Blocage un score de 96 peut importe le terrain

Explications : On peut pas vraiment faire un nombre infini de combos en 70s donc peut importe le terrain il va trouver l’enchaine des cases/figures à faire pour le maximiser même si à la fin le chemin est diff on a un truc semblable niveau accrobaties (a verifier)

Si je change la durée d’un round, à 80s, on a au max 110 de score (de ce que je vois)

Peut importe la seed de génération aléatoire on semble être bloqué à 96 même après 3millions de générations (on y arrive plus ou moins vite en revanche)

Se pencher sur la température et les différentes methodes de mutations (même si j’en vois pas vrmt d’autres que celle en place)

/!\\ pas de notion d’expérience dans le calcul du score encore ni du nombre d’accrobaties

A faire :
- Sérialisation des informations
- Algorithme glouton
- Traitement des données
- Continuer de lire le livre et en chercher d’autres sur les températures et l’optimisation de mon prgm

Stockage de la population à chaque itération dans la classe GeneticAlgorithm

Sérialisation :
```json
{
	athlete : {
		xp,
		FigureFav (id)
	},
	field : [[Case, Case], [Case, Case]],
	dataGenerations : [
		{
			genes : [[(x,y), FigureId, tick],],
			fitness,
			age,
			size,
		}
	]
}
```

Pour 101199 athlètes (505 itérations de 200 athlètes), on a un fichier de 34mo, voir s’il ne vaut mieux par reduire par au lieu de prendre tous les chromosomes, on prend tous les premiers chromosomes et prend ~10s pour sérialiser toutes les données

Python prend ~234mo de ram

# 23/06/2023
J'essaye de faire mes premiers traitements de ma data avec le fichier `traitement.py`

#### Changelog
- Changement de la façon de stocker les données (on ne stock plus que les 20 meilleurs de chaque générations et non plus tout le monde) 
  Variable `NUMBER_OF_CHROMOSOME_TO_KEEP` pour changer combien on veut en garder par génération
- Création du graphe de la fréquence des figures les plus utilisées
- Enregistrement des images dans le dossier traitement
- Changement du nom des fichiers json de sortie par leurs caractéristiques

![[1_freq.png]]
Premiere image du traitement des données, c'est la fréquence d'utilisation de chaque figure 

Enlever le fait de ne rien faire (do_nothing) ?

Deuxieme schema :
![[1_evol_fitness.png]]
Qui montre l'avancement du score en fonction du nb de générations

![[1_cases.png]]
Sorte de gradiant qui montre a quel point chaque cases est utililisée

J'ai téléchargé deux nouveaux livres sur les algos gloutons (mais c'est pas des vrais search paper donc pas fou faut trouver mieux elo) et sur les algo génétiques

### Trucs à faire
- Algo glouton
- Prendre un vrai terrain [[Notation du score.pdf]]
- Optimisation de l'algo génétic [[Genetic Algorithms in Elixir Solve Problems Using Evolution (Sean Moriarity) (Z-Library).pdf]]
- Un meilleur scorage [[Notation du score.pdf]]
- Refaire le schema des classes [[Classes.canvas|Classes]]
- Faire une grille rectangulaire et non carré
- Ajouter des infos supplémentaires dans le json (informatiosn sur la taille du terrain, sur les paramètres utilisés comme la position initiale et tout)
- Pouvoir faire un tas de mesures et faire une moyenne de tout 
- Moyenne de nombre de combos par partie

