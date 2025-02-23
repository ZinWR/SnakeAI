import pygame
import random
from enum import Enum
from collections import namedtuple

pygame.init()
font = pygame.font.Font('arial.ttf', 25)

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

Point = namedtuple('Point', 'x, y')

# Constants
BLOCK_SIZE = 20
SPEED = 40

# RGB COLORS CUSTOMIZATION
BLACK = (0,0,0)
WHITE = (255, 255, 255)
RED = (200, 0, 0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)

class SnakeGame:
    def __init__(self, width=640 , height=480):
        self.width = width
        self.height = height

        # Display Init
        self.display = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()

        # Game State Init
        self.direction = Direction.RIGHT # Snake initially moves to the right
        self.head = Point(self.width/2, self.height/2)
        self.snake = [self.head, Point(self.head.x-BLOCK_SIZE, self.head.y),
                      Point(self.head.x-(2*BLOCK_SIZE), self.head.y)]
        self.score = 0
        self.food = None
        self._place_food()

    # Helper func
    def _place_food(self):
        x = random.randint(0, (self.width-BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(0, (self.height-BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        self.food = Point(x,y)
        if self.food in self.snake: # Make sure food doesn't overlap with snake
            self._place_food()

    def play_step(self):
        # 1. Collect user input
        # 2. Move
        # 3. Check if game over
        # 4. Place new food or just move
        # 5. Update UI & clock
        self._update_ui()
        self.clock.tick(SPEED)
    
        # 6. Return update (game over & score)
        game_over = False
        return game_over, self.score

    def _update_ui(self):
        self.display.fill(BLACK)

        # Draw snake
        for pt in self.snake:
            pygame.draw(self.display, BLUE1, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw(self.display, BLUE2, pygame.Rect(pt.x+4, pt.y+4, 12, 12))

        # Draw food
        pygame.draw(self.display, RED, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))

        # Score upper left
        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip() # update/render on the screen

if __name__ == '__main__':
    game = SnakeGame()

    # Game Loop
    while True:
        game_over, score = game.play_step()

        # Break if Game Over
        if game_over == True:
            break

    print('Final Score', score)
    pygame.quit()