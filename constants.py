from math import sqrt
import pygame

LENGTH, WIDTH = 800, 600 # Fills the screen on an Amazon Fire 7
SIDE_BUTTON_SIZE = WIDTH // 9
NODE_LENGTH, NODE_WIDTH = LENGTH // 16, WIDTH // 20 # Approximately the number of rooms in the school dimension-wise

DIAGONAL_DISTANCE = sqrt(2)
DIAGONAL_DISTANCE_REPR = "√2"
NODE_LENGTH_DISTANCE, NODE_WIDTH_DISTANCE, STAIR_DISTANCE = 40, 33, 56

WHITE = (255, 255, 255) # 100% Luminosity
BLACK = (0, 0, 0) # 0%
GREY = (128, 128, 128) # 50%

BLUE = (0, 0, 255) # Most classrooms
BROWN = (160, 82, 45) # Some classrooms
LIGHT_BROWN = (255, 248, 220) # Some classrooms

pygame.font.init()
FONT = pygame.font.SysFont("comicsans", 30)
