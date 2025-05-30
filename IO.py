from math import sin, cos, pi, floor
from collections import defaultdict

from xml.etree import ElementTree
import pickle

from utils import HEIGHT, STAIRCASE_LENGTH, DIAGONAL_DISTANCE, Node, NodeDict, upstairs

def adjust_from_kml() -> dict[str, list[float, float]]:
    prefix = "{http://www.opengis.net/kml/2.2}"

    tree = ElementTree.parse("coordinates.kml")
    root = tree.getroot()[0]

    coordinates = {}

    def rotate(x, y, theta=303*pi/180):
        return [x * cos(theta) - y * sin(theta), y * cos(theta) + x * sin(theta)]

    left, right = 500, -500
    top, bottom = -500, 500

    for place in root.findall(prefix + "Placemark"):
        name = place.find(prefix + "name").text
        longitude, latitude, _ = map(float, place.find(prefix + "Point").find(prefix + "coordinates").text.split(","))
        coordinates[name] = rotate(longitude, latitude)

        left = min(coordinates[name][0], left)
        right = max(coordinates[name][0], right)
        top = max(coordinates[name][1], top)
        bottom = min(coordinates[name][1], bottom)

    print(f"X: {left} -> {right}, diff={right - left}")
    print(f"Y: {bottom} -> {top}, diff={top - bottom}")

    print(f"average diff: {coordinates["12.2"][0] - coordinates["12.1"][0]}")

    def make_equal(*args: list[str], longitude=True, latitude=True, goto=False):
        if goto:
            for arg in args[:-1]:
                if longitude:
                    coordinates[arg][0] = coordinates[args[-1]][0]

                if latitude:
                    coordinates[arg][1] = coordinates[args[-1]][1]

            return

        average_longitude = 0
        average_latitude = 0

        for arg in args:
            if longitude:
                average_longitude += coordinates[arg][0]

            if latitude:
                average_latitude += coordinates[arg][1]

        average_longitude /= len(args)
        average_latitude /= len(args)

        if longitude and latitude:
            coordinates[args[0]] = [average_longitude, average_latitude]

            for arg in args:
                coordinates[arg] = coordinates[args[0]]

            return

        for arg in args:
            if longitude:
                coordinates[arg][0] = average_longitude

            if latitude:
                coordinates[arg][1] = average_latitude

    make_equal("A101.1", "A201.1")
    make_equal("A101.2", "A201.2")
    make_equal("A106.1", "A205.1")
    make_equal("A106.2", "A205.2")
    make_equal("B101.1", "B201.1")
    make_equal("B101.2", "B201.2")
    make_equal("B106.1", "B205.1")
    make_equal("B106.2", "B205.2")
    make_equal("C101.1", "C201.1")
    make_equal("C101.2", "C201.2")
    make_equal("C107.1", "C205.1")
    make_equal("C107.2", "C205.2")
    make_equal("D105.1", "D205.1")
    make_equal("D105.2", "D205.2")
    make_equal("D106.1", "D206.1")
    make_equal("D106.2", "D206.2")
    make_equal("D110.1", "D210.1")
    make_equal("D110.2", "D210.2")
    make_equal("D112.1", "D212.1")
    make_equal("D112.2", "D212.2")
    make_equal("E101.1", "E201.1")
    make_equal("E101.2", "E201.2")
    make_equal("E107.1", "E205.1")
    make_equal("E107.2", "E205.2")
    make_equal("GB4.2", "1.2", "2.2", "3.2")
    make_equal("4.2", "5.2", "10.2", "11.2")
    make_equal("6.2", "7.2", "8.2", "9.2")
    make_equal("12.2", "13.2", "14.2", "15.2")
    make_equal("BLR.2", "GLR.2")
    make_equal("21B.2", "17.2")
    make_equal("18.2", "21.2")
    make_equal("19.2", "22.2")
    make_equal("BLR.1", "GLR.1", longitude=False)
    make_equal("3.2", "GB4.2", "1.2", "2.2", "7.2", "6.2", "8.2", "9.2", "12.2", "13.2", "14.2", "15.2", "40.2", "41.2", longitude=False)
    make_equal("4.2", "5.2", "10.2", "11.2", "16.1", "20.2", "21B.2", "17.2", "21.2", "18.2", "22.2", "19.2", "23.2", "24.2", longitude=False)
    make_equal("BB4.1", "4.1", "1.1", "6.1", "5.1", "9.1", "12.1", "15.1", "40.1", longitude=False)
    make_equal("2.1", "3.1", "7.1", "8.1", "13.1", "14.1", "41.1", longitude=False)
    make_equal("10.1", "11.1", "20.1", "21B.1", "21.1", "22.1", "23.1", "24.1", longitude=False)
    make_equal("16A.1", "16.2", longitude=False)
    make_equal("B101.1", "B201.1", "B106.1", "B205.1", "GB2.1", "GB3.1", "BB2.1", "BB3.1", "D105.1", "D205.1", "D106.1", "D206.1", "D110.1", "D210.1", "D112.1", "D212.1", longitude=False)
    make_equal("B101.2", "B201.2", "B106.2", "B205.2", "GB2.2", "GB3.2", "BB2.2", "BB3.2", "D105.2", "D205.2", "D106.2", "D206.2", "D110.2", "D210.2", "D112.2", "D212.2", longitude=False)
    make_equal("11.1", "6.1", "5.1", "7.1", "A101.2", "A201.2", "A106.2", "A205.2", "B101.2", "B201.2", latitude=False)
    make_equal("10.1", "1.1", "4.1", "3.1", latitude=False)
    make_equal("BB4.1", "GB4.1", "2.1", latitude=False)
    make_equal("9.1", "8.1", "B106.1", "B205.1", "GB2.2", "GB3.2", latitude=False)
    make_equal("GB2.1", "GB3.1", "BB2.2", "BB3.2", latitude=False)
    make_equal("6.2", "7.2", "8.2", "9.2", "A101.1", "A106.1", "A201.1", "A205.1", "B101.1", "B201.1", "B106.2", "B205.2", "Office.1", latitude=False)
    make_equal("12.1", "13.1", "C101.1", "C107.1", "C201.1", "C205.1", "D105.2", "D205.2", latitude=False)
    make_equal("12.2", "13.2", "14.2", "15.2", "C101.2", "C107.2", "C201.2", "C205.2", "D105.1", "D205.1", "D106.2", "D206.2", "Office.2", latitude=False)
    make_equal("16A.1", "16.1", "20.1", "15.1", "14.1", "D106.1", "D206.1", "D110.2", "D210.2",  latitude=False)
    make_equal("D110.1", "D210.1", "D112.2", "D212.2", latitude=False)
    make_equal("D112.1", "D212.1", latitude=False)
    make_equal("20.2", "21B.1", latitude=False)
    make_equal("17.2", "21B.2", "21.1", "16.2", "16A.2", "E101.1", "E201.1", "E107.1", "E205.1", latitude=False)
    make_equal("23.1", "19.2", "22.2", "18.1", latitude=False)
    make_equal("23.2", "19.1", "40.1", "41.2", latitude=False)

    make_equal("GB.1", "BB.1", longitude=False)
    make_equal("GB.2", "BB.2", longitude=False)
    GB_width, BB_width = coordinates["GB.2"][0] - coordinates["GB.1"][0], coordinates["BB.2"][0] - coordinates["BB.1"][0]
    coordinates["GB.1"][0] = coordinates["BB.1"][0]
    coordinates["GB.2"][0] = coordinates["BB.1"][0] + GB_width
    coordinates["BB.1"][0] = coordinates["GB.2"][0]
    coordinates["BB.2"][0] = coordinates["BB.1"][0] + BB_width

    make_equal(*[f"{number}.1" for number in range(24, 37)], "28A.1", "GB.1", latitude=False, goto=True)
    make_equal(*[f"{number}.2" for number in range(24, 37)], "28A.2", "BB.2", latitude=False, goto=True)
    make_equal(*[f"{number}.1" for number in range(37, 48)], latitude=False)
    make_equal(*[f"{number}.2" for number in range(37, 48)], latitude=False)

    coordinates["4.2"][0] = (coordinates["4.1"][0] + coordinates["5.1"][0]) / 2
    make_equal("5.2", "10.2", "11.2", "GLR.1", "4.2", latitude=False, goto=True)

    for classroom in range(24, 47):
        if classroom < 37:
            if classroom not in [28, 29, 36]:
                make_equal(f"{classroom}.2", f"{classroom + 1}.1", longitude=False)

        else:
            if classroom not in [39, 40, 41]:
                make_equal(f"{classroom}.1", f"{classroom + 1}.2", longitude=False)

            if classroom == 39:
                make_equal("39.1", "42.2", longitude=False)

    make_equal("17.1", "18.1", "19.1", "16A.2", "4.1", "5.1", "26.2", longitude=False, goto=True)
    make_equal("25.2", "26.2", longitude=False, goto=True)
    make_equal("26.1", "25.2", longitude=False, goto=True)
    make_equal("26.2", "27.2", longitude=False, goto=True)
    make_equal("27.1", "26.2", longitude=False, goto=True)
    make_equal("27.2", "28.2", longitude=False, goto=True)
    make_equal("28.1", "27.2", longitude=False, goto=True)
    make_equal("28.2", "41.1", longitude=False, goto=True)
    make_equal("28A.1", "28.2", longitude=False, goto=True)

    coordinates["28A.2"][1] = (coordinates["BB.1"][1] + coordinates["BB.2"][1]) / 2

    make_equal("BB.1", "GB.1", "BB.2", longitude=False, goto=True)
    make_equal("BB.2", "GB.2", "29.1", longitude=False, goto=True)

    make_equal("29.1", "29.2", longitude=False, goto=True)
    make_equal("29.2", "30.1", longitude=False, goto=True)

    difference = coordinates["30.2"][1] - coordinates["30.1"][1]
    coordinates["29.2"][1] += difference/4
    coordinates["30.1"][1] += difference/3

    make_equal("4.2", "5.2", "10.2", "11.2", "24.2", "21.2", longitude=False, goto=True)
    make_equal("16A.1", "16.2", longitude=False)

    shift = (coordinates["4.1"][0] - coordinates["1.1"][0]) / 4
    coordinates["4.1"][0] -= shift
    coordinates["10.1"][0] -= shift
    coordinates["5.1"][0] += shift
    coordinates["11.1"][0] += shift

    make_equal("22.1", "18.2", "21.2", "17.1", "40.2", "41.2", "37.2", latitude=False, goto=True)

    coordinates["21B.1"][0] = (coordinates["20.1"][0] + coordinates["21.1"][0]) / 2
    coordinates["20.2"][0] = (coordinates["20.1"][0] + coordinates["21.1"][0]) / 2

    make_equal("A101.1", "A106.2", longitude=False)
    make_equal("A201.1", "A205.2", longitude=False)
    make_equal("C107.2", "C101.1", longitude=False)
    make_equal("C205.2", "C201.1", longitude=False)
    make_equal("E107.2", "E101.1", longitude=False)
    make_equal("E205.2", "E201.1", longitude=False)
    make_equal("A101.2", "A201.2", "E107.1", "E205.1", "C107.1", longitude=False)
    make_equal("C101.2", "C201.2", "E101.2", "E201.2", "A106.1", longitude=False)

    make_equal("D112.1", "D212.1", "E101.2", "E107.2", "E201.2", "E205.2", latitude=False, goto=True)

    make_equal("Band.2", "SG.1", "GB4.2", longitude=False, goto=True)
    make_equal("SG.2", "24.1", longitude=False, goto=True)

    coordinates["GB.1"][0] = coordinates["GB.2"][0] - (coordinates["BB.2"][0] - coordinates["BB.1"][0])
    coordinates["BB2.1"][0] = coordinates["BB3.1"][0] = coordinates["BB2.2"][0] + (coordinates["GB2.1"][0] - coordinates["GB2.2"][0])

    make_equal("BB4.2", "GB4.2", latitude=False, goto=True)

    coordinates["GB4.1"][1] = coordinates["BB4.2"][1] = (coordinates["GB4.2"][1] + coordinates["BB4.1"][1]) / 2

    make_equal("LG.3", "LG.1", latitude=False, goto=True)

    make_equal("SA.1", "SA.2", latitude=False, goto=True)
    make_equal("SB.1", "SB.2", latitude=False, goto=True)
    make_equal("SC.1", "SC.2", latitude=False, goto=True)
    make_equal("SD.1", "SD.2", longitude=False, goto=True)
    make_equal("SE.2", "SE.1", latitude=False, goto=True)

    coordinates["SC.1"][1] = coordinates["SA.1"][1]

    coordinates["SC.2"][1] = coordinates["SA.2"][1]

    coordinates["SE.2"][1] = coordinates["SA.1"][1]

    coordinates["SA.2"][1] = coordinates["SC.2"][1] = coordinates["SE.1"][1]

    avg_y = (coordinates["SD.1"][1] + coordinates["SD.2"][1] + coordinates["SB.2"][1]) / 3
    coordinates["SD.1"][1] = coordinates["SD.2"][1] = coordinates["SB.2"][1] = avg_y

    coordinates["A101.1"][1] = coordinates["A201.1"][1] = coordinates["C101.1"][1] = coordinates["C201.1"][1] = coordinates["E101.1"][1] = coordinates["E201.1"][1] = coordinates["A106.2"][1] = coordinates["A205.2"][1] = coordinates["C107.2"][1] = coordinates["C205.2"][1] = coordinates["E107.2"][1] = coordinates["E205.2"][1] = (coordinates["E101.2"][1] + coordinates["E107.1"][1]) / 2

    coordinates["16A.1"][1] = coordinates["16.2"][1] = (coordinates["16A.2"][1] + coordinates["16.1"][1]) / 2

    make_equal("25.1", "24.2", longitude=False, goto=True)
    make_equal("D205.3", "D205.1", longitude=False, goto=True)

    left, right = 500, -500
    top, bottom = 500, -500

    for place in root.findall(prefix + "Placemark"):
        name = place.find(prefix + "name").text
        left = min(coordinates[name][0], left)
        right = max(coordinates[name][0], right)
        top = min(coordinates[name][1], top)
        bottom = max(coordinates[name][1], bottom)

    coordinates_new = {}

    for place in root.findall(prefix + "Placemark"):
        name = place.find(prefix + "name").text
        coordinates_new[name] = [0, 0]
        coordinates_new[name][0] = (coordinates[name][0] - left) * 370000
        coordinates_new[name][1] = (coordinates[name][1] - top) * 370000

    return coordinates_new

def create_graph(coordinates: dict[str, list[float, float]]):
    points = NodeDict()
    adjacency = defaultdict(list)
    
    locations: dict[tuple[int, int], Node] = {}

    for name, (longitude, latitude) in coordinates.items():
        original = name
        name = name[:-2] if (name[0] != "S" or name[:2] == "SG") and name != "D205.3" else name  # D205.3 is a dummy value for C201 & D205 adjacency

        y_subtraction = 425 if upstairs(name) else 30

        if name in points:
            points[name].min_x = min(points[name].min_x, longitude)
            points[name].max_x = max(points[name].max_x, longitude)
            points[name].min_y = min(points[name].min_y, HEIGHT - latitude - y_subtraction)
            points[name].max_y = max(points[name].max_y, HEIGHT - latitude - y_subtraction)
        else:
            points[name] = Node(min_x=longitude, max_x=longitude, min_y=HEIGHT - latitude - y_subtraction, max_y=HEIGHT - latitude - y_subtraction, type_=name)
            
        if original[-1] in ("1", "3") or original[0] == "S" and original[:-2] != "SG":
            points[name].corner_x = longitude
            points[name].corner_y = HEIGHT - latitude - y_subtraction
            
    for name, node in points.items():
        node.min_x = floor(node.min_x)
        node.max_x = floor(node.max_x)
        node.min_y = floor(node.min_y)
        node.max_y = floor(node.max_y)
        node.corner_x = floor(node.corner_x)
        node.corner_y = floor(node.corner_y)
            
    adjacency[points["A201"]] = [(points["SA.2"], 14.56), (points["A205"], 29)]
    adjacency[points["A205"]] = [(points["SA.2"], 43.21), (points["A201"], 29), (points["B201"], 4)]
    adjacency[points["B201"]] = [(points["A205"], 4), (points["B205"], 22.78), (points["SB.2"], 22.48)]
    adjacency[points["B205"]] = [(points["A205"], 23.13), (points["B201"], 22.78), (points["SB.2"], 10.33), (points["GB3"], 10.74)]
    adjacency[points["GB3"]] = [(points["B205"], 10.74), (points["SB.2"], 12.01), (points["BB3"], 7.9)]
    adjacency[points["BB3"]] = [(points["SB.2"], 19.71), (points["GB3"], 7.9), (points["C201"], 38.9), (points["D205.3"], 11.22)]
    adjacency[points["D205.3"]] = [(points["BB3"], 11.22), (points["D205"], 27.46), (points["SB.2"], 30.83), (points["SD.2"], 28.55)]
    adjacency[points["D205"]] = [(points["D205.3"], 27.46), (points["D206"], 22.17), (points["SD.2"], 6.59)]
    adjacency[points["D206"]] = [(points["D205"], 22.17), (points["D210"], 16.27), (points["SD.2"], 23.77)]
    adjacency[points["D210"]] = [(points["D206"], 16.27), (points["D212"], 20.1), (points["SD.2"], 39.65), (points["E201"], 36.76)]
    adjacency[points["D212"]] = [(points["D210"], 20.1), (points["SD.2"], 59.56)]
    adjacency[points["C201"]] = [(points["BB3"], 38.9), (points["D205.3"], 36.41), (points["C205"], 28.1), (points["SC.2"], 27.76)]
    adjacency[points["C205"]] = [(points["C201"], 28.1), (points["SC.2"], 4.04)]
    adjacency[points["E201"]] = [(points["D210"], 36.76), (points["E205"], 28.22), (points["SE.2"], 14.96)]
    adjacency[points["E205"]] = [(points["E201"], 28.22), (points["SE.2"], 39.47)]

    adjacency[points["SA.2"]] = [(points["A201"], 14.56), (points["A205"], 43.21), (points["SA.1"], STAIRCASE_LENGTH)]
    adjacency[points["SB.2"]] = [(points["B201"], 22.48), (points["B205"], 10.33), (points["GB3"], 12.01), (points["BB3"], 19.71), (points["D205.3"], 30.83), (points["SB.1"], STAIRCASE_LENGTH)]
    adjacency[points["SC.2"]] = [(points["C201"], 27.76), (points["C205"], 4.04), (points["SC.1"], STAIRCASE_LENGTH)]
    adjacency[points["SD.2"]] = [(points["D205"], 6.59), (points["D206"], 23.77), (points["D210"], 39.65), (points["D212"], 59.56), (points["D205.3"], 28.55), (points["SD.1"], STAIRCASE_LENGTH)]
    adjacency[points["SE.2"]] = [(points["E201"], 14.96), (points["E205"], 39.47), (points["SE.1"], STAIRCASE_LENGTH)]
    adjacency[points["SA.1"]] = [(points["SA.2"], STAIRCASE_LENGTH)]
    adjacency[points["SB.1"]] = [(points["SB.2"], STAIRCASE_LENGTH)]
    adjacency[points["SC.1"]] = [(points["SC.2"], STAIRCASE_LENGTH)]
    adjacency[points["SD.1"]] = [(points["SD.2"], STAIRCASE_LENGTH)]
    adjacency[points["SE.1"]] = [(points["SE.2"], STAIRCASE_LENGTH)]

    for node in points.values():
        locations[(node.corner_x, node.corner_y)] = node

    min_x, min_y, max_x, max_y = 1000, 1000, -1000, -1000
    
    for node in points.values():
        if not upstairs(node):
            min_x = min(min_x, node.corner_x)
            max_x = max(max_x, node.corner_x)
            min_y = min(min_y, node.corner_y)
            max_y = max(max_y, node.corner_y)

    for x in range(min_x, max_x + 1, 1):
        for y in range(min_y, max_y + 1, 1):
            if locations.get((x, y)):
                continue

            tangencies = 0
            corner = False

            for node in points.rooms.values():
                if node.min_x < x < node.max_x and node.min_y < y < node.max_y:
                    tangencies = 100
                    break

                if node.min_x <= x <= node.max_x and node.min_y <= y <= node.max_y:
                    tangencies += 1

                    if x in [node.min_x, node.max_x] and y in [node.min_y, node.max_y]:
                        corner = True
                        break

            if tangencies <= 1 or corner:
                points[f"Empty @ ({x}, {y})"] = Node(x, x, y, y, "empty", corner_x=x, corner_y=y)
                locations[(x, y)] = points[f"Empty @ ({x}, {y})"]

    for node in points.values():
        if not upstairs(node) or node.type_ == "empty":
            for x_change in range(-1, 2, 1):
                for y_change in range(-1, 2, 1):
                    if (x_change or y_change) and (adjacent := locations.get((node.corner_x + x_change, node.corner_y + y_change))):
                        adjacency[node].append((adjacent, 1 if abs(x_change) + abs(y_change) == 1 else DIAGONAL_DISTANCE))
    
    with open("classrooms.pkl", "wb") as file:
        pickle.dump(points, file)
        
    with open("adjacency.pkl", "wb") as file:   
        pickle.dump(adjacency, file)

if __name__ == "__main__":
    create_graph(adjust_from_kml())
