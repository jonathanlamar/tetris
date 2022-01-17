from __future__ import annotations
from enum import Enum

import numpy as np

from config import BOARD_SIZE

MIDDLE_COL = BOARD_SIZE[1] // 2

ROTATE_MATRIX = np.array([[0, -1], [1, 0]])


class KeyPress(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4
    NONE = 5


class Tetramino:
    def __init__(self, squares: np.ndarray, pivotIndex: int, letter: str) -> None:
        self.squares = squares
        self.pivotIndex = pivotIndex
        self.letter = letter

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
            self._rotate()

    def _rotate(self) -> None:
        shift = self.squares[self.pivotIndex]
        self.squares = np.dot(self.squares - shift, ROTATE_MATRIX) + shift

    @property
    def belowSquares(self) -> np.ndarray:
        xs = np.unique(self.squares[:, 1])
        ys = [self.squares[self.squares[:, 1] == x, 0].max() + 1 for x in xs]

        return np.array(list(zip(ys, xs)))


class Eye(Tetramino):
    def __init__(self) -> None:
        super().__init__(
            squares=np.array(
                [(0, MIDDLE_COL), (1, MIDDLE_COL), (2, MIDDLE_COL), (3, MIDDLE_COL)]
            ),
            pivotIndex=1,
            letter="I",
        )


class Ell(Tetramino):
    def __init__(self) -> None:
        super().__init__(
            squares=np.array(
                [(0, MIDDLE_COL), (1, MIDDLE_COL), (2, MIDDLE_COL), (2, MIDDLE_COL + 1)]
            ),
            pivotIndex=1,
            letter="L",
        )


class Ohh(Tetramino):
    def __init__(self) -> None:
        super().__init__(
            squares=np.array(
                [
                    (0, MIDDLE_COL),
                    (0, MIDDLE_COL + 1),
                    (1, MIDDLE_COL),
                    (1, MIDDLE_COL + 1),
                ]
            ),
            pivotIndex=0,
            letter="O",
        )


class Tee(Tetramino):
    def __init__(self) -> None:
        super().__init__(
            squares=np.array(
                [(0, MIDDLE_COL), (1, MIDDLE_COL), (1, MIDDLE_COL + 1), (2, MIDDLE_COL)]
            ),
            pivotIndex=1,
            letter="T",
        )


class Zee(Tetramino):
    def __init__(self) -> None:
        super().__init__(
            squares=np.array(
                [
                    (0, MIDDLE_COL),
                    (1, MIDDLE_COL),
                    (1, MIDDLE_COL + 1),
                    (2, MIDDLE_COL + 1),
                ]
            ),
            pivotIndex=1,
            letter="Z",
        )
