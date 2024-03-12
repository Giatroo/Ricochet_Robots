import warnings

import numpy as np

from ricochet_robots.representation.robot import Color, Robot
from ricochet_robots.representation.token import Name, Token


class Board:
    """Class representing the board of the game.

    Attributes
    ----------
    width : int
        The width of the board.
    height : int
        The height of the board.
    walls : np.ndarray
        A 3D array representing the walls of the board. It is a boolean array
        with shape (width, height, 4), where the last dimension represents the
        walls in the following order: right, down, left, up. For example, if
        walls[i, j] is [True, False, False, True], it means that there are
        walls to the right and up of the cell (i, j).
    """

    width: int
    height: int
    walls: np.ndarray
    robots: np.ndarray
    tokens: np.ndarray
    _color_to_robots: dict[Color, Robot]
    _color_name_to_token: dict[tuple[Color, Name], Token]

    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.walls = np.zeros((width, height, 4), dtype=bool)
        self.robots = np.full((width, height), None, dtype=object)
        self.tokens = np.full((width, height), None, dtype=object)

        self._color_to_robots = {}
        self._color_name_to_token = {}

    def add_robot(self, robot: Robot) -> None:
        """Add a robot to the board.

        If a robot with the same color is already in the board, it replaces it.

        Parameters
        ----------
        robot : Robot
            The robot to be added to the board.

        Raises
        ------
        ValueError
            If the robot is being placed in a position where there is already a
            token or another robot.
        """
        color = robot.color
        if old_robot := self._color_to_robots.get(color):
            self.remove_robot(old_robot)

        self._color_to_robots[color] = robot
        position = robot.position
        if self.robots[position] is not None:
            raise ValueError(f"Position {position} already occupied.")

        self.robots[position] = robot

    def remove_robot(self, robot: Robot):
        """Remove a robot from the board.

        If the robot is not in the board, it does nothing (just warns the user).

        Parameters
        ----------
        robot : Robot
            The robot to be removed from the board.
        """
        old_robot = self._color_to_robots.pop(robot.color, None)
        if not old_robot:
            warnings.warn(
                f"Trying to remove {robot.color.name.title()} robot, but it's "
                " not on the board."
            )
            return

        if self.robots[robot.position] != robot:
            msg = (
                f"Trying to remove {robot.color.name.title()} robot from "
                f"position {robot.position}, but there's no robot in such "
                f"position. "
                f"(The old robot is in position {old_robot.position})"
            )
            warnings.warn(msg)
        self.robots[robot.position] = None

    def get_robot(self, color: Color) -> Robot:
        """Get the color with the specified color.

        Parameters
        ----------
        color : Color
            The color of the robot to be retrieved.

        Returns
        -------
        Robot
            The robot with the specified color.

        Raises
        ------
        ValueError
            If there is no robot with the specified color.
        """
        if robot := self._color_to_robots.get(color):
            return robot
        raise ValueError(f"{color.name.title()} robot not found.")

    def get_robots(self) -> list[Robot]:
        """Get a list with all the robots in the board.

        Note that this method returns a copy of the list of robots, so the
        original list is not modified.

        Returns
        -------
        list[Robot]
            A list with all the robots in the board.
        """
        return list(self._color_to_robots.values()).copy()

    def add_token(self, token: Token) -> None:
        """Add a token to the board.

        It doesn't check if a token with that particular name and color is
        already in the board. Also, it doesn't check if the token is being
        placed in a valid position.

        Parameters
        ----------
        token : Token
            The token to be added to the board.
        """
        color = token.color
        name = token.name
        if old_token := self._color_name_to_token.get((color, name), None):
            self.remove_token(old_token)

        self._color_name_to_token[(color, name)] = token
        position = token.position
        if self.tokens[position] is not None:
            raise ValueError(f"Position {position} already occupied.")

        self.tokens[position] = token

    def remove_token(self, token: Token) -> None:
        """Remove a token from the board.

        Parameters
        ----------
        token : Token
            The token to be removed from the board.
        """
        old_token = self._color_name_to_token.pop(
            (token.color, token.name), None
        )
        if not old_token:
            warnings.warn(
                f"Trying to remove {token.color.name.title()} "
                f"{token.name.name.title()}, but it's  not on the board."
            )
            return

        if self.tokens[token.position] != token:
            msg = (
                f"Trying to remove {token.color.name.title()} "
                f"{token.name.name.title()} from position {token.position}, "
                "but there's no robot in such position. "
                f"(The old robot is in position {old_token.position})"
            )
            warnings.warn(msg)
        self.tokens[token.position] = None

    def get_token(self, name: Name, color: Color) -> Token:
        """Get the token with the specified name and color.

        Parameters
        ----------
        name : Name
            Name of the token.
        color : Color
            Color of the token.

        Returns
        -------
        Token
            The token with the specified name and color.

        Raises
        ------
        ValueError
            If there is no token with the specified name and color.
        """
        if token := self._color_name_to_token.get((color, name), None):
            return token
        raise ValueError(
            f"{color.name.title()} {name.name.title()} token not found."
        )

    def get_tokens(self) -> list[Token]:
        """Get a list with all the tokens in the board.

        Note that this method returns a copy of the list of tokens, so the
        original list is not modified.

        Returns
        -------
        list[Token]
            A list with all the tokens in the board.
        """
        return list(self._color_name_to_token.values()).copy()
