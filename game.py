import pygame
from pygame.locals import *
import random
import sys

# shape parameters
size = width, height = (800, 800)
road_w = int(width / 1.6)
roadmark_w = int(width / 80)
# location parameters
right_lane = width / 2 + road_w / 4
left_lane = width / 2 - road_w / 4
# animation parameters
speed = 1

# initialize the app
pygame.init()
running = True

# set window size
screen = pygame.display.set_mode(size)
# set window title
pygame.display.set_caption("Jonathan's car game")

# define colors
red = (204, 0, 0)
white = (255, 255, 255)
blue = (0, 0, 153)

# load player vehicle
car = pygame.image.load("car.png")
# resize image
car = pygame.transform.scale(car, (100, 100))  # Adjust width here
car_loc = car.get_rect()
car_loc.center = right_lane, height * 0.8

# load enemy vehicle
car2 = pygame.image.load("otherCar.png")
car2 = pygame.transform.scale(car2, (100, 100))  # Adjust width here
car2_loc = car2.get_rect()
car2_loc.center = left_lane, height * 0.2

# font setup
font = pygame.font.Font(None, 36)

counter = 0
game_over = False
# game loop
while running:
    counter += 1

    # increase game difficulty over time
    if counter == 5000:
        speed += 0.15
        counter = 0
        print("level up", speed)

    # animate enemy vehicle
    car2_loc.y += speed
    if car2_loc.y > height:
        # randomly select lane
        if random.randint(0, 1) == 0:
            car2_loc.center = right_lane, -200
        else:
            car2_loc.center = left_lane, -200

    # end game logic
    if car_loc.colliderect(car2_loc):
        print("GAME OVER!")
        game_over = True

    # event listeners
    for event in pygame.event.get():
        if event.type == QUIT:
            # collapse the app
            running = False
        if event.type == KEYDOWN:
            # move user car to the left
            if event.key in [K_a, K_LEFT]:
                car_loc = car_loc.move([-int(road_w / 2), 0])
            # move user car to the right
            if event.key in [K_d, K_RIGHT]:
                car_loc = car_loc.move([int(road_w / 2), 0])

    # draw British flag background
    screen.fill(white)
    pygame.draw.rect(screen, red, (0, 0, width // 3, height))
    pygame.draw.rect(screen, blue, (2 * width // 3, 0, width // 3, height))

    # draw road
    pygame.draw.rect(
        screen,
        (50, 50, 50),
        (width / 2 - road_w / 2, 0, road_w, height))
    # draw center line
    pygame.draw.rect(
        screen,
        white,
        (width / 2 - roadmark_w / 2, 0, roadmark_w, height))
    # draw left road marking
    pygame.draw.rect(
        screen,
        (255, 255, 255),
        (width / 2 - road_w / 2 + roadmark_w * 2, 0, roadmark_w, height))
    # draw right road marking
    pygame.draw.rect(
        screen,
        (255, 255, 255),
        (width / 2 + road_w / 2 - roadmark_w * 3, 0, roadmark_w, height))

    # place car images on the screen
    screen.blit(car, car_loc)
    screen.blit(car2, car2_loc)

    if game_over:
        # Render the game over text
        game_over_text = font.render("Game Over!", True, (255, 0, 0))
        text_rect = game_over_text.get_rect(center=(width / 2, height / 2))
        screen.blit(game_over_text, text_rect)

    # Display speed
    speed_text = font.render(f"Speed: {speed:.2f}", True, (0, 0, 0))
    screen.blit(speed_text, (10, 10))

    # apply changes
    pygame.display.update()

    if game_over:
        # Wait for a short moment before exiting the game
        pygame.time.wait(2000)
        running = False

# collapse application window
pygame.quit()
sys.exit()
