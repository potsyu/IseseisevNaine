import pygame, sys

pygame.init()

#ekraani seaded
screen=pygame.display.set_mode([640,480])
pygame.display.set_caption("RallyRacer4000")
screen.fill([204, 255, 204])
clock = pygame.time.Clock()

#Lisame background'i
bg = pygame.image.load("bg_rally.jpg")
screen.blit(bg, [0,0])
pygame.display.flip()

#lisame Auto (punane)
red = pygame.image.load("f1_red.png")
posX, posY = 0, 0
screen.blit(red,[300,390])

#Lisame Autod (Sinine)
blue1 = pygame.image.load("f1_blue.png")
posX, posY = 0, 0
speedX = 1

gameover = False
while not gameover:
    clock.tick(30)
    screen.blit(blue1, (posX,posY))

    posX += speedX
  #graafika kuvamine ekraanil
    pygame.display.flip()

#Lisame background'i
bg = pygame.image.load("bg_rally.jpg")
screen.blit(bg, [0,0])
pygame.display.flip()

#Kood, et ekraan automaatselt ei läheks kinni.

while True:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      quit()