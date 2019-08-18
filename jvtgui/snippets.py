# This is a file for code that is not my own. The source of the snippet will be commented
# above the symbol(s), snippets from the same source will be adjacent.

# Human-readable data size units by Fred Cirera.
# Modified for Python 3 and to use proper units in accordance to this:
# https://en.wikipedia.org/wiki/Binary_prefix#Inconsistent_use_of_units
# https://web.archive.org/web/20111010015624/http://blogmag.net/blog/read/38/Print_human_readable_file_size


def sizeof_fmt(num, suffix="B"):
    for unit in ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]:
        if abs(num) < 1024.0:
            return f"{num:3.1f} {unit}{suffix}"

        num /= 1024.0

    return "{num:.1f} Yi{suffix}"
