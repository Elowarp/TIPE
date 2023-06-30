'''
 Name : Elowan
 Creation : 02-06-2023 11:00:05
 Last modified : 01-07-2023 00:14:43
'''

from Terrain import Field
from Models import Athlete, FIGURES

from consts import INITIAL_POSITION, MAX_TICK_COUNT


class Game:
    """
    Classe représentant un round de la compétition
    """

    instances = []
    def __init__(self, athlete):
        self.field = Field()
        self.field.createField()
        self.athlete = athlete
        self.state = 0          # Etat de la partie
        self.tickCount = 0      # 1 tick = 1 seconde 

        self.athlete.setField(self.field)
        
        Game.instances.append(self)

    def start(self):
        """Initialisation des valeurs de depart de la competition"""
        self.tickCount = 0
        self.state = 1
        self.athlete.position = INITIAL_POSITION

    def update(self):
        """Met à jour l'état de l'athlète et retourne l'état de la compétition"""
        if self.tickCount >= MAX_TICK_COUNT:
            self.end()
            return self.state
        
        self.athlete.takeAction(self.tickCount)

        self.tickCount += 1
        return self.state

    def end(self):
        """Fonction appelée lorque la competition termine"""
        self.state = 2

    def play(self, iterate=lambda x: None, callback=lambda x: None):
        """Fait faire une partie entière au jeu
        Params:
            iterate (function)  - Prend en paramètre l'instance du jeu et ne 
                                    renvoie rien. Elle est executee a chaque 
                                    tick de la partie

            callback (function) - Prend en paramètre l'instance du jeu et ne 
                                    renvoie rien. Elle est executee a la fin de
                                    la partie
                                
        """
        self.start()
        while self.update() == 1:
            iterate(self)
        
        callback(self)

    def _getGameByAthlete(athlete):
        for i in Game.instances:
            if i.athlete.id == athlete.id:
                return i
            
    def resetGames():
        """Reset toutes les instances de Game"""
        Game.instances = []

if __name__ == "__main__":
    athlete = Athlete(5, FIGURES["backflip"])
    game = Game(athlete)
    def iterate(game):
        print("Athlete state (in the second {}) : ".format(game.tickCount))
        print("  - Position ({},{})".format(
                game.athlete.position[0], game.athlete.position[1]
        ))
        print("  - Case : {}".format(
            game.field.getCase(game.athlete.position).name
        ))
        print("  - Current movement : {} since {} seconds".format(
            game.athlete.state["movement"], game.athlete.state["ticksSinceStartedMoving"]
        ))
        print()

    def callback(game):
        print("Game state : {}\nFor {} ticks".format(game.state, game.tickCount))
        print("Combos : {}".format(athlete.combos))

    print("Game started !")
    game.play(iterate=iterate, callback=callback)