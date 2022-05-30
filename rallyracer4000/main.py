import pygame  # Imports modules
import random  # Imports modules

pygame.init()  # initialize display

screenX = 640  # set screen size
screenY = 480  # set screen size
pygame.display.set_caption("RallyRacer4000")  # set window title

screen = pygame.display.set_mode((screenX, screenY))  # set screen size

clock = pygame.time.Clock()  # create clock object

Score = 0  # initialize score

blue = [0, 45, 167]  # initalize blue color

f1_blue_image = pygame.image.load("f1_blue.png")  # load car image

f1_red_image = pygame.image.load("f1_red.png")  # load car image
f1_red_image = pygame.transform.rotate(f1_red_image, 180)  # rotate red car 180 degrees

bg_rally = pygame.image.load("bg_rally.jpg")  # load car image
bg_rally2 = pygame.image.load("bg_rally.jpg")  # load car image
gameoverbg = pygame.image.load("surm.jpg")  # load gameover image

f1_blue_posY = 344  # Position on Y axis
f1_blue_posX = 300  # Poistion on X axis

f1_red_speed = 8  # red car speed
f1_red_posY = 230  # red Position on Y axis
f1_red_posX = 420  # red Position on X axis

bg_rally_speed = 5  # BG speed
bg_rally_posY = 0  # bg position

bg_rally2_posY = -480  # 2nd background position

gameover = False  # game running
while not gameover:
    clock.tick(60)  # appoints an fps mark
    events = pygame.event.get()
    for i in events:
        if i.type == pygame.QUIT:
            quit()

        # move blue car with arrow keys
        if i.type == pygame.KEYDOWN:
            if i.key == pygame.K_LEFT and f1_blue_posX != 180:  # move car
                f1_blue_posX -= 120  # move only 120 pixels

            if i.key == pygame.K_RIGHT and f1_blue_posX != 420:  # move car
                f1_blue_posX += 120  # move only 120 pixels

    f1_red_posY += f1_red_speed  # lahutad positsioonist kiiruse
    bg_rally_posY += bg_rally_speed  # liidab positsioonile kiiruse
    bg_rally2_posY += bg_rally_speed  # liidab positsioonile kiiruse

    screen.blit(bg_rally2, (0, bg_rally2_posY))  # blit background
    screen.blit(bg_rally, (0, bg_rally_posY))  # blit bacground

    f1_blue = pygame.Rect(f1_blue_posX, f1_blue_posY, 45, 90)  # make hitboxes
    screen.blit(f1_blue_image, f1_blue)  # # blit car

    f1_red = pygame.Rect(f1_red_posX, f1_red_posY, 45, 90)  # make hitboxes
    screen.blit(f1_red_image, f1_red)  # blit car

    # code makes background move smoothly
    if bg_rally_posY > screenY:
        bg_rally_posY = -480
    if bg_rally2_posY > screenY:
        bg_rally2_posY = -480

    if f1_blue_posY < 0 - 90:
        f1_blue_posY = 480
    # making red cars come towards you from up top randomly
    if f1_red_posY > 480:  # if red car moves higher than 480 pixels
        f1_red_posY = -90  # it goes down to -90 pixels
        f1_red_speed = random.randrange(6, 15, 1)  # makes cars randomly come down from 3 lanes different speeds
        f1_red_posX = random.randrange(180, 540, 120)  # makes cars randomly come down from 3 lanes different speeds
        Score += 1
    # Game over stuff
    if f1_red.colliderect(f1_blue):  # checks if two different rectangles are collided
        gameover = True  # if they are you dead
    screen.blit(pygame.font.Font(None, 30).render(f"Skoor: {Score}", True, [255, 255, 255]), [10, 10])  # show score
    pygame.display.flip()  # update display
# code for being able to quit from the X
while gameover:
    events = pygame.event.get()
    for i in events:
        if i.type == pygame.QUIT:
            quit()
    screen.blit(gameoverbg, (0, 0))  # displays game over bg
    screen.blit(pygame.font.Font(None, 50).render(f"Skoor: {Score}", True, [255, 255, 255]), [250, 400])  # show score
    pygame.display.flip()  # update display
