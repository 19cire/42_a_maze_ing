from mazegen import build_the_grid, open_wall, get_unvisited_neighbours, NORTH, EAST, SOUTH, WEST

grid = build_the_grid(20, 15)
print("===================================================")
print(grid[4][4], grid[4][5])
print("===================================================")
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
try:
    open_wall(grid, 14, 14, SOUTH)
    print("no error")
except ValueError as error:
    print("correctly refused:", error)
try:
    open_wall(grid, 0, 7, WEST)
    print("no error")
except ValueError as error:
    print("correctly refused:", error)
print("===================================================")
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