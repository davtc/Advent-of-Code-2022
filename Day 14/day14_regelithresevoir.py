""" --- Day 14: Regolith Reservoir ---
The distress signal leads you to a giant waterfall! Actually, hang on - the signal seems like it's coming from the waterfall itself, and that doesn't make any sense. However, you do notice a little path that leads behind the waterfall.

Correction: the distress signal leads you behind a giant waterfall! There seems to be a large cave system here, and the signal definitely leads further inside.

As you begin to make your way deeper underground, you feel the ground rumble for a moment. Sand begins pouring into the cave! If you don't quickly figure out where the sand is going, you could quickly become trapped!

Fortunately, your familiarity with analyzing the path of falling material will come in handy here. You scan a two-dimensional vertical slice of the cave above you (your puzzle input) and discover that it is mostly air with structures made of rock.

Your scan traces the path of each solid rock structure and reports the x,y coordinates that form the shape of the path, where x represents distance to the right and y represents distance down. Each path appears as a single line of text in your scan. After the first point of each path, each point indicates the end of a straight horizontal or vertical line to be drawn from the previous point. For example:

498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9
This scan means that there are two paths of rock; the first path consists of two straight lines, and the second path consists of three straight lines. (Specifically, the first path consists of a line of rock from 498,4 through 498,6 and another line of rock from 498,6 through 496,6.)

The sand is pouring into the cave from point 500,0.

Drawing rock as #, air as ., and the source of the sand as +, this becomes:


  4     5  5
  9     0  0
  4     0  3
0 ......+...
1 ..........
2 ..........
3 ..........
4 ....#...##
5 ....#...#.
6 ..###...#.
7 ........#.
8 ........#.
9 #########.
Sand is produced one unit at a time, and the next unit of sand is not produced until the previous unit of sand comes to rest. A unit of sand is large enough to fill one tile of air in your scan.

A unit of sand always falls down one step if possible. If the tile immediately below is blocked (by rock or sand), the unit of sand attempts to instead move diagonally one step down and to the left. If that tile is blocked, the unit of sand attempts to instead move diagonally one step down and to the right. Sand keeps moving as long as it is able to do so, at each step trying to move down, then down-left, then down-right. If all three possible destinations are blocked, the unit of sand comes to rest and no longer moves, at which point the next unit of sand is created back at the source.

So, drawing sand that has come to rest as o, the first unit of sand simply falls straight down and then stops:

......+...
..........
..........
..........
....#...##
....#...#.
..###...#.
........#.
......o.#.
#########.
The second unit of sand then falls straight down, lands on the first one, and then comes to rest to its left:

......+...
..........
..........
..........
....#...##
....#...#.
..###...#.
........#.
.....oo.#.
#########.
After a total of five units of sand have come to rest, they form this pattern:

......+...
..........
..........
..........
....#...##
....#...#.
..###...#.
......o.#.
....oooo#.
#########.
After a total of 22 units of sand:

......+...
..........
......o...
.....ooo..
....#ooo##
....#ooo#.
..###ooo#.
....oooo#.
...ooooo#.
#########.
Finally, only two more units of sand can possibly come to rest:

......+...
..........
......o...
.....ooo..
....#ooo##
...o#ooo#.
..###ooo#.
....oooo#.
.o.ooooo#.
#########.
Once all 24 units of sand shown above have come to rest, all further sand flows out the bottom, falling into the endless void. Just for fun, the path any new sand takes before falling forever is shown here with ~:

.......+...
.......~...
......~o...
.....~ooo..
....~#ooo##
...~o#ooo#.
..~###ooo#.
..~..oooo#.
.~o.ooooo#.
~#########.
~..........
~..........
~..........
Using your scan, simulate the falling sand. How many units of sand come to rest before sand starts flowing into the abyss below? """

""" --- Part Two ---
You realize you misread the scan. There isn't an endless void at the bottom of the scan - there's floor, and you're standing on it!

You don't have time to scan the floor, so assume the floor is an infinite horizontal line with a y coordinate equal to two plus the highest y coordinate of any point in your scan.

In the example above, the highest y coordinate of any point is 9, and so the floor is at y=11. (This is as if your scan contained one extra rock path like -infinity,11 -> infinity,11.) With the added floor, the example above now looks like this:

        ...........+........
        ....................
        ....................
        ....................
        .........#...##.....
        .........#...#......
        .......###...#......
        .............#......
        .............#......
        .....#########......
        ....................
<-- etc #################### etc -->
To find somewhere safe to stand, you'll need to simulate falling sand until a unit of sand comes to rest at 500,0, blocking the source entirely and stopping the flow of sand into the cave. In the example above, the situation finally looks like this after 93 units of sand come to rest:

............o............
...........ooo...........
..........ooooo..........
.........ooooooo.........
........oo#ooo##o........
.......ooo#ooo#ooo.......
......oo###ooo#oooo......
.....oooo.oooo#ooooo.....
....oooooooooo#oooooo....
...ooo#########ooooooo...
..ooooo.......ooooooooo..
#########################
Using your scan, simulate the falling sand until the source of the sand becomes blocked. How many units of sand come to rest? """

import numpy as np

def parse():
    with open('Day 14 - input.txt') as f:
        lines = [line.rstrip('\n') for line in f]

    rocks = []
    min_x = float('inf')
    max_x = 0 
    max_y = 0

    for line in lines:
        rock_structure = []
        points = line.split(' -> ')
        for point in points:
            if rock_structure == []:
                start_point = True
            x = int(point.split(',')[0])
            y = int(point.split(',')[1])
            min_x = min(min_x, x)
            max_x = max(max_x, x)
            max_y = max(max_y, y)
            rock_structure.append((x, y))

        rocks.append(rock_structure)
    
    return max_x - min_x, max_y, min_x, (0, 500 - min_x), rocks

# Add points to connect the rock points together.
def connect_rocks(rocks):
    connected_rocks = []
    for rock in rocks:
        rock_path = set()
        for i in range(1, len(rock)):
            x = rock[i][0]
            prev_x = rock[i-1][0]
            y = rock[i][1]
            prev_y = rock[i-1][1]
            rock_path.add((x, y))
            rock_path.add((prev_x, prev_y))
            if x == prev_x and y >= prev_y:
                for j in range(prev_y, y):
                    rock_path.add((x, j))
            elif x == prev_x and y < prev_y:
                for j in range(y, prev_y):
                    rock_path.add((x, j))
            elif y == prev_y and x >= prev_x:
                for j in range(prev_x, x):
                    rock_path.add((j, y))
            elif y == prev_y and x < prev_x:
                for j in range(x, prev_x):
                    rock_path.add((j, y))
        connected_rocks.append(rock_path)

    return connected_rocks

def scan_cave(x_range, y_range, min_x, sand, rocks):
    scan = np.array([['.'] * (x_range + 1)] * (y_range + 1))
    scan[sand] = '+'

    # Draw rock structures
    for rock in rocks:
        for point in rock:
            x = point[0] - min_x
            y = point[1]
            scan[y, x] = '#'
    return scan

def check_south(scan, point):
    if point[0] + 1 <  len(scan[:, 1]):
        return scan[point[0]+1, point[1]]
    else:
        return -1

def check_lower_left(scan, point):
    if point[0] + 1 <  len(scan[:, 1]) and point[1]-1 >= 0:
        return scan[point[0]+1, point[1]-1]
    else:
        return -1

def check_lower_right(scan, point):
    if point[0] + 1 <  len(scan[:, 1]) and point[1]+1 < len(scan[1,:]):
        return scan[point[0]+1, point[1]+1]
    else:
        return -1

def simulate_sand(scan, sand):
    current_point = sand
    stop = False
    while not stop and scan[sand] == '+':
        # Go downwards
        south = check_south(scan, current_point)
        lower_left = check_lower_left(scan, current_point)
        lower_right = check_lower_right(scan, current_point)
        if south == '#' or south == 'o':
            if lower_left == '#' or lower_left == 'o':
                if lower_right == '#' or lower_right == 'o':
                    scan[current_point] = 'o'
                    current_point = sand
                elif lower_right == '.':
                    current_point = (current_point[0]+1, current_point[1]+1)
                elif lower_right == -1:
                    stop = True
                else:
                    scan[current_point] = 'o'
                    current_point = sand
            elif lower_left == '.':
                current_point = (current_point[0]+1, current_point[1]-1)
            elif lower_left == -1:
                stop = True
            else:
                scan[current_point] = 'o'
                current_point = sand
        elif south == '.':
            current_point = (current_point[0]+1, current_point[1])
        elif south == -1:
            stop = True   
        else:
            scan[current_point] = 'o'
            current_point = sand
    return scan

def print_scan(scan):
    str = ''
    for i in range(len(scan[:,1])):
        str += ''.join(scan[i,:]) + '\n'
    print(str)

def main():
    x_range, y_range, min_x, sand, rocks = parse()
    rocks = connect_rocks(rocks)
    scan = scan_cave(x_range, y_range, min_x, sand, rocks)
    scan = simulate_sand(scan, sand)
    print_scan(scan)
    print(np.count_nonzero(scan == 'o')) # Part 1 Ans: 832

if __name__ == '__main__':
    main()