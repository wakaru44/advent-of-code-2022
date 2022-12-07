
import itertools

test_data = "mjqjpqmgbljsphdztnvjfqwrcgsmlb"

p1_test_cases = [
    (7, test_data,),
    (5, "bvwbjplbgvbhsrlpgdmjqwftvncz",),
    (6, "nppdvjthqldpwncqszvftbrmjlhg",),
    (10, "nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg",),
    (11, "zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw")
]

p2_test_cases = [
    (19, test_data,),
    (23, "bvwbjplbgvbhsrlpgdmjqwftvncz",),
    (23, "nppdvjthqldpwncqszvftbrmjlhg",),
    (29, "nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg",),
    (26, "zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw")
]


def get_data(fname="input.csv", test_data=None):
    """
    Load the file, and process the data a little bit.

    >>> get_data(test_data=test_data).__next__()   # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    'm'

    """
    if test_data is not None:
        it = test_data.split("\n")
    else:
        it = open(fname, "r")
    for line in it:
        cline = line.strip()
        if cline != '':  # if the line is empty, ignore it.
            try:
                for c in cline:
                    yield c
            except ValueError as e:
                print("FUCK {e}")
                print(cline)
        else:
            continue
    if test_data is None:
        it.close()  # we are not using with, so we must close manually.


def are_uniq(chars, t_size=4):
    """
    Verify that the 4 chares passed are unique, and actually t_size of them.

    >>> are_uniq('abcd')
    True

    >>> are_uniq('aabcd')
    False

    """
    #print("FUCK",chars)
    if len(chars) != t_size:
        raise ValueError("Chars too short")
    return len(list(set(chars))) == len(chars)


def digest(data, t_size=4):
    """
    Process the stream

    >>> digest(iter('aaoeutn'))
    5

    >>> for expect,input in p1_test_cases:
    ...    result = digest(iter(input))
    ...    if result != expect:
    ...        print(expect,result,input)

    >>> for expect,input in p2_test_cases:
    ...    result = digest(iter(input), t_size=14)
    ...    if result != expect:
    ...        print(expect,result,input)

    """
    success = False
    readed = list(itertools.islice(data, t_size))
    for c in data:
        if not success:
            readed.append(c)
        if are_uniq(readed[-t_size:], t_size):
            success = True
            break
    return len(readed)


def part1(data):
    return (digest(data))


def part2(data):
    return (digest(data,t_size=14))


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    print("Results:")
    print(part1(get_data()))
    print(part2(get_data()))
