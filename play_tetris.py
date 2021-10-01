from __future__ import annotations
from time import sleep

from game import GameState
from pynput.keyboard import Key, Listener
from utils import KeyPress


def onPress(key: Key) -> None:
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


def mainLoop(game):
    global KEYPRESS
    KEYPRESS = KeyPress.NONE

    while not game.dead:
        game.update(KEYPRESS)
        KEYPRESS = KeyPress.NONE
        game.draw()
        sleep(0.15)


if __name__ == "__main__":
    with Listener(on_press=onPress) as listener:
        game = GameState()
        mainLoop(game)
    print("You lose!")
