from math import sqrt, floor
from functools import total_ordering
from dataclasses import dataclass, field
from xml.etree import ElementTree
from constants import *

@total_ordering
@dataclass
class Node:
    min_x: float
    max_x: float
    min_y: float
    max_y: float
    type_: str # either: empty, classroom (#), obstacle
    color: tuple[int, int, int] = WHITE
    adjacent_nodes: list[tuple['Node', float]] = field(default_factory=lambda: [])
    corner_x: float = -1
    corner_y: float = -1
    from_: tuple['Node', float] = None
    distance: float = float("inf")

    def __hash__(self):
        return hash((self.min_x, self.max_x, self.min_y, self.max_y, self.color, self.type_))

    def __repr__(self):
        return f"{self.type_} @ ({self.min_x}, {self.min_y}), ({self.max_x}, {self.max_y})"

    def __lt__(self, other):
        return (self.min_x, self.max_x, self.min_y, self.max_y, self.color, self.type_) < (other.min_x, other.max_x, other.min_y, other.max_y, other.color, other.type_)

    # def __eq__(self, other):
    #     (self.min_x, self.max_x, self.min_y, self.max_y, self.color, self.type_) < (other.min_x, other.max_x, other.min_y, other.max_y, other.color, other.type_)

def upstairs(node: Node | str):
    if isinstance(node, Node):
        return node.corner_y < 224

    if len(node) > 2:
        if node[1] == "2" or node[2] == "3" or node[0] == "S" and node[3] == "2":
            return True

    return False

def create_graph() -> tuple[dict[str, Node], dict[tuple[int, int], Node]]:
    tree = ElementTree.parse("classrooms.kml")
    root = tree.getroot()[0]

    namespaces = {"ns0": "http://www.opengis.net/kml/2.2", "ns1": "http://www.google.com/kml/ext/2.2"}

    rooms: dict[str, Node] = {}
    locations: dict[tuple[int, int], Node] = {}

    for place in root.findall("ns0:Placemark", namespaces=namespaces):
        name = place.find("ns0:name", namespaces=namespaces).text
        longitude, latitude, _ = map(float, place.find("ns0:Point", namespaces=namespaces).find("ns0:coordinates", namespaces=namespaces).text.split(","))

        original = name
        name = name[:-2] if name[0] != "S" or name[:2] == "SG" else name

        y_subtraction = 320 if upstairs(name) else 50

        if name in rooms:
            rooms[name].min_x = min(rooms[name].min_x, longitude)
            rooms[name].max_x = max(rooms[name].max_x, longitude)
            rooms[name].min_y = min(rooms[name].min_y, HEIGHT - latitude - y_subtraction)
            rooms[name].max_y = max(rooms[name].max_y, HEIGHT - latitude - y_subtraction)

        else:
            rooms[name] = Node(min_x=longitude, max_x=longitude, min_y=HEIGHT - latitude - y_subtraction, max_y=HEIGHT - latitude - y_subtraction, type_=name)

        if original[-1] == "1" or original[0] == "S" and original[:-2] != "SG":
            rooms[name].corner_x = longitude
            rooms[name].corner_y = HEIGHT - latitude - y_subtraction

    rooms["A201"].adjacent_nodes = [(rooms["SA.2"], 14.56), (rooms["A205"], 29)]
    rooms["A205"].adjacent_nodes = [(rooms["SA.2"], 43.21), (rooms["A201"], 29), (rooms["B201"], 4)]
    rooms["B201"].adjacent_nodes = [(rooms["A205"], 4), (rooms["B205"], 22.78), (rooms["SB.2"], 22.48)]
    rooms["B205"].adjacent_nodes = [(rooms["A205"], 23.13), (rooms["B201"], 22.78), (rooms["SB.2"], 10.33), (rooms["GB3"], 10.74)]
    rooms["GB3"].adjacent_nodes = [(rooms["B205"], 10.74), (rooms["SB.2"], 12.01), (rooms["BB3"], 7.9)]
    rooms["BB3"].adjacent_nodes = [(rooms["SB.2"], 19.71), (rooms["GB3"], 7.9), (rooms["C201"], 38.9), (rooms["D205"], 38.67)]
    rooms["D205"].adjacent_nodes = [(rooms["BB3"], 38.67), (rooms["D206"], 22.17), (rooms["SD.2"], 6.59)]
    rooms["D206"].adjacent_nodes = [(rooms["D205"], 22.17), (rooms["D210"], 16.27), (rooms["SD.2"], 23.77)]
    rooms["D210"].adjacent_nodes = [(rooms["D206"], 16.27), (rooms["D212"], 20.1), (rooms["SD.2"], 39.65), (rooms["E201"], 36.76)]
    rooms["D212"].adjacent_nodes = [(rooms["D210"], 20.1), (rooms["SD.2"], 59.56)]
    rooms["C201"].adjacent_nodes = [(rooms["BB3"], 38.9), (rooms["C205"], 28.1), (rooms["SC.2"], 35.8)]
    rooms["C205"].adjacent_nodes = [(rooms["C201"], 28.1), (rooms["SC.2"], 4.04)]
    rooms["E201"].adjacent_nodes = [(rooms["D210"], 36.76), (rooms["E205"], 28.22), (rooms["SE.2"], 14.96)]
    rooms["E205"].adjacent_nodes = [(rooms["E201"], 28.22), (rooms["SE.2"], 39.47)]

    rooms["SA.2"].adjacent_nodes = [(rooms["A201"], 14.56), (rooms["A205"], 43.21), (rooms["SA.1"], STAIRS_DISTANCE)]
    rooms["SB.2"].adjacent_nodes = [(rooms["B201"], 22.48), (rooms["B205"], 10.33), (rooms["GB3"], 12.01), (rooms["BB3"], 19.71), (rooms["SB.1"], STAIRS_DISTANCE)]
    rooms["SC.2"].adjacent_nodes = [(rooms["C201"], 35.8), (rooms["C205"], 4.04), (rooms["SC.1"], STAIRS_DISTANCE)]
    rooms["SD.2"].adjacent_nodes = [(rooms["D205"], 6.59), (rooms["D206"], 23.77), (rooms["D210"], 39.65), (rooms["D212"], 59.56), (rooms["SD.1"], STAIRS_DISTANCE)]
    rooms["SE.2"].adjacent_nodes = [(rooms["E201"], 14.96), (rooms["E205"], 39.47), (rooms["SE.1"], STAIRS_DISTANCE)]
    rooms["SA.1"].adjacent_nodes.append((rooms["SA.2"], STAIRS_DISTANCE))
    rooms["SB.1"].adjacent_nodes.append((rooms["SB.2"], STAIRS_DISTANCE))
    rooms["SC.1"].adjacent_nodes.append((rooms["SC.2"], STAIRS_DISTANCE))
    rooms["SD.1"].adjacent_nodes.append((rooms["SD.2"], STAIRS_DISTANCE))
    rooms["SE.2"].adjacent_nodes.append((rooms["SE.2"], STAIRS_DISTANCE))

    for name, node in rooms.items():
        node.min_x = floor(node.min_x)
        node.max_x = floor(node.max_x)
        node.min_y = floor(node.min_y)
        node.max_y = floor(node.max_y)
        node.corner_x = floor(node.corner_x)
        node.corner_y = floor(node.corner_y)

    for node in rooms.values():
        locations[(node.corner_x, node.corner_y)] = node

    return rooms, locations

def heuristic(node: Node, end: Node) -> float:
    if upstairs(node) != upstairs(end):
        return (sqrt((node.corner_x - end.corner_x) ** 2 + (abs(node.corner_y - end.corner_y) - 270) ** 2) + STAIRS_DISTANCE) * 1.001

    return sqrt((node.corner_x - end.corner_x) ** 2 + (node.corner_y - end.corner_y) ** 2) * 1.001

# Draw the credits
def multiline_render(window: pygame.surface, text: str, start_x: float, start_y: float, font: pygame.font.Font) -> None:
    x, y = start_x, start_y

    for line in text.split("\n"):
        window.blit(font.render(line, True, BLACK), (x, y))
        y += font.get_height()
