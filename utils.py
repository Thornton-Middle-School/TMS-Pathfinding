from math import sqrt
from functools import total_ordering

from collections.abc import MutableMapping
from dataclasses import dataclass, field, replace

import pygame

LENGTH, HEIGHT = 1600, 960

DIAGONAL_DISTANCE = sqrt(2)
STAIRCASE_LENGTH = 35
SCALE = 0.8572 # approximate scale calculated after finding distance from 24-36 and comparing with px in app

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (128, 128, 128)

BLUE = (0, 0, 240)
GREEN = (0, 230, 0)
RED = (230, 0, 0)
ORANGE = (255, 165, 0)

pygame.font.init()
MICRO_FONT = pygame.font.Font("font.otf", 10)
TINY_FONT = pygame.font.Font("font.otf", 12)
MINI_FONT = pygame.font.Font("font.otf", 14)
MEDIUM_FONT = pygame.font.Font("font.otf", 16)
BIG_FONT = pygame.font.Font("font.otf", 30)
HUGE_FONT = pygame.font.Font("font.otf", 45)
SLIGHTLY_BIG_FONT = pygame.font.Font("font.otf", 22)
TYPING_SIZE_FONT = pygame.font.Font("font.otf", 40)
KEY_FONT = pygame.font.Font("font.otf", 25)
INSTRUCTION_FONT = pygame.font.Font("font.otf", 20)

@total_ordering
@dataclass
class Node:
    min_x: float
    max_x: float
    min_y: float
    max_y: float
    type_: str
    color: tuple[int, int, int] = WHITE
    corner_x: float = -1
    corner_y: float = -1
    from_: tuple['Node', float] = None
    distance: float = float("inf")

    def __hash__(self):
        return hash((self.min_x, self.max_x, self.min_y, self.max_y, self.color, self.type_))

    def __repr__(self):
        return f"{self.type_} @ ({self.min_x}, {self.min_y})<->({self.max_x}, {self.max_y})"

    def __lt__(self, other):
        return (self.min_x, self.max_x, self.min_y, self.max_y, self.color, self.type_) < (other.min_x, other.max_x, other.min_y, other.max_y, other.color, other.type_)

    def __eq__(self, other):
        return hash(self) == hash(other) 
    
    def copy(self):
        return replace(self)
    
class NodeDict(MutableMapping[str, dict[str, Node]]):
    def __init__(self, data: dict[str, dict[str, Node]]=None):
        self.data = data if data is not None else {"Rooms": {}, "Other": {}}
        
    @property
    def rooms(self) -> dict[str, Node]:
        return self.data["Rooms"]
    
    @property
    def other(self) -> dict[str, Node]:
        return self.data["Other"]
    
    def placement(self, key: str):
        if not isinstance(key, str):
            raise TypeError(f"Key must be a string, not {type(key).__name__}")
        
        return "Other" if key.startswith("Empty @ ") else "Rooms"
        
    def __getitem__(self, key: str) -> Node:
        if not isinstance(key, str):
            raise TypeError(f"Key must be a string, not {type(key).__name__}")
        
        return self.data[self.placement(key)][key]
    
    def __setitem__(self, key: str, value: Node):
        if not isinstance(key, str):
            raise TypeError(f"Key must be a string, not {type(key).__name__}")
        
        self.data[self.placement(key)][key] = value
        
    def __delitem__(self, key: str):
        del self.data[self.placement(key)][key]
        
    def __iter__(self):
        return (self.rooms | self.other).__iter__()

    def __len__(self):
        return self.rooms.__len__() + self.other.__len__()
    
    def __dict__(self):
        return self.data
    
    def __getstate__(self):
        return self.data
    
    def __setstate__(self, state):
        self.data = state
    
    def __repr__(self):
        return f"NodeDict({self.data})"
    
def upstairs(node: Node | str):
    name = node.type_ if isinstance(node, Node) else node

    if len(name) > 2:
        if name[1] == "2" or name[2] == "3" or name[0] == "S" and name[3] == "2":
            return True

    return False

def octile_heuristic(node: Node, end: Node):
    y_difference = abs(node.corner_y - end.corner_y) if upstairs(node) == upstairs(end) else abs(abs(node.corner_y - end.corner_y) - 270)
    return (abs(node.corner_x - end.corner_x) + y_difference + (DIAGONAL_DISTANCE - 2) * min(abs(node.corner_x - end.corner_x), y_difference) + (upstairs(node) != upstairs(end)) * STAIRCASE_LENGTH) * 1.001

def euclidean_heuristic(node: Node, end: Node) -> float:
    if upstairs(node) != upstairs(end):
        return (sqrt((node.corner_x - end.corner_x) ** 2 + (abs(node.corner_y - end.corner_y) - 270) ** 2) + STAIRCASE_LENGTH) * 1.001

    return sqrt((node.corner_x - end.corner_x) ** 2 + (node.corner_y - end.corner_y) ** 2) * 1.001

def closest_to_heuristic(node: Node, ends: list[Node], heuristic_function):
    return min(heuristic_function(node, end) for end in ends)

def multiline_render(window: pygame.Surface, text: str, x: float, y: float, font: pygame.font.Font, color=BLACK, center=False, spacing=1.0) -> None:
    line_count = text.count("\n") + 1
    rendered_lines = [font.render(line, True, color) for line in text.split("\n")]

    if center:
        y -= (sum(rendered.get_height() for rendered in rendered_lines) + font.get_height() * (line_count - 1) * (spacing - 1)) / 2

    for line, rendered in zip(text.split("\n"), rendered_lines):
        window.blit(rendered, (((x - rendered.get_width() / 2) if center else x), y))
        y += rendered.get_height() + font.get_height() * (spacing - 1)