import PIL

from puzzle import Puzzle


class SokobanPuzzle(Puzzle):
    """Summary: breaks tiles into pieces and scrambles them by flipping them"""

    def __init__(
        self,
        image: PIL.Image.Image,
        pieces_per_side: int,
        output_size: tuple[int, int] = (),
        puzzle_pos: tuple[int, int] = (0, 0),
        area: tuple[int, int] = (),
    ):
        super().__init__(image, pieces_per_side, output_size, puzzle_pos)
        self.area_for_puzzle = area
        self.image_update()
