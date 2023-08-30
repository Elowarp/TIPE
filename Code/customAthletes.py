'''
 Name : Elowan
 Creation : 30-08-2023 15:03:52
 Last modified : 30-08-2023 16:41:12
'''
from Models import Athlete, FIGURES
from Terrain import Field
from main import AthleteChromosome

# Lilou Ruel
lilou = Athlete(8, FIGURES["gaet_flip"])
lilou.combos = [
    ((7, 31), FIGURES["double_cork"], 0),
    ((7, 31), FIGURES["jump"], 4),
    ((8, 33), FIGURES["180"], 5),
    ((6, 35), FIGURES["cast_backflip"], 7),
    ((7, 31), FIGURES["jump"], 10),
    ((6, 29), FIGURES["cast_backflip_360"], 11),
    ((5, 30), FIGURES["jump"], 13),
    ((2, 31), FIGURES["double_cork"], 15),
    ((1, 33), FIGURES["inward_flip"], 18),
    ((2, 28), FIGURES["180"], 22),
    ((4, 28), FIGURES["cork"], 23),
    ((7, 27), FIGURES["gaet_flip"], 26),
    ((8, 26), FIGURES["run"], 27),
    ((8, 24), FIGURES["run"], 28),
    ((8, 22), FIGURES["jump"], 29),
    ((8, 20), FIGURES["jump"], 30),
    ((6, 18), FIGURES["double_swing_gainer"], 31),
    ((5, 18), FIGURES["run"], 35),
    ((4, 16), FIGURES["180"], 38),
    ((3, 15), FIGURES["jump"], 40),
    ((3, 15), FIGURES["180"], 41),
    ((3, 15), FIGURES["jump"], 43),
    ((4, 15), FIGURES["run"], 44),
    ((5, 15), FIGURES["jump"], 45),
    ((6, 15), FIGURES["180"], 46),
    ((7, 15), FIGURES["jump"], 47),
    ((8, 15), FIGURES["cork"], 48),
]

if __name__ == "__main__":
    field = Field()
    field.createField()

    lilou.setField(field)
    lilouAthelte = AthleteChromosome(lilou)
    print(lilouAthelte.detailedFitness)
    print(lilouAthelte.fitness)