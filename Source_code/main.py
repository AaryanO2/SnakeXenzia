import time

import pygame
import random
import os

pygame.mixer.init()
pygame.init()
pygame.mixer.music.load("b_music.mp3")
pygame.mixer.music.play()

# ***********************************Game Display Window***********************************
background_color = (152, 148, 68)
snake_color = (43, 35, 28)
food_color = snake_color
screen_width = 800
screen_height = 800
gameWindow = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Snake Xenzia")
pygame.display.update()
pygame_icon = pygame.image.load('icon.png')
pygame.display.set_icon(pygame_icon)


# Function to display text
def display_text(text, color, x, y, font_style, size):
    text_font = pygame.font.SysFont(font_style, size)
    screen_text = text_font.render(text, True, color)
    gameWindow.blit(screen_text, [x, y])


# Function to plot snake
def plot_snake(d):
    for x, y in snake_list[1:]:
        pygame.draw.rect(gameWindow, snake_color, [x, y, snake_size, snake_size])

    # Draw eye
    x, y = snake_list[-1]
    pygame.draw.rect(gameWindow, snake_color, [x, y, snake_size, snake_size])
    if d == 0:
        pygame.draw.circle(gameWindow, background_color, [x + 20, y + 20], 7)
    elif d == 1:
        pygame.draw.circle(gameWindow, background_color, [x + 20, y + 20], 7)
    elif d == 2:
        pygame.draw.circle(gameWindow, background_color, [x + 20, y + 20], 7)
    elif d == 3:
        pygame.draw.circle(gameWindow, background_color, [x + 20, y + 20], 7)

    # Draw design
    for x, y in snake_list[-15::-15]:
        pygame.draw.rect(gameWindow, background_color, [x + 10, y + 30, 10, 10], 2)


# *********************************** Game state variables ***********************************

# Game mode
classic = 0
adventure = 0
exit_game = False
main_menu = True
game_over = False

# Main-menu
option = 0

# Snake control Variables
snake_list = []
snake_length = 1
snake_size = 50
initial_x = 400
initial_y = 400
snake_x = initial_x
snake_y = initial_y
direction = 0  # Direction 0:(left) 1:(right) 2:(up) 3:(down)
velocity = 25
velocity_x = 0
velocity_y = 0

# Food variables
food_x = random.randint(60, screen_width - 90)
food_y = random.randint(80, screen_height - 100)
food_size = 40
points = 0

# Game Performance
clock = pygame.time.Clock()
fps = 60

# Database Variables
if not os.path.exists("high_score.txt"):
    with open("high_score.txt", "w") as f:
        f.write("0\n")
        f.write("0")
with open("high_score.txt", "r") as f:
    high_score_classic = int(f.readline())
    high_score_adventure = int(f.readline())

# To control turns
left = 0
right = 0
up = 0
down = 0

# ******************************************** Game loop ********************************************

while not exit_game:
    if main_menu:  # Display main-menu
        gameWindow.fill(background_color)
        pygame.draw.rect(gameWindow, snake_color, [100, 150, 600, 150], 20)
        display_text("SnakeXenzia", snake_color, 142, 165, "IMPACT", 100)

        for event in pygame.event.get():  # Events in main-menu
            if event.type == pygame.QUIT:
                exit_game = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if option == 0:
                        pygame.mixer.music.stop()
                        pygame.mixer.music.load("start.mp3")
                        pygame.mixer.music.play()
                        classic = 1
                    if option == 1:
                        pygame.mixer.music.stop()
                        pygame.mixer.music.load("start.mp3")
                        pygame.mixer.music.play()
                        adventure = 1
                    if option == 2:
                        pygame.mixer.music.stop()
                        pygame.mixer.music.load("start.mp3")
                        pygame.mixer.music.play()
                        exit_game = True
                    main_menu = False
                if event.key == pygame.K_UP:
                    option -= 1
                    option %= 3
                if event.key == pygame.K_DOWN:
                    option += 1
                    option %= 3
        # Draw main-menu
        if option == 0:
            pygame.draw.rect(gameWindow, snake_color, [0, 342, screen_width, 80])
            display_text("Classic Mode", background_color, 280, 350, "IMPACT", 50)
            display_text("Adventure Mode", snake_color, 250, 450, "IMPACT", 50)
            display_text("Exit", snake_color, 380, 550, "IMPACT", 50)
        elif option == 1:
            pygame.draw.rect(gameWindow, snake_color, [0, 442, screen_width, 80])
            display_text("Classic Mode", snake_color, 280, 350, "IMPACT", 50)
            display_text("Adventure Mode", background_color, 250, 450, "IMPACT", 50)
            display_text("Exit", snake_color, 380, 550, "IMPACT", 50)
        elif option == 2:
            pygame.draw.rect(gameWindow, snake_color, [0, 542, screen_width, 80])
            display_text("Classic Mode", snake_color, 280, 350, "IMPACT", 50)
            display_text("Adventure Mode", snake_color, 250, 450, "IMPACT", 50)
            display_text("Exit", background_color, 380, 550, "IMPACT", 50)

    # ******************************************** GameOver protocol ********************************************
    elif game_over:
        # Update Scores
        gameWindow.fill(background_color)
        if classic:
            display_text(f"CLASSIC MODE", snake_color, 35, 15, "IMPACT", 25)
            if points > high_score_classic:
                with open("high_score.txt", "w") as f:
                    f.write(str(points) + "\n")
                    f.write(str(high_score_classic))
                    high_score_classic = points
            display_text(f"High-score: {high_score_classic}", snake_color, 450, 15, "IMPACT", 25)

        if adventure:
            display_text(f"ADVENTURE MODE", snake_color, 35, 15, "IMPACT", 25)
            if points > high_score_adventure:
                with open("high_score.txt", "w") as f:
                    f.write(str(high_score_adventure) + "\n")
                    f.write(str(points))
                    high_score_adventure = points
            display_text(f"High-score: {high_score_adventure}", snake_color, 450, 15, "IMPACT", 25)
        # Creating Game Over Window
        pygame.draw.rect(gameWindow, snake_color, [35, 60, screen_width - 70, screen_height - 95], 5)
        display_text(f"Score: {points}", snake_color, 645, 15, "IMPACT", 25)
        display_text("** GAME OVER **", food_color, 125, 300, "IMAPCT", 100)
        display_text("** Press enter to restart **", food_color, 260, 430, "IMAPCT", 35)
        display_text("** Press esc to return to main-menu **", food_color, 190, 480, "IMAPCT", 35)
        for event in pygame.event.get():
            # Quit game
            if event.type == pygame.QUIT:
                exit_game = True
            # Restart game
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    #  Reset game over state variable
                    velocity_x = 0
                    velocity_y = 0
                    game_over = False

                elif event.key == pygame.K_ESCAPE:
                    #  Reset to main menu state variable
                    classic = 0
                    adventure = 0
                    velocity_x = 0
                    velocity_y = 0
                    main_menu = True
                    game_over = False
                    pygame.mixer.music.load("b_music.mp3")
                    pygame.mixer.music.play()
                # Reset remaining common Variables
                points = 0
                snake_x = initial_x
                snake_y = initial_y
                snake_list = []
                snake_length = 1

    # ******************************************** Adventure mode ********************************************
    elif adventure:
        for event in pygame.event.get():
            # Quit game
            if event.type == pygame.QUIT:
                exit_game = True

            # Control movement
            # Detect Keys pressed
            if event.type == pygame.KEYDOWN:
                # detect changes in Movement
                if event.key == pygame.K_UP and not velocity_y > 0 and not up:
                    direction = 2
                    velocity_y = -velocity
                    velocity_x = 0

                if event.key == pygame.K_DOWN and not velocity_y < 0 and not down:
                    direction = 3
                    velocity_y = velocity
                    velocity_x = 0

                if event.key == pygame.K_LEFT and not velocity_x > 0 and not left:
                    direction = 0
                    velocity_y = 0
                    velocity_x = -velocity

                if event.key == pygame.K_RIGHT and not velocity_x < 0 and not right:
                    direction = 1
                    velocity_y = 0
                    velocity_x = velocity

        # Point system
        if abs(snake_y - food_y) < 30 and abs(snake_x - food_x) < 30:
            pygame.mixer.music.load("coin.wav")
            pygame.mixer.music.play()
            points += 10
            snake_length += 7
            # Respawn fruit
            food_x = random.randint(90, screen_width - 90)
            food_y = random.randint(90, screen_height - 90)

        # Move snake
        # Co-ordinates after movement
        snake_x += velocity_x
        snake_y += velocity_y
        # Make next rect after movement
        snake_head = [snake_x, snake_y]
        snake_list.append(snake_head)
        # Erase tail rectangle
        if len(snake_list) > snake_length:
            del (snake_list[0])

        # Update display
        gameWindow.fill(background_color)
        pygame.draw.rect(gameWindow, snake_color, [35, 60, screen_width - 70, screen_height - 95], 15)
        display_text(f"ADVENTURE MODE", snake_color, 35, 15, "IMPACT", 25)
        display_text(f"Score: {points}", snake_color, 645, 15, "IMPACT", 25)
        display_text(f"High-score: {high_score_adventure}", snake_color, 450, 15, "IMPACT", 25)
        pygame.draw.rect(gameWindow, food_color, [food_x, food_y, food_size, food_size])
        plot_snake(direction)

        # Detect GameOver
        if (snake_x > screen_width - 90) or (snake_x < 40) or (snake_y > screen_height - 90) or (snake_y < 65):
            game_over = True
            pygame.mixer.music.stop()
            pygame.mixer.music.load("death.wav")
            pygame.mixer.music.play()
        elif snake_head in snake_list[:-1]:
            game_over = True
            pygame.mixer.music.stop()
            pygame.mixer.music.load("death.wav")
            pygame.mixer.music.play()

    # ******************************************** Classic mode ********************************************
    elif classic:
        for event in pygame.event.get():
            # Quit game
            if event.type == pygame.QUIT:
                exit_game = True

            # Control movement
            # Detect Keys pressed
            if event.type == pygame.KEYDOWN:
                # Controlling movement
                if event.key == pygame.K_UP and not velocity_y > 0 and not up:
                    direction = 2
                    velocity_y = -velocity
                    velocity_x = 0

                if event.key == pygame.K_DOWN and not velocity_y < 0 and not down:
                    direction = 3
                    velocity_y = velocity
                    velocity_x = 0

                if event.key == pygame.K_LEFT and not velocity_x > 0 and not left:
                    direction = 0
                    velocity_y = 0
                    velocity_x = -velocity

                if event.key == pygame.K_RIGHT and not velocity_x < 0 and not right:
                    direction = 1
                    velocity_y = 0
                    velocity_x = velocity

        # Point system
        if abs(snake_y - food_y) < 30 and abs(snake_x - food_x) < 30:
            pygame.mixer.music.load("coin.wav")
            pygame.mixer.music.play()
            points += 10
            snake_length += 7
            # ReSpawn food
            food_x = random.randint(90, screen_width - 90)
            food_y = random.randint(90, screen_height - 90)

        # Move snake
        snake_x += velocity_x
        snake_y += velocity_y
        # append head
        snake_head = [snake_x, snake_y]
        snake_list.append(snake_head)
        # erase tail
        if len(snake_list) > snake_length:
            del (snake_list[0])

        # Update display
        gameWindow.fill(background_color)
        pygame.draw.rect(gameWindow, snake_color, [40, 60, screen_width - 70, screen_height - 95], 15)
        display_text(f"CLASSIC MODE", snake_color, 35, 15, "IMPACT", 25)
        display_text(f"Score: {points}", snake_color, 645, 15, "IMPACT", 25)
        display_text(f"High-score: {high_score_classic}", snake_color, 450, 15, "IMPACT", 25)
        pygame.draw.rect(gameWindow, food_color, [food_x, food_y, food_size, food_size])
        plot_snake(direction)

        # For Infinite mode loop the snake in the box
        if snake_x > screen_width - 89:
            snake_x = 40

        elif snake_x < 45:
            snake_x = screen_width - 89

        elif snake_y > screen_height - 91:
            snake_y = 65

        elif snake_y < 65:
            snake_y = screen_height - 86

        # Detect GameOver
        elif snake_head in snake_list[:-1]:
            pygame.mixer.music.stop()
            pygame.mixer.music.load("death.wav")
            pygame.mixer.music.play()
            game_over = True

    # ************************* Update display for each cycle of while loop *************************
    pygame.display.update()
    # ******************************************** Set Fps for the game ********************************************
    clock.tick(fps)

# *********************************************** Quit Game ***********************************************
pygame.quit()