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
    _robots: list[Robot]
    _tokens: list[Token]

    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.walls = np.zeros((width, height, 4), dtype=bool)
        self._robots = []
        self._tokens = []

    def add_robot(self, robot: Robot) -> None:
        """Add a robot to the board.

        It doesn't check if a robot with that particular color is already in
        the board. Also, it doesn't check if the robot is being placed in a
        valid position.

        Parameters
        ----------
        robot : Robot
            The robot to be added to the board.
        """
        self._robots.append(robot)

    def remove_robot(self, robot: Robot):
        """Remove a robot from the board.

        If the robot is not in the board, it does nothing.

        Parameters
        ----------
        robot : Robot
            The robot to be removed from the board.
        """
        self._robots.remove(robot)

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
        for robot in self._robots:
            if robot.color == color:
                return robot
        raise ValueError(f"Robot {color} not found.")

    def get_robots(self) -> list[Robot]:
        """Get a list with all the robots in the board.

        Note that this method returns a copy of the list of robots, so the
        original list is not modified.

        Returns
        -------
        list[Robot]
            A list with all the robots in the board.
        """
        return self._robots.copy()

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
        self._tokens.append(token)

    def remove_token(self, token: Token) -> None:
        """Remove a token from the board.

        Parameters
        ----------
        token : Token
            The token to be removed from the board.
        """
        self._tokens.remove(token)

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
        for token in self._tokens:
            if token.name == name and token.color == color:
                return token
        raise ValueError(f"Token {color} {name} not found.")

    def get_tokens(self) -> list[Token]:
        """Get a list with all the tokens in the board.

        Note that this method returns a copy of the list of tokens, so the
        original list is not modified.

        Returns
        -------
        list[Token]
            A list with all the tokens in the board.
        """
        return self._tokens.copy()
