from enum import Enum
from typing import Any

import pygame
import numpy as np
import numpy.typing


def make_2d_surface_from_array(array: numpy.typing.NDArray, swap_axes=True,
                               color_key: tuple[int, int, int] = (0, 0, 0)) -> pygame.Surface:
    """Make a 2d surface from a numpy array

    Accepts both RGB and RGBA arrays

    Arguments:
        array: Numpy NDArray of shape (n, m, 3) or (n, m, 4)
        swap_axes: By default, images from PIL need their x/y dimensions to be swapped
        color_key: What color to use as the alpha for RGBA images, ignored for RGB images

    """
    if len(array.shape) != 3 or array.shape[2] not in (3, 4):
        raise ValueError(f"Must be an array with shape (n, m, 3) or (n, m, 4). Received array is {array.shape}")
    if swap_axes:
        axes_swap = (0, 1)
    else:
        axes_swap = (0, 0)
    if array.shape[2] == 3:
        return pygame.surfarray.make_surface(np.swapaxes(array, *axes_swap))
    elif array.shape[2] == 4:
        temp_surface = pygame.surfarray.make_surface(np.swapaxes(array[:, :, :3], *axes_swap))
        temp_surface.set_colorkey(color_key)
        return temp_surface


class Event:
    def __init__(self, event):
        self.event = event
        self.type = event  # Change later if we want Event to store any actual data

    def __eq__(self, other):
        return self.event == other


class EventHandler:
    """Simple event handler that stores event enums in a list, then clears it on read"""
    _events: list[Event] = []

    @staticmethod
    def add(event: Enum) -> None:
        EventHandler._events.append(Event(event))

    @staticmethod
    def get() -> list[Event]:
        temp_list = EventHandler._events
        EventHandler._events = []
        return temp_list
