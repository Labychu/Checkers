import pygame


WIDTH, HEIGHT = 700, 700
ROWS, COLS = 8, 8
SQUARE_SIZE = HEIGHT // ROWS

RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
CLR1 = (237, 191, 104)
CLR2 = (122, 64, 20)
BG = (43, 64, 48)

CROWN = pygame.transform.scale(pygame.image.load("assets/crown.png"), (44, 25))
