"""
Pour les class Enums
"""

import enum


class CellType(enum.Enum):
    GRASS = 1
    WALL = 2
    MOUNTAIN = 3
    WATER = 4