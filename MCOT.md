# Algorithme génétique : Etude des performances par l'exemple du Parkour

Le Parkour est un sport qui a acquis une popularité mondiale durant les dernières années, il met en avant la maîtrise de son corps dans des environnements urbains divers et variés. Différents types de compétitions existent et étudier le comportement d'un algorithme informatique pour maximiser le score attribué au parcours effectué par des athlètes semble correspondre parfaitement à la thématique de cette année.

Nous étudierons les effets sur l'algorithme génétique et les répercussions sur les scores théoriques obtenues suite aux différents enchaînements de figures effectués selon la variation de différents paramètres comme la taille de la population et les probabilités de mutation et de croisement.

## Positionnement thématique

INFORMATIQUE PRATIQUE (Algorithmes génétiques) ;  *INFORMATIQUE* THÉORIQUE (Algorithmique) ;

## Mots clés

- Algorithme génétique
- Parkour
- Mutation
- Croisement
- Opitimisation

## Key-Words

- Genetic Algorithm
- Parkour
- Mutation
- Crossover
- Optimization

## Problématique retenue
Quel est l'impact des probabilités de mutations et de croisements sur un algorithme génétique pour l'optimisation d'un enchaînement de figures à une compétition de Parkour

## Bibliographie commentée

Le Parkour est un sport qui se pratique seul et qui consiste à passer le plus rapidement et esthétiquement possible des obstacles urbains tels que des murets, des barrières ou des escaliers en centre-ville. Ce sport est encore très jeune, la popularité venant en grande partie du film Yamakasi de 2001, et les compétitions dans celui-ci le sont tout aussi et sont encore vouées à beaucoup de changements [1]. Nous nous baserons sur la version "Freestyle" de ces compétitions, qui consistent en la mise en concurrence de différents athlètes (nommés "Traceurs") sur un même terrain de 40m² parsemé d'obstacles (e.g. murs, barres), où chaque athlète dispose de 70 secondes pour proposer un enchaînement de figures [1] utilisant le mobilier disponible. La variété des techniques, la fluidité de l’enchaînement et la bonne maîtrise de ces techniques sont au centre du score final de l'athlète.

L'algorithme génétique est un type d'algorithme méta-heuristique servant dans la majorité des cas à résoudre des problèmes d'optimisation. Le choix d'un algorithme méta-heuristique est fortement conseillé étant donné que la notation de chaque athlète ne peut dépendre que du parcours final effectué et qu'il ne peut pas être estimé pendant le passage de l'athlète [2]. Cet algorithme se décompose en cinq parties : Création d'une population initiale, attribution d'un score à chaque individu de la population, croisements d'individus pour créer une nouvelle population enfantée par la précédente, mutation de certains enfants et la comparaison de la population à un critère de terminaison dépendant du problème étudié [3].

Nous définissons la performance de l'algorithme comme la proportion de fois où l'algorithme permet à un athlète virtuel d'avoir un score dans un intervalle défini par son niveau de maîtrise, par rapport au nombre d’exécution de l'algorithme [4]. Nous tenterons donc d'étudier ces performances sur le problème de maximisation du score obtenu dans une compétition de Parkour et de comparer ces résultats avec ceux obtenus par l'algorithme génétique de l'étude [5] pour une fonction avec beaucoup de maximas. Etant donné qu'il y a plusieurs chemins possibles pour atteindre le meilleur score, une fonction où il y a plusieurs solutions possibles pour atteindre un score maximal semble être la meilleure comparaison disponible dans cette étude [5]. Les performances de l'algorithme étant étudiées selon les paramètres suivants : la taille de la population, la probabilité de mutation et la probabilité de croisement des individus.

Nous tenterons de modéliser ces compétitions grâce à des simulations python avec comme modèle un jeu de tour par tour, chaque tour représentant une seconde dans la réalité, chaque jeu représentant une performance d'un athlète et où à chaque tour l'athlète (ici le joueur) peut choisir d'effectuer une figure dans une liste prédéfinie [2], se déplacer ou ne rien faire. Si une figure était déjà en cours avant le tour actuel, il la continuera jusqu'à la fin de la durée déterminée, indépendente de l'athlète (1 à 5 secondes). Le terrain de jeu est modélisé par une grille de 40 par 10 où chaque case représente un mobilier urbain (mur, barre ou sol) présent à la compétition qui nous servira de référence : Parkour World Cup 2022 à Sofia en Bulgarie [5].

Afin de pouvoir attester de la cohérence des chiffres obtenus via le système de notation implanté avec les incertitudes dû aux facteurs humains rentrant beaucoup en jeu dans ces compétitions, nous utiliserons la performance d'une athlète française durant cette même compétition à Sofia [6] : Lilou Ruel.

## Objectifs du TIPE du candidat

1. Modélisation informatique d'une compétition de Parkour
2. Evalution de la cohérence du modèle avec la réalité [5]  [6]
3. Comparer les résultats obtenues avec l'algorithme génétique dans le cas de la compétition de Parkour avec les résultats obtenues par l'étude [5] pour les mêmes paramètres d'entrée et une fonction multimodale

## Références bibliographiques

[1] FIG : Code de pointage 2019-2021, octobre 2019, https://fr.readkong.com/page/code-de-pointage-2019-2021-parkour-f-d-ration-2054990
[2] Parkour commission : Code of points 2022-2024, Table of tricks 2023, mai 2023, https://www.gymnastics.sport/publicdir/rules/files/en_1.1%20-%20PK%20Code%20of%20Points%202022-2024%20-%20Table%20of%20tricks%202023.pdf
[3] RANDY (L), SUE (E) : Practical Genetic Algorithms, 2004
[4] Deb (K) and Agrawal (S) : Understanding Interactions among Genetic Algorithm Parameters, 1999, https://www.egr.msu.edu/~kdeb/papers/k99003.pdf
[5] Vidéo 2022 Parkour World cup FIG https://www.youtube.com/watch?v=ubQ1w7awah8
[6] FIG : Results Book, septembre 2022 https://www.gymnastics.sport/site/events/results.php?idEvent=16813