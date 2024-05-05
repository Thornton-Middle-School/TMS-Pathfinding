# Thornton-Shortest-Paths
Find the shortest path between any two rooms in Thornton Middle School (Fremont, CA, USA). The school map was created by using Google Earth, and the path is found using the A* Pathfinding Algorithm.

## Dependencies
- Python 3.12
- Pygame 2.5.2

## Instructions
1. Using the map shown, enter in your starting and ending room
  - The inputs must be the exact same as the name on the map. For example, if you start in room 1, you can not input "One" or "Room 1" (you have to type "1").
  - All letters (if applicable) must be uppercase.
  - You must select each box, or click away. The enter key does not work.

2. Click the Submit button.
3. The shortest path will be shown in orange and a green and red dot for the starting and ending positions respectively. The distance and predicted walking time (assumes you walk at 4 ft/second) are displayed on the right. Otheriwse, "Invalid Input" is displayed on the right in red, and so are the invalid inputs.

4. If you want to enter in more rooms, press "Reset".

## Example Input & Path
![image](https://github.com/Pramad712/Thornton-Shortest-Paths/assets/77818951/7e6d6f4f-aa98-481b-a5aa-05a50967be33)

- Rooms 4 & E205 do exist
- "E" is uppercase
- The green dot is the starting position (room 4)
- The red dot is the ending position (E205)
- The path between the points is in orange
- The distance is shown in feet on the right (392 feet)
- The estimated time to walk that path is also on the right (1 minute and 38 seconds)
- The part of the path that is upstairs may not seem optimal. However, there is a railing around the classrooms.

  ### Credits
  - My 7th grade semester 2 elective teacher - Mr. Register (this repository was my creation for the final project)
  - The creators & contributors to Google Earth - without them, the map would have been very inaccurate

