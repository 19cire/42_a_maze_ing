import random
PATTERN_42 = [
    "#.#.####",
    "#.#....#",
    "###.####",
    "..#.#...",
    "..#.####",
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


def count_open_walls(cell: int) -> int:
    """This function count how many walls are open,
    help to identify dead ends

    Args:
        cell: the cell's wall we are counting

    Returns:
        an int telling us how many walls are opened
    """
    open_count = 0
    for direction in DIRECTION_STEP:
        if not is_wall_closed(cell, direction):
            open_count += 1
    return open_count


def would_create_3x3_open_area(grid: list[list[int]], x: int,
                               y: int, direction: int) -> bool:
    """This function tell us if a 3x3 open area is opened

    Args:
        grid: our maze we are working with
        x: cell coordinate i.e the column
        y: cell coordinate i.e the row
        direction: indicate which walls are opened

    Returns:
        a bool telling us if a 3x3 open area is present
    """
    dx, dy = DIRECTION_STEP[direction]
    neighbour_x = x + dx
    neighbour_y = y + dy
    first_by = max(0, max(y, neighbour_y) - 2)
    last_by = min(min(y, neighbour_y), len(grid) - 3)
    first_bx = max(0, max(x, neighbour_x) - 2)
    last_bx = min(min(x, neighbour_x), len(grid[0]) - 3)
    if direction in (NORTH, WEST):
        x, y = neighbour_x, neighbour_y
        direction = DIRECTION_OPPOSITE[direction]
    for by in range(first_by, last_by + 1):
        for bx in range(first_bx, last_bx + 1):
            fully_open = True
            for cy in range(by, by + 3):
                for cx in range(bx, bx + 3):
                    if (cx < bx + 2 and is_wall_closed(grid[cy][cx], EAST) and
                            not (cx == x and cy == y and direction == EAST)):
                        fully_open = False
                    if (cy < by + 2 and is_wall_closed(grid[cy][cx], SOUTH) and
                            not (cx == x and cy == y and direction == SOUTH)):
                        fully_open = False
            if fully_open:
                return True
    return False


def add_loops(grid: list[list[int]], rng: random.Random,
              blocked: set[tuple[int, int]] | None = None) -> None:
    """This functions helps us adding loops for PERFECT=False

    Args:
        grid: our maze we are working with
        rng: the random generator object
        blocked: the blocks of the 42 pattern to avoid

    Returns:
        None
    """
    if blocked is None:
        blocked = set()
    dead_ends: list[tuple[int, int]] = []
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if count_open_walls(grid[y][x]) == 1:
                dead_ends.append((x, y))
    for (cell_x, cell_y) in dead_ends:
        candidate_to_open: list[int] = []
        for direction in DIRECTION_STEP:
            dx, dy = DIRECTION_STEP[direction]
            neighbour_x = cell_x + dx
            neighbour_y = cell_y + dy
            if not (neighbour_x >= 0 and neighbour_x < len(grid[0])
                    and neighbour_y >= 0 and neighbour_y < len(grid)):
                continue
            if (neighbour_x, neighbour_y) in blocked:
                continue
            if not is_wall_closed(grid[cell_y][cell_x], direction):
                continue
            if would_create_3x3_open_area(grid, cell_x, cell_y, direction):
                continue
            candidate_to_open.append(direction)
        if candidate_to_open:
            direction = rng.choice(candidate_to_open)
            open_wall(grid, cell_x, cell_y, direction)


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

# PATH funcions


def check_directions(point: int) -> list[str]:
    dir: list[str] = []
    if not point & NORTH:
        dir.append("N")
    if not point & EAST:
        dir.append("E")
    if not point & SOUTH:
        dir.append("S")
    if not point & WEST:
        dir.append("W")
    return dir


def go(direction: str,
       x: int,
       y: int,
       queue: list[tuple[int, int]],
       came_from: dict[tuple[int, int], tuple[int, int] | None]
       ) -> None:
    if direction == "N" and (x, y - 1) not in came_from:
        queue.append((x, y - 1))
        came_from[((x, y - 1))] = (x, y)

    if direction == "E" and (x + 1, y) not in came_from:
        queue.append((x + 1, y))
        came_from[((x + 1, y))] = (x, y)

    if direction == "S" and (x, y + 1) not in came_from:
        queue.append((x, y + 1))
        came_from[((x, y + 1))] = (x, y)
    if direction == "W" and (x - 1, y) not in came_from:
        queue.append((x - 1, y))
        came_from[((x - 1, y))] = (x, y)


def shortest_path(grid: list[list[int]],
                  start: tuple[int, int],
                  end: tuple[int, int]
                  ) -> list[tuple[int, int]]:
    queue: list[tuple[int, int]] = [start]
    came_from: dict[tuple[int, int], tuple[int, int] | None] = {start:  None}

    while queue:
        x, y = queue.pop(0)
        if (x, y) == end:
            break
        directions: list[str] = check_directions(grid[y][x])
        for direction in directions:
            go(direction, x, y, queue, came_from)
    path: list[tuple[int, int]] = []
    current: tuple[int, int] | None = end
    while current is not None:
        path.append(current)
        current = came_from[current]
    path.reverse()
    return path


def entry_exit_validation(width: int, height: int, maze_entry: tuple[int, int],
                          maze_exit: tuple[int, int],
                          blocked: set[tuple[int, int]] | None = None) -> None:
    """This function check that both entry and exit are valid

    Args:
        width: an int indicating the width of the grid
        height: an int indicating the height of the grid
        maze_entry: coordinate of the entry point
        maze_exit: coordinates of the exit point
        blocked: the cells of the 42 pattern

    Returns:
        None
    """
    if blocked is None:
        blocked = set()
    entry_x, entry_y = maze_entry
    exit_x, exit_y = maze_exit
    if not (0 <= entry_x < width and 0 <= entry_y < height):
        raise ValueError("The entry is not in the maze!")
    if not (0 <= exit_x < width and 0 <= exit_y < height):
        raise ValueError("The exit is not in the maze!")
    if (entry_x, entry_y) == (exit_x, exit_y):
        raise ValueError("Entry and exit must not be the same!")
    if (entry_x, entry_y) in blocked or (exit_x, exit_y) in blocked:
        raise ValueError("Entry or exit must not be inside the 42 pattern!")


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

    def __init__(self, width: int, height: int, maze_entry: tuple[int, int],
                 maze_exit: tuple[int, int],
                 seed: int, perfect: bool) -> None:
        self.width = width
        self.height = height
        self.maze_entry = maze_entry
        self.maze_exit = maze_exit
        self.seed = seed
        self.blocked: set[tuple[int, int]] = set()
        self.rng = random.Random(self.seed)
        self.perfect = perfect
        self.grid: list[list[int]] = []
        self.solution: list[tuple[int, int]] = []

    def generate(self) -> None:
        self.grid = build_the_grid(self.width, self.height)
        # Reset the random generator from the seed, so repeated calls
        # are reproducible.
        # Mark the 42 cells — call construct_pattern_42, get the blocked set.
        self.rng = random.Random(self.seed)
        self.blocked = construct_pattern_42(self.width, self.height)
        entry_exit_validation(self.width, self.height, self.maze_entry,
                              self.maze_exit, self.blocked)
        check_connectivity(self.width, self.height, self.blocked)
        carve_maze(self.grid, 0, 0, self.rng, self.blocked)
        if not self.perfect:
            add_loops(self.grid, self.rng, self.blocked)
        self.solution = shortest_path(self.grid,
                                      self.maze_entry, self.maze_exit)
