import os

import pygame
from PIL import Image

from helpers import EventHandler, EventTypes, get_tiles_something
from Player.player import Player
from Puzzles.flipping_puzzle import FlippingPuzzle
from Puzzles.lights_out_puzzle import LightsOut
from Puzzles.sliding_puzzle import SlidingPuzzle
from game_map import GameMap


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

    screen_size = (320, 512)
    screen = pygame.display.set_mode(screen_size)  # Start PyGame initialization.
    # This is required in order to convert PIL images into PyGame Surfaces
    pygame.init()

    running = True

    screen.fill((255, 0, 0))
    active_puzzle = switch_puzzle(current_puzzle, puzzles)
    # screen.blit(active_puzzle.image, (0, 0))
    tile_pixels = (16, 16)
    scaling_factor = 4
    tile_number = get_tiles_something(screen_size, tile_pixels, scaling_factor)  # TODO: un-tired this
    middle_tile_pixels = ((((tile_number[0]-1) * scaling_factor)//2) * tile_pixels[0], ((tile_number[1])*scaling_factor)//2 * tile_pixels[1])
    game_map = GameMap("game_map.png", tile_pixels, tile_number, scaling_factor, (0, 0))
    player = Player(scaling_factor, (2, 4))

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            player.loop(event)
            active_puzzle.loop(event)

        for event in EventHandler.get():
            if event.type == EventTypes.MAP_POSITION_UPDATE:
                screen.blit(game_map.update(event.data), (0, 0))
                screen.blit(player.image, middle_tile_pixels)
            if event.type == EventTypes.PLAYER_SPRITE_UPDATE:
                screen.blit(player.image, middle_tile_pixels)
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
