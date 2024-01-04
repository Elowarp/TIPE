# Techniques d'améliorations sportives : modélisation par l'informatique

Le parkour est un sport qui a acquis une grande popularité mondiale, en plus d'être spectaculaire à regarder, il met en avant la beauté de la maîtrise de son corps dans des environnements différents. Qui dit sport, dit compétition, qui dit compétition, dit optimisation des gains. Étudier le comportement des athlètes (traceurs) au moyen d'un modèle informatique pour tenter d'extraire des techniques applicables ou appliquées réellement semble correspondre parfaitement à la thématique de cette année.

Le parkour étant mon sport favori, ce sujet de l'informatique en découle naturellement.

## Positionnement thématique

INFORMATIQUE PRATIQUE (Algorithmes génétiques) ;  *INFORMATIQUE* THEORIQUE (Algorithmique) ;

## Mots clés

- Parkour
- Algorithme génétique
- Score
- Aléatoire
- Séquentielle

## Problématique retenue

Comment utiliser des modèles informatiques afin d'en tirer des techniques à appliquer pour maximiser ses chances de gagner une compétition de Parkour ?

## Bibliographie commentée

Le parkour est un sport qui se pratique seul, comme la course à pied, et qui consiste en le passage le plus rapidement et esthétiquement possible d'obstacles urbains tels que des murets, des barrières ou des escaliers en centre-ville. Ce sport existant depuis les années 90, les compétitions mondiales sont encore toutes jeunes et sont encore vouées à beaucoup de changements [3]. Nous nous baserons sur la version "Freestyle" de ces compétitions, qui consistent en la mise en concurrence de différent.e.s athlètes (nommés "Traceur.euse") sur un même terrain de 40m^2 parsemé d'obstacles en tout genre, où chaque athlète dispose de 70secondes pour proposer un enchainement de figures [4] utilisant le mobilier disponible. La variété des techniques, l'enchainement fluide et la bonne maitrîse de celle ci sont au centre de du score final de l'athlète. Ainsi tout le but de ce TIPE serait de trouver une optimisation de ces enchaînements, des techniques notables, voire déjà utilisées dans le monde réel, afin de maximiser le score final de l'athlète [3].

Nous tenterons de modéliser ces compétitions grâce à des simulations python avec comme modèle un jeu de tour par tour, chaque tour représentant une seconde dans la réalité, chaque jeu représentant une performance d'un athlète et où à chaque tour l'athlète (ici le joueur) peut choisir d'effectuer une figure dans une liste prédéfinie [4], se déplacer ou ne rien faire. Si une figure était déjà en cours avant le tour actuel, il la continuera jusqu'à la fin de la durée déterminée, indépendente de l'athlète (1 à 5secondes). Le terrain de jeu est modélisé par une grille de 40 par 10 où chaque case représente un mobilier urbain (mur, barre ou sol) présent à la compétition qui nous servira de référence : Parkour World Cup 2022 à Sofia en Bulgarie [5].

La notation étant énormément dépendante de l'avis subjectif du jury, et étant rendu à la fin de la performance et non construite au fûr et à mesure de celle ci, toute méthode heuristique ne peut être appliqué à notre problème, c'est pour cela que j'ai choisi d'implémenter un algorithme méta-heuristique : Un algorithme génétique (L'aspect général de l'algorithme [2] et une implémentation en code/pseudo-code [2])

Afin d'avoir une comparaison des résultats obtenus à la réalité, nous utiliserons les perfomances d'althlètes durant cette même compétition à Sofia [5].

<!-- Le parkour est encore jeune, et les compétitions encore plus. Le règlement de ces compétitions changent encore d'une année à l'autre, des changements au niveau de la notation [3] mais aussi des reclassement des figures et de leurs points attribués [4]. Ce qui serait intéressant, ce serait de comprendre comment les mécanismes et techniques notables sont utilisées dans ce sport urbain afin d'en optimiser le score résultant [3].

Le modèle représentant la compétition choisit fut un tour par tour, chaque tour durant 1s dans lequel on peut faire toutes les figures ayant un temps défini de réalisation. Le terrain étant implémenter par un tableau de case "mur", "sol", "barre" comme selon la compétition de 2022 à Sofia en Bulgarie [5] et les athlètes par des personnages se mouvant toutes les secondes.
J'ai en choisi d'implémenter un algorithme génétique en python ([1] et [2]) afin de pouvoir simuler une compétition, chaque itération de l'algorithme rejouant une compétition complète en changeant les figures et chemins empruntés par les athlètes afin d'en retenir les meilleurs.

Il y a aussi eu un phase d'implémentation de parcours d'athlètes [5] afin de pouvoir comparer de réels scores aux scores donnés par mon algorithme. -->

## Objectifs du TIPE du candidat

1. Mettre au point un modèle informatique d'une compétition de Parkour type
2. Traiter des vidéos d'athlètes afin de reproduire leur performance à travers le modèle et étudier les différences et points faibles de celui-ci
3. Essayer de trouver une corrélation entre les techniques pratiquées en conditions réelles et celles utilisées par le modèle pour maximiser le score via des simulations

## Références bibliographiques

[1] MORIARITY (S) : Genetic Alogirthms in Elixir : Solve Problems Using Evolution, janvier 2021
[2] RANDY (L), SUE (E) : Practical Genetic Algorithms, 2004
[3] FIG : Code de pointage 2019-2021, octobre 2019
[4] Parkour commission : Code of points 2022-2024, Table of tricks 2023, avril 2023
[5] Vidéo 2022 Parkour World cup FIG https://www.youtube.com/watch?v=ubQ1w7awah8