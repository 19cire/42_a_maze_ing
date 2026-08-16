from maze_functions.color import bg_square
from .variables import NORTH, EAST, SOUTH


def clear_screen() -> None:
    print("\033[H\033[J", end="")


def maze_viewer(grid: list[list[int]],
                entry: tuple[int],
                exit: tuple[int],
                color: int = 42,
                path: list[tuple[int,  int]] | None = None
                ) -> None:
    clear_screen()
    symbol: str = bg_square(color)
    count_x: int = 0
    count_y: int = 0
    for x in grid:
        line1: list[str] = [symbol]
        line2: list[str] = [symbol]
        line3: list[str] = [symbol]
        count_y = 0
        for y in x:
            line1.append(symbol if y & NORTH else "  ")
            line1.append(symbol)
            if entry == (count_y, count_x):
                line2.append("😄")
            elif exit == (count_y, count_x):
                line2.append("🥳")
            elif path and (count_y, count_x) in path[1:-1]:
                line2.append("🐠")
            else:
                line2.append("  ")
            line2.append(symbol if y & EAST else "  ")
            line3.append(symbol if y & SOUTH else "  ")
            line3.append(symbol)
            count_y += 1

        print("".join(line1))
        print("".join(line2))
        count_x += 1
    print("".join(line3))
