import os

import numpy as np
import pygame
from PIL import Image

from game_map import GameMap
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

    screen_size = np.array((320, 512))
    screen = pygame.display.set_mode(screen_size)  # Start PyGame initialization.
    # This is required in order to convert PIL images into PyGame Surfaces
    pygame.init()

    running = True

    screen.fill((255, 0, 0))
    # active_puzzle = switch_puzzle(current_puzzle, puzzles)
    # screen.blit(active_puzzle.image, (0, 0))
    tile_pixel_size = np.array((16, 16))
    scaling_factor = 4
    fitting_tile_amount = np.array(screen_size) // (
        np.array(tile_pixel_size) * scaling_factor
    )
    middle_tile_location = (fitting_tile_amount // 2) * tile_pixel_size * scaling_factor
    game_map = GameMap(
        "game_map.png",
        "game_map.png",
        tile_pixel_size,
        fitting_tile_amount,
        scaling_factor,
        (0, 0),
    )
    player = Player(scaling_factor, (2, 4))

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            player.loop(event)
            # active_puzzle.loop(event)

        for event in EventHandler.get():
            if event.type == EventTypes.MAP_POSITION_UPDATE:
                game_map.update(event.data)
                screen.blit(game_map.floor_surface, (0, 0))
                screen.blit(player.image, middle_tile_location)
            if event.type == EventTypes.PLAYER_SPRITE_UPDATE:
                screen.blit(player.image, middle_tile_location)
            if event.type == EventTypes.INTERACTION_EVENT:
                print(event.data)
            #     if event == PlayerEvents.SPRITE_UPDATE:
            #         screen.blit(player.image, (0, 0))
            # if event.type == EventTypes.PUZZLE_SPRITE_UPDATE:
            #     screen.blit(active_puzzle.image, (0, 0))
            # if event.type == EventTypes.PUZZLE_SOLVED:
            #     current_puzzle += 1
            #     active_puzzle = switch_puzzle(current_puzzle, puzzles)

        pygame.display.flip()
