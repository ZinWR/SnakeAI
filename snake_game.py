import pygame
import random

pygame.init()

class SnakeGame:
    def __init__(self, width=640 , height=480):
        self.width = width
        self.height = height
        # Display Init

        # Game State Init

    def play_step(self):
        pass

if __name__ == '__main__':
    game = SnakeGame()

    # Game Loop
    while True:
        game.play_step()

        # Break if Game Over
        pass

    pygame.quit()