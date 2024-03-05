
# TODO: prevent snake from eating itself

import pygame
import random

pygame.init()
square_width = 750
pixel_width = 50
screen = pygame.display.set_mode([square_width] * 2)
clock = pygame.time.Clock()
running = True
snake_speed = 6
last_key = ""
score = 0


def generate_starting_position():
    position_range = (pixel_width // 2, square_width - pixel_width // 2, pixel_width)
    return [random.randrange(*position_range), random.randrange(*position_range)]


def is_out_of_bounds():
    return snake_pixel.bottom > square_width or snake_pixel.top < 0 \
        or snake_pixel.left < 0 or snake_pixel.right > square_width


snake_pixel = pygame.rect.Rect([0, 0, pixel_width - 2, pixel_width - 2])
snake_pixel.center = generate_starting_position()
snake = [snake_pixel.copy()]
snake_direction = (0, 0)
snake_length = 1


target = pygame.rect.Rect([0, 0, pixel_width - 2, pixel_width - 2])
target.center = generate_starting_position()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    def draw_snake():
        for snake_part in snake:
            pygame.draw.rect(screen, "blue", snake_part)


    def draw_target():
        pygame.draw.rect(screen, "red", target)


# HITTING THE WALL

    if is_out_of_bounds():
        snake_length = 1 # reset snake length
        snake_speed = 6 # reset snake speed
        snake_direction = (0, 0) # reset snake direction so it stays still after reset
        last_key = "" # reset last key so that if we lost moving in one direction...
        # ...we are able to start moving in the opposite direction after reset

        target.center = generate_starting_position() # generate new positions
        snake_pixel.center = generate_starting_position()
        print("Your score is: ", score)
        score = 0 # reset score


# EATING THE TARGET

    if snake_pixel.center == target.center:
        target.center = generate_starting_position()
        snake_length += 1
        snake.append(snake_pixel.copy())
        snake_speed += 1
        score += 1

# STEERING

    keys = pygame.key.get_pressed()

    if keys[pygame.K_UP] and last_key != "down":
        last_key = "up"
        snake_direction = (0, - pixel_width)

    if keys[pygame.K_DOWN] and last_key != "up":
        last_key = "down"
        snake_direction = (0, pixel_width)

    if keys[pygame.K_LEFT] and last_key != "right":
        last_key = "left"
        snake_direction = (- pixel_width, 0)

    if keys[pygame.K_RIGHT] and last_key != "left":
        last_key = "right"
        snake_direction = (pixel_width, 0)


# DRAWING SNAKE AND TARGET

    screen.fill("black")

    draw_snake()

    draw_target()


# MOVING ANIMATION

    snake.append(snake_pixel.copy())
    snake_pixel.move_ip(snake_direction)
    snake = snake[-snake_length:]

    pygame.display.flip()

    clock.tick(snake_speed)


pygame.quit()