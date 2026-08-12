

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
    except (FileNotFoundError, IndexError) as e:
        print(f"{e.__class__.__name__}: {e}")
    return data
