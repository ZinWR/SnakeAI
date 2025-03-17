import pygame
import random
from enum import Enum
from collections import namedtuple
import numpy as np

pygame.init()
font = pygame.font.Font('arial.ttf', 25)

########## AI Agent Implementation Reiteration
## Frameworks
# Reward: eat_food (+10), game_over (-10), else (0)
# Action: [1,0,0] -> straight, [0,1,0] -> right turn, [0,0,1] -> left turn --> [straight, right, left]

# TODO: build out these
# reset 
# reward
# play(action) -> direction
# game_iteration
# is_collision

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

Point = namedtuple('Point', 'x, y')

# Constants
BLOCK_SIZE = 20
SPEED = 20

# RGB COLORS CUSTOMIZATION
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (200, 0, 0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)

class SnakeGameAI:
    def __init__(self, width=640, height=480):
        self.width = width
        self.height = height

        # Display Init
        self.display = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()
        self.reset()

        # Game State Init
        self.direction = Direction.RIGHT  # Snake initially moves to the right
        self.head = Point(self.width / 2, self.height / 2)
        self.snake = [self.head, Point(self.head.x - BLOCK_SIZE, self.head.y),
                      Point(self.head.x - (2 * BLOCK_SIZE), self.head.y)]
        self.score = 0
        self.food = None
        self._place_food()

    def reset(self):
        # Game State Init
        self.direction = Direction.RIGHT  # Snake initially moves to the right
        self.head = Point(self.width / 2, self.height / 2)
        self.snake = [self.head, Point(self.head.x - BLOCK_SIZE, self.head.y),
                      Point(self.head.x - (2 * BLOCK_SIZE), self.head.y)]
        self.score = 0
        self.food = None
        self._place_food()
        self.frame_iteration = 0

    # Helper func
    def _place_food(self):
        x = random.randint(0, (self.width - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(0, (self.height - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake:  # Make sure food doesn't overlap with snake
            self._place_food()

    def play_step(self, action):
        self.frame_iteration += 1

        # 1. Collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # 2. Move & Update snake head
        self._move(action)
        self.snake.insert(0, self.head)

        # 3. Check if game over or snake going nowhere (nothing happen)
        reward = 0
        game_over = False
        if self.is_collision() or self.frame_iteration > 100*len(self.snake):
            game_over = True
            reward = -10
            return reward, game_over, self.score

        # 4. Place new food or just move
        if self.head == self.food:
            self.score += 1
            reward = 10
            self._place_food()
        else:
            self.snake.pop()

        # 5. Update UI & clock
        self._update_ui()
        self.clock.tick(SPEED)

        # 6. Return update (game over & score)
        return reward, game_over, self.score
    
    def is_collision(self, pt=None):
        if pt is None:
            pt = self.head

        # check for boundary
        if pt.x > self.width - BLOCK_SIZE or pt.x < 0 or pt.y > self.height - BLOCK_SIZE or pt.y < 0:
            return True

        # check for self
        if pt in self.snake[1:]:
            return True
        
        return False

    def _update_ui(self):
        self.display.fill(BLACK)

        # Draw snake
        for pt in self.snake:
            pygame.draw.rect(self.display, BLUE1, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, BLUE2, pygame.Rect(pt.x + 4, pt.y + 4, 12, 12))

        # Draw food (Fixed line)
        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))

        # Score upper left
        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()  # update/render on the screen

    def _move(self, action):
        # [straight, right, left]
        clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx = clock_wise.index(self.direction)

        if np.array_equal(action, [1,0,0]):
            new_direction = clock_wise[idx] # no change
        
        elif np.array_equal(action, [0,1,0]):
            next_idx = (idx + 1) % 4
            new_direction = clock_wise[idx] # right turn r -> d -> l -> u
        
        else: # [0,0,1]
            next_idx = (idx - 1) % 4
            new_direction = clock_wise[idx] # left turn r -> u -> l -> d

        self.direction = new_direction

        x = self.head.x
        y = self.head.y
        if self.direction == Direction.RIGHT:
            x += BLOCK_SIZE
        if self.direction == Direction.LEFT:
            x -= BLOCK_SIZE
        if self.direction == Direction.UP:
            y -= BLOCK_SIZE
        if self.direction == Direction.DOWN:
            y += BLOCK_SIZE

        self.head = Point(x,y)

# Main Game
# if __name__ == '__main__':
#     game = SnakeGameAI()

#     # Game Loop
#     while True:
#         game_over, score = game.play_step()

#         # Break if Game Over
#         if game_over:
#             break

#     print('Final Score', score)
#     pygame.quit()