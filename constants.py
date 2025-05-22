from math import sqrt
import pygame

LENGTH, HEIGHT = 1600, 960

DIAGONAL_DISTANCE = sqrt(2)
STAIRS_DISTANCE = 39.6
SCALE = 0.8572 # approximate scale calculated after finding distance from 24-36 and comparing with px in app

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (128, 128, 128)

BLUE = (0, 0, 240)
GREEN = (0, 230, 0)
RED = (230, 0, 0)
ORANGE = (255, 165, 0)

pygame.font.init()
MICRO_FONT = pygame.font.SysFont("timesnewroman", 10)
TINY_FONT = pygame.font.SysFont("timesnewroman", 12)
MINI_FONT = pygame.font.SysFont("timesnewroman", 14)
MEDIUM_FONT = pygame.font.SysFont("timesnewroman", 16)
BIG_FONT = pygame.font.SysFont("timesnewroman", 30)
HUGE_FONT = pygame.font.SysFont("timesnewroman", 45)
SLIGHTLY_BIG_FONT = pygame.font.SysFont("timesnewroman", 22)
TYPING_SIZE_FONT = pygame.font.SysFont("timesnewroman", 40)
KEY_FONT = pygame.font.SysFont("timesnewroman", 25)
INSTRUCTION_FONT = pygame.font.SysFont("timesnewroman", 20)
