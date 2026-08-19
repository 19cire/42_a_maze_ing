import random
PATTERN_42 = [
    "#..#..####",
    "#..#.....#",
    "#..#.....#",
    "####..####",
    "...#..#...",
    "...#..#...",
    "...#..####",
]
ALL_WALLS_CLOSED = 15
NORTH = 1
EAST = 2
SOUTH = 4
WEST = 8
DIRECTION_STEP = {NORTH: (0, -1), EAST: (1, 0), SOUTH: (0, 1), WEST: (-1, 0)}
DIRECTION_OPPOSITE = {NORTH: SOUTH, EAST: WEST, SOUTH: NORTH, WEST: EAST}


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


def construct_pattern_42(width: int, height: int) -> set[tuple[int, int]]:
    """This function will check if the grid dimensions can handle the
    42 pattern, then generate it

    Args:
        width: an int indicating the width of the grid
        height: an int indicating the height of the grid

    Returns:
        a set of coordinates of the 42 pattern
    """
    pattern_width = len(PATTERN_42[0])
    pattern_height = len(PATTERN_42)
    pattern_cells: set[tuple[int, int]] = set()
    if width < pattern_width + 2 or height < pattern_height + 2:
        raise ValueError("This labyrinth cannot handle the '42' pattern!")
    origin_x = (width - pattern_width) // 2
    origin_y = (height - pattern_height) // 2
    for row_index, line in enumerate(PATTERN_42):
        for column_index, character in enumerate(line):
            if character == "#":
                cell_x = origin_x + column_index
                cell_y = origin_y + row_index
                pattern_cells.add((cell_x, cell_y))
    return pattern_cells


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
        raise ValueError("You are outside of the labyrinth!")
    grid[y][x] &= ~direction
    grid[neighbour_y][neighbour_x] &= ~opposite_direction


def get_unvisited_neighbours(grid: list[list[int]], x: int, y: int,
                             visited: set[tuple[int, int]],
                             blocked: set[tuple[int, int]]
                             | None = None) -> list[int]:
    """This function give us all possible unvisited neighbours,
        where DFS can carve a wall

    Args:
        grid: the grid we are working with
        x: cell coordinate i.e the column
        y: cell coordinate i.e the row
        visited: a set with the coordinates of visited cells
        blocked: a set with the coordinates of the 42 pattern

    Returns:
        a list of int indicating the direction to adjacent unvisted cells
    """
    unvisited: list[int] = []
    if blocked is None:
        blocked = set()
    for direction in DIRECTION_STEP:
        dx, dy = DIRECTION_STEP[direction]
        neighbour_x = x + dx
        neighbour_y = y + dy
        if not (neighbour_x >= 0 and neighbour_x < len(grid[0])
                and neighbour_y >= 0 and neighbour_y < len(grid)):
            continue
        if (neighbour_x, neighbour_y) in visited:
            continue
        if (neighbour_x, neighbour_y) in blocked:
            continue
        unvisited.append(direction)
    return unvisited


def check_connectivity(width: int, height: int,
                       blocked: set[tuple[int, int]] | None = None) -> None:
    """This function check if all cells except 42 pattern are connected

    Args:
        width: an int indicating the width of the grid
        height: an int indicating the height of the grid
        blocked: a set with the coordinates of the 42 pattern

    Returns:
        None
    """
    if blocked is None:
        blocked = set()
    free_cells_total = (width * height) - len(blocked)
    reached: set[tuple[int, int]] = {(0, 0)}
    stack: list[tuple[int, int]] = [(0, 0)]
    if (0, 0) in blocked:
        raise ValueError("This cell is blocked, "
                         "cannot start connectivity check!")
    while stack:
        current_x, current_y = stack.pop()
        for direction in DIRECTION_STEP:
            dx, dy = DIRECTION_STEP[direction]
            neighbour_x = current_x + dx
            neighbour_y = current_y + dy
            if not (neighbour_x >= 0 and neighbour_x < width
                    and neighbour_y >= 0 and neighbour_y < height):
                continue
            if (neighbour_x, neighbour_y) in blocked:
                continue
            if (neighbour_x, neighbour_y) in reached:
                continue
            reached.add((neighbour_x, neighbour_y))
            stack.append((neighbour_x, neighbour_y))
    if len(reached) != free_cells_total:
        raise ValueError("The maze is not connected!")


def carve_maze(grid: list[list[int]], x: int, y: int,
               rng: random.Random, blocked: set[tuple[int, int]]
               | None = None) -> None:
    """This is the main function carving walls in the DFS algorithm

    Args:
        grid: the grid we are working with
        x: coordinate of starting cell i.e column
        y: coordinate of starting cell i.e row
        rng: random generator object
        blocked: a set with the coordinates of the 42 pattern

    Returns:
        None
    """
    visited: set[tuple[int, int]] = {(x, y)}
    stack: list[tuple[int, int]] = [(x, y)]
    while stack:
        current_x, current_y = stack[-1]
        directions = get_unvisited_neighbours(grid, current_x,
                                              current_y, visited, blocked)
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


class MazeGenerator:
    """The class of the generator

    Args:
        width: the width of the maze x axis
        height: the height of the maze y axis
        maze_entry: the coordinates of entry point
        maze_exit: the coordinates of exit point
        seed: the seed of the maze's generation
        perfect: a bool telling us if maze is perfect or not
    """

    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height

    # def __init__(self, width: int, height: int, maze_entry: tuple[int, int],
    #              maze_exit: tuple[int, int],
    #               seed: int, perfect: bool) -> None:
    #     self.width = width
    #     self.height = height
    #     self.maze_entry = maze_entry
    #     self.maze_exit = maze_exit
    #     self.seed = seed
    #     self.rng = random.Random(self.seed)
    #     self.perfect = perfect
    #     self.grid: list[list[int]] = []
    #     self.solution: list[tuple[int, int]] = []

    def generate(self) -> None:
        # Reset the random generator from the seed, so repeated calls
        # are reproducible.
        # Mark the 42 cells — call construct_pattern_42, get the blocked set.
        # Must happen before carving, because sealing cells after a
        # spanning tree exists would cut the maze into islands.

        # Verify connectivity of the non-blocked cells —
        # confirm the 42 hasn't fragmented the grid into separate regions.

        # Check that starting cell is not part of 42 pattern.

        # Carve the spanning tree with carve_maze,
        # passing blocked so DFS avoids the sealed cells.

        # Open the entry and exit in the outer border —
        # a separate step, since open_wall refuses border openings by design.

        # If not perfect: the loop pass — fix dead-ends,
        # guarded by the 3×3 check and the no-border rule.

        # Compute the shortest path from entry to exit
        # and store it in self.solution.
        pass
