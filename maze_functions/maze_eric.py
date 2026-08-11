from typing import Any


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


def show_maze(maze_board: dict[tuple[int, int], MazeBox],
              fourty: dict[tuple[int, int], MazeBox]) -> None:
    last_key = next(reversed(maze_board))
    height: int = maze_board[last_key].y
    width: int = maze_board[last_key].x
    color1 = change_color()
    color2 = change_color()
    for line in range(height + 1):
        symbol: str = bg_square(color1[0], color1[1], color1[2])
        line1: list[str] = [symbol]
        line2: list[str] = [symbol]
        line3: list[str] = [symbol]
        """printfirst line"""
        for row in range(0, width + 1):
            line1.append(symbol) if maze_board.get(
                (row, line)) else line1.append("  ")
            line1.append(symbol)

            line2.append(bg_square(color2[0], color2[1], color2[2])) if (
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
