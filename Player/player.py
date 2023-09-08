from enum import Enum

import PIL
import numpy as np
import numpy.typing
import pygame
from types import SimpleNamespace
from typing import assert_never

import pygame.event

from helpers import make_2d_surface_from_array, EventHandler


class MovementDirections(Enum):
    UP = (0, 1)
    DOWN = (0, -1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)


KEYPRESS_ALTERNATIVES: dict[pygame.event.EventType, MovementDirections] = {
    **dict.fromkeys([pygame.K_w, pygame.K_UP], MovementDirections.UP),
    **dict.fromkeys([pygame.K_s, pygame.K_DOWN], MovementDirections.DOWN),
    **dict.fromkeys([pygame.K_a, pygame.K_LEFT], MovementDirections.LEFT),
    **dict.fromkeys([pygame.K_d, pygame.K_RIGHT], MovementDirections.RIGHT),
}

PLAYER_SPRITES: dict[MovementDirections, numpy.typing.NDArray] = {
    MovementDirections.UP: np.array(PIL.Image.open("Player/player_up.png")),
    MovementDirections.DOWN: np.array(PIL.Image.open("Player/player_down.png")),
    MovementDirections.LEFT: np.array(PIL.Image.open("Player/player_left.png")),
    MovementDirections.RIGHT: np.array(PIL.Image.open("Player/player_right.png")),
}


class PlayerEvents(Enum):
    SPRITE_UPDATE = 0


class Player:
    def __init__(self):
        self.image = PLAYER_SPRITES[MovementDirections.DOWN]
        self.position = numpy.array([0, 0])

    def loop(self, event: pygame.event):
        if event.type != pygame.KEYDOWN:
            return
        if all(event.key != alternatives for alternatives in KEYPRESS_ALTERNATIVES):
            return
        movement_direction = KEYPRESS_ALTERNATIVES[event.key]
        sprite = PLAYER_SPRITES[movement_direction]
        self.image = make_2d_surface_from_array(sprite)
        EventHandler.add(PlayerEvents.SPRITE_UPDATE)
