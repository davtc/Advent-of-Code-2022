""" --- Day 15: Beacon Exclusion Zone ---
You feel the ground rumble again as the distress signal leads you to a large network of subterranean tunnels. You don't have time to search them all, but you don't need to: your pack contains a set of deployable sensors that you imagine were originally built to locate lost Elves.

The sensors aren't very powerful, but that's okay; your handheld device indicates that you're close enough to the source of the distress signal to use them. You pull the emergency sensor system out of your pack, hit the big button on top, and the sensors zoom off down the tunnels.

Once a sensor finds a spot it thinks will give it a good reading, it attaches itself to a hard surface and begins monitoring for the nearest signal source beacon. Sensors and beacons always exist at integer coordinates. Each sensor knows its own position and can determine the position of a beacon precisely; however, sensors can only lock on to the one beacon closest to the sensor as measured by the Manhattan distance. (There is never a tie where two beacons are the same distance to a sensor.)

It doesn't take long for the sensors to report back their positions and closest beacons (your puzzle input). For example:

Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3
So, consider the sensor at 2,18; the closest beacon to it is at -2,15. For the sensor at 9,16, the closest beacon to it is at 10,16.

Drawing sensors as S and beacons as B, the above arrangement of sensors and beacons looks like this:

               1    1    2    2
     0    5    0    5    0    5
 0 ....S.......................
 1 ......................S.....
 2 ...............S............
 3 ................SB..........
 4 ............................
 5 ............................
 6 ............................
 7 ..........S.......S.........
 8 ............................
 9 ............................
10 ....B.......................
11 ..S.........................
12 ............................
13 ............................
14 ..............S.......S.....
15 B...........................
16 ...........SB...............
17 ................S..........B
18 ....S.......................
19 ............................
20 ............S......S........
21 ............................
22 .......................B....
This isn't necessarily a comprehensive map of all beacons in the area, though. Because each sensor only identifies its closest beacon, if a sensor detects a beacon, you know there are no other beacons that close or closer to that sensor. There could still be beacons that just happen to not be the closest beacon to any sensor. Consider the sensor at 8,7:

               1    1    2    2
     0    5    0    5    0    5
-2 ..........#.................
-1 .........###................
 0 ....S...#####...............
 1 .......#######........S.....
 2 ......#########S............
 3 .....###########SB..........
 4 ....#############...........
 5 ...###############..........
 6 ..#################.........
 7 .#########S#######S#........
 8 ..#################.........
 9 ...###############..........
10 ....B############...........
11 ..S..###########............
12 ......#########.............
13 .......#######..............
14 ........#####.S.......S.....
15 B........###................
16 ..........#SB...............
17 ................S..........B
18 ....S.......................
19 ............................
20 ............S......S........
21 ............................
22 .......................B....
This sensor's closest beacon is at 2,10, and so you know there are no beacons that close or closer (in any positions marked #).

None of the detected beacons seem to be producing the distress signal, so you'll need to work out where the distress beacon is by working out where it isn't. For now, keep things simple by counting the positions where a beacon cannot possibly be along just a single row.

So, suppose you have an arrangement of beacons and sensors like in the example above and, just in the row where y=10, you'd like to count the number of positions a beacon cannot possibly exist. The coverage from all sensors near that row looks like this:

                 1    1    2    2
       0    5    0    5    0    5
 9 ...#########################...
10 ..####B######################..
11 .###S#############.###########.
In this example, in the row where y=10, there are 26 positions where a beacon cannot be present.

Consult the report from the sensors you just deployed. In the row where y=2000000, how many positions cannot contain a beacon? """

import numpy as np

def parse():
    with open('Day 15 - input.txt') as f:
        lines = [line.rstrip('\n') for line in f]

        sensors = {}

        for line in lines:
            split = line.split(' ')
            sensor_x = int(split[2][2:-1])
            sensor_y = int(split[3][2:-1])
            beacon_x = int(split[8][2:-1])
            beacon_y = int(split[9][2:])
            sensors[(sensor_x, sensor_y)] = (beacon_x, beacon_y)

        return sensors

def manhattan_distance(start, end):
    return abs(end[0] - start[0]) + abs(end[1] - start[1])

def init_row(sensors):
    x_min = float('inf')
    x_max = 0
    y_min = float('inf')
    y_max = 0

    for sensor, beacon in sensors.items():
        distance = manhattan_distance(sensor, beacon)
        x_min = min(x_min, sensor[0] - distance)
        x_max = max(x_max, sensor[0] + distance)
        y_min = min(y_min, sensor[1] - distance)
        y_max = max(y_max, sensor[1] + distance)

    row = ['.'] * (x_max - x_min)

    return row, x_max - x_min, x_min, y_min

def in_range(sensor, beacon, point):
    if manhattan_distance(sensor, point) <= manhattan_distance(sensor, beacon):
        return True
    else:
        return False

def no_beacon(row, sensors, x_range, x_min, y):
    start = []
    end = []
    for sensor, beacon in sensors.items():
        if sensor[1] == y:
            row[sensor[0] + abs(x_min)] = 'S'
        if beacon[1] == y:
            row[beacon[0] + abs(x_min)] = 'B'
        
        distance = manhattan_distance(sensor, beacon)
        if abs(y - sensor[1]) <= distance:
            remaining_distance = distance - abs(y - sensor[1])
            start.append(sensor[0] - remaining_distance)
            end.append(sensor[0] + remaining_distance)

    start.sort()
    end.sort()
    open = 0
    s = 0
    e = 0
    for i in range(len(row)):
        x = i + x_min
        while s < len(start) and x == start[s]:
            s += 1
            open += 1
        if open > 0 and row[i] == '.':
            row[i] = '#'
        while e < len(end) and x == end[e]:
            e += 1
            open -=1

    return row

def print_row(row, x_min):
    for n, char in zip(range(x_min, x_min + len(row)), row):
        print(str(n) + ' ' + char)

def n_pos_no_beacon(row):
    row = [char for char in row if char != '.']
    row = [char for char in row if char != 'B']
    row = [char for char in row if char != 'S']
    return len(row)

def main():
    sensors = parse()
    row, x_range, x_min, y_min = init_row(sensors)
    # print_map(map)
    # print_row(map[10 + abs(y_min), :], x_min)
    row = no_beacon(row, sensors, x_range, x_min, 2000000)
    # print_row(row, x_min)
    print(n_pos_no_beacon(row)) # Part 1 Ans: 5127797

if __name__ == '__main__':
    main()