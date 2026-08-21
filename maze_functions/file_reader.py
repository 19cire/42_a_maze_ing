def read_file(file: str) -> dict[str, str]:
    data: dict[str, str] = {}
    try:
        with open(file, "r") as f:
            for line in f:
                line = line.strip()
                value = line.split("=")
                data[value[0]] = value[1]
    except (FileNotFoundError, IndexError) as e:
        print(f"{e.__class__.__name__}: {e}")
    return data


def parse_coordinate(value: str) -> tuple[int, int]:
    parts = value.split(",")
    return (int(parts[0]), int(parts[1]))
