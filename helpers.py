from enum import Enum, auto
from typing import Any

import numpy as np
import numpy.typing
import pygame


def make_2d_surface_from_array(
    array: numpy.typing.NDArray,
    swap_xy=True,
    color_key: tuple[int, int, int] = (0, 0, 0),
    scaling_factor: int = 1,
) -> pygame.Surface:
    """Make a 2d surface from a numpy array, accepts both RGB and RGBA arrays

    Args:
        array: Numpy NDArray of shape (n, m, 3) or (n, m, 4)
        swap_xy: By default, images from PIL need their x/y dims to be swapped
        color_key: What color to key for alpha in RGBA images, ignored for RGB images
        scaling_factor: Make the image bigger by scaling_factor
    """
    if len(array.shape) != 3 or array.shape[2] not in (3, 4):
        raise ValueError(
            f"Must be an array with shape (n, m, 3) or (n, m, 4), "
            f"received array is {array.shape}"
        )
    array = array.repeat(scaling_factor, axis=0).repeat(scaling_factor, axis=1)
    if swap_xy:
        array = np.swapaxes(array, 0, 1)
    temp_surface = pygame.surfarray.make_surface(array[:, :, :3])
    if array.shape[2] == 4:
        temp_surface.set_colorkey(color_key)
    return temp_surface


def get_tiles_something(screen_size: tuple[int, int], tile_size: tuple[int, int], scaling_factor: int):  # TODO: un-tired this
    return screen_size[0] // (tile_size[0] * scaling_factor), screen_size[1] // (tile_size[1] * scaling_factor)

class EventTypes(Enum):
    """All the event types that will be used"""

    PLAYER_SPRITE_UPDATE = auto()
    PLAYER_MOVEMENT_UPDATE = auto()
    PUZZLE_SPRITE_UPDATE = auto()
    PUZZLE_SOLVED = auto()
    MAP_POSITION_UPDATE = auto()


class Event:
    """Event class meant to mimic pygame's events

    Args:
        event_type: Event type Enum value
        event_data: Any data for the event to store. None by default

    Attributes:
        type: Event type
        data: Stored data of the event, default None
    """

    def __init__(self, event_type: Enum, event_data: Any = None):
        self.type = event_type
        self.data = event_data

    def __eq__(self, other: Enum):
        return self.type == other


class EventHandler:
    """Static event handler that stores a list of Events, then clears on read"""

    _events: list[Event] = []

    @staticmethod
    def add(event: Enum, data: Any = None) -> None:
        """Adds an event to be handled

        Args:
            event: Enum for event
            data: Data to be stored with the event
        """
        EventHandler._events.append(Event(event, data))

    @staticmethod
    def get() -> list[Event]:
        """Gets all events from the handler and clears the internal storage

        Returns:
            list[Event]
        """
        temp_list = EventHandler._events
        EventHandler._events = []
        return temp_list
