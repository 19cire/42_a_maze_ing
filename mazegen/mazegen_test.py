import random
from mazegen.mazegen import (build_the_grid, is_wall_closed, open_wall,
                          get_unvisited_neighbours, carve_maze,
                          construct_pattern_42,
                          check_connectivity,
                          count_open_walls,
                          add_loops,
                          DIRECTION_STEP,
                          ALL_WALLS_CLOSED
                          )
from mazegen.mazegen import NORTH, EAST, WEST, SOUTH
grid = build_the_grid(20, 15)
print("====Grid buiding test====")
print(grid[4][4], grid[4][5])
print("\n====Wall opening test====")
open_wall(grid, 4, 4, EAST)
print(grid[4][4], grid[4][5])
try:
    open_wall(grid, 0, 0, NORTH)
    print("no error")
except ValueError as error:
    print("correctly refused:", error)
try:
    open_wall(grid, 19, 4, WEST)
    print("no error")
except ValueError as error:
    print("correctly refused:", error)
print("\n====Neighbour visiting test===")
visited: set[tuple[int, int]] = set()
unvisited = get_unvisited_neighbours(grid, 0, 0, visited)
print("corner (0,0), nothing visited:", unvisited)
print("expected: [EAST, SOUTH] =", [EAST, SOUTH])
unvisited = get_unvisited_neighbours(grid, 4, 4, visited)
print("interior (4,4), nothing visited:", unvisited)
print("expected: [NORTH, EAST, SOUTH, WEST] =", [NORTH, EAST, SOUTH, WEST])
visited = {(4, 3)}
unvisited = get_unvisited_neighbours(grid, 4, 4, visited)
print("interior (4,4), NORTH visited:", unvisited)
print("expected: [EAST, SOUTH, WEST] =", [EAST, SOUTH, WEST])
visited = {(4, 3), (5, 4), (4, 5), (3, 4)}
unvisited = get_unvisited_neighbours(grid, 4, 4, visited)
print("interior (4,4), ALL visited:", unvisited)
print("expected: [] =", [])
print("====Cells not reached after DFS====")
rng = random.Random(42)
carve_maze(grid, 0, 0, rng)
untouched = 0
for row in grid:
    for cell in row:
        if cell == ALL_WALLS_CLOSED:
            untouched += 1
print("cells never reached:", untouched, "- expected 0")
print("\n====Maze representation in hexdecimal test====")
grid = build_the_grid(20, 15)
rng = random.Random(42)
carve_maze(grid, 0, 0, rng)
for row in grid:
    line = ""
    for cell in row:
        line += f"{cell:x}"
    print(line)
print("\n====Number of walled opened after DFS test====")
open_count = 0
for row in grid:
    for cell in row:
        for direction in DIRECTION_STEP:
            if not is_wall_closed(cell, direction):
                open_count += 1
print("open walls:", open_count // 2, "- expected 299")
print("\n====Reproductility through seed test====")
grid_a = build_the_grid(20, 15)
rng_a = random.Random(42)
carve_maze(grid_a, 0, 0, rng_a)
grid_b = build_the_grid(20, 15)
rng_b = random.Random(42)
carve_maze(grid_b, 0, 0, rng_b)
grid_c = build_the_grid(20, 15)
rng_c = random.Random(7)
carve_maze(grid_c, 0, 0, rng_c)
print(grid_a == grid_b)
print(grid_a == grid_c)
print("\n====42 Pattern test====")
cells = construct_pattern_42(20, 15)
for y in range(15):
    line = ""
    for x in range(20):
        line += "#" if (x, y) in cells else "."
    print(line)
print("\n====Connectivity after 42 pattern test====")
check_connectivity(20, 15, construct_pattern_42(20, 15))
check_connectivity(20, 15, set())
wall = {(10, y) for y in range(15)}
try:
    check_connectivity(20, 15, wall)
    print("No error")
except ValueError as error:
    print("correctly refused!:", error)
print("\n====Counting of opened wall test====")
wall_opened = count_open_walls(15)
wall_opened_1 = count_open_walls(11)
wall_opened_2 = count_open_walls(0)
print(wall_opened)
print(wall_opened_1)
print(wall_opened_2)
print("\n====Number of dead ends test===")
grid = build_the_grid(20, 15)
rng = random.Random(42)
carve_maze(grid, 0, 0, rng, construct_pattern_42(20, 15))
add_loops(grid, rng, construct_pattern_42(20, 15))
print("====Loop adding test====")
grid = build_the_grid(20, 15)
blocked = construct_pattern_42(20, 15)
rng = random.Random(42)
carve_maze(grid, 0, 0, rng, blocked)
add_loops(grid, rng, blocked)
after = 0
for row in grid:
    for cell in row:
        if count_open_walls(cell) == 1:
            after  += 1
print("dead-ends after:", after, "- was 26")
open_count = 0
for row in grid:
    for cell in row:
        for direction in DIRECTION_STEP:
            if not is_wall_closed(cell, direction):
                open_count += 1
print("open walls:", open_count // 2, "- expected 325")
for (x, y) in blocked:
    if grid[y][x] != ALL_WALLS_CLOSED:
        print("PATTERN BROKEN at", x, y)
