function compareVersions(firstVer, secondVer) {
    let first = firstVer.split(".");
    let second = secondVer.split(".");

    while (first.length > second.length) {
        if (first[0] != 0)
            return true;

        first.shift();
    }

    while (second.length > first.length) {
        if (second[0] != 0)
            return false;

        second.shift();
    }

    for (parts of first.map((item, index) => [item, second[index]])) {
        if (parts[0] > parts[1])
            return true;
        else if (parts[1] > parts[0])
            return false;
    }

    return false;
}
