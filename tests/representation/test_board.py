from itertools import product

import pytest

from ricochet_robots.representation import Board, Color, Name, Robot, Token


def test_initialization():
    board = Board(3, 3)

    assert board.width == 3
    assert board.height == 3
    assert board.walls.shape == (3, 3, 4)
    assert board.robots.shape == (3, 3)
    assert board.tokens.shape == (3, 3)
    assert not board._color_to_robots
    assert not board._color_name_to_token
    for i, j in product(range(3), range(3)):
        assert board.robots[i, j] is None
        assert board.tokens[i, j] is None


@pytest.mark.parametrize(
    "robot",
    [
        pytest.param(Robot(Color.BLUE, (1, 1)), id="blue-1-1"),
        pytest.param(Robot(Color.BLUE, (0, 1)), id="blue-0-1"),
        pytest.param(Robot(Color.RED, (2, 2)), id="red-2-2"),
    ],
)
def test_adding_a_robot(robot: Robot):
    board = Board(3, 3)
    board.add_robot(robot)

    assert len(board.get_robots()) == 1
    assert board.get_robots()[0] == robot
    assert board.robots[robot.position] == robot


def test_adding_multiple_robots():
    board = Board(3, 3)
    robot1 = Robot(Color.BLUE, (1, 1))
    robot2 = Robot(Color.RED, (2, 2))
    board.add_robot(robot1)
    board.add_robot(robot2)

    assert len(board.get_robots()) == 2
    assert board.get_robots() == [robot1, robot2]
    assert board.robots[robot1.position] == robot1
    assert board.robots[robot2.position] == robot2


def test_adding_multiple_robots_in_the_same_position():
    board = Board(3, 3)
    robot1 = Robot(Color.BLUE, (1, 1))
    robot2 = Robot(Color.RED, (1, 1))
    board.add_robot(robot1)

    with pytest.raises(ValueError):
        board.add_robot(robot2)


def test_adding_multiple_robots_with_the_same_color():
    board = Board(3, 3)
    robot1 = Robot(Color.BLUE, (1, 1))
    robot2 = Robot(Color.BLUE, (2, 2))
    board.add_robot(robot1)
    board.add_robot(robot2)

    assert len(board.get_robots()) == 1
    assert board.get_robots() == [robot2]
    assert board.robots[robot1.position] is None
    assert board.robots[robot2.position] == robot2


def test_remove_unexistent_robot():
    board = Board(3, 3)
    robot = Robot(Color.BLUE, (1, 1))

    with pytest.warns(UserWarning):
        board.remove_robot(robot)


@pytest.mark.parametrize(
    "robot",
    [
        pytest.param(Robot(Color.BLUE, (1, 1)), id="blue-1-1"),
        pytest.param(Robot(Color.BLUE, (0, 1)), id="blue-0-1"),
        pytest.param(Robot(Color.RED, (2, 2)), id="red-2-2"),
    ],
)
def test_remove_robot(robot: Robot):
    board = Board(3, 3)
    board.add_robot(robot)
    board.remove_robot(robot)
    position = robot.position

    assert not board.get_robots()
    assert not board._color_to_robots
    assert board.robots[position] is None


@pytest.mark.parametrize(
    "robot",
    [
        pytest.param(Robot(Color.BLUE, (1, 1)), id="blue-1-1"),
        pytest.param(Robot(Color.BLUE, (0, 1)), id="blue-0-1"),
        pytest.param(Robot(Color.RED, (2, 2)), id="red-2-2"),
    ],
)
def test_get_robot(robot: Robot):
    board = Board(3, 3)
    board.add_robot(robot)

    assert board.get_robot(robot.color) == robot


def test_get_unexistent_robot():
    board = Board(3, 3)

    with pytest.raises(ValueError):
        board.get_robot(Color.BLUE)


def test_get_robot_with_multiple_robots():
    board = Board(3, 3)
    robot1 = Robot(Color.BLUE, (1, 1))
    robot2 = Robot(Color.RED, (2, 2))
    board.add_robot(robot1)
    board.add_robot(robot2)

    assert board.get_robot(Color.BLUE) == robot1
    assert board.get_robot(Color.RED) == robot2


def test_get_robots():
    board = Board(3, 3)
    robot1 = Robot(Color.BLUE, (1, 1))
    robot2 = Robot(Color.RED, (2, 2))
    board.add_robot(robot1)
    board.add_robot(robot2)

    assert board.get_robots() == [robot1, robot2]


def test_get_robots_empty():
    board = Board(3, 3)

    assert not board.get_robots()


@pytest.mark.parametrize(
    "token",
    [
        pytest.param(Token(Name.MOON, Color.BLUE, (1, 1)), id="moon-blue-1-1"),
        pytest.param(Token(Name.MOON, Color.BLUE, (0, 1)), id="moon-blue-0-1"),
        pytest.param(Token(Name.MOON, Color.RED, (2, 2)), id="moon-red-2-2"),
        pytest.param(Token(Name.STAR, Color.BLUE, (1, 1)), id="star-blue-1-1"),
    ],
)
def test_adding_a_token(token: Token):
    board = Board(3, 3)
    board.add_token(token)

    assert len(board.get_tokens()) == 1
    assert board.get_tokens()[0] == token
    assert board.tokens[token.position] == token


def test_adding_multiple_tokens():
    board = Board(3, 3)
    token1 = Token(Name.MOON, Color.BLUE, (1, 1))
    token2 = Token(Name.STAR, Color.RED, (2, 2))
    board.add_token(token1)
    board.add_token(token2)

    assert len(board.get_tokens()) == 2
    assert board.get_tokens() == [token1, token2]
    assert board.tokens[token1.position] == token1
    assert board.tokens[token2.position] == token2


def test_adding_multiple_tokens_in_the_same_position():
    board = Board(3, 3)
    token1 = Token(Name.MOON, Color.BLUE, (1, 1))
    token2 = Token(Name.STAR, Color.RED, (1, 1))
    board.add_token(token1)

    with pytest.raises(ValueError):
        board.add_token(token2)


def test_adding_multiple_tokens_with_the_same_color_and_name():
    board = Board(3, 3)
    token1 = Token(Name.MOON, Color.BLUE, (1, 1))
    token2 = Token(Name.MOON, Color.BLUE, (2, 2))
    board.add_token(token1)
    board.add_token(token2)

    assert len(board.get_tokens()) == 1
    assert board.get_tokens() == [token2]
    assert board.tokens[token1.position] is None
    assert board.tokens[token2.position] == token2


def test_adding_multiple_tokens_with_the_same_color_but_different_names():
    board = Board(3, 3)
    token1 = Token(Name.MOON, Color.BLUE, (1, 1))
    token2 = Token(Name.STAR, Color.BLUE, (2, 2))
    board.add_token(token1)
    board.add_token(token2)

    assert len(board.get_tokens()) == 2
    assert board.get_tokens() == [token1, token2]
    assert board.tokens[token1.position] == token1
    assert board.tokens[token2.position] == token2


def test_remove_unexistent_token():
    board = Board(3, 3)
    token = Token(Name.MOON, Color.BLUE, (1, 1))

    with pytest.warns(UserWarning):
        board.remove_token(token)


def test_remove_token():
    board = Board(3, 3)
    token = Token(Name.MOON, Color.BLUE, (1, 1))
    board.add_token(token)
    board.remove_token(token)
    position = token.position

    assert not board.get_tokens()
    assert not board._color_name_to_token
    assert board.tokens[position] is None


def test_get_token():
    board = Board(3, 3)
    token = Token(Name.MOON, Color.BLUE, (1, 1))
    board.add_token(token)

    assert board.get_token(Name.MOON, Color.BLUE) == token


def test_get_unexistent_token():
    board = Board(3, 3)

    with pytest.raises(ValueError):
        board.get_token(Name.MOON, Color.BLUE)


def test_get_token_with_multiple_tokens():
    board = Board(3, 3)
    token1 = Token(Name.MOON, Color.BLUE, (1, 1))
    token2 = Token(Name.STAR, Color.RED, (2, 2))
    board.add_token(token1)
    board.add_token(token2)

    assert board.get_token(Name.MOON, Color.BLUE) == token1
    assert board.get_token(Name.STAR, Color.RED) == token2


def test_get_tokens():
    board = Board(3, 3)
    token1 = Token(Name.MOON, Color.BLUE, (1, 1))
    token2 = Token(Name.STAR, Color.RED, (2, 2))
    board.add_token(token1)
    board.add_token(token2)

    assert board.get_tokens() == [token1, token2]


def test_get_tokens_empty():
    board = Board(3, 3)

    assert not board.get_tokens()
