

test_data = """30373
25512
65332
33549
35390
"""


def get_data(fname="input.csv", test_data=None):
    """
    Today the data is just one big matrix

    >>> get_data(test_data=test_data)   # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    [['3', '0', '3', '7', '3'], ['2', '5', '5', '1', '2'], ['6', '5', '3', '3', '2'], ['3', '3', '5', '4', '9'], ['3', '5', '3', '9', '0']]

    """
    if test_data is not None:
        it = test_data.split("\n")
    else:
        it = open(fname, "r")
    matrix = []
    for line in it:
        cline = line.strip()
        if cline != '':  # if the line is empty, ignore it.
            try:
                matrix.append(list(cline))
            except ValueError as e:
                print("FUCK {e}")
                print(cline)
        else:
            continue
    if test_data is None:
        it.close()  # we are not using with, so we must close manually.
    return matrix


def check_eastwest(pos, line):
    """
    Validate that the tree can be seen east or west of it

    >>> check_eastwest((0,0), '011')
    True

    >>> check_eastwest((0,2), '011')
    True

    >>> check_eastwest((1,99), '33549')
    False

    >>> check_eastwest((3,99), '33549')
    False

    >>> check_eastwest((1,99), '71349')
    False

    >>> check_eastwest((3,99), '25512')
    False

    """
    x = pos[0]
    y = pos[1]
    east = line[:x]
    west = line[x+1:]
    tree = int(line[x])
    if x == 0 or y == 0:
        return True  # In the border is visible
    if y == 98:
        # print("bingY",pos)
        return True  # In the border is visible
    if x == len(line)-1:
        # print("bingx",pos)
        return True
    bigger_east = False
    bigger_west = False
    for other in east:
        if int(other) >= tree:
            bigger_east = True
    for other in west:
        if int(other) >= tree:
            bigger_west = True
    return not bigger_east or not bigger_west


def transpose(matrix):
    """ do that

    >>> transpose([[1,2],[3,4]])
    [[1, 3], [2, 4]]
    """
    return list(map(list, zip(*matrix)))


def is_visible(pos, forest):
    """ with a tuple of x,y position, and a forest, find if a tree is visible

    >>> forest = get_data(test_data=test_data)
    >>> is_visible( (0,1) ,forest)
    True

    >>> forest = get_data(test_data=test_data)
    >>> is_visible( (1,1) ,forest)
    True

    >>> forest = get_data(test_data=test_data)
    >>> is_visible( (1,4) ,forest)
    True

    >>> forest = get_data(test_data=test_data)
    >>> is_visible( (2,2) ,forest)
    False

    >>> forest = get_data(test_data=test_data)
    >>> is_visible( (3,3) ,forest)
    False

    >>> forest = get_data(test_data=test_data)
    >>> is_visible( (4,4) ,forest)
    True

    >>> forest = get_data(test_data=test_data)
    >>> is_visible( (1,3) ,forest)
    False

    >>> forest = get_data(test_data=test_data)
    >>> for y in range(5):
    ...     for x in range(5):
    ...         vis = is_visible((x,y),forest)
    ...         if not vis:
    ...             print("Not visible: ", (x,y))
    Not visible:  (2, 2)
    Not visible:  (1, 3)
    Not visible:  (3, 3)
    Not visible:  (3, 1)
    """
    # first we should check east
    x = pos[0]
    y = pos[1]
    line = forest[y]
    east = check_eastwest(pos, line)

    # Then we can transpose the matrix, transpose our position, read again.
    tran_forest = transpose(forest)
    tx = y
    ty = x
    line = tran_forest[y]
    south = check_eastwest((tx, ty), line)

    return east or south


def part1(forest):
    """
    count the numebr of trees visible from outside the thing.

    >>> forest = get_data(test_data=test_data)   # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    >>> part1(forest)
    21

    >>> forest = [['3', '0', '3', '7', '3'], ['2', '0', '0', '0', '2'], ['6', '0', '0', '0', '2'], ['3', '0', '0', '0', '9'], ['3', '5', '3', '9', '0']]
    >>> part1(forest)
    16

    >>> forest = [['1', '1', '1'], ['1', '1', '1'], ['1', '1', '1']]
    >>> part1(forest)
    8

    >>> forest = get_data()
    >>> part1(forest)
    1782

    """
    count = 0
    for y, line in enumerate(forest):
        for x, tree in enumerate(line):
            count += 1*is_visible((x, y), forest)
    return count


def paint(forest):
    """
    Paint the forest mask on screen. seen is a x unseen is a .

    >>> forest = [['1', '1', '1'], ['1', '1', '1'], ['1', '1', '1']]
    >>> paint(forest)
    xxx
    x.x
    xxx

    >>> forest = [['3', '0', '3', '7', '3'], ['2', '5', '5', '1', '2'], ['6', '5', '3', '3', '2'], ['3', '3', '5', '4', '9'], ['3', '5', '3', '9', '0']]
    >>> paint(forest)
    xxxxx
    xxx.x
    xx.xx
    x.x.x
    xxxxx
    """
    for y, line in enumerate(forest):
        output = ""
        for x, tree in enumerate(line):
            if is_visible((x, y), forest):
                output += "x"  # tree
            else:
                output += "."
        print(output)
    return None


def part2(forest):
    pass


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    print("Results:")
    print(part1(get_data()))
    print(part2(get_data()))
