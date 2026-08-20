from mazegen import build_the_grid, carve_maze
import numpy as np
import random


def generate_maze(config_data: dict[str, str],
                  new: bool = False
                  ) -> list[list[int]]:
    entry = int(config_data["ENTRY"][0]), int(config_data["ENTRY"][1])
    maze_exit = int(config_data["EXIT"][0]), int(config_data["EXIT"][1])
    grid = build_the_grid(
        int(config_data["WIDTH"]), int(config_data["HEIGHT"]))
    if new:
        seed = np.random.randint(0, 1000)
        carve_maze(grid, 0, 0, random.Random(seed), entry, maze_exit)
    else:
        carve_maze(grid, 0, 0, random.Random(42), entry, maze_exit)
    return grid
