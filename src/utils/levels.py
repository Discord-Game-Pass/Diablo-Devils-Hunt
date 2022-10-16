import math

from utils.translations import fake_translation as _


LEVELS = [
    {"level": -3, "expMin": -999999,  "name": _("Chaos Lord"), "accuracy": 95, "reliability": 85, "bullets": 6, "magazines": 1}, # Beginner's luck
    {"level": -2, "expMin": -99999,  "name": _("Black Knight"), "accuracy": 95, "reliability": 85, "bullets": 6, "magazines": 1}, # Beginner's luck
    {"level": -1, "expMin": -9999,  "name": _("Berserker"), "accuracy": 95, "reliability": 85, "bullets": 6, "magazines": 1}, # Beginner's luck
    {"level": 0, "expMin": -999,  "name": _("Novice"), "accuracy": 54, "reliability": 85, "bullets": 6, "magazines": 1}, 
    {"level": 1, "expMin": -6,    "name": _("Apprentice"), "accuracy": 56, "reliability": 85, "bullets": 6, "magazines": 2},  
    {"level": 2, "expMin": 20,    "name": _("Hunter"), "accuracy": 58, "reliability": 86, "bullets": 6, "magazines": 2},     
    {"level": 3, "expMin": 50,    "name": _("Stategist"), "accuracy": 60, "reliability": 87, "bullets": 6, "magazines": 2},  
    {"level": 4, "expMin": 90,    "name": _("Ruffian"), "accuracy": 61, "reliability": 88, "bullets": 8, "magazines": 2},
    {"level": 5, "expMin": 140,   "name": _("Savage"), "accuracy": 62, "reliability": 89, "bullets": 8, "magazines": 2},
    {"level": 6, "expMin": 200,   "name": _("Warrior"), "accuracy": 63, "reliability": 90, "bullets": 8, "magazines": 2},
    {"level": 7, "expMin": 270,   "name": _("Phalanx"), "accuracy": 64, "reliability": 93, "bullets": 4, "magazines": 3},
    {"level": 8, "expMin": 350,   "name": _("Fanatic"), "accuracy": 65, "reliability": 93, "bullets": 4, "magazines": 3},
    {"level": 9, "expMin": 440,   "name": _("Haruspex"), "accuracy": 66, "reliability": 93, "bullets": 4, "magazines": 3},
    {"level": 10, "expMin": 540,  "name": _("Gallant"), "accuracy": 67, "reliability": 94, "bullets": 4, "magazines": 3},
    {"level": 11, "expMin": 650,  "name": _("Lord"), "accuracy": 68, "reliability": 94, "bullets": 4, "magazines": 3},
    {"level": 12, "expMin": 770,  "name": _("Sovereign"), "accuracy": 69, "reliability": 94, "bullets": 4, "magazines": 3},
    {"level": 13, "expMin": 900,  "name": _("Conqueror"), "accuracy": 70, "reliability": 95, "bullets": 4, "magazines": 3},
    {"level": 14, "expMin": 1040, "name": _("Vanguard"), "accuracy": 71, "reliability": 95, "bullets": 4, "magazines": 3},
    {"level": 15, "expMin": 1190, "name": _("Incantatrix"), "accuracy": 72, "reliability": 95, "bullets": 4, "magazines": 3},
    {"level": 16, "expMin": 1350, "name": _("White Knight"), "accuracy": 73, "reliability": 97, "bullets": 2, "magazines": 4},
    {"level": 17, "expMin": 1520, "name": _("Templar"), "accuracy": 74, "reliability": 97, "bullets": 2, "magazines": 4},
    {"level": 18, "expMin": 1700, "name": _("Paladin"), "accuracy": 75, "reliability": 97, "bullets": 2, "magazines": 4},
    {"level": 19, "expMin": 1890, "name": _("Sun Champion"), "accuracy": 76, "reliability": 97, "bullets": 2, "magazines": 4},
    {"level": 20, "expMin": 2090, "name": _("Fury"), "accuracy": 77, "reliability": 97, "bullets": 2, "magazines": 4},
    {"level": 21, "expMin": 2300, "name": _("Virtuous"), "accuracy": 78, "reliability": 98, "bullets": 2, "magazines": 4},
    {"level": 22, "expMin": 2520, "name": _("Righteous"), "accuracy": 79, "reliability": 98, "bullets": 2, "magazines": 4},
    {"level": 23, "expMin": 2750, "name": _("Luminier"), "accuracy": 80, "reliability": 98, "bullets": 2, "magazines": 4},
    {"level": 24, "expMin": 2990, "name": _("Radiant"), "accuracy": 81, "reliability": 98, "bullets": 2, "magazines": 4},
    {"level": 25, "expMin": 3240, "name": _("Defender"), "accuracy": 82, "reliability": 98, "bullets": 2, "magazines": 4},
    {"level": 26, "expMin": 3500, "name": _("Valiant"), "accuracy": 83, "reliability": 99, "bullets": 1, "magazines": 5},
    {"level": 27, "expMin": 3770, "name": _("Fearless"), "accuracy": 84, "reliability": 99, "bullets": 1, "magazines": 5},
    {"level": 28, "expMin": 4050, "name": _("Paragon"), "accuracy": 85, "reliability": 99, "bullets": 1, "magazines": 5},
    {"level": 29, "expMin": 4340, "name": _("Protector"), "accuracy": 86, "reliability": 99, "bullets": 1, "magazines": 5},
    {"level": 30, "expMin": 4640, "name": _("Herald"), "accuracy": 87, "reliability": 99, "bullets": 1, "magazines": 5},
    {"level": 31, "expMin": 4950, "name": _("Archon"), "accuracy": 88, "reliability": 99, "bullets": 1, "magazines": 5},
    {"level": 32, "expMin": 5270, "name": _("Renegade"), "accuracy": 89, "reliability": 99, "bullets": 1, "magazines": 5},
    {"level": 33, "expMin": 5600, "name": _("Avenger"), "accuracy": 90, "reliability": 99, "bullets": 1, "magazines": 5},
    {"level": 34, "expMin": 5940, "name": _("Destroyer"), "accuracy": 91, "reliability": 99, "bullets": 1, "magazines": 5},
    {"level": 35, "expMin": 6290, "name": _("Guardian"), "accuracy": 92, "reliability": 99, "bullets": 1, "magazines": 5},
    {"level": 36, "expMin": 6650, "name": _("Valkyrie"), "accuracy": 93, "reliability": 99, "bullets": 1, "magazines": 5},
    {"level": 37, "expMin": 7020, "name": _("Mystic Knight"), "accuracy": 94, "reliability": 99, "bullets": 1, "magazines": 5},
    {"level": 38, "expMin": 7400, "name": _("Saint Knight"), "accuracy": 95, "reliability": 99, "bullets": 1, "magazines": 5},
    {"level": 39, "expMin": 7790, "name": _("Holy Knight"), "accuracy": 96, "reliability": 99, "bullets": 1, "magazines": 5},
    {"level": 40, "expMin": 8200, "name": _("Angel"), "accuracy": 97, "reliability": 99, "bullets": 1, "magazines": 5},
    {"level": 41, "expMin": 9999, "name": _("Archangel"), "accuracy": 98, "reliability": 99, "bullets": 1, "magazines": 6},
    {"level": 42, "expMin": 11111, "name": _("Legend"), "accuracy": 99, "reliability": 99, "bullets": 1, "magazines": 7}
]


def get_level_info(experience):
    return next((level for level in reversed(LEVELS) if level["expMin"] <= experience), LEVELS[0])


def get_level_info_from_id(level_id):
    return next((level for level in LEVELS if level["level"] == level_id), None)


def get_higher_level():
    return get_level_info(math.inf)

