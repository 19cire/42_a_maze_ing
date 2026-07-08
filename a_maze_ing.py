#!/usr/bin/python3

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

def create_maze(width: int, height: int) -> list[list[list[int]]]:
    """Create a 2D maze grid initialized with walls.

    Args:
        width: Number of columns.
        height: Number of rows.

    Returns:
        2D list where each cell is [top, right, bottom, left] wall flags.
    """
    return [[[1, 1, 1, 1] for _ in range(width)] for _ in range(height)]

if __name__ == "__main__":
    maze_data = read_file("config.txt")
    maze = create_maze(int(maze_data['WIDTH']), int(maze_data['HEIGHT']))
    for key, value in maze_data.items():
        print(f"{key} = {value}")


    for line in maze:
        top = ""
        mid = ""
        bottom = ""
        for point in line:
            top +=  "+" + ("--" if point[0] else "")
            mid += ("|" if point[3] else " ") + "XO"
        
        print(top + "+") 
        print(mid + "|" if point[1] else " ")

        # for point in line:
        #     bottom +=  "+" + ("--" if point[2] else "  ")

        # print( bottom + "+")
