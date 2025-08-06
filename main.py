import sys
import pickle
import asyncio

from re import sub

from collections import defaultdict

from time import perf_counter

from utils import *
from pathfinding import shortest_path

async def main():
    window = pygame.display.set_mode((LENGTH, HEIGHT))
    window.fill(WHITE)

    pygame.display.set_caption("Thornton Middle School Pathfinding")
    pygame.display.set_icon(pygame.image.load("logo.png"))

    multiline_render(window, "Loading ...", LENGTH / 2, HEIGHT / 2, HUGE_FONT, color=BLACK, center=True)
    pygame.display.update()
    await asyncio.sleep(0)

    with open("classrooms.pkl", "rb") as file:
        points: NodeDict = pickle.load(file)
        
    with open("adjacency.pkl", "rb") as file:    
        adjacency: defaultdict[Node, list[list[Node | float]]] = defaultdict(list, pickle.load(file))
    
    print("Loaded")
    
    # Create static background surface to avoid redrawing static elements
    background = pygame.Surface((LENGTH, HEIGHT))
    background.fill(WHITE)
    
    # Draw all static elements once on background
    for node in points.rooms.values():
        if node.type_ == "D205.3":
            continue
        
        pygame.draw.rect(background, BLACK, (node.min_x, node.min_y, node.max_x - node.min_x, node.max_y - node.min_y), 1)

        if node.type_ in ["GB", "BB", "GB2", "GB3", "BB2", "BB3", "GB4", "BB4", "21B", "D110", "D210"]:
            font = MICRO_FONT
            
        elif node.type_ in ["16A", "20", "29", "28A", "37", "47", "A101", "A201", "A106", "A205", "B101", "B201", "B106", "B205", "D105", "D205", "D106", "D206", "D112", "D212", "E101", "E107", "E201", "E205"]:
            font = TINY_FONT
            
        elif node.type_ in ["Band", "32", "33", "34", "35", "36", "C101", "C201", "C107", "C205"]:
            font = MINI_FONT
            
        elif node.type_ in ["SG", "LG"]:
            font = BIG_FONT
            
        else:
            font = MEDIUM_FONT

        name = "S" if len(node.type_) == 4 and node.type_[-2] == "." else node.type_ if node.type_ not in ("GB", "BB") else node.type_[0] + "1"
        
        if len(name) > 2 and name[:2] in ("BB", "GB") and name[-1] in ("2", "3"):
            name = f"{name[:-1]}\n{node.type_[-1]}"

        multiline_render(background, name, (node.min_x + node.max_x) / 2, (node.min_y + node.max_y) / 2, font, color=BLUE, center=True)
    
    # Draw static labels and instructions on background
    multiline_render(background, "Upstairs", 495, 70, HUGE_FONT, color=BLACK, center=True)
    background.blit(HUGE_FONT.render("Downstairs", True, BLACK), (188, 382))

    key_text = ("Key:\n"
                "B/BB or G/GB + (identifier) (very small font): Boys/Girls Bathroom\n"
                "LG/SG: Large/Small Gym\n"
                "BLR/GLR: Boys/Girls Locker Room\n"
                "S: Stairs")
    
    width = max(KEY_FONT.render(line, True, BLACK).get_width() for line in key_text.split("\n"))
    multiline_render(background, key_text, (2411 - width) // 2, HEIGHT - 2 - KEY_FONT.get_height() * 8, KEY_FONT, spacing=1.5)

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
    multiline_render(background, instructions, (2411 - width) // 2, HEIGHT - 40 - KEY_FONT.get_height() * 8 - INSTRUCTION_FONT.get_height() * 15, INSTRUCTION_FONT, spacing=1.5)
    
    # create pure pygame UI elements
    start_text_box = TextBox(pygame.Rect(1045, 62, 150, 60), TYPING_SIZE_FONT)
    end_text_box   = TextBox(pygame.Rect(1045, 162, 150, 60), TYPING_SIZE_FONT)

    start_text_box.activate(window)
    end_text_box.deactivate()

    start_text_box.draw(window)
    end_text_box.draw(window)

    submit_button    = Button("Submit", pygame.Rect(1345, 112, 150, 60), TYPING_SIZE_FONT)
    reset_button = Button("Reset", pygame.Rect(1345, 112, 150, 60), TYPING_SIZE_FONT, bg_color=RED)

    reset_button.visible = False  # initially hide reset button
    submit_button.visible = True  # ensure submit button is visible at start
    
    while True:
        # Copy static background instead of redrawing everything
        window.blit(background, (0, 0))
        
        invalid_surface = TYPING_SIZE_FONT.render("Invalid Input", True, RED)

        complete = False
        
        start_text, end_text = "", ""
        current = start_text_box
        
        beginning_time = perf_counter()
        # draw text boxes and submit/reset buttons before input
        start_text_box.draw(window)
        end_text_box.draw(window)
        submit_button.draw(window)
        reset_button.draw(window)

        # draw labels for text boxes with fixed horizontal offset
        start_label = TYPING_SIZE_FONT.render("Start:", True, BLACK)
        # position 50px left of the start box, vertically centered via helper
        label_x = start_text_box.rect.x - 50 - start_label.get_width()
        _, label_y = center_one_line(start_text_box.rect, start_label, TYPING_SIZE_FONT)
        window.blit(start_label, (label_x, label_y))
        
        end_label = TYPING_SIZE_FONT.render("End:", True, BLACK)
        label_x = end_text_box.rect.x - 50 - end_label.get_width()
        _, label_y = center_one_line(end_text_box.rect, end_label, TYPING_SIZE_FONT)
        window.blit(end_label, (label_x, label_y))
        
        # Initial display update to show all UI elements
        pygame.display.update()
        await asyncio.sleep(0)
        
        while True:
            for event in pygame.event.get():
                submitted = False

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONUP:
                    if start_text_box.is_pressed(pygame.mouse.get_pos()):
                        start_text_box.activate(window)
                        end_text_box.deactivate()
                        current = start_text_box

                    elif end_text_box.is_pressed(pygame.mouse.get_pos()):
                        end_text_box.activate(window)
                        start_text_box.deactivate()
                        current = end_text_box

                    elif submit_button.is_pressed(pygame.mouse.get_pos()):
                        submitted = True
                        current = None

                    else:
                        # Click outside: deactivate both
                        start_text_box.deactivate()
                        end_text_box.deactivate()
                        current = None
                    # Redraw text boxes after focus change
                    start_text_box.draw(window)
                    end_text_box.draw(window)
                    submit_button.draw(window)
                    pygame.display.update()
                    await asyncio.sleep(0)

                if event.type == pygame.KEYDOWN:
                    # Skip if no box is focused or space pressed
                    if current is None or event.key == pygame.K_SPACE:
                        continue
                    # ESC to clear focus
                    if event.key == pygame.K_ESCAPE:
                        start_text_box.deactivate()
                        end_text_box.deactivate()
                        current = None
                        start_text_box.draw(window)
                        end_text_box.draw(window)
                        pygame.display.update()
                        await asyncio.sleep(0)
                        continue

                    if event.key == pygame.K_RETURN:
                        submitted = True
                        current = None

                    elif event.key == pygame.K_BACKSPACE:
                        if current == start_text_box:
                            start_text_box.update_text(event)

                        else:
                            end_text_box.update_text(event)

                    elif event.key == pygame.K_TAB:
                        # Toggle focus between start and end text boxes
                        if current == start_text_box:
                            start_text_box.deactivate()
                            end_text_box.activate(window)
                            current = end_text_box
                        else:
                            # current is end_text_box or None
                            end_text_box.deactivate()
                            start_text_box.activate(window)
                            current = start_text_box

                    else:
                        if current == start_text_box:
                            start_text_box.update_text(event)

                        elif current == end_text_box:
                            end_text_box.update_text(event)

                    start_text_box.draw(window)
                    end_text_box.draw(window)
                    submit_button.draw(window)
                    pygame.display.update()
                    await asyncio.sleep(0)
                    
                # Update cursor flicker only for active textbox
                if current == start_text_box:
                    start_text_box.flicker_cursor(perf_counter() - beginning_time)
                    start_text_box.draw(window)
                elif current == end_text_box:
                    end_text_box.flicker_cursor(perf_counter() - beginning_time)
                    end_text_box.draw(window)
                beginning_time = perf_counter()
                    
                if submitted:
                    pygame.draw.rect(window, WHITE, (
                        1205 - invalid_surface.get_width() // 2, 367 - invalid_surface.get_height() // 2,
                        invalid_surface.get_width(),
                        invalid_surface.get_height()))

                    original_start_text, original_end_text = start_text_box.text, end_text_box.text

                    start_text = start_text_box.text.upper()
                    end_text = end_text_box.text.upper()

                    start_text = sub(r"[^A-Z0-9]", "", start_text)
                    end_text = sub(r"[^A-Z0-9]", "", end_text)
                    
                    start_text = start_text.replace(" ", "")
                    end_text = end_text.replace(" ", "")
                    
                    bads = [not start_text, not end_text]
                    texts = [start_text, end_text]
                    
                    for index in range(2):
                        if bads[index]:
                            continue
                        
                        if texts[index] in ("OFFICE", "BAND"):
                            texts[index] = texts[index][0] + texts[index][1:].lower()
                        
                        if texts[index] in ("G", "B") or len(texts[index]) == 2 and texts[index][0] in ("G", "B") and texts[index][1] in ("2", "3", "4"):
                            texts[index] = texts[index][0] + "B" + texts[index][1:]

                        if texts[index] in ("GB1", "BB1"):
                            texts[index] = texts[index][0] + "1"
                        
                        if not points.rooms.get(texts[index]) and texts[index] not in ("G1", "B1") or texts[index][0] == "S" and texts[index] != "SG" or texts[index] == "D205.3":
                            bads[index] = True
                            
                    start_text_box.draw(window, valid=not bads[0])
                    end_text_box.draw(window, valid=not bads[1])

                    if any(bads):
                        multiline_render(window, "Invalid Input", 1205, 367, TYPING_SIZE_FONT, color=RED, center=True)
                        pygame.display.update()
                        await asyncio.sleep(0)
                        
                        start_text, end_text = original_start_text, original_end_text
                        continue

                    else:
                        complete = True 
                        start_text, end_text = texts

            if complete:
                break
            # Flicker cursor and redraw active textbox each frame
            if current == start_text_box:
                start_text_box.flicker_cursor(perf_counter() - beginning_time)
                start_text_box.draw(window)
            elif current == end_text_box:
                end_text_box.flicker_cursor(perf_counter() - beginning_time)
                end_text_box.draw(window)
            beginning_time = perf_counter()
            
            # Single display update per frame
            pygame.display.update()
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
        
        # switch buttons: hide submit, show reset
        submit_button.visible = False
        reset_button.visible = True

        # redraw buttons with current visibility once
        submit_button.draw(window)
        reset_button.draw(window)
        pygame.display.update()
        await asyncio.sleep(0)
        
        # wait for reset click to restart
        clock = pygame.time.Clock()
        while True:
            clock.tick(60)  # Limit to 60 FPS to reduce CPU usage
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                if event.type == pygame.MOUSEBUTTONUP and reset_button.is_pressed(pygame.mouse.get_pos()):
                    # reset for new input
                    start_text_box.text = ""
                    end_text_box.text = ""
                    
                    start_text_box.activate(window)
                    end_text_box.deactivate()
                    
                    submit_button.visible = True
                    reset_button.visible = False
                    
                    break
            else:
                # Required for web deployment - yield control to browser
                await asyncio.sleep(0)
                continue
            
            break

if __name__ == "__main__":
    asyncio.run(main())