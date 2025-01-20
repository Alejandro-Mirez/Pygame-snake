# accept that the snake can safely hit itself

import pygame
import random

pygame.init()

font = pygame.font.SysFont("Arial", 20, False, False)
welcome_message = font.render("Welcome to the Snake Game!", False, (255, 255, 255))
guide_message = font.render("Press SPACE to select option", False, (255, 255, 255))

hidden_message = font.render("", False, (0, 0, 0))
play_message = font.render("Play", False, (255, 255, 255))
quit_message = font.render("Quit", False, (255, 255, 255))
square_width = 750
pixel_width = 50
screen = pygame.display.set_mode([square_width] * 2)
snake_pixel = pygame.rect.Rect([0, 0, pixel_width - 2, pixel_width - 2])
running = True
playing_screen_on = False
start_screen_on = True
score_screen_on = False

play_button_pixel = pygame.rect.Rect([(screen.get_width()-100) / 2, 320, pixel_width * 2, pixel_width])
play_again_button_pixel = pygame.rect.Rect([(screen.get_width()-150) / 2, 320, pixel_width * 3, pixel_width])
quit_button_pixel = pygame.rect.Rect([(screen.get_width()-100) / 2, 420, pixel_width * 2, pixel_width])
option = "play"




# ------------------- PLAYING SCREEN -------------------

def play():

    global running
    global snake_pixel
    global playing_screen_on
    global score_screen_on

    snake_pixel.center = generate_starting_position()
    snake = [snake_pixel.copy()]
    snake_direction = (0, 0)
    snake_length = 1
    snake_speed = 6
    last_key = ""
    score = 0

    target = pygame.rect.Rect([0, 0, pixel_width - 2, pixel_width - 2])
    target.center = generate_starting_position()

    while running and playing_screen_on:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        def draw_snake():
            for snake_part in snake:
                pygame.draw.rect(screen, "green", snake_part)


        def draw_target():
            pygame.draw.rect(screen, "red", target)


        # HITTING THE WALL

        if is_out_of_bounds():
            snake_length = 1 # reset snake length
            snake_speed = 6 # reset snake speed
            snake_direction = (0, 0) # reset snake direction so it stays still after reset
            last_key = "" # reset last key so that if we lost moving in one direction...
            # ...we are able to start moving in the opposite direction after reset

          #  target.center = generate_starting_position() # generate new positions
          #  snake_pixel.center = generate_starting_position()
            playing_screen_on = False
            score_screen_on = True
            generate_score_screen(score)
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
        clock = pygame.time.Clock()
        draw_snake()

        draw_target()


        # MOVING ANIMATION

        snake.append(snake_pixel.copy())
        snake_pixel.move_ip(snake_direction)
        snake = snake[-snake_length:]

        pygame.display.flip()

        clock.tick(snake_speed)


def generate_starting_position():
    position_range = (pixel_width // 2, square_width - pixel_width // 2, pixel_width)
    return [random.randrange(*position_range), random.randrange(*position_range)]


def is_out_of_bounds():
    global snake_pixel
    return snake_pixel.bottom > square_width or snake_pixel.top < 0 \
        or snake_pixel.left < 0 or snake_pixel.right > square_width

# ------------------- SCORE SCREEN -------------------

def generate_score_screen(score):
    global play_again_button_pixel
    global quit_button_pixel
    global quit_message
    global score_screen_on
    global playing_screen_on
    global option
    global running



    screen.fill("black")

    score_message = font.render("Your score is: " + str(score), False, (255, 255, 255))
    score_msg = screen.blit(score_message, ((screen.get_width() - score_message.get_width()) / 2, 220))
    play_again_message = font.render("Play Again", False, (255, 255, 255))
    play_again_btn = pygame.draw.rect(screen, "green", play_again_button_pixel)
    play_btn_txt = screen.blit(play_again_message, (330, 331))
    quit_btn = pygame.draw.rect(screen, "gray30", quit_button_pixel)
    quit_btn_txt = screen.blit(quit_message, (356.5, 431))
    screen.blit(guide_message, ((screen.get_width() - guide_message.get_width()) / 2, 520))


    while running and score_screen_on:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False



       # while running:

            #events = pygame.event.get()

         #   for e in events:
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    option = "play"
                    pygame.draw.rect(screen, "gray30", quit_button_pixel)
                    pygame.draw.rect(screen, "green", play_again_button_pixel)
                    screen.blit(quit_message, (356.5, 431))
                    screen.blit(play_again_message, (330, 331))
                elif event.key == pygame.K_DOWN:
                    option = "quit"
                    pygame.draw.rect(screen, "green", quit_button_pixel)
                    pygame.draw.rect(screen, "gray30", play_again_button_pixel)
                    screen.blit(quit_message, (356.5, 431))
                    screen.blit(play_again_message, (330, 331))
                elif event.key == pygame.K_SPACE:
                    if option == "quit":
                        screen.fill("black")
                        playing_screen_on = False
                        running = False
                    elif option == "play":
                        screen.fill("black")
                        playing_screen_on = True
                        score_screen_on = False
                        play()

        pygame.display.flip()

# ------------------- START SCREEN -------------------

def generate_start_screen():

    global running
    global option
    global playing_screen_on
    msg = screen.blit(welcome_message, ((screen.get_width() - welcome_message.get_width()) / 2, 220))
    guide_msg = screen.blit(guide_message, ((screen.get_width() - guide_message.get_width()) / 2, 520))
    play_btn = pygame.draw.rect(screen, "green", play_button_pixel)
    play_btn_txt = screen.blit(play_message, (356, 331))
    quit_btn = pygame.draw.rect(screen, "gray30", quit_button_pixel)
    quit_btn_txt = screen.blit(quit_message, (356.5, 431))

    while running:
        events = pygame.event.get()

        for e in events:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_UP:
                    option = "play"
                    pygame.draw.rect(screen, "green", play_button_pixel)
                    pygame.draw.rect(screen, "gray30", quit_button_pixel)
                    screen.blit(play_message, (356, 331))
                    screen.blit(quit_message, (356.5, 431))
                elif e.key == pygame.K_DOWN:
                    option = "quit"
                    pygame.draw.rect(screen, "green", quit_button_pixel)
                    pygame.draw.rect(screen, "gray30", play_button_pixel)
                    screen.blit(play_message, (356, 331))
                    screen.blit(quit_message, (356.5, 431))
                elif e.key == pygame.K_SPACE:
                    if option == "quit":
                        running = False
                    elif option == "play":
                        screen.fill("black")
                        playing_screen_on = True
                        play()

        pygame.display.flip()

generate_start_screen()

pygame.quit()