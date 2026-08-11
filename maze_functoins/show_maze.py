from maze_functoins.color import change_color, bg_square
from maze_functoins.mazegen import NORTH, EAST, SOUTH


def maze_viewer(grid: list[list[int]]) -> None:
    color1 = change_color()
    symbol: str = bg_square(color1[0], color1[1], color1[2])
    for x in grid:
        line1: list[str] = [symbol]
        line2: list[str] = [symbol, "  "]
        line3: list[str] = [symbol]

        for y in x:
            line1.append(symbol if y & NORTH else "  ")
            line1.append(symbol)
            line2.append(symbol if y & EAST else "  ")
            line2.append("  ")
            line3.append(symbol if y & SOUTH else "  ")
            line3.append(symbol)

        print("".join(line1))
        print("".join(line2))
    print("".join(line3))
