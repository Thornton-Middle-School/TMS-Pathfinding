import sys
from heapq import heappush, heappop
import pygame
from graph import *

def main():
    window = pygame.display.set_mode((LENGTH, HEIGHT))
    window.fill(WHITE)
    pygame.display.set_caption("Thornton Pathfinding")
    pygame.display.set_icon(pygame.image.load("logo.png"))

    loading = HUGE_FONT.render("Loading...", True, BLACK)
    window.blit(loading, (400 - loading.get_width() / 2, 300 - loading.get_height() / 2))
    pygame.display.update()

    rooms, locations = create_graph()
    original = rooms.copy()

    min_x, min_y, max_x, max_y = 1000, 1000, -1000, -1000

    for node in original.values():
        if not upstairs(node):
            min_x = min(min_x, node.corner_x)
            max_x = max(max_x, node.corner_x)
            min_y = min(min_y, node.corner_y)
            max_y = max(max_y, node.corner_y)

    for x in drange(min_x, max_x + 1, 1):
        for y in drange(min_y, max_y + 1, 1):
            if locations.get((x, y)):
                continue

            tangencies = 0
            corner = False

            for node in original.values():
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
            for x_change in drange(-1, 2, 1):
                for y_change in drange(-1, 2, 1):
                    if not (x_change == 0 and y_change == 0) and (
                            adjacent := locations.get((node.corner_x + x_change, node.corner_y + y_change))):
                        node.adjacent_nodes.append(
                            (adjacent, 1 if abs(x_change) + abs(y_change) == 1 else DIAGONAL_DISTANCE))

    while True:
        window.fill(WHITE)

        for node in original.values():
            if node.type_ == "D205.3":
                continue

            pygame.draw.rect(window, BLACK, (node.min_x, node.min_y, node.max_x - node.min_x, node.max_y - node.min_y),
                             1)

            FONT = None

            if node.type_ in ["GB", "BB", "GB2", "GB3", "BB2", "BB3", "21B", "D110", "D210"]:
                FONT = MICRO_FONT

            elif node.type_ in ["16A", "20", "29", "28A", "37", "47", "A101", "A201", "A106", "A205", "B101", "B201",
                                "B106", "B205", "D105", "D205", "D106", "D206", "D112", "D212", "E101", "E107", "E201",
                                "E205"]:
                FONT = TINY_FONT

            elif node.type_ in ["Band", "32", "33", "34", "35", "36", "C101", "C201", "C107", "C205"]:
                FONT = MINI_FONT

            elif node.type_ in ["SG", "LG"]:
                FONT = BIG_FONT

            else:
                FONT = MEDIUM_FONT

            if len(node.type_) == 3 and node.type_[1] == "B":
                top = FONT.render(str(node.type_[:-1]), True, BLUE)
                multiline_render(window, f"{node.type_[:-1]}\n  {node.type_[-1]}", (node.min_x + node.max_x) / 2 - top.get_width() / 2,
                                 (node.min_y + node.max_y) / 2 - top.get_height() / 2, font=FONT, color=BLUE)

            else:
                text = FONT.render("S" if len(node.type_) == 4 and node.type_[-2] == "." else node.type_, True, BLUE)
                window.blit(text, ((node.min_x + node.max_x) / 2 - text.get_width() / 2,
                                   (node.min_y + node.max_y) / 2 - text.get_height() / 2))

        window.blit(HUGE_FONT.render("Upstairs", True, BLACK), (205, 20))
        window.blit(HUGE_FONT.render("Downstairs", True, BLACK), (100, 265))

        window.blit(TYPING_SIZE_FONT.render("Start: ", True, BLACK), (490, 66))
        window.blit(TYPING_SIZE_FONT.render("  End: ", True, BLACK), (490, 162))

        start_text_box = pygame.Rect(620, 63, 120, 50)
        end_text_box = pygame.Rect(620, 156, 120, 50)
        submit_button = pygame.Rect(560, 340, 120, 50)

        pygame.draw.rect(window, BLACK, start_text_box, width=5)
        pygame.draw.rect(window, BLACK, end_text_box, width=5)
        pygame.draw.rect(window, GREEN, submit_button)

        submit = TYPING_SIZE_FONT.render("Submit", True, BLACK)
        window.blit(submit, (620 - submit.get_width() / 2, 365 - submit.get_height() / 2))

        credits_text = ("Credits to:\n"
                        "The creator: Pranav Maddineedi\n"
                        "Mr. Register for measurements & the opportunity\n"
                        "to make this app\n"
                        "The creators of Google Earth for making a\n"
                        "product that contributed to the map's accuracy\n")

        multiline_render(window, credits_text, 445, 455, CREDITS_FONT)
        pygame.display.update()

        start_text = ""
        end_text = ""
        current = None

        INVALID = TYPING_SIZE_FONT.render("Invalid Input", True, RED)

        complete = False

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONUP:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if start_text_box.left < mouse_x < start_text_box.right and start_text_box.top < mouse_y < start_text_box.bottom:
                        current = start_text_box

                    elif end_text_box.left < mouse_x < end_text_box.right and end_text_box.top < mouse_y < end_text_box.bottom:
                        current = end_text_box

                    elif submit_button.left < mouse_x < submit_button.right and submit_button.top < mouse_y < submit_button.right:
                        start_bad = False
                        end_bad = False

                        if not original.get(start_text) or start_text[0] == "S" and start_text != "SG" or start_text == "D205.3":
                            pygame.draw.rect(window, RED, start_text_box, width=5)
                            start_bad = True

                        else:
                            pygame.draw.rect(window, BLACK, start_text_box, width=5)

                        if not original.get(end_text) or end_text[0] == "S" and end_text != "SG" or end_text == "D205.3":
                            pygame.draw.rect(window, RED, end_text_box, width=5)
                            end_bad = True

                        else:
                            pygame.draw.rect(window, BLACK, end_text_box, width=5)

                        if start_bad or end_bad:
                            window.blit(INVALID, (620 - INVALID.get_width() / 2, 270 - INVALID.get_height() / 2))
                            pygame.display.update()

                        else:
                            pygame.draw.rect(window, WHITE, (
                            620 - INVALID.get_width() / 2, 270 - INVALID.get_height() / 2, INVALID.get_width(),
                            INVALID.get_height()))
                            complete = True

                    else:
                        current = None

                if event.type == pygame.KEYDOWN:
                    if current in [None, pygame.K_SPACE]:
                        continue

                    if event.key == pygame.K_RETURN:
                        start_bad = False
                        end_bad = False

                        if not original.get(start_text) or start_text[0] == "S" and start_text != "SG" or start_text == "D205.3":
                            pygame.draw.rect(window, RED, start_text_box, width=5)
                            start_bad = True

                        else:
                            pygame.draw.rect(window, BLACK, start_text_box, width=5)

                        if not original.get(end_text) or end_text[0] == "S" and end_text != "SG" or end_text == "D205.3":
                            pygame.draw.rect(window, RED, end_text_box, width=5)
                            end_bad = True

                        else:
                            pygame.draw.rect(window, BLACK, end_text_box, width=5)

                        if start_bad or end_bad:
                            window.blit(INVALID, (620 - INVALID.get_width() / 2, 270 - INVALID.get_height() / 2))
                            pygame.display.update()

                        else:
                            pygame.draw.rect(window, WHITE, (
                            620 - INVALID.get_width() / 2, 270 - INVALID.get_height() / 2, INVALID.get_width(),
                            INVALID.get_height()))
                            complete = True

                    elif event.key == pygame.K_BACKSPACE:
                        if current == start_text_box:
                            start_text = start_text[:-1]

                        else:
                            end_text = end_text[:-1]

                    else:
                        start_text_surface_original = TYPING_SIZE_FONT.render(start_text + event.unicode.upper(), True, BLACK)
                        end_text_surface_original = TYPING_SIZE_FONT.render(end_text + event.unicode.upper(), True, BLACK)

                        if current == start_text_box and start_text_surface_original.get_width() < start_text_box.width - 10:
                            start_text += event.unicode.upper()

                        elif current == end_text_box and end_text_surface_original.get_width() < end_text_box.width - 10:
                            end_text += event.unicode.upper()

                    pygame.draw.rect(window, WHITE, (
                    start_text_box.left + 5, start_text_box.top + 5, start_text_box.width - 10,
                    start_text_box.height - 10))
                    pygame.draw.rect(window, WHITE, (
                    end_text_box.left + 5, end_text_box.top + 5, end_text_box.width - 10, end_text_box.height - 10))

                    start_text_surface = TYPING_SIZE_FONT.render(start_text, True, BLACK)
                    end_text_surface = TYPING_SIZE_FONT.render(end_text, True, BLACK)

                    window.blit(start_text_surface,
                                (680 - start_text_surface.get_width() / 2, 88 - start_text_surface.get_height() / 2))
                    window.blit(end_text_surface,
                                (680 - end_text_surface.get_width() / 2, 181 - end_text_surface.get_height() / 2))
                    pygame.display.update()

            if complete:
                break

        window.blit(CREDITS_FONT.render("Calculating...", True, BLACK), (50, 70))
        pygame.display.update()

        start, ends = [], []

        if len(end_text) >= 2 and end_text[1] == "B":
            start, ends = rooms[start_text], ([rooms["BB"], rooms["BB2"], rooms["BB3"]] if end_text[0] == "B"
                                              else [rooms["GB"], rooms["GB2"], rooms["GB3"]])

        else:
            start, ends = rooms[start_text], [rooms[end_text]]

        priority_queue: tuple[float, Node, float, float] = []
        start.distance = 0

        start_heuristic = overall_heuristic(start, ends, octile_heuristic)
        heappush(priority_queue, (start_heuristic, start_heuristic, 0, start))

        visited = {start}

        best_end = None

        while priority_queue:
            _, _, distance, node = heappop(priority_queue)

            if distance > node.distance:
                continue

            if node in ends:
                best_end = node
                break

            for adjacent, edge_weight in node.adjacent_nodes:
                if adjacent.distance > distance + edge_weight:
                    adjacent.from_ = (node, edge_weight)
                    adjacent.distance = distance + edge_weight

                    prediction = overall_heuristic(adjacent, ends, octile_heuristic)
                    heappush(priority_queue, (prediction + distance + edge_weight,
                                                    prediction, distance + edge_weight, adjacent))

                    visited.add(adjacent)

        node = best_end
        distance = 0.0

        while node.from_ is not None:
            if not (node.type_[:-1] == node.from_[0].type_[:-1] and node.type_[0] == "S" and node.type_ != "SG"):
                pygame.draw.line(window, ORANGE, (node.corner_x, node.corner_y),
                                 (node.from_[0].corner_x, node.from_[0].corner_y), width=2)

            _next = node.from_
            distance += _next[1]
            node.from_ = None
            node = _next[0]

        start.distance = float("inf")
        distance *= SCALE

        for node in visited:
            node.distance = float("inf")

        pygame.draw.circle(window, GREEN, (start.corner_x, start.corner_y), 4)
        pygame.draw.circle(window, RED, (best_end.corner_x, best_end.corner_y), 4)

        pygame.draw.rect(window, RED, submit_button)
        reset = TYPING_SIZE_FONT.render("Reset", True, BLACK)
        window.blit(reset, (620 - reset.get_width() / 2, 365 - reset.get_height() / 2))

        pygame.draw.rect(window, WHITE, (50, 70, 100, 50))

        text = (f"  Distance: {floor(distance)} ft\n"
                f"Walking Time: {floor((distance / 4) // 60)}:{("0" if floor((distance / 4) % 60) < 10 else "") + str(floor((distance / 4) % 60))}")

        rendered = TYPING_SIZE_FONT.render(text, True, BLACK)
        multiline_render(window, text, 620 - rendered.get_width() / 4, 270 - rendered.get_height(), TYPING_SIZE_FONT)

        pygame.display.update()

        while True:
            reset = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONUP:
                    mouse_x, mouse_y = pygame.mouse.get_pos()

                    if submit_button.left <= mouse_x <= submit_button.right and submit_button.top <= mouse_y <= submit_button.bottom:
                        reset = True
                        break

            if reset:
                break

if __name__ == "__main__":
    main()
