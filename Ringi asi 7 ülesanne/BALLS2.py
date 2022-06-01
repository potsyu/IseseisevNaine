# Importing pygame module
import pygame
import random
from pygame.locals import *

# initiate pygame and give permission
# to use pygame's functionality.
pygame.init()


# making a random color class
def random_color():
    levels = range(32, 256, 32)
    return tuple(random.choice(levels) for _ in range(3))


# ekraani seaded
screen = pygame.display.set_mode([640, 480])
screen.fill([255, 255, 255])

# radius of the circle
circle_radius = 10

# Creating a while loop
while True:

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
            circle_radius += 1

    # Draws the surface object to the screen.
    pygame.display.update()
