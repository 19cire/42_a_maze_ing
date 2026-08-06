from mazegen import build_the_grid, open_wall, SOUTH, NORTH

grid = build_the_grid(3, 3)
print(grid[1][1], grid[2][1])
open_wall(grid, 1, 1, SOUTH)
print(grid[1][1], grid[2][1])
try:
    open_wall(grid, 0, 0, NORTH)
    print("no error - this would be a bug")
except ValueError as error:
    print("correctly refused:", error)
