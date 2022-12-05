from string import ascii_lowercase, ascii_uppercase


def split_pockets(rawsack):
    """ get a stripped line, return a tuple of rucksack"""
    half = int(len(rawsack)/2)
    return (rawsack[:half], rawsack[half:])


def get_data(fname="input.csv"):
    """Return the data in rucksacks"""
    with open(fname, "r") as fh:
        for line in fh:
            yield split_pockets(line.strip())


def find_common(rucksack):
    """Find the item that appears in both pockets"""
    pA = rucksack[0]
    pB = rucksack[1]
    assert type(pA) == type(".")
    assert type(pB) == type(".")
    assert type(rucksack) == type((1, 2))
    return set([item for item in pA if item in pB]).pop()


def get_prio(item):
    """Given an item type, return its priority int."""
    prios = ascii_lowercase+ascii_uppercase
    return prios.find(item)+1


def get_groups(data):
    group = []
    for elf in data:
        group.append(elf)
        if len(group) == 3:  # We got a group.
            yield group
            # Then reset, and start counting again.
            group = []
        else:
            continue


def find_badge(group):
    """Given a group of sacks, find the common stuff."""
    e1 = group[0]
    e2 = group[1]
    e3 = group[2]

    s1 = set("".join(e1))
    s2 = set("".join(e2))
    s3 = set("".join(e3))

    # Get the intersection of A|B, then that against C.
    intsec1 = s1.intersection(s2)
    intsec2 = intsec1.intersection(s3)

    return intsec2.pop()


def part1():
    return sum(
            map(
                lambda x: get_prio(find_common(x)),
                get_data()
            )
        )

def part2():
    """Calculate the total of the prio of each group badge"""
    return sum(
        map(
            lambda x: get_prio(find_badge(x)),
            get_groups(get_data())
        )
    )

if __name__ == "__main__":
    print("Part 1")
    print(part1())
    print("Part 2")
    print(part2())
    
