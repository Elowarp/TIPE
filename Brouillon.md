# 26 / 05 / 2023

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

# 27/06/2023

#### Traitement cases 10x15
On peut voir que même après l'ajout d'un terrain bcp plus grand, les cases utilisées ne bougent pas beaucoup et ça reste dans la zone de départ

![[2_cases.png]]
Autres graphes :
![[2_freq.png]]
![[2_evol_fitness.png]]

On aurait pas un biais des stats ? en mode on va avoir jsp cb de corks mais c'est pcq on a jsp cb de fois le même parent qui a fait un cork et qui a donné naissance a d'autres golmon de gosses

1 milliard de générations = 7.8Go de ram, c'est pas viable donc faudrait voir pour faire une interface ou faire une sauvegarde temporaire tous les x générations dans un json pour vider la ram

Utiliser de la quantization ? 
> **Quantization**, in mathematics and [digital signal processing](https://en.wikipedia.org/wiki/Digital_signal_processing "Digital signal processing"), is the process of mapping input values from a large set (often a continuous set) to output values in a (countable) smaller set, often with a finite [number of elements](https://en.wikipedia.org/wiki/Cardinality "Cardinality"). [Rounding](https://en.wikipedia.org/wiki/Rounding "Rounding") and [truncation](https://en.wikipedia.org/wiki/Truncation "Truncation") are typical examples of quantization processes. (Wikipédia)

> If one does not know the initial search region, there must be enough diversity in the initial population to explore a reasonably sized variable space before focusing on the most promising regions

Positions de départ, milieu de map ?

The traditional handwaving proof of convergence for the binary GA is called the schema theorem

Changer la terminaison par une détection de variation 

Commencer d'un point différent de la carte pour chaque athlète (est ce que c'est le cas des vrais competitions ?)
Uniforme sampling 
La mutation est pas opti mais comment jpeux faire mieux ?

Fonction d'arret : Si le score max n'a pas été changé depuis au moins 5k générations, on stop 

#### Score 
Ya 6 juges pour 3 par critères, chaque critère vaut au maximum 15pts (donc un total de 30 pts max) :
- Execution
	- Surete 
		-  Surete : Enlever 1 pt pour de grosses erreurs, et 1/2 pour les plus petite (Mauvais attérissage, vitesse et le fait des froler les obstacles/gens)(Nb de pts de départ 3pts, max 3)
		- Presentation : Ajouter 1pt pour avoir prit du mobilier (utiliser une barre par ex)(Nb pts départ :0 max 2)
	- Flow
		- Flow : Enlever un point a chaque fois qu'on s'arrete completement, un demi point si on marchouille un peu (Nb pts départ : 3 max 3)
		- Connexion : Ajouter un demi/complet point pour le nb d'elements liés avec la liste de référence (Table des tricks changeant toutes les années) (Nb depart 0 max 2)
	- Course
		- Parts : Ajouter un point pour chaque parties définies où l'athlète fait un trick (Nb depart 0 max 3)
		- Types : Ajouter un demi point pour chaque trick fait en intéraction avec le sol, un rebord, une bar ou un mur (Nb depart 0 max 2)
- Difficulté
	- Trick
		- Table des tricks : Scoring accordé à une liste de référence, le score attribué au trick est au depart celui de la feuille avec un potentiel plus en fct de l'endroit fait. Lier 2 mouv entraine l'ajout du score de 2 mouv liés (Nb depart 0 max 5)
	- Run
		- Placement : Ajouter un point pour un trick fait au debut du run, au milieu et a la fin du run(Nb de depart 0 max 3)
		- Temps : Ajouter un demi point pour la longueur du run selon la liste reference(Nb depart 0 max 2)
	- Variete
		- Variete : Ajoute un demi point pour un trick fait en dehors de la category de parlour classic, rotations forward, rotation sideways, rotation backwards, twist, spin (Nb depart 0 max 3)
		- Technique : Ajouter un point ou demi pour la qualité technique de l'élément clé comme une montée ou un twists (Nb depart 0 max 2)

### Done
- Refont du diagramme de classe
- Ajout d'un terrain de 10x15 et de son traitement (10 par 15m c'est qui est pas déconnant)
- Nouvelle fonction d'arret qui s'arrete des que ça fait 5000 générations qu'on a pas touché au résultat

### To do:
- Evaluer la complexité de mes fonctions
- Algo glouton
- Optimisation de l'algo génétic [[Genetic Algorithms in Elixir Solve Problems Using Evolution (Sean Moriarity) (Z-Library).pdf]]
- Un meilleur scorage [[Notation du score.pdf]]
- Ajouter des infos supplémentaires dans le json (informatiosn sur la taille du terrain, sur les paramètres utilisés comme la position initiale et tout)
- Pouvoir faire un tas de mesures et faire une moyenne de tout 
- Moyenne de nombre de combos par partie

# 28/06/2023
Concentration maximale sur le score

Pour modéliser les passements, chaque combo différent on fait un passement (soit 0.5 pts de plus ?)

Longueur d'un run = temps écoulé entre deux arrets/courses ou deux accros sols (vaut pour les connexions entre figures)
Surete aléatoire (no peut louper une fig sans faire expres, mais chances moindre si cest notre fig pref)
Ajout d'un demi point pour si on fait un tricks rare (donc distribution de probabilité ?)
Ajout du nb de points associée 
Version homme femme ?

`Complexity` d'une figure devient les points initiaux associés par la table des tricks

Ajout des figures suivantes : 
```python
FIGURES = {

"do_nothing": Figure("do_nothing", 1, 0), # Ne rien faire pendant 1s
"run": Figure("run", 1, 0), # Courir pendant 1s
"jump": Figure("jump", 1, 0), # Sauter pendant 1s

"180": Figure("180", 1, 0.5), # Faire un 180 pendant 1s
"frontflip": Figure("frontflip", 1, 0.5), # Faire un frontflip pendant 1s
"backflip": Figure("backflip", 1, 0.5), # Faire un backflip pendant 1s
"gaet_flip": Figure("gaet_flip", 1, 0.5), # Faire un gaet flip (back en appui sur un coin de mur) pendant 1s

"cork": Figure("360", 1, 1), # Faire un cork pendant 1s
"cast_backflip": Figure("cast_backflip", 1, 1), # Faire un cast backflip (backflip en appui sur un mur) pendant 1s
"inward_flip": Figure("inward_flip", 1, 1), # Faire un inward flip (front qui te fait reculer) pendant 1s

"540": Figure("540", 1, 1.5), # Faire un 540 pendant 1s

"double_cork": Figure("double_cork", 2, 2), # Faire un double cork
"kong_gainer": Figure("kong_gainer", 1, 2), # Faire un kong gainer

"cast_backflip": Figure("cast_backflip", 2, 2.5), # Faire un cast backflip 360

"double_swing_gainer": Figure("double_swing_gainer", 2, 3), # back sur une barre

"double_front": Figure("double_front", 2, 4), # Faire un double front
"double_back": Figure("double_back", 2, 4), # Faire un double back

"double_flip_360": Figure("double_flip_360", 2, 4.5), # Faire un double flip 360
}
```

Résultat de l'ajout de toutes les figures sans changer la façon de noter :

![[Code/images/1er load des 15 figures/cases.png]]
![[Code/images/1er load des 15 figures/evol_fitness.png]]
![[Code/images/1er load des 15 figures/freq.png]]

Ajouter 15 figures a fait faire 1Milliards d'athlètes (~8000 générations) et un fichier de 100mo

On peut calculer le nombre de possibilité de combinaison (drole)

>[!caution] 
>protentiel probleme avec le fait qu'on reste sur les mêmes chemins a partir du moment ou on atteint le pic de score

Maintenant va pour le meilleur scoring
Tout ce qui est impossible a modeliser on fait jouer un `randint` ou `weightes_random` qui est un random avec plus de chance d'obtenir le haut de panier que le bas (ou l'inverse)

>[!info] Première exécution
> On a une alternance entre 60, 61 et 62.5, ce que fait que le programme ne s'arretera jamais, de plus, la fonction ne marche plus, il faudrait faire quelque chose qui detecte le mouvement, comme une dérivée
> Fun fact le max de score c'est 30, on a le double. Et le temps d'exécution pour parvenir a 1milliards d'athlète à facilement tripellé voir quadrupelé 

>[!info] Deuxieme execution
>Au final l'algorithme s'arrête, vu que c'est l'atteinte d'un max, si on ne tape pas plus haut que le max pendant 5000 generations alors il s'arrete qd meme

Traitement de la deuxieme execution :
![[Code/images/1 Generation avec nv scoring/cases.png]]
![[Code/images/1 Generation avec nv scoring/evol_fitness.png]]
![[Code/images/1 Generation avec nv scoring/freq.png]]

### Generation avec un athlète d'xp = 2
![[Code/images/2XP/cases.png]]
![[Code/images/2XP/evol_fitness.png]]
![[Code/images/2XP/freq.png]]
### Generation avec xp=10
![[Code/images/10XP/cases.png]]
![[Code/images/10XP/evol_fitness.png]]
![[Code/images/10XP/freq.png]]
Ce qu'on voit surtout c'est l'invariance des résultats quasiment malgré le fait que le niveau soit très bas

> [!info] Conclusion :
>  l'exprerience n'affecte en rien la technique utilisé pour gagner, elle influence que de peu le score 
Ainsi on voit qu'il y a changement à faire (je pense au niveau de l'enchainement des passements) et potentiellement TROP d'aléatoire

De plus si on regarde les images pour une mutation  de resp 3 et 7% on obtient les mêmes resultats (diff de 0.02 de moyenne) sauf pour l'utilisation des cases
![[Code/images/mutation 3%/cases.png]]
![[Code/images/mutation 7%/cases.png]]

J'ai une trop grosse convergence des cas, fin, un algo trop généralisé et je peux rien trop en tirer pour l'instant

### To do:
- Baisser le taux d'aléatoire et faire un lock (pas de grosses acrobaties pour les petits niveaux)
- Evaluer la complexité de mes fonctions
- Ajouter des infos supplémentaires dans le json (informatiosn sur les paramètres utilisés comme la position initiale, la mutation, etc)
- Pouvoir faire un tas de mesures et faire une moyenne de tout 
- Moyenne de nombre de combos par partie
- Nombre de combinaisons possibles
- Faire un vrai terrain

# 29/06/2023
On va instaurer un niveau minimal pour effectuer chaque figure
Pour se faire, on peut faire toutes les figures de complexité inférieure strictement au niveau de l'athlète/2 (pour avoir des valeurs entre 0 et 5)

> [!caution] 
> Est ce qu'il y a un pb avec le fait de prendre les meilleurs a chaque tour sachant qu'on loupe toujours le maximum au final?

Après ajout du niveau minimal par figure, on remarque que le jump est toujours la figure la plus utilisée (pour tous les niveaux), 25% pour les 3xp et 10% pour les 10xp

On obtient très vite une convergence des points vers des chiffres entre 20 et 30 pour tous les niveaux

> [!info] Changement de la seed (2207 -> 12)
> On voit surtout un gros changement sur les figures utilisées et les cases parcourues mais une différence de 0.01 sur la moyenne pour un même niveau :

Seed: 12
![[Code/images/8XP SEED 12/cases.png]]
![[Code/images/8XP SEED 12/evol_fitness.png]]
![[Code/images/8XP SEED 12/freq.png]]

Seed 2207 :
![[Code/images/8XP SEED 2207/cases.png]]
![[Code/images/8XP SEED 2207/evol_fitness.png]]
![[Code/images/8XP SEED 2207/freq.png]]


### Done:
- Tri de l'histogramme par ordre lexicographique
- Baisse du nombre de générations après la valeur maximale (5000 -> 1000) 
- Changement de la seed (2207 -> 12)
- Temps réel par figure (chronométré a la shlag via ytb)
- Changement du graphe de l'evolution de la fitness par un graphe montrant la fitness maximal, la moyenne par génération, la moyenne et le score total

### To do:
- Ajouter le champ variété par figure pour coller avec la table de jugement des juges
- Faire démarrer les athlètes avec des chemins tous différents
- Evaluer la complexité de mes fonctions
- Ajouter des infos supplémentaires dans le json (informations sur les paramètres utilisés comme la position initiale, la mutation, etc)
- Pouvoir faire un tas de simulations et faire les graphes de toutes les générations
- Trouver le chemin utilisé pour avoir le meilleur score
- Moyenne de nombre de combos par partie
- Nombre de combinaisons possibles
- Faire un vrai terrain
- Faire un graphe de l’évolution de la fitness (z) par l’évolution de l'xp (x) 

# 30/06/2023
Bon j'ai un peu troll je sais que j'ai pas tout noté mais en gros j'ai fait :
### Done:
- Suppression d'une part d'aléatoire dans le scoring => Convergence en 7 générations => Nul.
- Changement complet de l'affichage des cases pour integrer les chemin suivit par l'athlète directement sur le dessin
- Création du premier diapo
- Application d'un terrain fixe (même si géné aléatoirement au debut)
- Suppression de l'aléatoire pour que le score soit de plus en plus corréler avec le niveau du joueur 
- Exportation des certaines fonctions / constantes dans des fichiers réservés
- Ajout de `POPULATION_NUMBER`, `NUMBER_OF_CHROMOSOME_TO_KEEP`, `MUTATION_RATE`, `NUMBER_OF_GENERATIONS` et `InitialPosition` au JSON
- Ajout de la fonctionnalité de faire plusieurs exécutions de l'algo génétique (en l'occurrence `ITERATION_NUMBER` fois) et de créer directement les graphiques associés (40s pour 10 exécutions de l'algo dont les générations d'images)
- Ajout de la création des images de plusieurs simulations en même temps (en mode moyenne de 10 simulations) /!\\ j'ai un pb avec les moyennes de scoring, faudrait faire ca a tete reposé 

Terrain : 
```python
[[0, 0, 0, 0, 2, 1, 1, 0, 1, 0], [1, 2, 2, 0, 2, 0, 2, 1, 0, 1], [2, 0, 0, 1, 0, 1, 2, 0, 2, 2], [1, 1, 2, 0, 0, 1, 2, 1, 2, 1], [2, 1, 1, 0, 1, 0, 0, 0, 2, 2], [2, 0, 1, 1, 2, 2, 0, 2, 0, 0], [1, 1, 0, 0, 1, 2, 2, 1, 0, 2], [0, 1, 2, 1, 2, 2, 1, 1, 1, 2], [2, 0, 0, 2, 0, 0, 1, 0, 1, 1], [1, 0, 0, 1, 2, 2, 1, 0, 0, 1], [1, 2, 1, 0, 2, 0, 0, 0, 0, 1], [1, 1, 2, 2, 1, 0, 2, 1, 0, 1], [1, 2, 1, 0, 1, 1, 1, 1, 0, 0], [1, 0, 1, 2, 0, 2, 1, 2, 2, 1], [2, 0, 2, 2, 1, 2, 0, 0, 0, 0]]
```

>[!info] Ce que je retiens
>En gros, on a une convergence très rapide, on a 1 premier athlète qui va se trouver bien bas et en prenant directement les meilleurs, on peut pas vraiment les faire se surpasser, il y a la prédominance du niveau de l'athlète (ce qui est logique) mais aucun chemin n'est a privilégié de ce que je vois 

![[Code/images/Changement Score relation lvl/freq.png]]
![[Code/images/Changement Score relation lvl/cases.png]]
![[Code/images/Changement Score relation lvl/evol_fitness.png]]

Entre deux générations différentes, on a des fréquences de figures hyper différentes mais une moyenne toujours identiques (quasiment)

Logique d'avoir une stagnation de score, mon algorithme cherche le meilleur athlète, donc celui avec le meilleur score donc une fois qu'il a trouvé son poulain super fort bah c'est tout il a fini

Je pense baisser encore les locks des figures genre 2xp tu peux faire 3 figures grand grand max

Peut être ne pas compter RUN dans le total des freq pcq c'est pas une figure c''est un lien entre les figures 

Ce qui serait vraiment bien ça serait de faire 10-20 générations pour pouvoir se rendre compte de toutes les valeurs (Fait)

### To do:
- Ajouter le champ variété par figure pour coller avec la table de jugement des juges
- Faire démarrer les athlètes avec des chemins tous différents
- Evaluer la complexité de mes fonctions
- Trouver le chemin utilisé pour avoir le meilleur score
- Moyenne de nombre de combos par partie
- Nombre de combinaisons possibles
- Faire un vrai terrain
- Faire un graphe de l’évolution de la fitness (z) par l’évolution de l'xp (x) 
# 01/07/2023
### Done:
- Multi-traitement et application directe après exécution de l'algo
![[Code/images/Images multi générations/cases.png]]
![[Code/images/Images multi générations/evol_fitness.png]]
![[Code/images/Images multi générations/freq.png]]
# 07/07/2023
### Todo:
- Ajouter toutes les figures mêmes non faites (freqs) (Done)
- Faire une legende avec toutes les figures et ses informations
- Pourquoi ya des valeurs qui sautent dans les générations (Done)

OK JE CROIS JAI REUSSI A AVOIR UN SCORE QUI EST EN ACCORD AVEC LA VIE REELLE

![[Code/images/Image scoring réelle/freq.png]]
![[Code/images/Image scoring réelle/evol_fitness.png]]
![[Code/images/Image scoring réelle/cases.png]]

>[!warning] Pique descendant
>Les piques descendants sont en fait du à une blessure !

Et 0 influence de la figure pref

seed 20 -> 24

### To do:
- Ajouter le champ variété par figure pour coller avec la table de jugement des juges (a voir)
- Faire démarrer les athlètes avec des chemins tous différents
- Evaluer la complexité de mes fonctions
- Moyenne de nombre de combos par partie
- Nombre de combinaisons possibles
- Faire un vrai terrain
- Faire un graphe de l’évolution de la fitness (z) par l’évolution de l'xp (x) 
-  Faire une légende avec toutes les figures et ses informations

# 10/08/2023
Légende des termes : 
> **Génération** : Le nombre de tour de boucle de l'algorithme génétique effectué (dépend de la partie en cours)
> **Fitness** : Le score attribué à chaque athlète
> **Exécutions** : Nombre de fois que l'on a commencé puis terminé une partie (dépend de la constante `ITERATION_NUMBER`)

### To do:
- Ajouter le champ variété par figure pour coller avec la table de jugement des juges (a voir)
- Faire démarrer les athlètes avec des chemins tous différents
- Evaluer la complexité de mes fonctions
- Moyenne de nombre de combos par partie
- Nombre de combinaisons possibles
- Faire un vrai terrain
- Faire un graphe de l’évolution de la fitness (z) par l’évolution de l'xp (x) 
-  Faire une légende avec toutes les figures et ses informations (et l'inclure dans un subplot a 4 cases)
- Changer les print en logging 
# 15/08/23
> [!error] Une echelle pour le score ??????? comment jpeux mesurer rien du tout si je nai meme pas de référence  

### Done
- Ajout de l'image constantes
- Changement des print en logging

### To Do (Important)
- Refaire le terrain de Sofia (Bulgarie) (Chiant mais pas si long 10mn max)
- Coder le parkour de Lilou Ruel (Chiant++ et moyen long 20mn max)
- Faire les diapos (cv 40mn max)

# 27/08/23
Seule vidéo du passage de lilou : https://www.youtube.com/watch?v=ubQ1w7awah8 (19:50)
Dimensions terrain : [[2021_PK_Workplan_Sofia.pdf]] (40 x 10m)

### Done
- Création du terrain de Sofia 
- Adaptation des images au nv terrain 
### To do
- Parcours Lilou
- Diapos
- Systeme de score

# 29/08/23
Recommencement du système des scores : [[Code pointage 2019-2021.pdf]]
### Infos extraites :
- Choix de l'athlète pour le départ
- Max 70s de passage, moins est autorisé
- Maximum de 30 pts, possibilité de donner des demis points
- Facon de noter :
	- Exécution 
		- Sécurité (max 3)
		- Fluidité  (max 3)
		- Maitrise (max 4)
	- Composition
		- Utilisation de l'espace (max 3)
		- Utilisation des obstacles (max 3)
		- Connections (max 4)
	- Difficulté
		- Variété (max 3)
		- Éléments individuels (max 3)
		- L'ensemble de la course (max 4)

### Done :
- Changement du scoring

### Issues:
- Cette façon de considérer le score fait grimper en flèche le fait de courir et non pas d'utiliser le plus l'environnement

# 30/08/23
Reproduction du parkour de Lilou -> Premier essaie a la zob : le systeme de score est plutot bon on a un delta de 3pts

Un des problemes c'est le 1s pour faire 1m qui n'est pas réaliste et qui joue dans le score et nombre de figures faites sur le terrain 

Comparaison du score moyen obtenu par un athlete de même xp que Lilou (8xp) qui commence au même endroit qu'elle (30 executions)

Véritable score (Total 21):
- E : 5.5
- C : 7.0
- D : 8.5

Score lilou (Total 17.8):
- E : 8.6
- C : 5.2
- D : 4

Générations (30-08-2023 16h31m49s):
![[Code/images/Génération comparaison lilou/constantes.png]]
![[Code/images/Génération comparaison lilou/freq&fitness.png]]
![[Code/images/Génération comparaison lilou/cases.png]]


Rmq : 
- Sur le score en lui même on a bien des différences sur le traitement ce qui montre un problème sur la notation et que le total soit "proche" du vrai résultat relève plus de la chance que d'autre chose 
- On voit que par rapport au véritable parcours de Lilou, le progm est bien plus restreint sur lui même -> Possibilité d'amélioration faire des demi-ticks (0.5s) et passer le saut et la course en demi tick on aurait donc plus de facilité a représenter la vraie course de Lilou
- A-t-on atteint les limites ? A cause du facteur humain assez présent dans le système de notation, et de l'infinité des figures possibles on se retrouve avec ces résultats quand même interprétables mais pas aussi bien applicable à la réalité qu'on le voudrait
### Done
- Ajout du fichier des combos customs
- Externalisation du terrain de Sofia

Comment j'organise le diapo ?
1. Définitions / Explication du sujet
2. Ma solution
	1. Utilisation de python
	2. Algorithme génétique
	3. Le modèle utilisé 
		1. cad la représentation que j'ai choisi
3. L'histoire
	1. D'abord fait x générations
	2. Trompé d'année pour faire mes comparaisons
	3. Récupérations des données via vidéo/informations trouvable sur internet
	4. Comparaison de ce que j'ai fait et de la représentation de la réalité via mon programme
4. Le problème
	1. Ca colle pas si bien à la réalité
	2. Trop d'humanité dans le système de score
	3. Infinité des figures
	4. Aléatoire
5. La conclusion
	1. On peut se rapprocher (et encore faudrait tester avec une deuxieme athlete) de la réalité mais on ne peut malheureusement pas sortir du programme une technique infaillible pour gagner. Malgré les problèmes, on note que on sent dans ces données que ce qui prime le plus c'est de ne pas aller trop loin, et de changer bcp de type de mobilier (notamment pour les figures utilisant des bouts de murs) ce qui n'est pas trop éloigné de la réalité 
6. Bibliographie

# 19/09/2023
Recherche d'un nouvel algorithme pour résoudre mon problème
- [A*](https://fr.wikipedia.org/wiki/Algorithme_A*)
	- Problème de l'algorithme : Impossible d'évaluer en temps réelle la totalité du score avant d'avoir atteint la fin, ce qui reviendrait à un parcours en force brute de toutes les possibilités
- [Métaheuristique](https://fr.wikipedia.org/wiki/M%C3%A9taheuristique) est un type de programmation pour résoudre des pb qui s'inspire de la vie
	- [Recuit Simulé](https://fr.wikipedia.org/wiki/Recuit_simul%C3%A9)(Ou Simulated Annealing)
		- [[Simulated Annealing and Boltzmann Machines A Stochastic Approach to Combinatorial Optimization and Neural Computing (Emile H. L. Aarts, Jan Korst) (Z-Library).pdf]]
		- Probablement celui voulu

# 26/09/23
- Faut expliquer PQ le score il marche pas bien
- Pq j'ai choisi le génétique à la place du recuit ou quoi 
# 03/10/23
Pourquoi le score pose problème ? 
- La façon de calculer le score : [[Code pointage 2019-2021.pdf]] ne se prête pas à la recherche d'une heuristique ou d'un plus court chemin. Le score est calculé sur un parcours total et non par partie (en tout cas pour la majorité)
- La façon de juger : Hyper subjectif et impossible à faire dans le modèle étudié. La seule façon trouvée pour le prendre en compte : soit de l'aléatoire pondéré soit un coefficient de proportionnalité avec le niveau de l'athlète

Répercussions sur les algorithmes possibles :
- Impossible d'utiliser des algorithmes avec heuristiques (= l'art d'inventer, de faire des découvertes en résolvant des problèmes à partir de connaissances incomplètes) car impossible de connaitre le score avant la fin d'une run
- Recherche alors tourné vers les algorithmes Métaheuristique (=résoudre des pb d'optimisation difficile pour lequel les méthodes classiques ne marchent pas), on veut pas la meilleure solution mais une solution approchée pour pouvoir ensuite en déduire des façon d'agir
	- Les algorithmes stochastiques(=apprendre les caractéristiques d’un problème afin d’en trouver une approximation de la meilleure solution)
		- Algorithme génétique (à population)
			- L’algorithme sera considéré comme faisant partie de la classe des algorithmes évolutionnaires s’il manipule une population _via_ des _opérateurs_, selon un algorithme général donné. ![Wikipedia](https://fr.wikipedia.org/wiki/M%C3%A9taheuristique#%C3%89volutionnaire_ou_non) 
			- S'inspire de la théorie de l'évolution pour résoudre des pb divers
		- Algorithme du recuit (à population) X
			- Dans cette classification, le recuit simulé occupe une place particulière, puisqu’on peut considérer qu’il échantillonne la fonction objectif en utilisant directement celle-ci comme distribution de probabilité (les meilleures solutions ayant une probabilité plus grande d’être tirées). Il n’est donc ni explicite ni implicite, mais plutôt « direct ». ![Wikipédia](https://fr.wikipedia.org/wiki/M%C3%A9taheuristique#Implicite,_explicite,_directe) 
		- Colonie de fourmis (à population) X
			- Résolution du pb du voyageur du commerce. Possibilité de l'utiliser car un chemin = une run et les run d'après utilisent ces mêmes runs pour faire de meilleurs scores
			- "En effet, dans les problèmes combinatoires, il est possible que la meilleure solution finisse par être trouvée, alors même qu’aucune fourmi ne l’aura éprouvée effectivement. Ainsi, dans l’exemple du problème du voyageur de commerce, il n’est pas nécessaire qu’une fourmi parcoure effectivement le chemin le plus court : celui-ci peut être construit à partir des segments les plus renforcés des meilleures solutions. **Cependant, cette définition peut poser problème dans le cas des problèmes à variables réelles, où aucune structure du voisinage n’existe.**" ![Wikipédia](https://fr.wikipedia.org/wiki/Algorithme_de_colonies_de_fourmis#Une_d%C3%A9finition_difficile) 
			- Problème avec la continuité des runs ?
		- GRASP
			- Création d'un chemin et modification petit à petit de ce chemin pour trouver le meilleur chemin (glouton + aléatoire)
			- Problème de la continuité a travers le voisinage
			- [[Optimization by GRASP Greedy Randomized Adaptive Search Procedures (Mauricio G.C. Resende, Celso C. Ribeiro (auth.)) (Z-Library).pdf]]

# 17/10/2023
## Plan d'attaque 
1. Définitions / Explication du sujet
2. Ma solution
	1. Utilisation de python
	2. Algorithme génétique
	3. Le modèle utilisé 
		1. cad la représentation que j'ai choisi
3. L'histoire
	1. D'abord fait x générations
	2. Trompé d'année pour faire mes comparaisons
	3. Récupérations des données via vidéo/informations trouvable sur internet
	4. Comparaison de ce que j'ai fait et de la représentation de la réalité via mon programme
4. Le problème
	1. Ca colle pas si bien à la réalité
	2. Trop d'humanité dans le système de score
	3. Infinité des figures
	4. Aléatoire
5. La conclusion
	1. On peut se rapprocher (et encore faudrait tester avec une deuxieme athlete) de la réalité mais on ne peut malheureusement pas sortir du programme une technique infaillible pour gagner. Malgré les problèmes, on note que on sent dans ces données que ce qui prime le plus c'est de ne pas aller trop loin, et de changer bcp de type de mobilier (notamment pour les figures utilisant des bouts de murs) ce qui n'est pas trop éloigné de la réalité 
6. Bibliographie

1. Introduction
	1. Définitions utiles
		1. Traceurs
		2. Compétition
	2. Problème posé : Comment améliorer ses chances de gagner une compétition de parkour ?
		1. Résolution grâce à un modèle informatique
2. Explication du modèle et des solutions
	1. Modélisation de la réalité
		1. Classes
		2. Discrétisation du temps
	2. Algorithme génétique
		1. Fonctionnement d'un algorithme génétique
		2. Application à notre problème
		3. Question du scoring 
			1. Comment noter le score ?
			2. Comment appliquer cette notation dans le modèle ?
			3. Les gros problèmes de cette façon de noter
				1. L'appréciation des juges
				2. Mouvements individuels
	3. Résultats
		1. Avoir des résultats c'est bien, pouvoir le comparer à quelque chose de concret c'est MIEUX !
			1. Introduction de Lilou Ruel
			2. Implémentation de son parcours dans le programme 
				1. Problèmes rencontrés
		2. Interprétation des résultats

# 28-11-23

Changement de plan !

On utilise l'algo génétique en tant que sujet d'étude et le parkour n'est qu'une application 

Il faut essayer de trouver des liens entres les parametres qu'on modifie et des papiers/recherches/etudes

Voir les liens entre beauté/technicité etc

Voir les statistiques que les points obtenues en fonctoin des classes de points 

S'orienter vers les stats et l'algo génétique pour avoir un bon TIPE

https://www.sciencedirect.com/science/article/pii/S0304397500004060?via%3Dihub

# 5-12-23

Lecture du lien précédent [[Theorry_Genetics.pdf]]

Chaines de markov inhomogène (= en temps, seulement faisable en simulation informatique)

> The crossover operation combined with fitness selection under no mutation shows a convergence effect for the algorithm, called genetic drift, which is not ergodic in nature, i.e., depends upon the initial population. See Section 7.5.

> The crossover operation does not play a signi5cant role in the asymptotic behavior of genetic algorithms, if the mutation rate stays positive and5tness scalings such as unbounded power-law scaling are used. See Theorem 8.3.

FAIRE AtTENTIOB AUX CROSSOVER (imgage telephone)

# 12-12-23

Mutation : force principale dans la phase de génération aléatoire d'un algorithme génétique

Etude d'une grande variété de tests avec une grande mutation 
https://link.springer.com/chapter/10.1007/3-540-61723-X_994

OK 
Faudra dire que l'on a fait comme les premiers documents, très peu de mutation et surtout un crossover, on va changer le crossover pour voir ce qu'il donne après, et ensuite tester une grande mutation 

> GP is plagued by premature convergence. That is, GP populations often lose their ability to evolve before the problem is solved. Increasing the mutation rate makes the runs continue to evolve for about twice as long (Table 6)that is, a high mutation run maintans its ability to evolve for longer.

J'ai mis la premiere version dans chromosomeV1 et je vais mettre la suivante suivant la photo dans chromosome V2

les choses a changer : la mutation le crossover et la facon de repr

Premiers tests avec Iteration à 10 pour un versus entre les deux représentations :
Aucun changement niveau mutation et crossover niveau code, seulement repr des genes

V1 execution 8xp 12-12-2023 16h39m20s
	1m10 d'exécution + voir images

V2 execution 8xp 12-12-2023 22h21h34s
	1m47 d'exécutions + images similaires

bon c'est pas mieux niveau perf

/!\ Suppression du cas où l'athlète se blesse qui été basé sur aucune donnée

# 19-12-2023

> Put the crossover operation in proper perspective by showing:
> ◦ The crossover operation assists mutation in the random generator phase of the algorithm by adding to the contraction process over the state space S. See Theorem 6.1.
> ◦ The crossover operation *does not play* a significant role in the asymptotic behavior of genetic algorithms, if the mutation rate stays positive and fitness scalings such as unbounded power-law scaling are used. See Theorem 8.3.

Theory de la génétique

On a une étude qui nous dit que le crossover EST le facteur le plus important (cf abstract et introduction) et donc étudie surtout la mutation pour voir réelle l'effet et une theory de la génétique qui lui prouve que le crossover n'est pas un facteur prédominant selon certaines conditions

C'est quoi le crossover :

- Prends 2 chemins
- On détecte 2 points communs et on swap les chemins entre ces deux là

Score lilou avec le nouveau systeme :

```text
{'execution': {'safety': 2.4, 'flow': 3, 'mastery': 3.2}, 'composition': {'use_of_space': 1.0, 'use_of_obstacles': 1.0, 'connection': 3.2}, 'difficulty': {'variety': 1.0, 'single_trick': 0, 'whole_run': 4}}
18.8
```

## TODO

- Création d'un Protocole
- Execution du protocole
- Comparaison avec les données de l'étude

# 24-12-2023

Nouvelle problématique : Dans quelle mesure la mutation affecte-elle les solutions obtenues par un algorithme génétique par rapport aux croisements intergénérationnels, cela observée à travers l'exemple d'une compétition de  parkour ?

## Présentation

### Modèle / Hypothèse

#### C'est quoi le parkour

#### C'est quoi une compétition de parkour

#### Comment on la représente

#### Pourquoi avoir choisi l'algorithme génétique / Description de celui ci

Problème de la notation

#### But final

Comparer les résultats que j'aurai obtenu à l'étude que j'ai choisie

### Paramètres / données dont tu as besoin et pourquoi celles-ci

#### Choix des figures

#### Explication de la récolte du temps moyen de chaque figure

#### Paramètre propre à l'étude (hypothèses utilisées)

- Pour garder le nombre d'individus évolué pair entre la mutation et la crossover, on fait soit un crossover soit une mutation sur 2 individus à chaque fois qu'une opération génétique est faite
- Dataset ??? Pas compris
- Taille de la population 3000
- Selection par tournois
- Taille maximale par individus 256 instructions contre le nb de coup possible en 70s
- Nombre total de run 10 aavec des seeds diff pour chaque paramètre
- Variation de la mutation 5-20-50-80%

- Notation de la fitness forcement différente entre l'étude et notre pb dû aux diff intrinsèque du problème
- Généralisation avec entrainement/tests
- Terminaison critère

/!\ Le papier

### Premiers résultats avec et sans crossover et les paramètres recommandées en général

#### Comparaison avec un résultat en conditions réelles (Lilou Ruel)

### Modification des paramètres selon l'étude

### Analyse des données récoltées et confrontation avec les résultats de l'étude

### Conclusion sur l'efficaticé de la mutation par rapport au crossover, ouverture sur les limites de ce modèle donnée par une dernière étude (théorie de l'algorithme génétique)

# 30-12-2023

On change de papier pcq l'autre est pas bon :
https://www.egr.msu.edu/~kdeb/papers/k99003.pdf

> Since the overall time to run a GA is more or less proportional to the number of function evaluations used, we set the number of function evaluations fixed for  all the GA runs. When such a bound on function evaluations is desired for comparing different GAs, most earlier GA parameter studies are not applicable, because in these cases GAs were run till complete population convergence. We feel that this study of comparing performance of different GAs for a fixed number of function evaluations is practical and useful from GA’s applicability in real-world scenarios

Ce qui nous correspond : "Massive Multimodal" fonction vu qu'on a pas UN unique parcours qui amene au meilleur score

Leur fonction est hyper bonne : y faire un commentaire

### Les paramètres

#### Selection

Mating : Selection des parents qu'on va faire reproduire
Crossover : Single point crossover (Ce qui est déjà le cas avec moi) probabilité pc
Mutation clock operator : Impossible a mettre en place avec notre forme de mutation

50 populations differentes de départ
Zeta = La mersure de performance : Proportion de réussite le l'algo génétique d'obtenir un score proche de epsilon d'un score référence attribué comme score parfait

S = nombre max d'execution de la fonction d'évaluation
N = taille de la population
T= S/N nombre de générations écoulées
U = 1 - F/S = Proportion de fonction evaluation non utilisé (F le nombre de fonction d'évaluation utilisée)

Solution au problème ?
Comparaison au score maximal possible à avoir en fonction de l'exp 
Calcule donne :
$$M_{xp} =  3*xp/10 + 3 +4*xp/10 + 3 + 3 + 4*xp/10 + 3 + 3 + 4*xp/10 = 15 + 15*xp/10$$

Soit pour une xp de 8 : 27

/!\ Changement du scoring parce que des choses ne collait pas avec le reglement et changement en demi seconde
Donc Lilou à maintenant un score de 25/30 comparé à 23/30 irl
Et le max pour un gars avec une xp de 8 : 27

Donc mon epsilon interval c'est +-0.5 autour de $M_{xp}$

Multimodal pcq plusieurs solutions pour un résultat maximum

# 21/02/24
Voir pour tout mettre en str

# 19/03/24
Mutation 20% par Practical Genetic Algorithm
Crossover 100% idem 

Réécriture de la mutation et du croisement selon les strings

TODO : Trouver pq bug avec x out of range 
Reduire la taille des fichiers en adaptant les nom json à un dictionnaire
Trouver pq gros pic à la fin

# 26/03/24

Description du json :

```json
{
    dataGenerations: {
        [
            {
                genes: str
                fitness: float
                detailedFitness : {
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
                age: int,
                size: int,
            }
        ],
        ...
    }
}
```

Into (Suppression de detailedFitness qui n'est pas utilisée)

```json
{
    dataGenerations: {
        [
            {
                g: str
                f: float
                a: int,
                s: int,
            },
            ...
        ]
    }
}
```

Nom de fichier de celui qui a réussi : 27-03-2024 11h42m15s

# 02 / 04 / 2024

https://www.egr.msu.edu/~kdeb/papers/k2012016.pdf

La mutation "mutation clock" est la mutation utilisé pour faire l'étude, donc il faudrait l'implémenter pour voir en fait comment eux ils le font