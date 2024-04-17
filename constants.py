from math import sqrt
import pygame

LENGTH, WIDTH = 800, 600
SIDE_BUTTON_SIZE = WIDTH // 9
NODE_LENGTH, NODE_WIDTH = LENGTH // 16, WIDTH // 20

DIAGONAL_DISTANCE = sqrt(2)
DIAGONAL_DISTANCE_REPR = "√"
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (128, 128, 128)
BLUE = (0, 0, 255)

NODE_LENGTH_DISTANCE, NODE_WIDTH_DISTANCE, STAIR_DISTANCE = ..., ..., ...

pygame.font.init()
FONT = pygame.font.SysFont("comicsans", 30)
