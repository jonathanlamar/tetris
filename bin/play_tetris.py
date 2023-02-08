#!/usr/bin/env python3

from __future__ import annotations
from time import sleep, time

from pynput.keyboard import Key, KeyCode, Listener

from tetris.game import GameState
from tetris.utils import KeyPress


def onPress(key: Key | KeyCode | None) -> None:
    global KEYPRESS
    if key == Key.up:
        KEYPRESS = KeyPress.UP
    elif key == Key.down:
        KEYPRESS = KeyPress.DOWN
    elif key == Key.left:
        KEYPRESS = KeyPress.LEFT
    elif key == Key.right:
        KEYPRESS = KeyPress.RIGHT
    else:
        KEYPRESS = KeyPress.NONE


def mainLoop(game: GameState):
    global KEYPRESS
    KEYPRESS = KeyPress.NONE

    while not game.dead:
        game.update(KEYPRESS)
        KEYPRESS = KeyPress.NONE
        game.draw()
        sleep(0.15)
        if time() - game.lastUpdateTime > 0.15:
            game.update(KeyPress.DOWN)


if __name__ == "__main__":
    with Listener(on_press=onPress) as listener:
        game = GameState()
        mainLoop(game)
    print("You lose!")
