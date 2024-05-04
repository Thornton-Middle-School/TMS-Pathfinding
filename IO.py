import xml.etree.ElementTree as ET
from math import sin, cos, pi
from copy import deepcopy

prefix = "{http://www.opengis.net/kml/2.2}"

tree = ET.parse("coordinates.kml")
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

old = deepcopy(coordinates)

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
make_equal("1A.2", "1.2", "2.2", "3.2")
make_equal("4.2", "5.2", "10.2", "11.2")
make_equal("6.2", "7.2", "8.2", "9.2")
make_equal("12.2", "13.2", "14.2", "15.2")
make_equal("BLR.2", "GLR.2")
make_equal("21B.2", "17.2")
make_equal("18.2", "21.2")
make_equal("19.2", "22.2")
make_equal("BLR.1", "GLR.1", longitude=False)
make_equal("3.2", "1A.2", "1.2", "2.2", "7.2", "6.2", "8.2", "9.2", "12.2", "13.2", "14.2", "15.2", "40.2", "41.2", longitude=False)
make_equal("16.1", "20.2", "21B.2", "17.2", "21.2", "18.2", "22.2", "19.2", "23.2", longitude=False)
make_equal("1A.1", "4.1", "1.1", "6.1", "5.1", "9.1", "12.1", "15.1", "40.1", longitude=False)
make_equal("2.1", "3.1", "7.1", "8.1", "13.1", "14.1", "41.1", longitude=False)
make_equal("10.1", "11.1", "20.1", "21B.1", "21.1", "22.1", "23.1", "24.1", longitude=False)
make_equal("16A.1", "16.2", longitude=False)
make_equal("B101.1", "B201.1", "B106.1", "B205.1", "GB2.1", "GB3.1", "BB2.1", "BB3.1", "D105.1", "D205.1", "D106.1", "D206.1", "D110.1", "D210.1", "D112.1", "D212.1", longitude=False)
make_equal("B101.2", "B201.2", "B106.2", "B205.2", "GB2.2", "GB3.2", "BB2.2", "BB3.2", "D105.2", "D205.2", "D106.2", "D206.2", "D110.2", "D210.2", "D112.2", "D212.2", longitude=False)
make_equal("11.1", "6.1", "5.1", "7.1", "A101.2", "A201.2", "A106.2", "A205.2", "B101.2", "B201.2", latitude=False)
make_equal("10.1", "1.1", "4.1", "3.1", latitude=False)
make_equal("1A.1", "2.1", latitude=False)
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
make_equal("22.1", "18.2", "21.2", "17.1", "40.2", "41.1", "E101.2", "E201.2", "E107.2", "E205.2", latitude=False)
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
make_equal("4.2", "5.2", "10.2", "11.2", "16.2", longitude=False)
make_equal("4.2", "5.2", "10.2", "11.2", "GLR.1", latitude=False, goto=True)

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
make_equal("4.2", "5.2", "10.2", "11.2", "25.2", longitude=False, goto=True)
make_equal("16A.1", "16.2", longitude=False)
coordinates["21B.1"][0] = (coordinates["20.1"][0] + coordinates["21.1"][0]) / 2
coordinates["20.2"][0] = (coordinates["20.1"][0] + coordinates["21.1"][0]) / 2

make_equal("A101.1", "A106.2", longitude=False)
make_equal("A201.1", "A205.2", longitude=False)
make_equal("C107.2", "C101.1", longitude=False)
make_equal("C205.2", "C201.1", longitude=False)
make_equal("E107.2", "E101.1", longitude=False)
make_equal("E205.2", "E201.1", longitude=False)
make_equal("A101.2", "A201.2", "E107.1", "E205.1", "C107.1", longitude=False, goto=True)
make_equal("C101.2", "C201.2", "E101.2", "E201.2", "A106.1", longitude=False, goto=True)

make_equal("Band.2", "SG.1", "1A.2", longitude=False, goto=True)
make_equal("SG.2", "24.1", longitude=False, goto=True)

left, right = 500, -500
top, bottom = 500, -500

x_diffs, y_diffs = [], []

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
    coordinates_new[name][0] = (coordinates[name][0] - left) * 200000
    coordinates_new[name][1] = (coordinates[name][1] - top) * 200000

left, right = 500, -500
top, bottom = 500, -500

for place in root.findall(prefix + "Placemark"):
    name = place.find(prefix + "name").text
    left = min(coordinates_new[name][0], left)
    right = max(coordinates_new[name][0], right)
    top = min(coordinates_new[name][1], top)
    bottom = max(coordinates_new[name][1], bottom)

for place in root.findall(prefix + "Placemark"):
    name = place.find(prefix + "name").text
    place.find(prefix + "LookAt").find(prefix + "longitude").text = f"{coordinates_new[name][0]}"
    place.find(prefix + "LookAt").find(prefix + "latitude").text = f"{coordinates_new[name][1]}"
    place.find(prefix + "Point").find(prefix + "coordinates").text = f"{coordinates_new[name][0]},{coordinates_new[name][1]},{place.find(prefix + "Point").find(prefix + "coordinates").text.split(",")[2]}"
    print(coordinates_new[name][0] - coordinates_new[name[:-1] + str(3 - int(name[-1]))][0], coordinates_new[name][1] - coordinates_new[name[:-1] + str(3 - int(name[-1]))][1])

    if coordinates_new[name][0] - coordinates_new[name[:-1] + str(3 - int(name[-1]))][0] == 0 or coordinates_new[name][1] - coordinates_new[name[:-1] + str(3 - int(name[-1]))][1] == 0:
        print(f"NAME {name}")

    x_diffs.append((coordinates_new[name][0], name))
    y_diffs.append((coordinates_new[name][1], name))

tree.write("classrooms.kml")

print(f"X: {left} -> {right}, diff={right - left}")
print(f"Y: {top} -> {bottom}, diff={bottom - top}")

print(f"average diff: {coordinates_new["12.2"][0] - coordinates_new["12.1"][0]}")

x_diffs.sort()
y_diffs.sort()

print(f"min x diff: {min((second[0] - first[0], first[1], second[1]) for first, second in zip(x_diffs[:-1], x_diffs[1:]) if second[0] != first[0])}, min y diff: {min((second[0] - first[0], first[1], second[1]) for first, second in zip(y_diffs[:-1], y_diffs[1:]) if second[0] != first[0])}")

if __name__ == "__main__":
    pass
