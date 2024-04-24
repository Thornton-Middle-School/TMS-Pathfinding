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

make_equal("3.2", "1A.2", "1.2", "2.2", "7.2", "6.2", "8.2", "9.2", "12.2", "13.2", "14.2", "15.2")
make_equal("4.2", "5.2", "10.2", "11.2", "16.1", "20.2", "21B.2", "17.2", "21.2", "18.2", "22.2", "19.2", "23.1", longitude=False)
make_equal("1A.1", "4.1", "1.1", "6.1", "5.1", "9.1", "12.1", "15.1", "40.1", longitude=False)
make_equal("2.1", "3.1", "7.1", "8.1", "13.1", "15.2", "41.1", longitude=False)
make_equal("10.1", "11.1", "20.1", "21B.1", "21.1", "22.1", "23.1", longitude=False)
