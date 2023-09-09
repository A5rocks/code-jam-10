from enum import Enum

import numpy as np
import numpy.typing
import PIL
import pygame
import pygame.event

from helpers import EventHandler, EventTypes, make_2d_surface_from_array


class MovementDirections(Enum):
    """Player movement directions enum"""

    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)
    NULL = (0, 0)


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


class Player:
    """Main player class"""

    def __init__(self, scaling_factor, start_pos):
        self.image = PLAYER_SPRITES[MovementDirections.DOWN]
        self.position = start_pos
        self._scaling_factor = scaling_factor
        self._collision_map = np.array(PIL.Image.open("collision_map.png")).swapaxes(
            0, 1
        )

    def loop(self, event: pygame.event.EventType):
        """Player update method

        Args:
            event:

        Returns:

        """
        if event.type != pygame.KEYDOWN:
            return
        if all(event.key != alternatives for alternatives in KEYPRESS_ALTERNATIVES):
            return
        movement_direction = KEYPRESS_ALTERNATIVES[event.key]
        sprite = PLAYER_SPRITES[movement_direction]
        self.image = make_2d_surface_from_array(
            sprite, scaling_factor=self._scaling_factor
        )
        if self._collision_map[
            self.position[0] + movement_direction.value[0],
            self.position[1] + movement_direction.value[1],
            0,
        ]:
            movement_direction = MovementDirections.NULL
        elif self._collision_map[
            self.position[0] + movement_direction.value[0],
            self.position[1] + movement_direction.value[1],
            1,
        ]:
            movement_direction = MovementDirections.NULL
            EventHandler.add(
                EventTypes.INTERACTION_EVENT,
                (
                    self.position[0] + movement_direction.value[0],
                    self.position[1] + movement_direction.value[1],
                ),
            )
        self.position = (
            self.position[0] + movement_direction.value[0],
            self.position[1] + movement_direction.value[1],
        )
        EventHandler.add(EventTypes.PLAYER_SPRITE_UPDATE)
        EventHandler.add(EventTypes.MAP_POSITION_UPDATE, movement_direction.value)
