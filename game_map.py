import os
from typing import Sequence

import numpy as np
import PIL.Image
import pygame

from helpers import make_2d_surface_from_array


class MapSlicer:
    """Helper class for slicing into an image array"""

    def __init__(
        self,
        start_pos: tuple[int, int] | Sequence[int],
        tiles_in_slice: tuple[int, int] | Sequence[int],
        tile_pixel_size: tuple[int, int] | Sequence[int],
    ):
        self._slice_start = np.array(start_pos)
        self._slice_size = np.array(tiles_in_slice)
        self._slice_multi = np.array(tile_pixel_size)

    def shift(self, shift_amount: tuple[int, int] | Sequence[int]):
        """Shift slicing window in-place"""
        self._slice_start += shift_amount

    def get_slices(self, reverse: bool = True) -> tuple[slice, slice]:
        """Get tuple[x slice, y slice] for use in slicing

        Args:
            reverse: True by default, will give y, x slices instead of x, y
        """
        start = self._slice_start * self._slice_multi
        end = (self._slice_start + self._slice_size) * self._slice_multi
        # Done like this since type checker complains if a comprehension is used
        reverse = -1 if reverse else 1
        return (slice(start[0], end[0]), slice(start[1], end[1]))[::reverse]


class GameMap:
    """Class for handling the game's map

    Args:
        floor_image_path: Path to the image to be used as the floor texture
        deco_image_path: Path to the image to be used as the decoration
        pixels_per_tile: How many pixels per floor tile
        tiles_on_screen: How many tiles fit on screen
        scaling_factor: Scale by which the image sizes will be increased
        starting_position: Offset to start the map at
    """

    def __init__(
        self,
        floor_image_path: str | os.PathLike,
        deco_image_path: str | os.PathLike,
        pixels_per_tile: tuple[int, int] | Sequence[int],
        tiles_on_screen: tuple[int, int] | Sequence[int],
        scaling_factor: int,
        starting_position: tuple[int, int] | Sequence[int],
    ):
        self._floor_image_array = np.array(PIL.Image.open(floor_image_path))
        self._deco_image_array = np.array(PIL.Image.open(deco_image_path))
        self._map_position = MapSlicer(
            starting_position, tiles_on_screen, pixels_per_tile
        )
        self._scaling_factor = scaling_factor
        self.floor_surface: pygame.Surface = pygame.Surface((0, 0))
        self.deco_surface: pygame.Surface = pygame.Surface((0, 0))

    def update(self, shift_amount):
        self._map_position.shift(shift_amount)
        # map_slices = self._map_position.get_slices()
        # image_shape = [map_slice.stop - map_slice.start for map_slice in map_slices]
        # floor_slice = np.zeros((*image_shape, self._floor_image_array.shape[2]), int)
        # deco_slice = np.zeros((*image_shape, self._deco_image_array.shape[2]), int)
        # lower = [-min(map_slice.start, 0) for map_slice in map_slices]
        # upper = [min(image_bound - map_slice.stop, 0) + image_bound for map_slice, image_bound in zip(map_slices, image_shape)]
        # padding_shape = (*((lower, upper) for lower, upper in zip(lower_differences, upper_differences)), (0, 0))
        # floor_slice[lower[0]:upper[0], lower[1]:upper[1]] =
        # print(image_shape, [*map_slices], lower_differences, upper_differences, padding_shape, floor_slice.shape)
        # self.floor_surface = make_2d_surface_from_array(np.pad(floor_slice, padding_shape, constant_values=0)[*map_slices], scaling_factor=self._scaling_factor)
        # self.deco_surface = make_2d_surface_from_array(np.pad(deco_slice, padding_size, constant_values=0), scaling_factor=self._scaling_factor)
        self.floor_surface = make_2d_surface_from_array(
            self._floor_image_array[*self._map_position.get_slices()],
            scaling_factor=self._scaling_factor,
        )
