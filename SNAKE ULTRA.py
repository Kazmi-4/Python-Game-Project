import pygame
import sys
import random
import os

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20

# Colors
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Clock to control the game speed
clock = pygame.time.Clock()

# Asset paths
ASSET_PATH = os.path.join(os.path.dirname(__file__), 'assets')
snake_segment_img_path = os.path.join(ASSET_PATH, "snake_segment.png")
food_img_path = os.path.join(ASSET_PATH, "food.png")
background_img_path = os.path.join(ASSET_PATH, "background.png")

# Load assets
snake_segment_img = pygame.image.load(snake_segment_img_path)  # Green square
snake_segment_img = pygame.transform.scale(snake_segment_img, (CELL_SIZE, CELL_SIZE))

food_img = pygame.image.load(food_img_path)  # Red circle/apple
food_img = pygame.transform.scale(food_img, (CELL_SIZE, CELL_SIZE))

background_img = pygame.image.load(background_img_path)  # Blue texture
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

# Snake initialization
snake = [(100, 100), (80, 100), (60, 100)]  # Initial snake positions (3 segments)
snake_dir = (CELL_SIZE, 0)  # Initial direction (moving right)

# Food initialization
food = (random.randint(0, (WIDTH - CELL_SIZE) // CELL_SIZE) * CELL_SIZE,
        random.randint(0, (HEIGHT - CELL_SIZE) // CELL_SIZE) * CELL_SIZE)

def draw_snake(snake):
    for segment in snake:
        screen.blit(snake_segment_img, segment)

def draw_food(food):
    screen.blit(food_img, food)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Controls
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and snake_dir != (0, CELL_SIZE):
        snake_dir = (0, -CELL_SIZE)
    if keys[pygame.K_DOWN] and snake_dir != (0, -CELL_SIZE):
        snake_dir = (0, CELL_SIZE)
    if keys[pygame.K_LEFT] and snake_dir != (CELL_SIZE, 0):
        snake_dir = (-CELL_SIZE, 0)
    if keys[pygame.K_RIGHT] and snake_dir != (-CELL_SIZE, 0):
        snake_dir = (CELL_SIZE, 0)

    # Move snake
    new_head = (snake[0][0] + snake_dir[0], snake[0][1] + snake_dir[1])
    snake = [new_head] + snake[:-1]

    # Check for collisions
    if new_head in snake[1:] or \
       new_head[0] < 0 or new_head[1] < 0 or \
       new_head[0] >= WIDTH or new_head[1] >= HEIGHT:
        pygame.quit()
        sys.exit()

    # Check if snake eats food
    if new_head == food:
        snake.append(snake[-1])  # Grow the snake
        food = (random.randint(0, (WIDTH - CELL_SIZE) // CELL_SIZE) * CELL_SIZE,
                random.randint(0, (HEIGHT - CELL_SIZE) // CELL_SIZE) * CELL_SIZE)

    # Draw everything
    screen.blit(background_img, (0, 0))  # Background image
    pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, HEIGHT), 10)  # Border
    draw_snake(snake)
    draw_food(food)

    # Update the display
    pygame.display.flip()

    # Control the game speed
    clock.tick(10)
