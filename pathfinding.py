from math import floor, sqrt
from heapq import heappush, heappop
from collections import defaultdict
import pygame
from utils import Node, DIAGONAL_DISTANCE, STAIRCASE_LENGTH, SCALE, ORANGE, GREEN, RED, WHITE, TYPING_SIZE_FONT, multiline_render


def upstairs(node: Node | str):
    """Check if a node is on the upstairs floor."""
    name = node.type_ if isinstance(node, Node) else node

    if len(name) > 2:
        if name[1] == "2" or name[2] == "3" or name[0] == "S" and name[3] == "2":
            return True

    return False


def octile_heuristic(node: Node, end: Node):
    """Calculate octile distance heuristic between two nodes."""
    y_difference = abs(node.corner_y - end.corner_y) if upstairs(node) == upstairs(end) else abs(
        abs(node.corner_y - end.corner_y) - 270)
    return (abs(node.corner_x - end.corner_x) + y_difference + (DIAGONAL_DISTANCE - 2) * min(
        abs(node.corner_x - end.corner_x), y_difference) + (upstairs(node) != upstairs(end)) * STAIRCASE_LENGTH) * 1.001


def euclidean_heuristic(node: Node, end: Node) -> float:
    """Calculate Euclidean distance heuristic between two nodes."""
    if upstairs(node) != upstairs(end):
        return (sqrt((node.corner_x - end.corner_x) ** 2 + (
                    abs(node.corner_y - end.corner_y) - 270) ** 2) + STAIRCASE_LENGTH) * 1.001

    return sqrt((node.corner_x - end.corner_x) ** 2 + (node.corner_y - end.corner_y) ** 2) * 1.001


def closest_to_heuristic(node: Node, ends: list[Node], heuristic_function):
    """Find the minimum heuristic distance from node to any of the end nodes."""
    return min(heuristic_function(node, end) for end in ends)


def shortest_path(start: Node, ends: Node, adjacency: defaultdict[Node, list[list[Node | float]]], window: pygame.Surface) -> None:
    """
    Find the shortest path from start node to any of the end nodes using A* algorithm.
    
    Args:
        start: Starting node
        ends: List of possible end nodes
        adjacency: Graph adjacency list
        window: Pygame surface for drawing the path
        
    Returns:
        List of nodes representing the shortest path
    """
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

    # Reconstruct and draw path
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
                    f"Walking Time: ~ {floor((distance / 308 * 75) // 60)}:{("0" if floor((distance / 308 * 75) % 60) < 10 else "") + str(floor((distance / 308 * 75) % 60))} (m:ss)")

    multiline_render(window, results_text, 1205, 327, TYPING_SIZE_FONT, center=True)
    
    pygame.display.update()
