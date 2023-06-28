'''
 Name : Elowan
 Creation : 02-06-2023 11:01:13
 Last modified : 28-06-2023 18:31:02
'''

from Models import Figure, FIGURES
from random import choice

SIZE_X = 10
SIZE_Y = 15

class Case:
    instanceCount = 0

    def __init__(self, name, figuresPossible):
        self.id = self.instanceCount
        self.name = name
        self.figuresPossible = figuresPossible
        Case.instanceCount += 1

    def getCaseById(id):
        """Retourne la case en fonction de son id, None sinon"""
        for case in CASES.values():
            if case.id == id:
                return case

        return None

    def __repr__(self) -> str:
        return str(self.id)
    
    def __str__(self) -> str:
        return self.__repr__()

class Field:
    def __init__(self, grille = [[None for j in range(SIZE_X)] 
                                 for i in range(SIZE_Y)]):
        self.grille = grille

    def createField(self):
        for i in range(SIZE_Y):
            for j in range(SIZE_X):
                self.grille[i][j] = choice(list(CASES.values()))

    def getCase(self, positions) -> Case:
        """Retourne la case en coordonée x y"""
        x = positions[0]
        y = positions[1]
        return self.grille[y][x]

    def __len__(self) -> int:
        return len(self.grille)

    def __repr__(self) -> str:
        # Représente le terrain comme une grille
        result = ""
        for i in range(len(self.grille)):
            result += "| "
            for case in self.grille[i]:
                result += str(case) + " | "

            # Empeche le dernier saut a la ligne
            result += "\n"

        return result
    
    def __str__(self) -> str:
        return self.__repr__()

CASES = {
    "empty": Case("empty", [                        # Sol plat vide
        FIGURES["do_nothing"], 
        FIGURES["run"],
        FIGURES["jump"],
        FIGURES["180"],
        FIGURES["backflip"], 
        FIGURES["frontflip"], 
        FIGURES["gaet_flip"],
        FIGURES["cork"],
        FIGURES["inward_flip"],
        FIGURES["540"],
        FIGURES["double_cork"],
        FIGURES["double_frontflip"],
        FIGURES["double_backflip"],
        FIGURES["double_flip_360"]
    ]),           
    "wall":  Case("wall", [                         # Mur 
        FIGURES["do_nothing"], 
        FIGURES["jump"], 
        FIGURES["run"],
        FIGURES["cast_backflip"],
        FIGURES["gainer"],
        FIGURES["kong_gainer"],
        FIGURES["cast_backflip_360"],
    ]),            
    "bar":  Case("bar", [                         # Trou
        FIGURES["do_nothing"], 
        FIGURES["jump"],
        FIGURES["run"],
        FIGURES["cast_backflip"],
        FIGURES["gainer"],
        FIGURES["cast_backflip_360"],
        FIGURES["double_swing_gainer"],
        FIGURES["double_backflip"],
    ]),               
}

if __name__ == "__main__":
    # Grille 3x3
    field = Field()
    field.createField()
    print(field)