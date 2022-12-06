

test_data = """
            2-4,6-8
            2-3,4-5
            5-7,7-9
            2-8,3-7
            6-6,4-6
            2-6,4-8
            """


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


def acontainsb(a, b):
    """
    Check that range A contains range B

    >>> acontainsb("1-8","2-3")
    True

    >>> acontainsb("2-8","2-3")
    True

    >>> acontainsb("1-3","2-3")
    True

    >>> acontainsb("3-3","3-3")
    True

    >>> acontainsb("2-3","1-8")
    False

    >>> acontainsb("2-3","4-8")
    False

    >>> acontainsb("2-4","6-8") # Starting the test cases of the book.
    False

    >>> acontainsb("2-3","4-5")
    False

    >>> acontainsb("5-7","7-9")
    False

    >>> acontainsb("2-8","3-7")
    True

    >>> acontainsb("6-6","4-6")
    False

    >>> acontainsb("4-6","6-6")
    True

    >>> acontainsb("2-6","4-8")
    False

    >>> oneanother("4-8","2-6")
    False

    """
    #print(f"DEBUG: {a}   {b}   {b[-1]} ")
    return a[0] <= b[0] and a[-1] >= b[-1]


def oneanother(a, b):
    """
    Check that a contains b or b contains a

    >>> oneanother("1-8","2-3")
    True

    >>> oneanother("2-3","1-8")
    True

    >>> oneanother("2-3","4-8")
    False


    >>> oneanother("2-4","6-8") # Starting the test cases of the book.
    False

    >>> oneanother("2-3","4-5")
    False

    >>> oneanother("5-7","7-9")
    False

    >>> oneanother("2-8","3-7")
    True

    >>> oneanother("6-6","4-6")
    True

    >>> oneanother("2-6","4-8")
    False
    """
    return acontainsb(a, b) or acontainsb(b, a)


def part1(data=None):
    """
    Count how many assignment pairs contain one range within the other

    >>> part1(get_data(test_data=test_data))
    2

    """
    assert data is not None
    return len(list(
        filter(
            lambda x: x[1] is True,
            map(
                lambda x: (x, oneanother(x[0], x[1])),
                data
            ))))


def inside(n, b):
    """
    Check if it's inside

    >>> inside(7,(5,10))
    True

    >>> inside(2,(5,10))
    False

    >>> inside(5,(5,10))
    True

    >>> inside(10,(5,10))
    True

    """
    start = b[0]
    end = b[-1]
    return n >= start and n <= end


def overlap(a, b):
    """
    Check if 2 ranges have any overlap

    >>> overlap( (5,10),(15,100) )
    False

    >>> overlap( (5,10),(7,14) )
    True

    """
    # ranges overlap if one starts within the other.
    # Or if it ends within the other.
    # a to overlap, The start of a has to be bigger than start of b and smaller that it's end.
    # or
    # a to overlap, the end of a has to be bigger than the start of b and smaller that it's end.
    # OTHERWISE for
    # b to overlap, b has to start within A. it could be that a false, b true.
    # So we need to repeat in both directions.

    return inside(a[0], b) or inside(a[1], b) or inside(b[0], a) or inside(b[1], a)


def part2(data=None):
    """
    Count how many assigment pairs just Overlap. (one touches the other)

    >>> part2(get_data(test_data=test_data))
    4

    """
    assert data is not None
    return len(list(
        filter(
            lambda x: x[1] is True,
            map(
                lambda x: (x, overlap(x[0], x[1])),
                data
            )
        )))


if __name__ == "__main__":
    import doctest
    doctest.ELLIPSIS = True
    doctest.testmod()
    print("Results:")
    print("Part 1: ", part1(get_data()))
    print("Part 2: ", part2(get_data()))
