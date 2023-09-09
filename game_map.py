import numpy as np
import PIL.Image
from helpers import make_2d_surface_from_array


class MapSlicer:
    def __init__(self, start_pos: tuple[int, int], slice_tile_size: tuple[int, int], tile_size: tuple[int, int]):
        self._slice_start = start_pos
        self._slice_size = slice_tile_size
        self._slice_multi = tile_size

    def shift(self, shift_amount: tuple[int, int]):
        self._slice_start = tuple(self._slice_start[i] + shift for i, shift in enumerate(shift_amount))

    @property
    def slices(self):
        return tuple(slice(start * multi, (start + size) * multi) for start, size, multi in zip(self._slice_start, self._slice_size, self._slice_multi))


class GameMap:
    def __init__(self, image_path: str, pixels_per_tile: tuple[int, int], tiles_on_screen: tuple[int, int], scaling_factor: int):
        self._map_image_array = np.array(PIL.Image.open(image_path))
        self._map_position = MapSlicer((0, 0), tiles_on_screen, pixels_per_tile)
        self._scaling_factor = scaling_factor

    def update(self, shift_amount):
        self._map_position.shift((shift_amount[0], shift_amount[1] * -1))
        return make_2d_surface_from_array(self._map_image_array[*reversed(self._map_position.slices)], scaling_factor=self._scaling_factor)
