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
WHITE = (255, 255, 255)
RED = (255, 0, 0)

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

# Font for text display
font = pygame.font.Font(None, 36)
big_font = pygame.font.Font(None, 72)

# Snake initialization
snake = [(100, 100), (80, 100), (60, 100)]  # Initial snake positions (3 segments)
snake_dir = (CELL_SIZE, 0)  # Initial direction (moving right)

# Food initialization
food = (random.randint(0, (WIDTH - CELL_SIZE) // CELL_SIZE) * CELL_SIZE,
        random.randint(0, (HEIGHT - CELL_SIZE) // CELL_SIZE) * CELL_SIZE)

# Score initialization
score = 0
high_score = 0

def draw_snake(snake):
    for segment in snake:
        screen.blit(snake_segment_img, segment)

def draw_food(food):
    screen.blit(food_img, food)

def draw_score(score):
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

def draw_high_score(high_score):
    high_score_text = font.render(f"High Score: {high_score}", True, WHITE)
    screen.blit(high_score_text, (WIDTH - 200, 10))

def death_screen(score, high_score):
    screen.fill(BLACK)
    death_text = big_font.render("GAME OVER", True, RED)
    score_text = font.render(f"Your Score: {score}", True, WHITE)
    high_score_text = font.render(f"High Score: {high_score}", True, WHITE)
    restart_text = font.render("Press ENTER to Restart", True, WHITE)

    screen.blit(death_text, (WIDTH // 2 - death_text.get_width() // 2, HEIGHT // 4))
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 - 40))
    screen.blit(high_score_text, (WIDTH // 2 - high_score_text.get_width() // 2, HEIGHT // 2))
    screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 40))

    pygame.display.flip()
    wait_for_restart()

def wait_for_restart():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return

def main_menu():
    screen.fill(BLACK)
    title_text = big_font.render("SNAKE GAME", True, WHITE)
    start_text = font.render("Press ENTER to Start", True, WHITE)

    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 3))
    screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2))

    pygame.display.flip()
    wait_for_start()

def wait_for_start():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return

# Main game loop
main_menu()
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
        high_score = max(high_score, score)
        death_screen(score, high_score)
        snake = [(100, 100), (80, 100), (60, 100)]  # Reset snake
        snake_dir = (CELL_SIZE, 0)  # Reset direction
        score = 0  # Reset score
        food = (random.randint(0, (WIDTH - CELL_SIZE) // CELL_SIZE) * CELL_SIZE,
                random.randint(0, (HEIGHT - CELL_SIZE) // CELL_SIZE) * CELL_SIZE)

    # Check if snake eats food
    if new_head == food:
        snake.append(snake[-1])  # Grow the snake
        score += 1  # Increase score
        food = (random.randint(0, (WIDTH - CELL_SIZE) // CELL_SIZE) * CELL_SIZE,
                random.randint(0, (HEIGHT - CELL_SIZE) // CELL_SIZE) * CELL_SIZE)

    # Draw everything
    screen.blit(background_img, (0, 0))  # Background image
    pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, HEIGHT), 10)  # Border
    draw_snake(snake)
    draw_food(food)
    draw_score(score)
    draw_high_score(high_score)

    # Update the display
    pygame.display.flip()

    # Control the game speed
    clock.tick(10)
