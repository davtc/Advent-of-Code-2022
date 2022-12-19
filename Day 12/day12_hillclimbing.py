""" --- Day 12: Hill Climbing Algorithm ---
You try contacting the Elves using your handheld device, but the river you're following must be too low to get a decent signal.

You ask the device for a heightmap of the surrounding area (your puzzle input). The heightmap shows the local area from above broken into a grid; the elevation of each square of the grid is given by a single lowercase letter, where a is the lowest elevation, b is the next-lowest, and so on up to the highest elevation, z.

Also included on the heightmap are marks for your current position (S) and the location that should get the best signal (E). Your current position (S) has elevation a, and the location that should get the best signal (E) has elevation z.

You'd like to reach E, but to save energy, you should do it in as few steps as possible. During each step, you can move exactly one square up, down, left, or right. To avoid needing to get out your climbing gear, the elevation of the destination square can be at most one higher than the elevation of your current square; that is, if your current elevation is m, you could step to elevation n, but not to elevation o. (This also means that the elevation of the destination square can be much lower than the elevation of your current square.)

For example:

Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
Here, you start in the top-left corner; your goal is near the middle. You could start by moving down or right, but eventually you'll need to head toward the e at the bottom. From there, you can spiral around to the goal:

v..v<<<<
>v.vv<<^
.>vv>E^^
..v>>>^^
..>>>>>^
In the above diagram, the symbols indicate whether the path exits each square moving up (^), down (v), left (<), or right (>). The location that should get the best signal is still E, and . marks unvisited squares.

This path reaches the goal in 31 steps, the fewest possible.

What is the fewest steps required to move from your current position to the location that should get the best signal? """

""" --- Part Two ---
As you walk up the hill, you suspect that the Elves will want to turn this into a hiking trail. The beginning isn't very scenic, though; perhaps you can find a better starting point.

To maximize exercise while hiking, the trail should start as low as possible: elevation a. The goal is still the square marked E. However, the trail should still be direct, taking the fewest steps to reach its goal. So, you'll need to find the shortest path from any square at elevation a to the square marked E.

Again consider the example from above:

Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
Now, there are six choices for starting position (five marked a, plus the square marked S that counts as being at elevation a). If you start at the bottom-left square, you can reach the goal most quickly:

...v<<<<
...vv<<^
...v>E^^
.>v>>>^^
>^>>>>>^
This path reaches the goal in only 29 steps, the fewest possible.

What is the fewest steps required to move starting from any square with elevation a to the location that should get the best signal? """

def parse():
    with open('Day 12 - input.txt') as f:
        lines = [line.rstrip('\n') for line in f]
    
    heights = []
    for line in lines:
        row = []
        for char in line:
            row.append(ord(char))
        heights.append(row)

    return heights

# Check if its possible to move north
def checkNorth(row, col, heights):
    if row - 1 < 0:
        return False
    current_height = heights[row][col]
    north_height = heights[row-1][col]
    if north_height - current_height <= 1:
        return True
    else:
        return False

def checkEast(row, col, heights):
    if col + 1 >= len(heights[row]):
        return False
    current_height = heights[row][col]
    east_height = heights[row][col+1]
    if east_height - current_height <= 1:
        return True
    else:
        return False

def checkSouth(row, col, heights):
    if row + 1  >= len(heights):
        return False
    current_height = heights[row][col]
    south_height = heights[row+1][col]
    if south_height - current_height <= 1:
        return True
    else:
        return False

def checkWest(row, col, heights):
    if col -1 < 0:
        return False
    current_height = heights[row][col]
    west_height = heights[row][col-1]
    if west_height - current_height <= 1:
        return True
    else:
        return False

def get_end_points(heights):
    start = (0, 0)
    end = (0, 0)

    for row in range(len(heights)):
        for col in range(len(heights[row])):
            if heights[row][col] == ord('S'):
                start = (row, col)
                heights[row][col] = ord('a')
            elif heights[row][col] == ord('E'):
                end = (row, col)
                heights[row][col] = ord('z')
    return start, end

def traverse(start, heights):
    visited = set([start])
    queue = [start]
    paths = {start: []}

    while queue != [] and len(visited) < len(heights) * len(heights[0]):
        row, col = queue.pop(0)
        # Check squares in each direction and add to queue if theres a path
        if checkNorth(row, col, heights):
            north = (row - 1, col)
            if north not in visited:
                queue.append(north)
                visited.add(north)
                paths[north] = paths[(row, col)] + [(row, col)]
        if checkEast(row, col, heights):
            east = (row, col + 1)
            if east not in visited:
                queue.append(east)
                visited.add(east)
                paths[east] = paths[(row, col)] + [(row, col)]
        if checkSouth(row, col, heights):
            south = (row + 1, col)
            if south not in visited:
                queue.append(south)
                visited.add(south)
                paths[south] = paths[(row, col)] + [(row, col)]
        if checkWest(row, col, heights):
            west = (row, col - 1)
            if west not in visited:
                queue.append(west)
                visited.add(west)
                paths[west] = paths[(row, col)] + [(row, col)]
            
    return paths

def any_starting_a(end, heights):
    shortest_path = float('inf')
    for row in range(len(heights)):
        for col in range(len(heights[row])):
            if heights[row][col] == ord('a'):
                new_paths = traverse((row, col), heights)
                if end in new_paths:
                    shortest_path = min(shortest_path, len(new_paths[end]))
    
    return shortest_path

def main():
    # Part 1
    heights = parse()
    start, end = get_end_points(heights)
    paths = traverse(start, heights)
    print(len(paths[end])) # Part 1 Ans: 350

    # Part 2
    shortest_path_from_any = any_starting_a(end, heights)
    print(shortest_path_from_any) # Part 2 Ans: 349
    
if __name__ == '__main__':
    main()