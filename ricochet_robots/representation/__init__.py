"""Package to store the representation of the game board and the robots.

It is used as a backend to the game entities, but does not contain any logic
or game rules.
"""

from ricochet_robots.representation.board import Board
from ricochet_robots.representation.robot import Color, Robot
from ricochet_robots.representation.token import Name, Token

__all__ = ["Board", "Robot", "Color", "Token", "Name"]
