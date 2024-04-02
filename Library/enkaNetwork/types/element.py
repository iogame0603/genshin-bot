from .base import BaseEnum

class ElementColor(BaseEnum):
    ICE = 0x99FFFF
    FIRE = 0xFF9999
    WIND = 0x80FFD7
    WATER = 0x80C0FF
    ROCK = 0xFFE699
    ELECTRIC = 0xFFACFF
    GRASS = 0x99FF88

    NONE = 0x000000

class ElementType(BaseEnum):
    ICE = "Ice"
    FIRE = "Fire"
    WIND = "Wind"
    WATER = "Water"
    ROCK = "Rock"
    ELECTRIC = "Electric"
    GRASS = "Grass"

    NONE = "None"