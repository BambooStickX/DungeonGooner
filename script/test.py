import pygame
from sys import exit

pygame.init()
screen = pygame.display.set_mode((1920, 1080))
pygame.display.set_caption("Platform Position Finder")
clock = pygame.time.Clock()

background = pygame.image.load("bilder/hintergrund.png").convert()

font = pygame.font.SysFont(None, 36)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    mouse_x, mouse_y = pygame.mouse.get_pos()

    screen.blit(background, (0, 0))

    # Text mit Maus-Koordinaten rendern
    coord_text = font.render(f"Mouse Position: ({mouse_x}, {mouse_y})", True, (255, 255, 255))
    screen.blit(coord_text, (20, 20))

    # Optional: Linien anzeigen, um eine bessere Referenz zu haben
    pygame.draw.line(screen, (255, 0, 0), (0, mouse_y), (1920, mouse_y), 1)
    pygame.draw.line(screen, (255, 0, 0), (mouse_x, 0), (mouse_x, 1080), 1)

    pygame.display.update()
    clock.tick(60)
