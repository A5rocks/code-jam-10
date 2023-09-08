import os

import pygame
from PIL import Image

from helpers import EventHandler, EventTypes
from Player.player import Player
from Puzzles.flipping_puzzle import FlippingPuzzle
from Puzzles.lights_out_puzzle import LightsOut
from Puzzles.sliding_puzzle import SlidingPuzzle


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

    screen = pygame.display.set_mode((380, 500))  # Start PyGame initialization.
    # This is required in order to convert PIL images into PyGame Surfaces
    pygame.init()

    running = True

    screen.fill((255, 0, 0))
    active_puzzle = switch_puzzle(current_puzzle, puzzles)
    screen.blit(active_puzzle.image, (0, 0))
    player = Player()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # player.loop(event)
            active_puzzle.loop(event)

        for event in EventHandler.get():
            #     if event == PlayerEvents.SPRITE_UPDATE:
            #         screen.blit(player.image, (0, 0))
            if event.type == EventTypes.PUZZLE_SPRITE_UPDATE:
                screen.blit(active_puzzle.image, (0, 0))
            if event.type == EventTypes.PUZZLE_SOLVED:
                current_puzzle += 1
                active_puzzle = switch_puzzle(current_puzzle, puzzles)

        pygame.display.flip()
