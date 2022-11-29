# importo librerie
import pygame
import random

# inizializzo Pygame
pygame.init()

# Caricamento immagini
sfondo = pygame.image.load('immagini/sfondo.png')
player = pygame.image.load('immagini/player.png')
base = pygame.image.load('immagini/base.png')
gameover = pygame.image.load('immagini/gameover.png')
tubo_giu = pygame.image.load('immagini/tubo.png')
tubo_su = pygame.transform.flip(tubo_giu, False, True)

# Costanti Globali
SCHERMO = pygame.display.set_mode((288, 512))
FPS = 50
VEL_AVA = 3
FONT = pygame.font.SysFont ('Comic Sans MS', 50, bold=True)

class ctubi:
    def __init__(self):
        self.x = 300
        self.y = random.randint(-75, 150)
    def avanza_tubo(self):
        self.x -= VEL_AVA
        SCHERMO.blit(tubo_giu, (self.x,self.y+210))
        SCHERMO.blit(tubo_su, (self.x,self.y-210))
    def collide(self, player, playerx, playery):
        tollero = 5
        player_lato_dx = playerx+player.get_width()-tollero
        player_lato_sx = playerx+tollero
        tubi_lato_dx = self.x + tubo_giu.get_width()
        tubi_lato_sx = self.x
        player_lato_su = playery+tollero
        player_lato_giu = playery+player.get_height()-tollero
        tubi_lato_su = self.y+110
        tubi_lato_giu = self.y+210
        if player_lato_dx > tubi_lato_sx and player_lato_sx < tubi_lato_dx:
            if player_lato_su < tubi_lato_su or player_lato_giu > tubi_lato_giu:
                perso()
    def fra_tubi(self, player, playerx):
        tollero = 5
        player_lato_dx = playerx+player.get_width()-tollero
        player_lato_sx = playerx+tollero
        tubi_lato_dx = self.x + tubo_giu.get_width()
        tubi_lato_sx = self.x
        if player_lato_dx > tubi_lato_sx and player_lato_sx < tubi_lato_dx:
            return True
        
def disegna_oggetti():
    SCHERMO.blit(sfondo, (0,0))
    for t in tubi:
        t.avanza_tubo()
    SCHERMO.blit(player, (playerx, playery))
    SCHERMO.blit(base, (basex,400))
    punti_render = FONT.render(str(punti), 1, (255,255,255))
    SCHERMO.blit(punti_render, (130,440))

def aggiorna():
    pygame.display.update()
    pygame.time.Clock().tick(FPS)


def inizializza():
    global playerx, playery, player_vely
    global basex
    global tubi
    global punti
    global fra_tubi
    playerx, playery = 60, 150
    player_vely = 0
    basex = 0
    punti = 0
    tubi = []
    tubi.append(ctubi())
    fra_tubi = False
    

def perso():
    SCHERMO.blit(gameover, (50,180))
    aggiorna()
    ricominciamo = False
    while not ricominciamo:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                inizializza()
                ricominciamo = True
            if event.type == pygame.QUIT:
                pygame.quit()
                
# inizializzo variabili
inizializza ()

### Ciclo Principale ###
while True:
    basex -= VEL_AVA
    if basex < -45: basex = 0
    # gravità
    player_vely += 0.5
    playery += player_vely
    # Comandi
    for event in pygame.event.get():
        if ( event.type == pygame.KEYDOWN
             and event.key == pygame.K_UP ):
            player_vely = -7
        if event.type == pygame.QUIT:
            pygame.quit()
    # Gestione tubi
    if tubi[-1].x < 150: tubi.append(ctubi())
    # Collisione Player tubo
    for t in tubi:
        t.collide (player, playerx, playery)
    if not fra_tubi:
        for t in tubi:
            if t.fra_tubi (player, playerx):
                fra_tubi = True
                break
    if fra_tubi:
        fra_tubi = False
        for t in tubi:
            if t.fra_tubi (player, playerx):
                fra_tubi = True
                break
        if not fra_tubi:
            punti += 1

    # Collisione Base
    if playery > 380:
        perso()
        
    # aggiornamento schermo
    disegna_oggetti()
    aggiorna()
    
    



