


test_data = ""


def get_data(fname="input.csv", test_data=None):
    """
    Load the file, and process the data a little bit.

    >>> get_data(test_data=test_data).__next__()   # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    ((2, 4), (6, 8))


    """
    if test_data is not None:
        it = test_data.split("\n")
    else:
        it = open(fname, "r")
    for line in it:
        cline = line.strip()
        if cline != '':  # if the line is empty, ignore it.
            try:
                yield tuple(
                    map(
                        lambda x: tuple(map(int, x.split("-"))),
                        cline.split(",")
                    )
                )
            except ValueError as e:
                print("FUCK {e}")
                print(cline)
        else:
            continue
    if test_data is None:
        it.close()  # we are not using with, so we must close manually.


def part1():
    pass


def part2():
    pass


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    print("Results:")
    print(part1(get_data()))
    print(part2(get_data()))
