import sys
import asyncio
import pickle

from math import floor

from heapq import heappush, heappop
from collections import defaultdict

from utils import *

def shortest_path(start: Node, ends: Node, adjacency: defaultdict[Node, list[list[Node, float]]], window: pygame.Surface) -> list[Node]:
    priority_queue: tuple[float, Node, float, float] = []
    start.distance = 0
    
    start_heuristic = closest_to_heuristic(start, ends, octile_heuristic)
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

        for adjacent, edge_weight in adjacency.get(node):
            if adjacent.distance > distance + edge_weight:
                adjacent.from_ = (node, edge_weight)
                adjacent.distance = distance + edge_weight

                prediction = closest_to_heuristic(adjacent, ends, octile_heuristic)
                heappush(priority_queue, (prediction + distance + edge_weight,
                                            prediction, distance + edge_weight, adjacent))

                visited.add(adjacent)

    node = best_end
    distance = 0.0

    while node.from_ is not None:
        print(node)
        
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

    pygame.draw.rect(window, WHITE, (50, 70, 150, 70))

    results_text = (f"Distance: {floor(distance)} ft\n"
                    f"Walking Time: ~ {floor((distance / 308 * 75) // 60)}:{("0" if floor((distance / 308 * 75) % 60) < 10 else "") + str(floor((distance / 308 * 75) % 60))}")

    multiline_render(window, results_text, 1205, 357, TYPING_SIZE_FONT, center=True)
    pygame.display.update()
    
async def main():
    window = pygame.display.set_mode((LENGTH, HEIGHT))
    window.fill(WHITE)

    pygame.display.set_caption("Thornton Middle School Pathfinding")
    pygame.display.set_icon(pygame.image.load("logo.png"))

    loading = HUGE_FONT.render("Loading...", True, BLACK)
    window.blit(loading, (LENGTH / 2 - loading.get_width() / 2, HEIGHT / 2 - loading.get_height() / 2))
    pygame.display.update()

    await asyncio.sleep(0)

    with open("classrooms.pkl", "rb") as file:
        points: NodeDict = pickle.load(file)
        
    with open("adjacency.pkl", "rb") as file:    
        adjacency: defaultdict[Node, list[list[Node, float]]] = defaultdict(list, pickle.load(file))
    
    while True:
        await asyncio.sleep(0)

        window.fill(WHITE)

        for node in points.rooms.values():
            if node.type_ == "D205.3":
                continue

            pygame.draw.rect(window, BLACK, (node.min_x, node.min_y, node.max_x - node.min_x, node.max_y - node.min_y),
                             1)

            if node.type_ in ["GB", "BB", "GB2", "GB3", "BB2", "BB3", "GB4", "BB4", "21B", "D110", "D210"]:
                font = MICRO_FONT

            elif node.type_ in ["16A", "20", "29", "28A", "37", "47", "A101", "A201", "A106", "A205", "B101", "B201",
                                "B106", "B205", "D105", "D205", "D106", "D206", "D112", "D212", "E101", "E107", "E201",
                                "E205"]:
                font = TINY_FONT

            elif node.type_ in ["Band", "32", "33", "34", "35", "36", "C101", "C201", "C107", "C205"]:
                font = MINI_FONT

            elif node.type_ in ["SG", "LG"]:
                font = BIG_FONT

            else:
                font = MEDIUM_FONT

            name = "S" if len(node.type_) == 4 and node.type_[-2] == "." else node.type_ if node.type_ not in (
            "GB", "BB") else node.type_[0] + "1"

            if len(name) > 2 and name[:2] in ("BB", "GB") and name[-1] in ("2", "3"):
                name = f"{name[:-1]}\n{node.type_[-1]}"
                multiline_render(window, name, (node.min_x + node.max_x) / 2, (node.min_y + node.max_y) / 2, font,
                                 color=BLUE, center=True)

            else:
                text = font.render(name, True, BLUE)
                window.blit(text, ((node.min_x + node.max_x) / 2 - text.get_width() / 2,
                                   (node.min_y + node.max_y) / 2 - text.get_height() / 2))

        multiline_render(window, "Upstairs", 495, 70, HUGE_FONT, color=BLACK, center=True)
        window.blit(HUGE_FONT.render("Downstairs", True, BLACK), (188, 379))

        start_text_box = pygame.Rect(1005, 97, 150, 60)
        end_text_box = pygame.Rect(1005, 197, 150, 60)
        submit_button = pygame.Rect(1305, 147, 150, 60)

        pygame.draw.rect(window, BLACK, start_text_box, width=5)
        pygame.draw.rect(window, BLACK, end_text_box, width=5)
        pygame.draw.rect(window, GREEN, submit_button)
        pygame.draw.rect(window, BLACK, submit_button, width=5)

        start_render_text = TYPING_SIZE_FONT.render("Start: ", True, BLACK)
        end_render_text = TYPING_SIZE_FONT.render("  End: ", True, BLACK)
        
        window.blit(start_render_text, (875, 129 - start_render_text.get_height() / 2))
        window.blit(end_render_text, (875, 229 - end_render_text.get_height() / 2))

        submit = TYPING_SIZE_FONT.render("Submit", True, BLACK)
        window.blit(submit, (1380 - submit.get_width() / 2, 182 - submit.get_height() / 2))

        key_text = ("Key:\n"
                    "B/BB or G/GB + (identifier) (very small font): Boys/Girls Bathroom\n"
                    "LG/SG: Large/Small Gym\n"
                    "BLR/GLR: Boys/Girls Locker Room\n"
                    "S: Stairs")

        width = max(KEY_FONT.render(line, True, BLACK).get_width() for line in key_text.split("\n"))
        multiline_render(window, key_text, (2411 - width) / 2, HEIGHT - 30 - KEY_FONT.get_height() * 7, KEY_FONT,
                         spacing=1.5)

        instructions = ("Instructions:\n"
                        "1. Click on the start and end boxes to enter the room numbers.\n"
                        "    Note: for bathrooms, type up the name as shown with or without the second letter (B).\n"
                        "    For the destination room, typing just B/BB or G/GB will show the path to the closest\n"
                        "    Boys'/Girls' bathroom.\n"
                        "2. When complete, press submit or press enter/return on your keyboard.\n"
                        "3. After a few seconds, a path should show up. Green is the start, ed is the end, orange\n"
                        "    is the path itself. \n"
                        "4. If you want to reset, click the reset button.\n")

        width = max(INSTRUCTION_FONT.render(line, True, BLACK).get_width() for line in instructions.split("\n"))
        multiline_render(window, instructions, (2411 - width) / 2, HEIGHT - 50 - KEY_FONT.get_height() * 7 - INSTRUCTION_FONT.get_height() * 14, INSTRUCTION_FONT, spacing=1.5)

        pygame.display.update()

        start_text = ""
        end_text = ""
        current = None

        invalid_surface = TYPING_SIZE_FONT.render("Invalid Input", True, RED)

        complete = False

        while True:
            for event in pygame.event.get():
                submit = False

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONUP:
                    mouse_x, mouse_y = pygame.mouse.get_pos()

                    # Add extra padding for web click detection
                    if (start_text_box.left - 5) <= mouse_x <= (start_text_box.right + 5) and (start_text_box.top - 5) <= mouse_y <= (start_text_box.bottom + 5):
                        current = start_text_box
                        pygame.display.update()

                    elif (end_text_box.left - 5) <= mouse_x <= (end_text_box.right + 5) and (end_text_box.top - 5) <= mouse_y <= (end_text_box.bottom + 5):
                        current = end_text_box
                        pygame.display.update()

                    elif (submit_button.left - 5) <= mouse_x <= (submit_button.right + 5) and (submit_button.top - 5) <= mouse_y <= (submit_button.bottom + 5):
                        submit = True
                        pygame.display.update()

                    else:
                        current = None

                if event.type == pygame.KEYDOWN:
                    if current in [None, pygame.K_SPACE]:
                        continue

                    if event.key == pygame.K_RETURN:
                        submit = True

                    elif event.key == pygame.K_BACKSPACE:
                        if current == start_text_box:
                            start_text = start_text[:-1]

                        else:
                            end_text = end_text[:-1]

                    else:
                        start_text_surface_original = TYPING_SIZE_FONT.render(start_text + event.unicode.upper(), True,
                                                                              BLACK)
                        end_text_surface_original = TYPING_SIZE_FONT.render(end_text + event.unicode.upper(), True,
                                                                            BLACK)

                        if current == start_text_box and start_text_surface_original.get_width() < start_text_box.width - 10:
                            start_text += event.unicode

                        elif current == end_text_box and end_text_surface_original.get_width() < end_text_box.width - 10:
                            end_text += event.unicode

                    pygame.draw.rect(window, WHITE, (
                        start_text_box.left + 5, start_text_box.top + 5, start_text_box.width - 10,
                        start_text_box.height - 10))
                    pygame.draw.rect(window, WHITE, (
                        end_text_box.left + 5, end_text_box.top + 5, end_text_box.width - 10, end_text_box.height - 10))

                    start_text_surface = TYPING_SIZE_FONT.render(start_text, True, BLACK)
                    end_text_surface = TYPING_SIZE_FONT.render(end_text, True, BLACK)

                    window.blit(start_text_surface,
                                (1080 - start_text_surface.get_width() / 2, 130 - start_text_surface.get_height() / 2))
                    window.blit(end_text_surface,
                                (1080 - end_text_surface.get_width() / 2, 230 - end_text_surface.get_height() / 2))
                    pygame.display.update()

                if submit:
                    original_start_text, original_end_text = start_text, end_text
                    
                    start_text = start_text.upper()
                    end_text = end_text.upper()
                    
                    if not start_text or not end_text:
                        window.blit(invalid_surface, (1205 - invalid_surface.get_width() / 2, 357 - invalid_surface.get_height() / 2))
                        pygame.display.update()
                        
                        start_text, end_text = original_start_text, original_end_text
                        continue
                    
                    if start_text == "OFFICE":
                        start_text = "Office"

                    if end_text == "OFFICE":
                        end_text = "Office"

                    if start_text in ("G", "B") or start_text[0] in ("G", "B") and start_text[1] in ("2", "3", "4"):
                        start_text = start_text[0] + "B" + start_text[1:]

                    if end_text in ("G", "B") or end_text[0] in ("G", "B") and end_text[1] in ("2", "3", "4"):
                        end_text = end_text[0] + "B" + end_text[1:]

                    if start_text in ("GB1", "BB1"):
                        start_text = start_text[0] + "1"

                    if end_text in ("GB1", "BB1"):
                        end_text = end_text[0] + "1"

                    start_bad = (start_text == "GB")
                    end_bad = False

                    for text, text_box in ((start_text, start_text_box), (end_text, end_text_box)):
                        if not points.rooms.get(text) and text not in ("G1", "B1") or text[0] == "S" and text != "SG" or text == "D205.3":
                            pygame.draw.rect(window, RED, text_box, width=5)
                            start_bad = True

                        else:
                            pygame.draw.rect(window, BLACK, text_box, width=5)

                    if start_bad or end_bad:
                        window.blit(invalid_surface,
                                    (1205 - invalid_surface.get_width() / 2, 357 - invalid_surface.get_height() / 2))
                        pygame.display.update()
                        
                        start_text, end_text = original_start_text, original_end_text
                        continue

                    else:
                        pygame.draw.rect(window, WHITE, (
                            1205 - invalid_surface.get_width() / 2, 357 - invalid_surface.get_height() / 2,
                            invalid_surface.get_width(),
                            invalid_surface.get_height()))
                        complete = True

            if complete:
                break

            await asyncio.sleep(0)

        window.blit(SLIGHTLY_BIG_FONT.render("Calculating...", True, BLACK), (50, 70))
        pygame.display.update()

        await asyncio.sleep(0)

        if start_text in ("B1", "G1"):
            start_text = start_text[0] + "B"

        if end_text in ("BB", "GB"):
            start, ends = points[start_text].copy(), ([points["BB"], points["BB2"], points["BB3"], points["BB4"]] if end_text[0] == "B"
                                              else [points["GB"], points["GB2"], points["GB3"], points["GB4"]])

        else:
            if end_text in ("G1", "B1"):
                end_text = end_text[0] + "B"
                
            start, ends = points[start_text].copy(), [points[end_text]]

        ends = [end.copy() for end in ends]
                
        shortest_path(start, ends, adjacency, window)
        
        pygame.draw.rect(window, RED, submit_button)
        pygame.draw.rect(window, BLACK, submit_button, width=5)
                
        reset = TYPING_SIZE_FONT.render("Reset", True, BLACK)
        window.blit(reset, (1380 - reset.get_width() / 2, 182 - reset.get_height() / 2))
        
        pygame.display.update()
        
        await asyncio.sleep(0)

        while True:
            reset = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.MOUSEBUTTONUP:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    
                    if (submit_button.left - 5) <= mouse_x <= (submit_button.right + 5) and (submit_button.top - 5) <= mouse_y <= (submit_button.bottom + 5):
                        reset = True
                        break

            if reset:
                break
            
            await asyncio.sleep(0)

if __name__ == "__main__":
    asyncio.run(main())
