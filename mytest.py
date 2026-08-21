import random

import pytest

from mazegen import (
    build_the_grid,
    is_wall_closed,
    open_wall,
    get_unvisited_neighbours,
    carve_maze,
    construct_pattern_42,
    check_connectivity,
    count_open_walls,
    add_loops,
    would_create_3x3_open_area,
    shortest_path,
    store_maze,
    entry_exit_validation,
    MazeGenerator,
    DIRECTION_STEP,
    ALL_WALLS_CLOSED,
)
from mazegen import NORTH, EAST, WEST, SOUTH


# ---------- Grid building ----------

def test_build_the_grid_dimensions() -> None:
    grid = build_the_grid(20, 15)
    assert len(grid) == 15
    assert len(grid[0]) == 20


def test_build_the_grid_cells_start_fully_walled() -> None:
    grid = build_the_grid(20, 15)
    assert grid[4][4] == ALL_WALLS_CLOSED
    assert grid[4][5] == ALL_WALLS_CLOSED


# ---------- Opening walls ----------

def test_open_wall_removes_wall_on_both_sides() -> None:
    grid = build_the_grid(20, 15)
    open_wall(grid, 4, 4, EAST)
    assert not is_wall_closed(grid[4][4], EAST)
    assert not is_wall_closed(grid[4][5], WEST)


def test_open_wall_refuses_border_north() -> None:
    grid = build_the_grid(20, 15)
    with pytest.raises(ValueError):
        open_wall(grid, 0, 0, NORTH)


def test_open_wall_refuses_border_west_on_right_edge() -> None:
    grid = build_the_grid(20, 15)
    with pytest.raises(ValueError):
        open_wall(grid, 32, 4, WEST)


# ---------- Neighbour visiting ----------

def test_unvisited_neighbours_corner_none_visited() -> None:
    grid = build_the_grid(20, 15)
    visited: set[tuple[int, int]] = set()
    unvisited = get_unvisited_neighbours(grid, 0, 0, visited)
    assert unvisited == [EAST, SOUTH]


def test_unvisited_neighbours_interior_none_visited() -> None:
    grid = build_the_grid(20, 15)
    visited: set[tuple[int, int]] = set()
    unvisited = get_unvisited_neighbours(grid, 4, 4, visited)
    assert unvisited == [NORTH, EAST, SOUTH, WEST]


def test_unvisited_neighbours_interior_one_visited() -> None:
    grid = build_the_grid(20, 15)
    visited = {(4, 3)}
    unvisited = get_unvisited_neighbours(grid, 4, 4, visited)
    assert unvisited == [EAST, SOUTH, WEST]


def test_unvisited_neighbours_interior_all_visited() -> None:
    grid = build_the_grid(20, 15)
    visited = {(4, 3), (5, 4), (4, 5), (3, 4)}
    unvisited = get_unvisited_neighbours(grid, 4, 4, visited)
    assert unvisited == []


# ---------- DFS maze carving ----------

def test_carve_maze_reaches_every_cell() -> None:
    grid = build_the_grid(20, 15)
    rng = random.Random(42)
    carve_maze(grid, 0, 0, rng)

    untouched = sum(
        1 for row in grid for cell in row if cell == ALL_WALLS_CLOSED
    )
    assert untouched == 0


def test_carve_maze_open_wall_count() -> None:
    grid = build_the_grid(20, 15)
    rng = random.Random(42)
    carve_maze(grid, 0, 0, rng)

    open_count = 0
    for row in grid:
        for cell in row:
            for direction in DIRECTION_STEP:
                if not is_wall_closed(cell, direction):
                    open_count += 1
    assert open_count // 2 == 299


def test_carve_maze_same_seed_is_reproducible() -> None:
    grid_a = build_the_grid(20, 15)
    carve_maze(grid_a, 0, 0, random.Random(42))

    grid_b = build_the_grid(20, 15)
    carve_maze(grid_b, 0, 0, random.Random(42))

    assert grid_a == grid_b


def test_carve_maze_different_seed_gives_different_maze() -> None:
    grid_a = build_the_grid(20, 15)
    carve_maze(grid_a, 0, 0, random.Random(42))

    grid_c = build_the_grid(20, 15)
    carve_maze(grid_c, 0, 0, random.Random(7))

    assert grid_a != grid_c


# ---------- "42" pattern ----------

def test_construct_pattern_42_is_connected() -> None:
    # Should not raise: the pattern itself must not isolate any cell.
    check_connectivity(20, 15, construct_pattern_42(20, 15))


def test_check_connectivity_empty_blocked_set_is_connected() -> None:
    check_connectivity(20, 15, set())


def test_check_connectivity_full_wall_is_rejected() -> None:
    wall = {(10, y) for y in range(15)}
    with pytest.raises(ValueError):
        check_connectivity(20, 15, wall)


# ---------- Counting open walls ----------

@pytest.mark.parametrize(
    "cell_value,expected",
    [
        (15, 0),
        (11, 1),
        (0, 4),
    ],
)
def test_count_open_walls(cell_value: int, expected: int) -> None:
    assert count_open_walls(cell_value) == expected


# ---------- Loop adding ----------

def test_add_loops_reduces_dead_ends_and_respects_blocked_pattern() -> None:
    grid = build_the_grid(20, 15)
    blocked = construct_pattern_42(20, 15)
    rng = random.Random(42)

    carve_maze(grid, 0, 0, rng, blocked)
    add_loops(grid, rng, blocked)

    dead_ends_after = sum(
        1 for row in grid for cell in row if count_open_walls(cell) == 1
    )
    assert dead_ends_after <= 26

    open_count = 0
    for row in grid:
        for cell in row:
            for direction in DIRECTION_STEP:
                if not is_wall_closed(cell, direction):
                    open_count += 1
    assert open_count // 2 == 304

    for (x, y) in blocked:
        assert grid[y][x] == ALL_WALLS_CLOSED, f"pattern broken at {x},{y}"


# ---------- 3x3 open area detection ----------

def test_would_create_3x3_open_area_detects_large_open_space() -> None:
    grid = build_the_grid(5, 5)
    open_wall(grid, 1, 1, EAST)
    open_wall(grid, 2, 1, EAST)
    open_wall(grid, 1, 2, EAST)
    open_wall(grid, 2, 2, EAST)
    open_wall(grid, 1, 3, EAST)
    open_wall(grid, 2, 3, EAST)
    open_wall(grid, 1, 1, SOUTH)
    open_wall(grid, 2, 1, SOUTH)
    open_wall(grid, 3, 1, SOUTH)
    open_wall(grid, 1, 2, SOUTH)
    open_wall(grid, 3, 2, SOUTH)

    assert would_create_3x3_open_area(grid, 2, 2, SOUTH) is True


# ---------- MazeGenerator + shortest path ----------

def test_maze_generator_produces_valid_solvable_maze(tmp_path: object) -> None:
    generator = MazeGenerator(20, 15, (1, 1), (18, 13), 42, False)
    generator.generate()

    grid = generator.grid
    result = shortest_path(grid, (1, 1), (18, 13))
    assert result is not None
    assert result[0] == (1, 1)
    assert result[-1] == (18, 13)

    # Every step in the path must move through an open wall, never through
    # a closed one.
    for i in range(len(result) - 1):
        x1, y1 = result[i]
        x2, y2 = result[i + 1]
        for direction, (dx, dy) in DIRECTION_STEP.items():
            if (x1 + dx, y1 + dy) == (x2, y2):
                assert not is_wall_closed(grid[y1][x1], direction), (
                    f"path walks through a wall at {x1},{y1}"
                )


def test_store_maze_writes_output_file(tmp_path: object) -> None:
    generator = MazeGenerator(20, 15, (1, 1), (18, 13), 42, False)
    generator.generate()

    output_file = str(tmp_path) + "/test_output.txt"
    store_maze(generator.grid, (1, 1), (18, 13), output_file)

    with open(output_file, "r") as f:
        content = f.read()
    assert len(content) > 0


# ---------- Entry/exit validation ----------

def test_entry_exit_validation_accepts_valid_positions() -> None:
    blocked = construct_pattern_42(20, 15)
    # Should not raise.
    entry_exit_validation(20, 15, (1, 1), (18, 13), blocked)


def test_entry_exit_validation_rejects_out_of_bounds() -> None:
    blocked = construct_pattern_42(20, 15)
    with pytest.raises(ValueError):
        entry_exit_validation(20, 15, (99, 1), (5, 99), blocked)


def test_entry_exit_validation_rejects_identical_entry_and_exit() -> None:
    blocked = construct_pattern_42(20, 15)
    with pytest.raises(ValueError):
        entry_exit_validation(20, 15, (1, 1), (1, 1), blocked)


def test_entry_exit_validation_rejects_blocked_position() -> None:
    blocked = construct_pattern_42(20, 15)
    with pytest.raises(ValueError):
        entry_exit_validation(20, 15, (1, 1), (6, 5), blocked)
