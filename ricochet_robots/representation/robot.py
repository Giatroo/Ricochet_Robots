from dataclasses import dataclass
from enum import Enum

from ricochet_robots._typing import Position


class Color(Enum):
    """Enumeration of the colors of the game.

    Some entities might have colors, like robots and tokens.
    """

    RED = 0
    GREEN = 1
    BLUE = 2
    YELLOW = 3


@dataclass
class Robot:
    """Representation of a robot in the board."""

    color: Color
    position: Position
