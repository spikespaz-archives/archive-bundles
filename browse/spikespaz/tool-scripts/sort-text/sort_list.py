def read_list(source):
    artists = []

    with open(source, "r") as fp:
        for line in fp.readlines():
            line = line.strip()

            if not line:
                continue

            if line.split(maxsplit=1)[0] == line[0] and line[0] in "!*-+":
                artists.append((line[0], line[1:].strip()))
            else:
                artists.append((None, line))

    return artists


def write_list(artists, dest):
    with open(dest, "w") as fp:
        for pair in artists:
            if pair[0]:
                fp.write(f"{pair[0]} {pair[1]}\n")
            else:
                fp.write(f"{pair[1]}\n")


if __name__ == "__main__":
    import sys

    from pathlib import Path

    SOURCE, DEST = Path(sys.argv[1]), Path(sys.argv[2])

    SORTED_ARTISTS = sorted(read_list(SOURCE), key=lambda x: x[1])

    write_list(SORTED_ARTISTS, DEST)
