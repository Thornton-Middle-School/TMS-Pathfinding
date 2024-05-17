# TMS-Pathfinding
Find the shortest path between any two rooms in Thornton Middle School (Fremont, CA, USA). The school map was created by using Google Earth, and the path is found using the A* Pathfinding Algorithm.

## Dependencies
- Python 3.12
- Pygame 2.5.2

## Instructions
#### Downloading the app
1. Go to the releases page on the right
2. Scroll down to the bottom
3. Download TMSPathfinding.exe

#### Using the app
1. Using the map shown, enter in your starting and ending room
  - The inputs must be the exact same as the name on the map. For example, if you start in room 1, you can not input "One" or "Room 1" (you have to type "1").
  - You must select each box, or click away.
  - Only an arbitrary number of characters will be output. If when you type a letter it will go outside the box, it will not be stored/output. You have to either proceed to step 2, click a different text box, or press backspace.
    
2. Click the Submit button or press "Enter"/"Return" on your keyboard.
  - Invalid Input will be displayed if the input criteria aren't met (the corresponding text boxes will be in red). If this is the case, go back to step 1.  
   
3. After at most a couple seconds, the shortest path will be shown in orange and a green and red dot for the starting and ending positions respectively. The distance and predicted walking time (assumes you walk at 4 ft/second) are displayed on the right. Otheriwse, "Invalid Input" is displayed on the right in red, and so are the invalid inputs.
  - If you type "BB" or "GB" (boys'/girls' bathroom) and then a number from 2-3 (or nothing to represent 1; there are three bathrooms for each gender) as the ending position, then the shortest path among that of all three bathrooms will be displayed. 

4. If you want to enter in more rooms, press "Reset".

### [Click this hyperlink to watch a quick video on how to download & use this app.](https://drive.google.com/file/d/1aeKbPn9trmSMnZFZG-2qBPAZ8cfzjj_P/view?usp=sharing)

## Example Input & Path
![image](https://github.com/Pramad712/Thornton-Shortest-Paths/assets/77818951/3d480c4b-c526-4bc5-b5a6-b502f9dcc323)

- Rooms SG (small gym) & E205 do exist
- The green dot is the starting position (SG)
- The red dot is the ending position (E205)
- The path between the points is in orange
- The distance is shown in feet on the right (427 feet)
- The estimated time to walk that path is also on the right (1 minute and 46 seconds)
- The part of the path that is upstairs may not seem optimal. However, there is a railing around the classrooms.

### Credits
- My 7th grade semester 2 elective teacher - Mr. Register (this repository was my creation for the final project)
  - [Website (See First)](https://www.mrregister.net/dmar/pac/)
  - [Slides](https://docs.google.com/presentation/d/1HcD0SSQhEydkitxebxhG70NtDNg3fa_p24LJYXlT_oA/edit?usp=sharing)
- The creators & contributors to Google Earth - without them, the map would have been very inaccurate

