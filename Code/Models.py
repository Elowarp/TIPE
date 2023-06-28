'''
 Name : Elowan
 Creation : 02-06-2023 11:00:02
 Last modified : 28-06-2023 18:28:23
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

    def getFigureById(id):
        """Retourne la figure en fonction de son id, None sinon"""
        for figure in FIGURES.values():
            if figure.id == id:
                return figure

        return None
    
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
            if self.state["ticksSinceStartedMoving"]+1 >= \
              self.state["movement"].duration:
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
        lastCoordPossibleY = len(self.field.grille[0])-1 
        lastCoordPossibleX = len(self.field.grille)-1 

        if self.position[0] == 0:
            if 0 not in positionToRemove: positionToRemove.append(0)
            if 7 not in positionToRemove: positionToRemove.append(7)
            if 6 not in positionToRemove: positionToRemove.append(6)
            
        elif self.position[0] == lastCoordPossibleY:
            if 2 not in positionToRemove: positionToRemove.append(2)
            if 3 not in positionToRemove: positionToRemove.append(3)
            if 4 not in positionToRemove: positionToRemove.append(4)

        if self.position[1] == 0:
            if 0 not in positionToRemove: positionToRemove.append(0)
            if 1 not in positionToRemove: positionToRemove.append(1)
            if 2 not in positionToRemove: positionToRemove.append(2)

        elif self.position[1] == lastCoordPossibleX:
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
    "do_nothing": Figure("do_nothing", 1, 0),       # Ne rien faire pendant 1s

    "run": Figure("run", 1, 0),                     # Courir pendant 1s
    "jump": Figure("jump", 1, 0),                   # Sauter pendant 1s

    "180": Figure("180", 1, 0.5),                   # Faire un 180 pendant 1s
    "frontflip": Figure("frontflip", 1, 0.5),       # Faire un frontflip pendant 1s
    "backflip": Figure("backflip", 1, 0.5),         # Faire un backflip pendant 1s
    "gaet_flip": Figure("gaet_flip", 1, 0.5),       # Faire un gaet flip (back 
                                                    # en appui sur un coin de mur) 
                                                    # pendant 1s
    
    "cork": Figure("cork", 1, 1),                   # Faire un cork pendant 1s
    "cast_backflip": Figure("cast_backflip", 1, 1), # Faire un cast backflip (
                                                    # backflip en appui sur un
                                                    # mur) pendant 1s
    "gainer": Figure("gainer", 1, 1),               # Faire un gainer pendant 1s
    "inward_flip": Figure("inward_flip", 1, 1),     # Faire un inward flip (
                                                    # front qui te fait reculer)
                                                    # pendant 1s    
    "540": Figure("540", 1, 1.5),                     # Faire un 540 pendant 1s
    "double_cork": Figure("double_cork", 2, 2),     # Faire un double cork
    "kong_gainer": Figure("kong_gainer", 1, 2),     # Faire un kong gainer
    "cast_backflip_360": Figure("cast_backflip_360",
                                 2, 2.5),           # Faire un cast backflip 360
    "double_swing_gainer": Figure("double_swing_gainer", 2, 3), # back sur une barre
    
    "double_frontflip": Figure("double_frontflip", 
                               2, 4),               # Faire un double front
    "double_backflip": Figure("double_backflip",
                               2, 4),               # Faire un double back

    "double_flip_360": Figure("double_flip_360", 2, 4.5), # Faire un double flip 360
}

if __name__ == "__main__":
    athlete = Athlete(5, FIGURES["frontflip"])
    print(athlete)