from dataclasses import dataclass
from enum import Enum

from ricochet_robots._typing import Position
from ricochet_robots.representation.robot import Color


class Name(Enum):
    """Enumeration of the names of the tokens."""

    MOON = 0
    STAR = 1
    SUN = 2
    PLANET = 3


@dataclass
class Token:
    """Representation of a token in the board."""

    name: Name
    color: Color
    position: Position
