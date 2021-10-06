from copy import deepcopy
import os

import numpy as np

from config import *
from utils import *


class GameState:
    def __init__(self) -> None:
        self.board = np.zeros(BOARD_SIZE)
        self.score = 0
        self.activePiece = GameState._getRandomPiece()
        self.nextPiece = GameState._getRandomPiece()
        self.dead = False

    def update(self, keyPress: KeyPress) -> None:
        if self._checkCollision(self.activePiece):
            self.dead = True
            return

        newPiece = deepcopy(self.activePiece)
        newPiece.move(keyPress)

        if self._checkCollision(newPiece):
            newPiece = self.activePiece

        if self._checkResting(newPiece):
            self._depositPiece(newPiece)
            self._eliminateRows()
            self.activePiece = self.nextPiece
            self.nextPiece = GameState._getRandomPiece()
        else:
            self.activePiece = newPiece

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
            (np.zeros((fullRows.sum(), BOARD_SIZE[1])), self.board[~fullRows])
        )

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
        print(
            "\033[{0};1HScore: {1} Next piece: {2}".format(
                num_rows + 3, self.score, self.nextPiece.letter
            )
        )

    @staticmethod
    def _getRandomPiece() -> Tetramino:
        return np.random.choice([Eye(), Ell(), Ohh(), Zee(), Tee()])
