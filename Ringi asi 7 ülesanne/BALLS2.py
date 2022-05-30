# Importing pygame module
import pygame
import random
from pygame.locals import *

# initiate pygame and give permission
# to use pygame's functionality.
pygame.init()
# värvid
White = [255, 255, 255]


# making a random color class
def random_color():
    levels = range(32, 256, 32)
    return tuple(random.choice(levels) for _ in range(3))


# ekraani seaded
screenX = 640
screenY = 480
screen = pygame.display.set_mode([screenX, screenY])
pygame.display.set_caption("töötav pallide mäng")
screen.fill(White)
clock = pygame.time.Clock()

# radius of the circle
circle_radius = 10

# Creating a variable which we will use
# to run the while loop
run = True

# Creating a while loop
while run:

    # Iterating over all the events received from
    # pygame.event.get()
    for event in pygame.event.get():

        # If the type of the event is quit
        # then setting the run variable to false
        if event.type == QUIT:
            run = False

        # if the type of the event is MOUSEBUTTONDOWN
        # then storing the current position
        if event.type == MOUSEBUTTONDOWN:
            # Drawing the circle
            x = random.randint(0, 620)
            y = random.randint(0, 620)
            pygame.draw.circle(screen, random_color(), [x, y], circle_radius)

        if event.type == MOUSEBUTTONDOWN:
            circle_radius += 1


    # Draws the surface object to the screen.
    pygame.display.update()
