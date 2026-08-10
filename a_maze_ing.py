#!/usr/bin/python3
from typing import Any
import sys


class SizeError(Exception):
    pass


def read_file(file: str) -> dict[str, str]:
    data = {}
    try:
        with open(file, "r") as f:
            for line in f:
                line = line.strip()
                value = line.split("=")
                if value[0] == "ENTRY" or value[0] == "EXIT":
                    data[value[0]] = value[1].split(",")
                else:
                    data[value[0]] = value[1]
    except FileNotFoundError as e:
        print(f"{e.__class__.__name__}: {e}")
    return data


class MazeBox():
    def __init__(self, x: int, y: int, left: bool = True, top: bool = True,
                 right: bool = True, bottom: bool = True,
                 visited: bool = False) -> None:
        self.left = left
        self.top = top
        self.right = right
        self.bottom = bottom
        self.x = x
        self.y = y
        self.visited = visited


def create_maze_base(data: dict[str, Any]) -> dict[tuple[int, int], MazeBox]:
    width = int(data["WIDTH"])
    height = int(data["HEIGHT"])
    boxes: dict[tuple[int, int], MazeBox] = {}
    for line in range(height):
        for row in range(width):
            boxes[(row, line)] = MazeBox(x=row, y=line)
    return boxes


def bg_square(r: int, g: int, b: int) -> str:
    return f"\033[48;2;{r};{g};{b}m  \033[0m"


def show_maze(maze_board: dict[tuple[int, int], MazeBox],
              fourty: dict[tuple[int, int], MazeBox]) -> None:
    last_key = next(reversed(maze_board))
    height: int = maze_board[last_key].y
    width: int = maze_board[last_key].x
    for line in range(height + 1):
        symbol: str = bg_square(0, 100, 255)
        line1: list[str] = [symbol]
        line2: list[str] = [symbol]
        line3: list[str] = [symbol]
        """printfirst line"""
        for row in range(0, width + 1):
            line1.append(symbol) if maze_board.get(
                (row, line)) else line1.append("  ")
            line1.append(symbol)
            line2.append(bg_square(160, 100, 255)) if (
                row, line) in fourty else line2.append("  ")
            line2.append(symbol) if maze_board.get(
                (row, line)) else line2.append("  ")
            line3.append(symbol)
            line3.append(symbol)

        print("".join(line1))
        print("".join(line2))

        if line == height:
            print("".join(line3))


def fourtytwo(maze: dict[tuple[int, int], MazeBox]) -> dict[tuple[int, int],
                                                            MazeBox]:
    last_key = next(reversed(maze))
    width: int = maze[last_key].x
    height: int = maze[last_key].y
    center: MazeBox = maze.get((width // 2, height // 2))
    four: dict[tuple[int, int], MazeBox] = {}
    # four
    four[(center.x - 1, center.y)] = maze.get((center.x - 1, center.y))
    four[(center.x - 2, center.y)] = maze.get((center.x - 2, center.y))
    four[(center.x - 3, center.y)] = maze.get((center.x - 3, center.y))
    four[(center.x - 1, center.y + 1)] = maze.get((center.x - 1, center.y + 1))
    four[(center.x - 1, center.y + 2)] = maze.get((center.x - 1, center.y + 2))
    four[(center.x - 3, center.y - 1)] = maze.get((center.x - 3, center.y - 1))
    four[(center.x - 3, center.y - 2)] = maze.get((center.x - 3, center.y - 2))
    # two
    four[(center.x + 1, center.y)] = maze.get((center.x + 1, center.y))
    four[(center.x + 2, center.y)] = maze.get((center.x + 2, center.y))
    four[(center.x + 3, center.y)] = maze.get((center.x + 3, center.y))
    four[(center.x + 1, center.y + 1)] = maze.get((center.x + 1, center.y + 1))
    four[(center.x + 1, center.y + 2)] = maze.get((center.x + 1, center.y + 2))
    four[(center.x + 2, center.y + 2)] = maze.get((center.x + 2, center.y + 2))
    four[(center.x + 3, center.y + 2)] = maze.get((center.x + 3, center.y + 2))

    four[(center.x + 3, center.y - 1)] = maze.get((center.x + 3, center.y - 1))
    four[(center.x + 3, center.y - 2)] = maze.get((center.x + 3, center.y - 2))
    four[(center.x + 2, center.y - 2)] = maze.get((center.x + 2, center.y - 2))
    four[(center.x + 1, center.y - 2)] = maze.get((center.x + 1, center.y - 2))
    return four


def main(config_data: dict[str, str]) -> None:

    maze_board = create_maze_base(config_data)
    show_maze(maze_board, fourtytwo(maze_board))
    print("====MAZE GENERATOR====")
    print("1) Change color")
    print("2) new mazr")
    print("3) say hello")
    print("4) store maze")
    number = input("What you wanna do?")
    print(number)


if __name__ == "__main__":
    config_file: str = sys.argv[1]
    config_data: dict[str, str] = read_file(config_file)
    main(config_data)
