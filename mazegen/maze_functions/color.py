import numpy as np


def bg_square(color_index: int) -> str:
    return f"\033[48;5;{color_index}m  \033[0m"


def change_color() -> int:
    color: int = np.random.randint(0, 256)
    return (color)
