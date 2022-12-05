


def get_input():
    """
    Load the input file into a list of lists
    """
    with open("input.csv","r") as fh:
        data = []
        anelf = []

        for line in fh.readlines():
            if line.strip() == "":
                # Start a new elf.
                data.append(anelf)
                anelf = []
            else:
                anelf.append(int(line.strip()))

    return data


def sumup( numbers ):
    """ Get a list of numbers, return the sum"""
    return sum(numbers)


def totals(elves):
    """sum up the totals"""
    return map(sum,elves)

def top3 (elves):
    """
    Find the top 3 elves consuming the most food
    """
    return sorted(elves)[-3:]


if __name__ == "__main__":
    data = get_input()
    print(max(totals( data )))

    print(sum(top3(totals(data))))