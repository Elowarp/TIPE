'''
 Name : Elowan
 Creation : 02-06-2023 11:00:02
 Last modified : 16-06-2023 14:22:01
'''
from random import randint, choice

class Figure:
    instanceCount = 0

    def __init__(self, name, duration, complexity):
        self.id = self.instanceCount
        self.name = name
        self.duration = duration
        self.complexity = complexity
        Figure.instanceCount += 1
    
    def __repr__(self) -> str:
        return self.name    
    
class Athlete: 
    instanceCount = 0

    def __init__(self, xp, figureFav):
        self.id = self.instanceCount
        self.xp = xp
        self.figureFav = figureFav
        self.combos = []                        # ((x, y), Figure, tickStarted)
        self.position = (0, 0)                  # Coordonnées en (x, y)
        self.state = {                          # Etat de l'athlete 
            "isMoving": False,
            "ticksSinceStartedMoving": 0,
            "movement": FIGURES["do_nothing"],  # Pas en mouvement 
        }
        self.field = None

        Athlete.instanceCount += 1

    def _getFigureByTick(self, tick):
        """Retourne le combo de l'athlete en fonction du tick de départ
        
        Params:
            tick (int): Le tick en question
        """
        for combo in self.combos:
            if combo[2] == tick:
                return combo

        return None

    def takeAction(self, tick):
        """Fait faire une figure à l'athlete
        
        Params:
            tick (int): Le tick actuel
        """

        if self.state["movement"] != FIGURES["do_nothing"]:
            if self.state["ticksSinceStartedMoving"]+1 >= self.state["movement"].duration:
                self._endMovement()
            
            else:
                self.state["ticksSinceStartedMoving"] += 1

        else:
            figure = self._getFigureByTick(tick)
            
            # Choisit où l'action doit être faite, si figure n'est 
            # pas None, alors on va aux coordonnées de la figure, sinon
            # on bouge aléatoirement autour de l'athlete
            self._moveAround(figure)

            # Fait la figure si le figure du combo n'est pas None sinon 
            # on fait une figure aléatoire
            self._startMovement(tick, figure = figure)
    
    def _moveAround(self, figure=None):
        """Fait bouger l'athlete sur une case collée"""
        # Si combo n'est pas None, alors on va aux coordonnées du combo
        if figure != None:
            self.position = figure[0]
            return

        # Note les cases adjacentes de 0 à 8 (0 = haut gauche
        # et croissant dans le sens horaire) et
        # supprime celles ou l'athlete ne peut aller
        possibleNextPosition = \
            self._removeImpossibleNextCases([x for x in range(8)])
        
        # Choisit aléatoirement parmis ces cases possibles
        nextCase = choice(possibleNextPosition)

        # Met a jour les coordonnees
        self._setNewCoords(nextCase)
        
        
    def _setNewCoords(self, nextCase):
        """
        En partant d'un nombre entre 0 et 7 inclus, on met a jour 
        les nouvelles coordonées. On a 0 dans le coin haut gauche et
        c'est croissant dans le sens horaire (Ex case bas gauche = 6)
        """
        match nextCase:
            case 0:
                self.position = (
                    self.position[0]-1,
                    self.position[1]-1,
                )   
            case 1:
                self.position = (
                    self.position[0],
                    self.position[1]-1,
                )    
            case 2:
                self.position = (
                    self.position[0]+1,
                    self.position[1]-1,
                )   
            case 3:
                self.position = (
                    self.position[0]+1,
                    self.position[1],
                )   
            case 4:
                self.position = (
                    self.position[0]+1,
                    self.position[1]+1,
                )    
            case 5:
                self.position = (
                    self.position[0],
                    self.position[1]+1,
                )  
            case 6:
                self.position = (
                    self.position[0]-1,
                    self.position[1]+1,
                )  
            case 7:
                self.position = (
                    self.position[0]-1,
                    self.position[1],
                )   
    
    def _removeImpossibleNextCases(self, cases):
        positionToRemove = []

        # Dernier x/y qui est encore sans le terrain
        lastCoordPossible = len(self.field)-1 

        if self.position[0] == 0:
            if 0 not in positionToRemove: positionToRemove.append(0)
            if 7 not in positionToRemove: positionToRemove.append(7)
            if 6 not in positionToRemove: positionToRemove.append(6)
            
        elif self.position[0] == lastCoordPossible:
            if 2 not in positionToRemove: positionToRemove.append(2)
            if 3 not in positionToRemove: positionToRemove.append(3)
            if 4 not in positionToRemove: positionToRemove.append(4)

        if self.position[1] == 0:
            if 0 not in positionToRemove: positionToRemove.append(0)
            if 1 not in positionToRemove: positionToRemove.append(1)
            if 2 not in positionToRemove: positionToRemove.append(2)

        elif self.position[1] == lastCoordPossible:
            if 4 not in positionToRemove: positionToRemove.append(4)
            if 5 not in positionToRemove: positionToRemove.append(5)
            if 6 not in positionToRemove: positionToRemove.append(6)

        # Retire toutes les cases impossibles
        for i in range(len(cases)-1, -1, -1):
            if i in positionToRemove: 
                cases.pop(i)

        return cases


    def _startMovement(self, tick, figure = None):
        """
        Regarde sur quelle case est l'athlete et commence la figure
        associée

        Params:
            tick (int): Tick actuel
        """
        # Si combo n'est pas None, alors on fait la figure du combo
        if figure != None:
            self.state["movement"] = figure[1]

        else:
            # Choisit aléatoirement le mouvement à faire parmis la liste possible
            figures = self.field.getCase(self.position).figuresPossible
            self.state["movement"] = figures[randint(0, len(figures)-1)]
            self.combos.append((self.position, self.state["movement"], tick))

        self.state["isMoving"] = True
        self.state["ticksSinceStartedMoving"] = 0


    def _endMovement(self):
        self.state["isMoving"] = False
        self.state["movement"] = FIGURES["do_nothing"]        
        self.state["ticksSinceStartedMoving"] = 0

    def setField(self, field):
        self.field = field

    def __repr__(self) -> str:
        return "{} :\n    - xp : {}\n    - figure fav : {}\n    - Combos : {}".format(
            self.id, self.xp, self.figureFav.name, self.combos
        )

FIGURES = {
    "do_nothing": Figure("do_nothing", 2, 0),       # Ne rien faire pendant 2s
    
    "jump": Figure("jump", 3, 2),                   # Jump pendant 5s
    "palm_flip": Figure("palm_flip", 5, 7),         # Palm_flip pendant 5s
    "backflip": Figure("backflip", 5, 4),           # Backflip pendant 5s
    "frontflip": Figure("frontflip", 5, 5),         # Frontflip pendant 5s
    "cork": Figure("cork", 5, 8),                   # Cork pendant 5s
}

if __name__ == "__main__":
    athlete = Athlete(5, FIGURES["frontflip"])
    print(athlete)