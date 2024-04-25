# import pygame
# import numpy
#
# def main():
#     window = pygame.display.set_mode((800, 600))
#
# if __name__ == "__main__":
#     main()

# import pygame
# import numpy
#
# def main():
#     window = pygame.display.set_mode((800, 600))
#
# if __name__ == "__main__":
#     main()

import xml.etree.ElementTree as ET
from math import sin, cos

prefix = "{http://www.opengis.net/kml/2.2}"

root = ET.parse("coordinates.kml").getroot()[0]

coordinates = {}

def rotate(x, y, theta=303):
    return [x * cos(theta) - y * sin(theta), y * cos(theta) + x * sin(theta)]

for place in root.findall(prefix + "Placemark"):
    name = place.find(prefix + "name").text
    coordinates[name] = rotate(float(place.find(prefix + "LookAt").find(prefix + "longitude").text), float(place.find(prefix + "LookAt").find(prefix + "latitude").text))
    print(name, coordinates[name])

def good(*args: list[str], longitude=True, latitude=True):
    for arg in args[1:]:
        if longitude:
            assert coordinates[arg][0] == coordinates[args[0]][0]

        if latitude:
            assert coordinates[arg][1] == coordinates[args[0]][1]

def make_equal(*args: list[str], longitude=True, latitude=True):
    for arg in args[1:]:
        if longitude:
            coordinates[arg][0] = coordinates[args[0]][0]

        if latitude:
            coordinates[arg][1] = coordinates[args[0]][1]

    good(*args, longitude=longitude, latitude=latitude)

make_equal("3.2", "1A.2", "1.2", "2.2", "7.2", "6.2", "8.2", "9.2", "12.2", "13.2", "14.2", "15.2", "40.2", "41.2", longitude=False)
make_equal("4.2", "5.2", "10.2", "11.2", "16.1", "20.2", "21B.2", "17.2", "21.2", "18.2", "22.2", "19.2", "23.1", longitude=False)
make_equal("1A.1", "4.1", "1.1", "6.1", "5.1", "9.1", "12.1", "15.1", "40.1", longitude=False)
make_equal("2.1", "3.1", "7.1", "8.1", "13.1", "15.2", "41.1", longitude=False)
make_equal("10.1", "11.1", "20.1", "21B.1", "21.1", "22.1", "23.1", longitude=False)
make_equal("11.1", "6.1", "5.1", "7.1", "A101.2", "A201.2", "A106.2", "A205.2", "B101.2", "B201.2", latitude=False)
make_equal("10.1", "1.1", "4.1", "3.1", "BLR.2", "GLR.2", latitude=False)
make_equal("1A.1", "2.1", "BLR.1")
make_equal("9.1", "8.1")
make_equal("6.2", "7.2", "8.2", "9.2", "A101.1", "A106.1", "A201.1", "A205.1", latitude=False)
make_equal("12.1", "13.1", "C101.1", "C107.1", "C201.1", "C205.1", latitude=False)
make_equal("12.2", "13.2", "14.2", "15.2", "C101.2", "C1107.2", "C201.2", "C205.2", latitude=False)
make_equal("20.1", "16.1", "16A.1", "15.1", "14.1", latitude=False)
make_equal("21B.1", "20.2")
make_equal("21.1", "21B.2", "17.2", "16.2", "16A.2", "E101.2", "E201.2", "E107.2", "E205.2", latitude=False)
make_equal("22.1", "18.2", "17.1", "40.2", "41.1", "E101.1", "E201.1", "E107.1", "E205.1", latitude=False)
make_equal("23.1", "19.2", "22.2", "18.1", latitude=False)
make_equal("23.2", "19.1", "40.1", "41.2", latitude=False)
make_equal(*[f"{number}.1" for number in range(24, 37)], "28A.1", "GB.1", latitude=False)
make_equal(*[f"{number}.2" for number in range(24, 37)], "28A.2", "BB.1", latitude=False)
make_equal(*[f"{number}.1" for number in range(37, 46)], latitude=False)
make_equal(*[f"{number}.2" for number in range(37, 46)], latitude=False)
make_equal("1A.2", "1.2", "2.2", "3.2")
make_equal("4.")

