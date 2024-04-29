import pygame
from xml.etree import ElementTree
from constants import *
from graph import *

def main():
    window = pygame.display.set_mode((LENGTH, HEIGHT))
    window.fill(WHITE)
    pygame.display.set_caption("Thornton Shortest Paths")

    tree = ElementTree.parse("classrooms.kml")
    root = tree.getroot()[0]

    namespaces = {"ns0": "http://www.opengis.net/kml/2.2", "ns1": "http://www.google.com/kml/ext/2.2"}

    rooms: dict[str, Node] = {}

    for place in root.findall("ns0:Placemark", namespaces=namespaces):
        name = place.find("ns0:name", namespaces=namespaces).text
        longitude, latitude, _ = map(float, place.find("ns0:Point", namespaces=namespaces).find("ns0:coordinates", namespaces=namespaces).text.split(","))

        name = name[:-2] if name[0] != "S" or name[:2] == "SG" else name

        if name in rooms:
            rooms[name].min_x = min(rooms[name].min_x, longitude)
            rooms[name].max_x = max(rooms[name].max_x, longitude)
            rooms[name].min_y = min(rooms[name].min_y, HEIGHT - latitude - 200)
            rooms[name].max_y = max(rooms[name].max_y, HEIGHT - latitude - 200)

        else:
            rooms[name] = Node(min_x=longitude, max_x=longitude, min_y=HEIGHT - latitude - 200, max_y=HEIGHT - latitude - 200, color=BLUE, type_=name)

    for node in rooms.values():
        pygame.draw.rect(window, BLACK, (node.min_x, node.min_y, node.max_x - node.min_x, node.max_y - node.min_y), 1)
        window.blit(FONT.render(node.type_, True, BLUE), (node.min_x, node.min_y))
        pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event == pygame.QUIT:
                exit()

if __name__ == "__main__":
    main()
