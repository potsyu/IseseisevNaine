# Pacman in Python with PyGame

# Github


import pygame
import time

# loome värvid
black = (0, 0, 0)
white = (255, 255, 255)
blue = (0, 0, 255)
green = (0, 255, 0)
red = (255, 0, 0)
purple = (255, 0, 255)
yellow = (255, 255, 0)

# Paneb pacman'i aknale ülesse vasakule
Trollicon = pygame.image.load('images/pacman.png')
pygame.display.set_icon(Trollicon)

# Toob muusika sisse
pygame.mixer.init()
pygame.mixer.music.load('pacman.mp3')
pygame.mixer.music.play(-1, 0.0)


# See klass tähistab allosas olevat riba, mida mängija juhib
class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color):
        # Kutsub "sprite" klassi, et grupid töötaks
        pygame.sprite.Sprite.__init__(self)

        # Teeb seina sisestatud mõõtmetes
        self.image = pygame.Surface([width, height])
        self.image.fill(color)  # Värvib seina sisestatud värvi

        self.rect = self.image.get_rect()  # Leiab seina ristküliku suuruse
        # Paneb seina sisestatud positsiooni
        self.rect.top = y
        self.rect.left = x


# See teeb kõik seinad ruumis 1
def setupRoomOne(all_sprites_list):
    # Loob seina objektide grupi, et neid paremini hallata
    wall_list = pygame.sprite.RenderPlain()

    # Info kõikide seinade kohta (x_positsioon, y_positsioon, laius, pikkus)
    walls = [[0, 0, 6, 600],
             [0, 0, 600, 6],
             [0, 600, 606, 6],
             [600, 0, 6, 606],
             [300, 0, 6, 66],
             [60, 60, 186, 6],
             [360, 60, 186, 6],
             [60, 120, 66, 6],
             [60, 120, 6, 126],
             [180, 120, 246, 6],
             [300, 120, 6, 66],
             [480, 120, 66, 6],
             [540, 120, 6, 126],
             [120, 180, 126, 6],
             [120, 180, 6, 126],
             [360, 180, 126, 6],
             [480, 180, 6, 126],
             [180, 240, 6, 126],
             [180, 360, 246, 6],
             [420, 240, 6, 126],
             [240, 240, 42, 6],
             [324, 240, 42, 6],
             [240, 240, 6, 66],
             [240, 300, 126, 6],
             [360, 240, 6, 66],
             [0, 300, 66, 6],
             [540, 300, 66, 6],
             [60, 360, 66, 6],
             [60, 360, 6, 186],
             [480, 360, 66, 6],
             [540, 360, 6, 186],
             [120, 420, 366, 6],
             [120, 420, 6, 66],
             [480, 420, 6, 66],
             [180, 480, 246, 6],
             [300, 480, 6, 66],
             [120, 540, 126, 6],
             [360, 540, 126, 6]
             ]

    # Käib läbi seinte listi, loob need ja lisab gruppidesse
    for item in walls:
        wall = Wall(item[0], item[1], item[2], item[3], blue)  # Kasutab Wall klassi funktsiooni
        wall_list.add(wall)  # Lisab seina seinte listi
        all_sprites_list.add(wall)  # Lisab seina kõikide mängu objektide listi

    # Tagastab uue seinte gruppi
    return wall_list


# See teeb alguse ukse kus pahad vanad välja tulevad
def setupGate(all_sprites_list):
    gate = pygame.sprite.RenderPlain()  # Loob ukse grupi
    gate.add(Wall(282, 242, 42, 2, white))  # Loob Wall funktsiooniga ukse ja lisab ukse gruppi
    all_sprites_list.add(gate)  # Lisab ukse kõikide mängu objektide gruppi
    return gate  # Tagastab uue ukse


class Block(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        # Kutsub "sprite" klassi, et grupid töötaks
        pygame.sprite.Sprite.__init__(self)

        # Loob plokid, mis võivad olla kas mängija või näiteks kummitus.
        self.image = pygame.Surface([width, height])  # Teeb ploki esitatud mõõtmetes
        self.image.fill(white)  # Teeb ploki valgeks
        self.image.set_colorkey(white)  # Seab plokki "värvikoodi", mis säilitab ploki värvi, kui miski peaks olema ees
        pygame.draw.ellipse(self.image, color, [0, 0, width, height])  # Joonistab ploki sisestatud värvis ja mõõtmetes

        # Leiab ja salvestab ploki dimensioonid.
        self.rect = self.image.get_rect()


# See klass teeb mängija, kuidas liigub, mis kiirus jne
class Player(pygame.sprite.Sprite):
    # Seadistab kiiruse vektori
    change_x = 0
    change_y = 0

    def __init__(self, x, y, filename):
        # Kutsub "sprite" klassi, et grupid töötaks
        pygame.sprite.Sprite.__init__(self)

        # Seadistab mängija pikkuse ja laiuse
        self.image = pygame.image.load(filename).convert()

        # Paigutab mängija
        self.rect = self.image.get_rect()  # Leiab dimensioonid
        # Seadistab positsioonid
        self.rect.top = y
        self.rect.left = x
        # Salvestab praeguse positsiooni hiljemaks
        self.prev_x = x
        self.prev_y = y

    # Kustutab mängija kiiruse, ehk peatab selle
    def prevdirection(self):
        self.prev_x = self.change_x
        self.prev_y = self.change_y

    # Muudab mängija kiirust
    def changespeed(self, x, y):
        self.change_x += x
        self.change_y += y

    # Leiab mängijale uue positsiooni
    def update(self, walls, gate):
        # Leiab vana postsiooni, juhuks kui peaksime senna tagasi minema
        old_x = self.rect.left
        new_x = old_x + self.change_x
        var = old_x + self.prev_x
        self.rect.left = new_x

        old_y = self.rect.top
        new_y = old_y + self.change_y
        var = old_y + self.prev_y

        # Kontrollib, kas järgmine käik oleks vastu seina
        x_collide = pygame.sprite.spritecollide(self, walls, False)
        if x_collide:
            # # Kui läheb vastu seina, viime tagasi eelmisesse positsiooni
            self.rect.left = old_x
        else:

            self.rect.top = new_y

            # Kontrollib, kas järgmine käik oleks vastu seina
            y_collide = pygame.sprite.spritecollide(self, walls, False)
            if y_collide:
                # Kui läheb vastu seina, viime tagasi eelmisesse positsiooni
                self.rect.top = old_y

        if gate:
            gate_hit = pygame.sprite.spritecollide(self, gate, False)
            if gate_hit:
                self.rect.left = old_x
                self.rect.top = old_y


# Teeb kummitused kes liiguvad, kiirus, kuidas liiguvad jne
class Ghost(Player):
    # Muudab kummituse kiirust
    def changespeed(self, list, ghost, turn, steps, l):
        try:
            z = list[turn][2]
            if steps < z:
                self.change_x = list[turn][0]
                self.change_y = list[turn][1]
                steps += 1
            else:
                if turn < l:
                    turn += 1
                elif ghost == "clyde":
                    turn = 2
                else:
                    turn = 0
                self.change_x = list[turn][0]
                self.change_y = list[turn][1]
                steps = 0
            return [turn, steps]
        except IndexError:
            return [0, 0]


# Pinky liikumis suunad
Pinky_directions = [
    [0, -30, 4],
    [15, 0, 9],
    [0, 15, 11],
    [-15, 0, 23],
    [0, 15, 7],
    [15, 0, 3],
    [0, -15, 3],
    [15, 0, 19],
    [0, 15, 3],
    [15, 0, 3],
    [0, 15, 3],
    [15, 0, 3],
    [0, -15, 15],
    [-15, 0, 7],
    [0, 15, 3],
    [-15, 0, 19],
    [0, -15, 11],
    [15, 0, 9]
]
# Kummituse liikumis suunad
Blinky_directions = [
    [0, -15, 4],
    [15, 0, 9],
    [0, 15, 11],
    [15, 0, 3],
    [0, 15, 7],
    [-15, 0, 11],
    [0, 15, 3],
    [15, 0, 15],
    [0, -15, 15],
    [15, 0, 3],
    [0, -15, 11],
    [-15, 0, 3],
    [0, -15, 11],
    [-15, 0, 3],
    [0, -15, 3],
    [-15, 0, 7],
    [0, -15, 3],
    [15, 0, 15],
    [0, 15, 15],
    [-15, 0, 3],
    [0, 15, 3],
    [-15, 0, 3],
    [0, -15, 7],
    [-15, 0, 3],
    [0, 15, 7],
    [-15, 0, 11],
    [0, -15, 7],
    [15, 0, 5]
]

# Kummituse liikumis suunad
Inky_directions = [
    [30, 0, 2],
    [0, -15, 4],
    [15, 0, 10],
    [0, 15, 7],
    [15, 0, 3],
    [0, -15, 3],
    [15, 0, 3],
    [0, -15, 15],
    [-15, 0, 15],
    [0, 15, 3],
    [15, 0, 15],
    [0, 15, 11],
    [-15, 0, 3],
    [0, -15, 7],
    [-15, 0, 11],
    [0, 15, 3],
    [-15, 0, 11],
    [0, 15, 7],
    [-15, 0, 3],
    [0, -15, 3],
    [-15, 0, 3],
    [0, -15, 15],
    [15, 0, 15],
    [0, 15, 3],
    [-15, 0, 15],
    [0, 15, 11],
    [15, 0, 3],
    [0, -15, 11],
    [15, 0, 11],
    [0, 15, 3],
    [15, 0, 1],
]

# Kummituse liikumis suunad
Clyde_directions = [
    [-30, 0, 2],
    [0, -15, 4],
    [15, 0, 5],
    [0, 15, 7],
    [-15, 0, 11],
    [0, -15, 7],
    [-15, 0, 3],
    [0, 15, 7],
    [-15, 0, 7],
    [0, 15, 15],
    [15, 0, 15],
    [0, -15, 3],
    [-15, 0, 11],
    [0, -15, 7],
    [15, 0, 3],
    [0, -15, 11],
    [15, 0, 9],
]

# Loob kummituste liikumise listi pikkuse muutujad
pl = len(Pinky_directions) - 1
bl = len(Blinky_directions) - 1
il = len(Inky_directions) - 1
cl = len(Clyde_directions) - 1

# Käivitab pygame
pygame.init()

# Teeb ekraani
screen = pygame.display.set_mode([606, 640])

# Seab akna nime
pygame.display.set_caption('Pac-Man')

# Loob aluse, millele saame "joonistada"
background = pygame.Surface(screen.get_size())

# Kasutatakse taustavärvide muutmiseks
background = background.convert()

# Täidab tausta musta väviga
background.fill(black)

clock = pygame.time.Clock()

pygame.font.init()
font = pygame.font.Font("freesansbold.ttf", 24)

# Tavalised asukohad pacmani jaoks ja kummituste jaoks
w = 303 - 16  # Width
p_h = (7 * 60) + 19  # Pacman height
m_h = (4 * 60) + 19  # Monster height
b_h = (3 * 60) + 19  # Binky height
i_w = 303 - 16 - 32  # Inky width
c_w = 303 + (32 - 16)  # Clyde width


# Tehakse funktsioon, mis alustab mängu ja kus kõik kood käivitub
def startGame():
    start_time = time.time()
    all_sprites_list = pygame.sprite.RenderPlain()

    block_list = pygame.sprite.RenderPlain()

    monsta_list = pygame.sprite.RenderPlain()

    pacman_collide = pygame.sprite.RenderPlain()

    wall_list = setupRoomOne(all_sprites_list)

    gate = setupGate(all_sprites_list)

    p_turn = 0
    p_steps = 0

    b_turn = 0
    b_steps = 0

    i_turn = 0
    i_steps = 0

    c_turn = 0
    c_steps = 0

    # Loob mängija kuju
    Pacman = Player(w, p_h, "images/pacman.png")
    all_sprites_list.add(Pacman)
    pacman_collide.add(Pacman)

    # Loob kummituste kujud
    Blinky = Ghost(w, b_h, "images/Blinky.png")
    monsta_list.add(Blinky)
    all_sprites_list.add(Blinky)

    Pinky = Ghost(w, m_h, "images/Pinky.png")
    monsta_list.add(Pinky)
    all_sprites_list.add(Pinky)

    Inky = Ghost(i_w, m_h, "images/Inky.png")
    monsta_list.add(Inky)
    all_sprites_list.add(Inky)

    Clyde = Ghost(c_w, m_h, "images/Clyde.png")
    monsta_list.add(Clyde)
    all_sprites_list.add(Clyde)

    # Teeb seinad
    for row in range(19):
        for column in range(19):
            if (row == 7 or row == 8) and (column == 8 or column == 9 or column == 10):
                continue
            else:
                block = Block(yellow, 4, 4)

                # Set a random location for the block
                block.rect.x = (30 * column + 6) + 26
                block.rect.y = (30 * row + 6) + 26

                b_collide = pygame.sprite.spritecollide(block, wall_list, False)
                p_collide = pygame.sprite.spritecollide(block, pacman_collide, False)
                if b_collide:
                    continue
                elif p_collide:
                    continue
                else:
                    # Add the block to the list of objects
                    block_list.add(block)
                    all_sprites_list.add(block)

    bll = len(block_list)

    score = 0

    done = False
    gameover = False
    cheat = False

    var = 0

    while not done:
        # Kõik nupu vajutused toimuvad siin, liikumine näiteks
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    Pacman.changespeed(-30, 0)
                if event.key == pygame.K_RIGHT:
                    Pacman.changespeed(30, 0)
                if event.key == pygame.K_UP:
                    Pacman.changespeed(0, -30)
                if event.key == pygame.K_DOWN:
                    Pacman.changespeed(0, 30)
                # Cheatid
                if event.key == pygame.K_w: #Kontrollib kas sa liigud tahteust kiiremini pmst
                    Pacman.changespeed(0, -60) # Ja aktiveerib sohi
                    cheat = True # ning muudab cheat muutuja True'ks
                if event.key == pygame.K_s: #Kontrollib kas sa liigud tahteust kiiremini pmst
                    Pacman.changespeed(0, 60)  # Ja aktiveerib sohi
                    cheat = True # ning muudab cheat muutuja True'ks
                if event.key == pygame.K_a: #Kontrollib kas sa liigud tahteust kiiremini pmst
                    Pacman.changespeed(-60, 0) # Ja aktiveerib sohi
                    cheat = True # ning muudab cheat muutuja True'ks
                if event.key == pygame.K_d: #Kontrollib kas sa liigud tahteust kiiremini pmst
                    Pacman.changespeed(60, 0) # Ja aktiveerib sohi
                    cheat = True # ning muudab cheat muutuja True'ks

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    Pacman.changespeed(30, 0)
                if event.key == pygame.K_RIGHT:
                    Pacman.changespeed(-30, 0)
                if event.key == pygame.K_UP:
                    Pacman.changespeed(0, 30)
                if event.key == pygame.K_DOWN:
                    Pacman.changespeed(0, -30)

                if event.key == pygame.K_w:
                    Pacman.changespeed(0, 60)
                if event.key == pygame.K_s:
                    Pacman.changespeed(0, -60)
                if event.key == pygame.K_a:
                    Pacman.changespeed(60, 0)
                if event.key == pygame.K_d:
                    Pacman.changespeed(-60, 0)


        # Mängu loogika
        Pacman.update(wall_list, gate)

        returned = Pinky.changespeed(Pinky_directions, False, p_turn, p_steps, pl)
        p_turn = returned[0]
        p_steps = returned[1]
        Pinky.changespeed(Pinky_directions, False, p_turn, p_steps, pl)
        Pinky.update(wall_list, False)

        returned = Blinky.changespeed(Blinky_directions, False, b_turn, b_steps, bl)
        b_turn = returned[0]
        b_steps = returned[1]
        Blinky.changespeed(Blinky_directions, False, b_turn, b_steps, bl)
        Blinky.update(wall_list, False)

        returned = Inky.changespeed(Inky_directions, False, i_turn, i_steps, il)
        i_turn = returned[0]
        i_steps = returned[1]
        Inky.changespeed(Inky_directions, False, i_turn, i_steps, il)
        Inky.update(wall_list, False)

        returned = Clyde.changespeed(Clyde_directions, "clyde", c_turn, c_steps, cl)
        c_turn = returned[0]
        c_steps = returned[1]
        Clyde.changespeed(Clyde_directions, "clyde", c_turn, c_steps, cl)
        Clyde.update(wall_list, False)

        # Vaatab kas pacman on millegile vastu läinud
        blocks_hit_list = pygame.sprite.spritecollide(Pacman, block_list, True)

        # Check the list of collisions.
        if len(blocks_hit_list) > 0:
            score += len(blocks_hit_list)

        # Joonistab seinad, kummituste koha ukse, pacmani ja kummitused
        screen.fill(black)

        wall_list.draw(screen)
        gate.draw(screen)
        all_sprites_list.draw(screen)
        monsta_list.draw(screen)
        screen.blit(
            pygame.font.Font(None, 32).render(f"Life Wasted: {int(time.time() - start_time)}", True,
                                                         [50, 255, 255]),
            [430, 613])  # show time elapsed
        # Kui cheatid paneb ekraanile teksti
        if cheat:
            text1 = font.render("Ära Marcellota", True, red)
            screen.blit(text1, [200, 200])

        # Toob skoori välja
        text = font.render("Score: " + str(score) + "/" + str(bll), True, red)
        screen.blit(text, [10, 610])


        # Kui kõik pallid on korjatud siis mäng saab läbi
        if score == bll:
            doNext("Congratulations, you won!", 145)

        monsta_hit_list = pygame.sprite.spritecollide(Pacman, monsta_list, False)
        # Kui Pac-Man läheb kummituste vastu
        if monsta_hit_list:
            done = True
            gameover = True

        pygame.display.flip()

        clock.tick(10)
    # sa kaotasid
    while gameover:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    quit()
                if event.key == pygame.K_RETURN:
                    startGame()
        # Paneb ekraanile kaotus pildi
        dead = pygame.image.load("images/dead.png")
        screen.blit(dead, (0, 0))

        pygame.display.flip()

        clock.tick(10)


# Funktsioon kus tehakse aknad kui kaotad, kas tahad mängu uuesti alustada või kinni panna
def doNext(message, left):
    while True:
        # ALL EVENT PROCESSING SHOULD GO BELOW THIS COMMENT
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                if event.key == pygame.K_RETURN:
                    startGame()

        # Hall taust
        w = pygame.Surface((400, 200))  # the size of your rect
        w.set_alpha(10)  # alpha level
        w.fill((128, 128, 128))  # this fills the entire surface
        screen.blit(w, (100, 200))  # (0,0) are the top-left coordinates

        # Võit või kaotus
        text1 = font.render(message, True, white)
        screen.blit(text1, [left, 233])

        pygame.display.flip()

        clock.tick(10)


# Ootab kuni vajutad nuppu K, et mäng peale hakkaks
while True:
    background = pygame.image.load('images/title.png')
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_k:
                startGame()

    pygame.display.flip()