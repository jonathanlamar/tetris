from __future__ import annotations
from enum import Enum
from config import BOARD_SIZE
import numpy as np

MIDDLE_COL = BOARD_SIZE[1] // 2

ROTATE_MATRIX = np.array([[0, -1], [1, 0]])


class KeyPress(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4
    NONE = 5


class Tetramino:
    def __init__(self, squares: np.ndarray) -> None:
        self.squares = squares

    # FIXME: Still shifts squares around
    def rotate(self) -> None:
        shift = self.squares.min(axis=0)
        self.squares = np.dot(self.squares - shift, ROTATE_MATRIX) + shift

    def move(self, direction: KeyPress) -> None:
        if direction == KeyPress.DOWN:
            self.squares[:, 0] += 2
        elif direction == KeyPress.LEFT:
            self.squares[:, 1] -= 1
        elif direction == KeyPress.RIGHT:
            self.squares[:, 1] += 1
        elif direction == KeyPress.NONE:
            self.squares[:, 0] += 1
        elif direction == KeyPress.UP:
            self.rotate()

    @property
    def belowSquares(self) -> np.ndarray:
        xs = np.unique(self.squares[:, 1])
        ys = [self.squares[self.squares[:, 1] == x, 0].max() + 1 for x in xs]

        return np.array(list(zip(ys, xs)))


class Eye(Tetramino):
    def __init__(self) -> None:
        super().__init__(
            np.array(
                [(0, MIDDLE_COL), (1, MIDDLE_COL), (2, MIDDLE_COL), (3, MIDDLE_COL)]
            )
        )


class Ell(Tetramino):
    def __init__(self) -> None:
        super().__init__(
            np.array(
                [(0, MIDDLE_COL), (1, MIDDLE_COL), (2, MIDDLE_COL), (2, MIDDLE_COL + 1)]
            )
        )


class Square(Tetramino):
    def __init__(self) -> None:
        super().__init__(
            np.array(
                [
                    (0, MIDDLE_COL),
                    (0, MIDDLE_COL + 1),
                    (1, MIDDLE_COL),
                    (1, MIDDLE_COL + 1),
                ]
            )
        )


class Tee(Tetramino):
    def __init__(self) -> None:
        super().__init__(
            np.array(
                [(0, MIDDLE_COL), (1, MIDDLE_COL), (1, MIDDLE_COL + 1), (2, MIDDLE_COL)]
            )
        )


class Zee(Tetramino):
    def __init__(self) -> None:
        super().__init__(
            np.array(
                [
                    (0, MIDDLE_COL),
                    (1, MIDDLE_COL),
                    (1, MIDDLE_COL + 1),
                    (2, MIDDLE_COL + 1),
                ]
            )
        )
