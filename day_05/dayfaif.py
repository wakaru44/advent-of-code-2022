

test_data = "move 99 from 9 to 9"

test_moves = """
             move 1 from 2 to 1
             move 3 from 1 to 3
             move 2 from 2 to 1
             move 1 from 1 to 2
             """

test_stack = """
    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 
"""

index = " 1   2   3   4   5   6   7   8   9 "


def get_col(col, index=index):
    """
    Get the position where the column number col is located

    >>> get_col(1)
    1

    """
    return index.find(str(col))


def get_stack(fname="input_stack.csv", test_data=None):
    """ transpose the stack, clean it, make it nice.

    >>> get_stack(test_data=test_stack)
    {1: [' ', 'N', 'Z'], 2: ['D', 'C', 'M'], 3: [' ', ' ', 'P']}

    """
    raw = read_stack(fname, test_data)
    trans = transpose(raw)
    # transpose is not enough, we have to retrieve only the good stuff
    stack = {}
    for i in range(1, 10):  # numbers 1 to 9
        try:
            stack[i] = trans[get_col(i)]
        except IndexError:
            pass  # We can ignore stacks that are too small for our index.
    return stack


def read_stack(fname="input_stack.csv", test_data=None):
    """
    Load the stack matrix. from the file

    >>> read_stack(test_data=test_stack)
    ['    [D]    ', '[N] [C]    ', '[Z] [M] [P]']

    """
    if test_data is not None:
        it = test_data.split("\n")
    else:
        it = open(fname, "r")

    stack = []  # The stack is a list of lists.
    index = ""  # The index is then a string? or can it be a list?

    for line in it:
        # cline = line.strip() # In this case, it can't be stripped of the whitespaces.
        cline = line.replace("\n", "")  # just remove them manually.
        # If is the index, put it in the index
        if cline.startswith(" 1") or "1" in cline:
            index = cline
        # if the line is empty, ignore it.
        elif cline != '':
            stack.append(cline)
        else:
            continue
    if test_data is None:
        it.close()  # we are not using with, so we must close manually.
    return stack


def encode_moves(line):
    """Get a line of moves and encode them in a tuple

    >>> encode_moves('move 1 from 2 to 1')
    {'move': 1, 'src': 2, 'dst': 1}

    >>> encode_moves('move 11 from 9 to 11')
    {'move': 11, 'src': 9, 'dst': 11}
    """

    trozos = line.split(" ")
    encoded = {
        'move': int(trozos[1]),
        'src':  int(trozos[3]),
        'dst':  int(trozos[5])
    }
    return encoded


def get_moves(fname="input_moves.csv", test_data=None):
    """
    Load the file, and process the data a little bit.

    >>> get_moves(test_data=test_data).__next__()   # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    {'move': 99, 'src': 9, 'dst': 9}

    >>> get_moves(test_data=test_moves).__next__()   # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    {'move': 1, 'src': 2, 'dst': 1}


    """
    if test_data is not None:
        it = test_data.split("\n")
    else:
        it = open(fname, "r")
    for line in it:
        cline = line.strip()
        if cline != '':  # if the line is empty, ignore it.
            try:
                yield encode_moves(cline)
            except ValueError as e:
                print("FUCK {e}")
                print(cline)
        else:
            continue
    if test_data is None:
        it.close()  # we are not using with, so we must close manually.


def transpose(matrix):
    """
    Transpose a list of lists.

    >>> transpose([[1,2],[3,4],[5,6]])
    [[1, 3, 5], [2, 4, 6]]
    """
    return list(map(list, zip(*matrix)))


def take_one(col, st="WTF"):
    """
    get the top item on this column. return a tuple of the item and the new stack

    >>> take_one(2, get_stack(test_data=test_stack) )
    ('D', {1: [' ', 'N', 'Z'], 2: [' ', 'C', 'M'], 3: [' ', ' ', 'P']})

    """
    assert st is not None
    hand = ''
    for pos, item in enumerate(st[col]):
        if item == ' ':  # the item is empty, go on to the next pos.
            continue
        else:  # the item is 'something', so we must take it out.
            hand = item
            st[col][pos] = ' '
            # and we are done
            return (hand, st)
    #print(f"DEBUG: {st} - {col}")
    print("OOPSIETAKE")  # we should never get here.


def put_one(col, hand, stack=None):
    """
    Put one item from the hand to the stack

    >>> st = get_stack(test_data=test_stack)
    >>> (hand,st) = take_one(2,st)
    >>> put_one(2,hand,st)
    {1: [' ', 'N', 'Z'], 2: ['D', 'C', 'M'], 3: [' ', ' ', 'P']}

    """
    assert stack is not None
    # print("DEBUG STACK ",stack) # FIXED: the stack was created with just 8.
    for pos, item in enumerate(stack[col]):
        if item == ' ':  # we don't care about empty
            continue
        else:  # The first one we hit, we do the did.
            if pos == 0:  # If we need to enlarge the pile
                stack[col].insert(0, hand)
            else:
                prev = pos-1
                stack[col][prev] = hand
            return stack
    # If we get here, means we are at the end of the pile.
    # append to the end and return the stack.
    stack[col].append(hand)
    return stack


def do_move(order, stack=None):
    """
    Perform the operations for a given move.

    >>> st = get_stack(test_data=test_stack)
    >>> do_move({'move':1, 'src': 2, 'dst':1},st)
    {1: ['D', 'N', 'Z'], 2: [' ', 'C', 'M'], 3: [' ', ' ', 'P']}

    >>> st = get_stack(test_data=test_stack)
    >>> moves = list(get_moves(test_data=test_moves))
    >>> do_move(moves[0],st)
    {1: ['D', 'N', 'Z'], 2: [' ', 'C', 'M'], 3: [' ', ' ', 'P']}

    >>> st = get_stack(test_data=test_stack)
    >>> moves = list(get_moves(test_data=test_moves))
    >>> st2 = do_move(moves[0],st)
    >>> do_move(moves[1],st2)
    {1: [' ', ' ', ' '], 2: [' ', 'C', 'M'], 3: ['Z', 'N', 'D', 'P']}

    >>> st = get_stack(test_data=test_stack)
    >>> moves = list(get_moves(test_data=test_moves))
    >>> st = do_move(moves[0],st)
    >>> st = do_move(moves[1],st)
    >>> #print(st)
    >>> do_move(moves[2],st)
    {1: [' ', ' ', 'M', 'C'], 2: [' ', ' ', ' '], 3: ['Z', 'N', 'D', 'P']}


    """
    assert stack is not None

    for n in range(order['move']):
        # print("DEBUGIOE",n, order['move']) # DAMAGE: I fucked up and returend too early.
        try:
            (hand, stack) = take_one(order['src'], stack)
            stack = put_one(order['dst'], hand, stack)
        except TypeError as e:
            print(f"DEBUG: {stack} - {order}")
            print(e)
            raise TypeError(e)
        except AssertionError as e:
            # Catch the assertions of put and take to debug.
            print(f"DEBUGAS: {stack} - {order}")
            print(e)
            #raise AssertionError(e)
    return stack  # Return the stack as it is updated.


def untranspose(stack):
    r"""
    un transpose the stack back into a vertical pile

    >>> untranspose({1:[1,2,3],2:[4,5,6]})
    [[1,2,3],[4,5,6]]

    >>> st = get_stack(test_data=test_stack)
    >>> untranspose(st)
    ' [ ] [D] [ ]\n [N] [C] [ ]\n [Z] [M] [P]'
    """
    horizontal = []
    for k, v in stack.items():
        horizontal.append(list(map(
            lambda x: f" [{x}]",
            v
        )))
    vertical = transpose(horizontal)
    return "\n".join(["".join(y) for y in vertical])


def part1(data=None):
    """Run all the moves through the stack"""
    stack = get_stack()
    print("Before")
    print(untranspose(stack))
    moves = get_moves()
    for move in moves:
        stack = do_move(move, stack)
    print("After")
    print(untranspose(stack))
    return "Nice"


def part2(data=None):
    pass


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    print("Results:")
    print(part1(get_moves()))
    print(part2(get_moves()))
