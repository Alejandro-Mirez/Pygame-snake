
# TODO: prevent snake from eating itself

import pygame
import random

pygame.init()
square_width = 750
pixel_width = 50
screen = pygame.display.set_mode([square_width] * 2)
clock = pygame.time.Clock()
running = True
player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
snake_speed = 7
last_key = []

def generate_starting_position():
    position_range = (pixel_width // 2, square_width - pixel_width // 2, pixel_width)
    return [random.randrange(*position_range), random.randrange(*position_range)]


def reset():
    target.center = generate_starting_position()
    snake_pixel.center = generate_starting_position()
    return snake_pixel.copy()


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

    screen.fill("black")

    if is_out_of_bounds():
        snake_length = 1
        snake_speed = 7
        target.center = generate_starting_position()
        snake_pixel.center = generate_starting_position()
        snake = [snake_pixel.copy()]

    if snake_pixel.center == target.center:
        target.center = generate_starting_position()
        snake_length += 1
        snake.append(snake_pixel.copy())
        print("previous speed: ", snake_speed)
        snake_speed += 2
        print("increased snake speed! Current speed: ", snake_speed)


# steering

    keys = pygame.key.get_pressed()

    if keys[pygame.K_UP]:
        if last_key == "down":
            print("bad move")
        else:
            last_key = "up"
            snake_direction = (0, - pixel_width)

    if keys[pygame.K_DOWN]:
        if last_key == "up":
            print("bad move")
        else:
            last_key = "down"
            snake_direction = (0, pixel_width)

    if keys[pygame.K_LEFT]:
        if last_key == "right":
            print("bad move")
        else:
            last_key = "left"
            snake_direction = (- pixel_width, 0)

    if keys[pygame.K_RIGHT]:
       if last_key == "left":
           print("bad move")
       else:
           last_key = "right"
           snake_direction = (pixel_width, 0)


    for snake_part in snake:
        pygame.draw.rect(screen, "blue", snake_part)

    pygame.draw.rect(screen, "red", target)

    snake_pixel.move_ip(snake_direction)
    snake.append(snake_pixel.copy())
    snake = snake[-snake_length:]

    pygame.display.flip()

    clock.tick(snake_speed)



pygame.quit()