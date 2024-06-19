#import "@preview/arkheion:0.1.0": arkheion, arkheion-appendices

#show: arkheion.with(
  title: "Etude des probabilités de croisement et de mutation dans les algorithmes génétiques via l'exemple du Parkour",
  // Insert your abstract after the colon, wrapped in brackets.
  // Example: `abstract: [This is my abstract...]`
  abstract: [Étude de l'impact des probabilités de mutations et de croisements sur un algorithme génétique pour l'optimisation d'un enchaînement de figures à une compétition Freestyle de Parkour ainsi que la comparaison de la performance de cet algorithme avec un autre algorithme génétique ayant une fonction de score semblable au premier abord à celle utilisée pour le Parkour.],
  date: datetime.today().display("[Month repr:long] [day], [year]"), 
)
#set cite(style: "chicago-author-date")
#show link: underline

// Add a table of contents

= Introduction
Le Parkour a gagné beaucoup de popularité chez les jeunes depuis les années 90s, notamment mis en lumière par des films comme "Yamakasi" ou "Banlieue 13". Ce sport fut mon coup de coeur dès lors que j'ai commencé à en pratiquer depuis mes 14ans, ce qui justifie l'importance que j'accorde à ce TIPE. 



= Définitions
On va définir dans cette section les termes et concepts importants pour la compréhension de ce TIPE.

== Le Parkour

=== Sport et compétition
Le Parkour est un sport sans réelle règle définie au préalable comme pourrait l'être le volleyball, il s'agit d'entrainements à la maitrise de son corps à travers des figures comme des saltos dans différents environnements, en ville comme en salle de gymnastique. Cette liberté au niveau des règles à permis l'émergence de différentes compétitions selon différentes règles comme celle qui nous intéresse aujourd'hui : _La compétition de Parkour Freestyle_. 

Pour cette compétition, l'athlète dispose de 70 secondes ainsi qu'une scène avec des murets, murs et barre en métal pour réalisé le meilleur enchainement de figure possible. Un score lui est ensuite attribué selon la difficulté des figures, la fluidité de l'enchainement ainsi que la variété des figures.

=== La notation
La notation est régis par des règles et des points accordables décidés par la _FIG_ (Fédération internationnale de Gymnastique). En voici les extraits officiels :

#figure(
  image("./images/scores.png", width: 70%),
  caption: [Extrait des points par figure pour la compétition féminine de Parkour Freestyle [1]]
) <scores>

#figure(
  image("./images/notation.png", width: 70%),
  caption: [Extrait de la fiche jury [2]]
) <notation>

Ces documents ne sont pas exactement ceux utilisées pour la compétition à Sofia en 2021 car ils sont introuvables. Cependant, ils sont très similaires avec ceux des années précédentes et permettent de comprendre le fonctionnement de la notation.

== L'algorithme génétique

=== Principe

#grid(
  columns: 2,
  gutter: 10pt,
  [
    L'algorithme génétique est une méthode d'optimisation qui s'inspire de la théorie de l'évolution. Il est composé de 4 étapes principales : la génération, l'évaluation, la sélection et la reproduction. 

    L'objectif est de trouver la meilleure solution à un problème donné en faisant évoluer une population d'individus au fil des générations.

    On génére une population de $n$ d'individus, chaque individus a des caractéristiques qui lui sont propres, que l'on appelle _gènes_. Ces gènes sont des valeurs numériques qui sont les seuls paramètres utiles à l'évaluation de l'individu.
  ],
  [
    #figure(
      image("./images/genetic_algorithm.png", width: 70%),
      caption: [Schéma de l'algorithme génétique]
    )
  ]
)

Une fois la population évaluée, on séléctionne $d$ meilleurs individus pour les reproduire jusqu'à avoir $n$ nouveaux individus. La reproduction se fait par copie littérale des parents ou alors si la probabilité de croisement $p_c$ ou de mutation $p_m$ sont assez haute, par croisement et mutation des gènes de certains des individus sélectionnés.

On continue ce processus jusqu'à ce qu'un critère de terminaison soit atteint, par exemple un _nombre maximal d'évaluation_ ou un score minimum.

On appelle _génération_ un tour de boucle et une _exécution_ de l'algorithme génétique une ensemble de générations jusqu'à la validation du critère de terminaison. 


= Adaptation de l'algorithme génétique au Parkour

== Modélisations
On décide de modéliser une compétition Freestyle par un jeu tour par tour où chaque tour représente une seconde écoulée. A chaque tour, l'athlète a un état représentant la figure qu'il est en train de réaliser ainsi que son emplacement sur le terrain.

=== Le terrain


#grid(
  columns: 2,
  gutter: 10pt,
  [
    Le terrain est modélisé par une matrice de taille $10 times 40$ où chaque case est représentée par un entier. On peut voir ce terrain comme un graphe où les sommets sont les cases et les arêtes les liens entre ces cases. Les cases peuvent être de 3 types :
    - 0 : sol
    - 1 : mur
    - 2 : barre

    On choisit alors de copier sur terrain sur la scène de la compétition Freestyle à Sofia en 2021.

    #figure(
      image("./images/terrain.png", width: 90%),
      caption: [Scène de la compétition Freestyle de Parkour à Sofia en 2021, © FIG]
    )
  ],
  [
    #figure(
      image("./images/terrain_modele.png", width: 65%),
      caption: [Terrain modélisé]
    )
  ]
)

=== Les individus
Chaque individu, appelé aussi athlète ou _chromosome_, est représenté par une suite finie de gènes $(g_k)_k$ et un niveau de maîtrise entre 0 et 10.

En effet, on définit cette suite comme :
- $(g_(3k))_k$ : La suite des absices des figures
- $(g_(3k+1))_k$ : La suite des ordonnées des figures
- $(g_(3k+2))_k$ : La suite des figures

Donc tous les 3 indices, on a les informations d'un point sur notre terrain, cette suite de gènes représente alors un _chemin_ dans notre graphe avec une information supplémentaire (la figure), voir @BoutChemin.

#figure(
  image("images/terrain.png", width: 50%),
  caption: [Représentation d'un bout de chemin sur un graphe]
) <BoutChemin>

=== Notation des individus
Pour noter un individu, on va appliquer les règles données par @scores et @notation sur le chemin représenté par les gènes de l'individu. 

Pour les sous catégories de la notation subjectives pour les jurys (ie Mastery, Connection, ...), on les modélise par des fonctions linéaires de la forme : 

#math.equation(block: true, numbering: none, [
    $
    f(x) = M / 10 x 
    $
  ]
)

Avec $x$ le niveau de maîtrise de l'individu et $M$ le nombre de points maximum pour cette catégorie. Pour un individu de niveau de maîtrise 8, la formule calculant le score de Connection est alors $8 times 4/10 = 3.2$ sur $4$.

Pour les sous catégories de la notation moins subjectives (ie Variety, Use of the obstacles, ...), on les modélise par des fonctions calculant le nombre de cases différentes dans le chemin ou le nombre de figures différentes réalisées.


== Les opérations de croisement et de mutation
On définit dans cette section les opérations de croisement et de mutation dépendante du problème du Parkour.

=== Croisement
Soient deux individus $A$ et $B$ avec des gènes $(g_k)_k$ et $(h_k)_k$, s'il y a croisement entre ces deux individus, on vérifie si les deux individus ont deux points du chemin en commun sans prendre en compte les figures. 

Ce qui revient à regarder s'il existe $i_1$ et $j_1$ tels que $g_(3i_1) = h_(3j_1)$ et $g_(3i_1+1) = h_(3j_1+1)$, de même pour $i_2$ et $j_2$ différents de $i_1$ et $j_1$.

Dès lors, on pose l'opération de croisement qui prend deux suites de gènes et les croise en prenant les points en commun pour former deux nouveaux gènes :

#math.equation(block: true, numbering: none, [
    $
    C(g, h) = ((g_1, ..., g_(3i_1-1), h_(3j_1), ..., h_(3j_2-1), g_(3i_2), ..., g_n), (h_1, ..., h_(3j_1-1), g_(3i_1), ..., g_(3i_2-1), h_(3j_2), ..., h_n))
    $
  ]
)

Cette opération est illustrée par @Crossover.

#figure(
  image("./images/crossover.png", width: 70%),
  caption: [Schéma de l'opération de croisement]
) <Crossover>

Supposons que $A$ et $B$ n'aient pas de points en commun, on  décide alors de ne pas les croiser et d'exécuter la même opération que sur les individus non croisés : créer des enfants identiques aux parents.

=== Mutation
En reprenant les mêmes individus $A$ et $B$ définis à la section précédente, on définit l'opération de mutation qui prend un individu et le modifie en changeant un de ses gènes.

#figure(
  image("./images/mutation.png", width: 70%),
  caption: [Schéma de l'opération de mutation]
) <Mutation>
)


== Critère de terminaison



= Optimisation du code

== Parallélisme

== Mutation Clock Operator



= Comparaison des performances

== Définitions de la performance
Rappel à la notation et critère de terminaison

== Fonction de Rastrigin
Pourquoi ce choix

== Comparaison

== Explication de pq la convergence tjrs et ce que leur graphe fait


= Conclusion

= Math

*Inline:* Let $a$, $b$, and $c$ be the side
lengths of right-angled triangle. Then, we know that: $a^2 + b^2 = c^2$

*Block without numbering:*

#math.equation(block: true, numbering: none, [
    $
    sum_(k=1)^n k = (n(n+1)) / 2
    $
  ]
)

*Block with numbering:*

As shown in @equation.

$
sum_(k=1)^n k = (n(n+1)) / 2
$ <equation>

*More information:*
- #link("https://typst.app/docs/reference/math/equation/")


= Figures and Tables

#figure(
  table(
    align: center,
    columns: (auto, auto),
    row-gutter: (2pt, auto),
    stroke: 0.5pt,
    inset: 5pt,
    [header 1], [header 2],
    [cell 1], [cell 2],
    [cell 3], [cell 4],
  ),
  caption: [#lorem(5)]
) <table>



= Références 
1. #link("https://www.gymnastics.sport/publicdir/rules/files/en_1.1%20-%20PK%20Code%20of%20Points%202022-2024%20-%20Table%20of%20tricks%202023.pdf") 
2. #link("https://fr.readkong.com/page/code-de-pointage-2019-2021-parkour-f-d-ration-2054990")