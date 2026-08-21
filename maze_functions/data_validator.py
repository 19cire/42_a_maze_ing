from .file_reader import parse_coordinate


class SizeError(Exception):
    pass


class LessThanZeroError(Exception):
    pass


class OutOfBoundsError(Exception):
    pass


class PerfectError(Exception):
    pass


def check_data(data: dict[str, str]) -> None:

    width: int = int(data["WIDTH"])
    height: int = int(data["HEIGHT"])
    entry: tuple[int, int] = parse_coordinate(data["ENTRY"])
    maze_exit: tuple[int, int] = parse_coordinate(data["EXIT"])
    if width < 12 or height < 9:
        raise SizeError("The width and height must be greater than 10!")
    if min(*entry, *maze_exit) < 0:
        raise LessThanZeroError(
            "The Entry and Exit points must be greater than Zero")
    if any(x >= width or y >= height for x, y in (entry, maze_exit)):
        raise OutOfBoundsError(
            "The Entry and Exit points must be inside the Maze")
    if data["PERFECT"] not in ("True", "False"):
        raise PerfectError("The value of 'PERFECT' must be True or False")
