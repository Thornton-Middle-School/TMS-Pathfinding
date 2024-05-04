from math import sqrt
import pygame

LENGTH, HEIGHT = 800, 600

DIAGONAL_DISTANCE = sqrt(2)
STAIRS_DISTANCE = 39.6
SCALE = 13/12

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (128, 128, 128)

BLUE = (0, 0, 240)
GREEN = (0, 230, 0)
RED = (230, 0, 0)
ORANGE = (255, 165, 0)

pygame.font.init()
MICRO_FONT = pygame.font.SysFont("comicsans", 7)
TINY_FONT = pygame.font.SysFont("comicsans", 8)
MINI_FONT = pygame.font.SysFont("comicsans", 9)
MEDIUM_FONT = pygame.font.SysFont("comicsans", 10)
BIG_FONT = pygame.font.SysFont("comicsans", 25)
HUGE_FONT = pygame.font.SysFont("comicsans", 40)
CREDITS_FONT = pygame.font.SysFont("comicsans", 15)
TYPING_SIZE_FONT = pygame.font.SysFont("comicsans", 30)
