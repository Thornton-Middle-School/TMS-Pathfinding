from dataclasses import dataclass, field
import numpy
import pygame
import constants


@dataclass
class Node:
   x: int
   y: int
   color: tuple[int, int, int]
   type_: str # either: empty, a number (classroom, use .is), obstacle


   def __hash__(self):
       return hash((self.x, self.y))


   def __repr__(self):
       return self.type_ if self.type_.isnumeric() else "X" if self.type_ == "obstacle" else " " if self.type_ == "stairs" else " "


@dataclass
class NodePathData:                                                                                                                                                                                                                                                                                                                                                                                                                                  
   node: Node
   from_: 'NodePathData'
   distance: float
   heuristic: float


def create_graph() -> list[list[Node]]:
