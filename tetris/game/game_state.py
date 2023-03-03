import os
from copy import deepcopy
from time import time

import numpy as np

from tetris.config.config import BOARD_SIZE, BUFFER_SHAPE
from tetris.utils.utils import Ell, Eye, KeyPress, Ohh, Tee, Tetramino, Zee


class GameState:
    boardBuffer: np.ndarray
    board: np.ndarray
    score: int
    activePiece: Tetramino
    nextPiece: Tetramino
    dead: bool
    lastAdvanceTime: float

    def __init__(self) -> None:
        self.boardBuffer = np.zeros(BUFFER_SHAPE, dtype=np.uint8)
        self.board = np.zeros(BOARD_SIZE, dtype=np.uint8)
        self.score = 0
        self.activePiece = GameState._getRandomPiece()
        self.nextPiece = GameState._getRandomPiece()
        self.dead = False
        self.lastAdvanceTime = time()

    def update(self, keyPress: KeyPress) -> None:
        noOp = True
        if self._checkCollision(self.activePiece):
            self.dead = True
            noOp = False
            return

        newPiece = deepcopy(self.activePiece)
        newPiece.move(keyPress)

        if self._checkCollision(newPiece):
            noOp = False
            newPiece = self.activePiece

        if self._checkResting(newPiece):
            noOp = False
            self._depositPiece(newPiece)
            self._eliminateRows()
            self.activePiece = self.nextPiece
            self.nextPiece = GameState._getRandomPiece()
        else:
            if keyPress != KeyPress.NONE:
                noOp = False
            self.activePiece = newPiece

        if not noOp:
            self._updateBuffer()
        if keyPress == KeyPress.DOWN:
            self.lastAdvanceTime = time()

    def _checkCollision(self, newPiece: Tetramino) -> bool:
        return (
            any(newPiece.squares[:, 0] >= BOARD_SIZE[0])
            or any(newPiece.squares[:, 1] < 0)
            or any(newPiece.squares[:, 1] >= BOARD_SIZE[1])
            or any([self.board[tuple(row)] for row in newPiece.squares])
        )

    def _checkResting(self, newPiece: Tetramino) -> bool:
        return any(newPiece.squares[:, 0] == BOARD_SIZE[0] - 1) or any(
            [self.board[tuple(row)] for row in newPiece.belowSquares]
        )

    def _depositPiece(self, newPiece: Tetramino) -> None:
        for idx in newPiece.squares:
            self.board[tuple(idx)] = 1

    def _eliminateRows(self) -> None:
        fullRows = (self.board == 1).all(axis=1)
        self.score += fullRows.sum()
        self.board = np.concatenate(
            (
                np.zeros((fullRows.sum(), BOARD_SIZE[1]), dtype=np.uint8),
                self.board[~fullRows],
            )
        )

    def _updateBuffer(self) -> None:
        board = np.concatenate(
            [deepcopy(self.board).reshape((1,) + BOARD_SIZE), np.zeros((1, BOARD_SIZE[0], 1), dtype=np.uint8)], axis=2
        )
        for idx in self.activePiece.squares:
            board[0, idx[0], idx[1]] = 2
        board[0, 0, -1] = ["I", "L", "O", "T", "Z"].index(self.nextPiece.letter)
        board[0, 1, -1] = int(self.dead)
        self.boardBuffer = np.concatenate([board, self.boardBuffer[:-1, :, :]])

    def draw(self) -> None:
        os.system("clear")
        num_rows, num_cols = BOARD_SIZE
        board = deepcopy(self.board)
        for idx in self.activePiece.squares:
            board[tuple(idx)] = 1

        # This weird printing syntax is an old school way of placing text
        # at coordinates.  Unfortunately those coordinates are indexed from
        # one, so this code is pretty ugly.
        # Place a horizonal top border
        print("\033[1;1H+" + "-" * num_cols + "+")
        for i in range(2, num_rows + 2):
            # Place part of the left border
            print("\033[{0};1H|".format(i))
            for j in range(2, num_cols + 2):
                # Print X for piece.
                if board[i - 2, j - 2] > 0:
                    print("\033[{0};{1}H{2}".format(i, j, "X"))
            # Print part of the right border
            print("\033[{0};{1}H|".format(i, num_cols + 2))
        # Print bottom border
        print("\033[{0};0H+".format(num_rows + 2) + "-" * num_cols + "+")
        # Print other self info
        print("\033[{0};1HScore: {1} Next piece: {2}".format(num_rows + 3, self.score, self.nextPiece.letter))

    @staticmethod
    def _getRandomPiece() -> Tetramino:
        return np.random.choice([Eye(), Ell(), Ohh(), Zee(), Tee()])
