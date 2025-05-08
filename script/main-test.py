import pygame
from sys import exit

pygame.init()
screen = pygame.display.set_mode((1920, 1080))
pygame.display.set_caption("Dungeon Gooner")
clock = pygame.time.Clock()

menu_background = pygame.image.load("bilder/richtige.png").convert()
game_background = pygame.image.load("bilder/hintergrund.png").convert()
newchar = pygame.image.load("bilder/katze.png").convert_alpha()

char_x = 100
char_y = 500
char_velocity_y = 0  # Vertikale Geschwindigkeit
gravity = 0.5

platforms = [
    pygame.Rect(100, 670, 110, 20),
    pygame.Rect(210, 960, 280, 20),
    pygame.Rect(1028, 960, 800, 20),
]

play_button_rect = pygame.Rect(720, 650, 500, 90)

game_state = "menu"

on_ground = False  # Zustand außerhalb der Schleife halten, damit der Sprungstatus konsistent ist

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_state == "menu":
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button_rect.collidepoint(event.pos):
                    game_state = "play"

    keys = pygame.key.get_pressed()

    if game_state == "play":
        # Horizontale Bewegung mit Kollisionsabfrage
        move_x = 0
        if keys[pygame.K_d]:
            move_x = 10
        elif keys[pygame.K_a]:
            move_x = -10

        char_rect = pygame.Rect(char_x + move_x, char_y, newchar.get_width(), newchar.get_height())
        horizontal_collision = False
        for platform in platforms:
            if char_rect.colliderect(platform):
                horizontal_collision = True
                break
        if not horizontal_collision:
            char_x += move_x

        # Vertikale Bewegung (Gravitation)
        char_velocity_y += gravity
        char_y += char_velocity_y

        # Rechteck für vertikale Kollision
        char_rect = pygame.Rect(char_x, char_y, newchar.get_width(), newchar.get_height())

        # Annahme: Solange der Charakter kollidiert und nach unten fällt, landet er auf der Plattform
        on_ground = False
        for platform in platforms:
            if char_rect.colliderect(platform):
                # Prüfe, ob Charakter von oben kommt (Fallgeschwindigkeit positiv) und nicht zu tief eindringt
                if char_velocity_y > 0 and char_rect.bottom <= platform.top + 15:
                    char_y = platform.top - newchar.get_height()
                    char_velocity_y = 0
                    on_ground = True
                    char_rect.bottom = platform.top  # Rechteck-Position anpassen, um "Durchrutschen" zu verhindern

        # Sprung nur ausführen, wenn auf dem Boden und nicht schon in der Luft
        if keys[pygame.K_SPACE] and on_ground:
            char_velocity_y = -15
            on_ground = False  # Sprung starten, nicht mehr am Boden

        screen.blit(game_background, (0, 0))
        screen.blit(newchar, (char_x, char_y))

    elif game_state == "menu":
        screen.blit(menu_background, (0, 0))

    pygame.display.update()
    clock.tick(60)
