from typing import Any
from dataclasses import dataclass, field
import numpy
import pygame
import constants

@dataclass
class Node:
    x: int
    y: int
    color: tuple[int, int, int]
    representation: str #
