import xml.etree.ElementTree as ET
prefix = "{http://www.opengis.net/kml/2.2}"

root = ET.parse("coordinates.kml").getroot()[0]

for place in root.findall(prefix + "Placemark"):
    print(place.find(prefix + "name").get("name"), place.find(prefix + "LookAt").find(prefix + "longitude").get("longitude"), place.find(prefix + "LookAt").find(prefix + "latitude").get("longitude"))
