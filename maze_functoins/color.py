import numpy as np


def bg_square(r: int, g: int, b: int) -> str:
    return f"\033[48;2;{r};{g};{b}m  \033[0m"


def change_color() -> None:
    color = np.random.randit(0, 256, size=3)
    print(color)
