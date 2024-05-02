import pygame
from xml.etree import ElementTree
from heapq import heappush, heappop
from copy import deepcopy
from constants import *
from graph import *

def main():
    while True:
        window = pygame.display.set_mode((LENGTH, HEIGHT))
        window.fill(WHITE)
        pygame.display.set_caption("Thornton Pathfinding")
        pygame.display.set_icon(pygame.image.load("logo.png"))

        rooms, locations = create_graph()

        for node in rooms.values():
            pygame.draw.rect(window, BLACK, (node.min_x, node.min_y, node.max_x - node.min_x, node.max_y - node.min_y), 1)

            FONT = None

            if node.type_ in ["GB", "BB", "GB2", "GB3", "BB2", "BB3", "21B", "D110", "D210", "E101", "E107", "E201", "E205"]:
                FONT = MICRO_FONT

            elif node.type_ in ["16A", "20", "29", "28A", "37", "47", "A101", "A201", "A106", "A206", "B101", "B201", "B106", "B206", "D105", "D205", "D106", "D206", "D112", "D212"]:
                FONT = TINY_FONT

            elif node.type_ in ["Band", "32", "33", "34", "35", "36", "C101", "C201", "C107", "C205"]:
                FONT = MINI_FONT

            elif node.type_ in ["SG", "LG"]:
                FONT = BIG_FONT

            else:
                FONT = MEDIUM_FONT

            text = FONT.render(node.type_[:-1] if len(node.type_) == 3 and node.type_[1] == "B" else "S" if len(node.type_) == 4 and node.type_[-2] == "." else node.type_, True, BLUE)
            window.blit(text, ((node.min_x + node.max_x) / 2 - text.get_width() / 2, (node.min_y + node.max_y) / 2 - text.get_height() / 2))

        window.blit(HUGE_FONT.render("Upstairs", True, BLACK), (190, 0))
        window.blit(HUGE_FONT.render("Downstairs", True, BLACK), (100, 240))

        window.blit(HUGE_FONT.render("Start: ", True, BLACK), (475, 50))
        window.blit(HUGE_FONT.render("  End: ", True, BLACK), (475, 170))

        start_text_box = pygame.Rect(620, 43, 120, 80)
        end_text_box = pygame.Rect(620, 163, 120, 80)
        submit_button = pygame.Rect(545, 283, 160, 80)

        pygame.draw.rect(window, BLACK, start_text_box, width=5)
        pygame.draw.rect(window, BLACK, end_text_box, width=5)
        pygame.draw.rect(window, GREEN, submit_button)

        window.blit(HUGE_FONT.render("Submit", True, BLACK), (560, 290))

        def multiline_render(text, start_x, start_y):
            x, y = start_x, start_y

            for line in text.split("\n"):
                window.blit(CREDITS_and_SIZE_FONT.render(line, True, BLACK), (x, y))
                y += CREDITS_and_SIZE_FONT.get_height()

        credits_text = ("Credits to:\n"
                        "The creator: Pranav Maddineedi\n"
                        "Mr. Register for measurements & the opportunity\n"
                        "to make this app\n"
                        "The creators of Google Earth for making a\n"
                        "product that contributed to the map's accuracy\n")

        multiline_render(credits_text, 450, 400)
        pygame.display.update()

        start_text = ""
        end_text = ""
        current = None

        complete = False

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.MOUSEBUTTONUP:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if start_text_box.left < mouse_x < start_text_box.right and start_text_box.top < mouse_y < start_text_box.bottom:
                        current = start_text_box

                    elif end_text_box.left < mouse_x < end_text_box.right and end_text_box.top < mouse_y < end_text_box.bottom:
                        current = end_text_box

                    elif submit_button.left < mouse_x < submit_button.right and submit_button.top < mouse_y < submit_button.right and rooms.get(start_text) and rooms.get(end_text):
                        complete = True

                    else:
                        current = None

                if event.type == pygame.KEYUP:
                    if current is None:
                        continue

                    if event.key == pygame.K_BACKSPACE:
                        if current == start_text_box:
                            start_text = start_text[:-1]

                        else:
                            end_text = end_text[:-1]

                    else:
                        if current == start_text_box:
                            start_text += event.unicode

                        else:
                            end_text += event.unicode

                    pygame.draw.rect(window, WHITE, (start_text_box.left + 5, start_text_box.top + 5, start_text_box.width - 10, start_text_box.height - 10))
                    pygame.draw.rect(window, WHITE, (end_text_box.left + 5, end_text_box.top + 5, end_text_box.width - 10, end_text_box.height - 10))

                    start_text_surface = HUGE_FONT.render(start_text, True, BLACK)
                    end_text_surface = HUGE_FONT.render(end_text, True, BLACK)

                    window.blit(start_text_surface,
                                (680 - start_text_surface.get_width() / 2, 83 - start_text_surface.get_height() / 2))
                    window.blit(end_text_surface,
                                (680 - end_text_surface.get_width() / 2, 203 - end_text_surface.get_height() / 2))
                    pygame.display.update()

            if complete:
                break

        window.blit(CREDITS_and_SIZE_FONT.render("Calculating...", True, BLACK), (50, 50))
        pygame.display.update()

        start, end = rooms[start_text], rooms[end_text]

        min_x, min_y, max_x, max_y = 1000, 1000, -1000, -1000

        for node in rooms.values():
            if not upstairs(node):
                min_x = min(min_x, node.corner_x)
                max_x = max(max_x, node.corner_x)
                min_y = min(min_y, node.corner_y)
                max_y = max(max_y, node.corner_y)

        original = list(rooms.values()).copy()

        for x in range(min_x, max_x + 1):
            for y in range(min_y, max_y + 1):
                if locations.get((x, y)):
                    continue

                tangencies = 0
                corner = False

                for node in original:
                    if node == end:
                        corner = corner

                    if node.min_x < x < node.max_x and node.min_y < y < node.max_y:
                        tangencies = 100
                        break

                    if node.min_x <= x <= node.max_x and node.min_y <= y <= node.max_y:
                        tangencies += 1

                        if x in [node.min_x, node.max_x] and y in [node.min_y, node.max_y]:
                            corner = True
                            break

                if tangencies <= 1 or corner:
                    rooms[f"Empty @ ({x}, {y})"] = Node(x, x, y, y, "empty", corner_x=x, corner_y=y)
                    locations[(x, y)] = rooms[f"Empty @ ({x}, {y})"]

        for node in rooms.values():
            if not upstairs(node) or node.type_ == "empty":
                for x_change in range(-1, 2):
                    for y_change in range(-1, 2):
                        if not (x_change == 0 and y_change == 0) and (adjacent := locations.get((node.corner_x + x_change, node.corner_y + y_change))):
                            node.adjacent_nodes.append((adjacent, 1 if abs(x_change) + abs(y_change) == 1 else DIAGONAL_DISTANCE))

        priority_queue: tuple[float, Node, float, float] = []
        start.distance = 0
        heappush(priority_queue, (heuristic(start, end), heuristic(start, end), 0, start))

        while priority_queue:
            _, _, distance, node = heappop(priority_queue)

            if distance > node.distance:
                continue

            if node == end:
                break

            for adjacent, edge_weight in node.adjacent_nodes:
                if adjacent.distance > distance + edge_weight:
                    adjacent.from_ = (node, edge_weight)
                    adjacent.distance = distance + edge_weight
                    heappush(priority_queue, (heuristic(adjacent, end) + distance + edge_weight, heuristic(adjacent, end), distance + edge_weight, adjacent))

        node = end
        distance = 0.0

        while node.from_ is not None:
            if not (node.type_[:-1] == node.from_[0].type_[:-1] and node.type_[0] == "S" and node.type_ != "SG"):
                pygame.draw.line(window, YELLOW, (node.corner_x, node.corner_y), (node.from_[0].corner_x, node.from_[0].corner_y), width=2)

            distance += node.from_[1]
            node = node.from_[0]

        distance *= SCALE

        pygame.draw.circle(window, GREEN, (start.corner_x, start.corner_y), 4)
        pygame.draw.circle(window, RED, (end.corner_x, end.corner_y), 4)

        pygame.draw.rect(window, RED, submit_button)
        window.blit(HUGE_FONT.render("Reset", True, BLACK), (570, 290))

        pygame.draw.rect(window, WHITE, (50, 50, 100, 50))
        multiline_render(f"Distance: {floor(distance)} ft\n"
                         f"Predicted Walking time: {floor((distance/4)//60):}min and {floor((distance/4)%60)}sec", # People walk at about 4 ft per second
                         20, 175)
        pygame.display.update()

        while True:
            reset = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.MOUSEBUTTONUP:
                    mouse_x, mouse_y = pygame.mouse.get_pos()

                    if submit_button.left <= mouse_x <= submit_button.right and submit_button.top <= mouse_y <= submit_button.bottom:
                        reset = True
                        break

            if reset:
                break

if __name__ == "__main__":
    main()
