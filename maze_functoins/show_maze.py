from maze_functoins.color import bg_square
from .variables import NORTH, EAST, SOUTH


def maze_viewer(grid: list[list[int]], color: list[int],
                entry: tuple[int], exit: tuple[int]) -> None:
    symbol: str = bg_square(color[0], color[1], color[2])
    count_x: int = 0
    count_y: int = 0
    for x in grid:
        line1: list[str] = [symbol]
        line2: list[str] = [symbol, "  "]
        line3: list[str] = [symbol]
        count_y = 0
        for y in x:
            line1.append(symbol if y & NORTH else "  ")
            line1.append(symbol)
            line2.append(symbol if y & EAST else "  ")
            if entry == (count_x, count_y):
                line2.append("🟢")
            elif exit == (count_x, count_y):
                line2.append("🏆")
            else:
                line2.append("  ")
            line3.append(symbol if y & SOUTH else "  ")
            line3.append(symbol)
            count_y += 1

        print("".join(line1))
        print("".join(line2))
        count_x += 1
    print("".join(line3))


def clear_screen() -> None:
    print("\033[H\033[J", end="")
