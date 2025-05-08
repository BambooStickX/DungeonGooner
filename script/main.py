import pygame
from sys import exit
from pytmx.util_pygame import load_pygame

# Pygame initialisieren
pygame.init()
screen = pygame.display.set_mode((960, 640))
pygame.display.set_caption("Dungeon Gooner")
clock = pygame.time.Clock()

# TMX-Datei laden
tmx_data = load_pygame("bilder/map/map.tmx")

# Spieler-Bilder (geordnet nach Richtung)
player_images = {
    "down": [pygame.image.load("bilder/player/vorne.png"),
             pygame.image.load("bilder/player/vorne2.png"),
             pygame.image.load("bilder/player/vorne3.png")],
    "right": [pygame.image.load("bilder/player/rechts.png"),
              pygame.image.load("bilder/player/rechts2.png"),
              pygame.image.load("bilder/player/rechts3.png")],
    "left": [pygame.image.load("bilder/player/links.png"),
             pygame.image.load("bilder/player/links2.png"),
             pygame.image.load("bilder/player/links3.png")],
    "up": [pygame.image.load("bilder/player/hinten.png"),
           pygame.image.load("bilder/player/hinten2.png"),
           pygame.image.load("bilder/player/hinten3.png")]
}

# Spieler-Position
playerx = 200
playery = 200
playerx_change = 0
playery_change = 0
direction = "down"
animation_index = 0
animation_timer = 0

def draw_player():
    global animation_index, animation_timer
    # Animation nur spielen, wenn Spieler sich bewegt
    if playerx_change != 0 or playery_change != 0:
        animation_timer += 1
        if animation_timer >= 15:  # wechsle Frame alle 15 Ticks
            animation_index = (animation_index + 1) % 3
            animation_timer = 0
    else:
        animation_index = 0  # stehendes Bild
    
    image = player_images[direction][animation_index]
    screen.blit(image, (playerx, playery))

def draw_map(surface, tmx_data):
    for layer in tmx_data.visible_layers:
        if hasattr(layer, "tiles"):
            for x, y, tile in layer.tiles():
                surface.blit(tile, (x * tmx_data.tilewidth, y * tmx_data.tileheight))

# Haupt-Loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                playerx_change = 3
                direction = "right"
            if event.key == pygame.K_a:
                playerx_change = -3
                direction = "left"
            if event.key == pygame.K_w:
                playery_change = -3
                direction = "up"
            if event.key == pygame.K_s:
                playery_change = 3
                direction = "down"

        if event.type == pygame.KEYUP:
            if event.key in [pygame.K_d, pygame.K_a]:
                playerx_change = 0
            if event.key in [pygame.K_w, pygame.K_s]:
                playery_change = 0

    playerx += playerx_change
    playery += playery_change

    screen.fill((0, 0, 0))
    draw_map(screen, tmx_data)
    draw_player()
    pygame.display.update()
    clock.tick(60)
