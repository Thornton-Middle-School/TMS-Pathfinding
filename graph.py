from dataclasses import dataclass, field
import numpy
import pygame
import constants


@dataclass
class Node:
    min_x: float
    max_x: float
    min_y: float
    max_y: float
    color: tuple[int, int, int]
    type_: str # either: empty, classroom (#), obstacle

    def __hash__(self):
        return hash((self.min_x, self.max_x, self.min_y, self.max_y, self.color, self.type_))

    def __repr__(self):
        return f"{self.type_} @ ({self.min_x}, {self.min_y}), ({self.max_x}, {self.max_y}"

@dataclass
class NodePathData:                                                                                                                                                                                                                                                                                                                                                                                                                                  
   node: Node
   from_: 'NodePathData'
   distance: float
   heuristic: float


def create_graph() -> list[list[Node]]:
