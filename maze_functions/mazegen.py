from .show_maze import maze_viewer, clear_screen
import time
import random
from .variables import (ALL_WALLS_CLOSED,
                        DIRECTION_STEP,
                        DIRECTION_OPPOSITE)


def build_the_grid(width: int, height: int) -> list[list[int]]:
    """This function build the whole grid

    Args:
        width: an int indicating the width of the grid
        height: an int indicating the height of the grid

    Returns:
        rows of cells, each cell being an int holding its wall bits
    """
    grid = [[ALL_WALLS_CLOSED for _ in range(width)] for _ in range(height)]
    return grid


def is_wall_closed(cell: int, wall: int) -> bool:
    """This function check if a wall is closed or not

    Args:
        cell: indicate which cell we are visiting
        wall: indicate which wall we are checking

    Returns:
        return a bool indicating if the wall is closed or not
    """
    return bool(cell & wall)


def open_wall(grid: list[list[int]], x: int, y: int, direction: int) -> None:
    """This function open a wall between two neighbour cells

    Args:
        grid: the grid we are working with
        x: cell coordinate i.e the column
        y: cell coordinate i.e the row
        direction: indicate which wall we are opening

    Returns:
        None
    """
    opposite_direction = DIRECTION_OPPOSITE[direction]
    dx, dy = DIRECTION_STEP[direction]
    neighbour_x = x + dx
    neighbour_y = y + dy
    if not (neighbour_x >= 0 and neighbour_x < len(grid[0])
            and neighbour_y >= 0 and neighbour_y < len(grid)):
        raise ValueError("You are outside of the labyrinth")
    grid[y][x] &= ~direction
    grid[neighbour_y][neighbour_x] &= ~opposite_direction


def get_unvisited_neighbours(grid: list[list[int]], x: int, y: int,
                             visited: set[tuple[int, int]]) -> list[int]:
    """This function give us all possible unvisited neighbours,
        where DFS can carve a wall

    Args:
        grid: the grid we are working with
        x: cell coordinate i.e the column
        y: cell coordinate i.e the row
        visited: a set with the coordinates of visited cells

    Returns:
        a list of int indicating the direction to adjacent unvisted cells
    """
    unvisited: list[int] = []
    for direction in DIRECTION_STEP:
        dx, dy = DIRECTION_STEP[direction]
        neighbour_x = x + dx
        neighbour_y = y + dy
        if not (neighbour_x >= 0 and neighbour_x < len(grid[0])
                and neighbour_y >= 0 and neighbour_y < len(grid)):
            continue
        if (neighbour_x, neighbour_y) in visited:
            continue
        unvisited.append(direction)
    return unvisited


def carve_maze(grid: list[list[int]], x: int, y: int,
               rng: random.Random, entry, exit) -> None:
    """This is the main function carving walls in the DFS algorithm

    Args:
        grid: the grid we are working with
        x: coordinate of starting cell i.e column
        y: coordinate of starting cell i.e row
        rng: random generator object

    Returns:
        None
    """
    visited: set[tuple[int, int]] = {(x, y)}
    stack: list[tuple[int, int]] = [(x, y)]
    while stack:
        clear_screen()
        current_x, current_y = stack[-1]
        directions = get_unvisited_neighbours(grid, current_x,
                                              current_y, visited)
        if not directions:
            stack.pop()
        else:
            direction = rng.choice(directions)
            open_wall(grid, current_x, current_y, direction)
            dx, dy = DIRECTION_STEP[direction]
            neighbour_x = current_x + dx
            neighbour_y = current_y + dy
            visited.add((neighbour_x, neighbour_y))
            stack.append((neighbour_x, neighbour_y))
        maze_viewer(grid, 21, entry, exit)
        time.sleep(0.03)
