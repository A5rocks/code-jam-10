import os
import random

import pygame
from PIL import Image

from helpers import make_2d_surface_from_array
from Puzzles.flipping_puzzle import FlippingPuzzle
from Puzzles.lights_out_puzzle import LightsOut
from Puzzles.sliding_puzzle import SlidingPuzzle
from Puzzles.sokoban_puzzle import SokobanPuzzle


def switch_puzzle(puzzle_index, puzzle_list: list):
    """Changes the active puzzle"""
    my_image = Image.open(puzzle_list[puzzle_index][1])
    my_pieces = puzzle_list[puzzle_index][2]
    my_puzzle = puzzle_list[puzzle_index][0](my_image, my_pieces, (380, 500))
    return my_puzzle


if __name__ == "__main__":
    os.chdir(os.path.dirname(__file__))
    current_puzzle = 0
    puzzles = [
        (FlippingPuzzle, "sample_images/Monalisa.png", 4),
        (SlidingPuzzle, "sample_images/Monalisa.png", 4),
        (LightsOut, "sample_images/Monalisa.png", 4),
    ]

    screen = pygame.display.set_mode(
        (380, 500), pygame.FULLSCREEN
    )  # Start PyGame initialization.
    # This is required in order to convert PIL images into PyGame Surfaces
    pygame.init()

    running = True

    screen.fill((255, 0, 0))
    sokoban = SokobanPuzzle(
        Image.open("sample_images/Monalisa.png"), 4, (500, 500)
    )  # third parameter is the size of the area we want to generate the pieces in
    print(type(sokoban.image))  # fix resize
    for i in sokoban.orderlist:
        randX = random.randint(
            sokoban.puzzle_x, sokoban.puzzle_x + sokoban.area_for_puzzle[0]
        )
        randY = random.randint(
            sokoban.puzzle_y, sokoban.puzzle_y + sokoban.area_for_puzzle[1]
        )
        pos = (randX, randY)  # Fix so no puzzles overlap
        img = make_2d_surface_from_array(sokoban.pieces[i].image)
        screen.blit(img, pos)  # make movable
    """active_puzzle = switch_puzzle(current_puzzle, puzzles)
    screen.blit(active_puzzle.image, (0, 0))"""

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            """active_puzzle.loop(event)

        if puzzle.Puzzle.UPDATE in active_puzzle.event:
            screen.blit(active_puzzle.image, (0, 0))
            active_puzzle.event.remove(puzzle.Puzzle.UPDATE)

        if puzzle.Puzzle.SOLVED in active_puzzle.event:
            current_puzzle += 1
            active_puzzle = switch_puzzle(current_puzzle, puzzles)"""

        pygame.display.flip()
