
import daytree as d

def test_base():
    """
    test
    """
    pass


test_data = """vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw
"""

def get_data(test_data=test_data):
    """return the data in rucksacks"""
    for l in test_data.split("\n"):
        yield d.split_pockets(l)

def test_split():
    """validate we split half of a rucksack"""
    pa,pb = d.split_pockets("vJrwpWtwJgWrhcsFMMfFFhFp")
    if len(pa) == len(pb):
        print(".")
    else:
        print(f"FAIL: {pa},{pb}")

def test_splits():
    for rucksack in get_data(test_data):
        assert len(rucksack[1]) == len(rucksack[0])
        
def validate_findcommon(rucksack, expected):
    """Validate that we can find the common elem."""
    result = d.find_common(rucksack)
    if result == expected:
        print(".")
    else:
        print(f"FAIL: {result}")

def test_findcommon():
    """validate all of them inputs"""
    validate_findcommon(("vJrwpWtwJgWr","hcsFMMfFFhFp"),"p")
    expectations = ["p","L","P","v","t","s"]
    for rucksack,expected in zip(get_data(test_data),expectations):
        validate_findcommon(rucksack,expected)

def validate_getprio(item, expected):
    """validate one prio"""
    result = d.get_prio(item)
    if result == expected:
        print(".")
    else:
        print(f"FAIL: {result} instead of {expected}")

def test_getprio():
    """run al the tests"""
    inputs = ["p","L","P","v","t","s"]
    expectations = [16,38,42,22,20,19]
    for rucksack,expected in zip(inputs,expectations):
        validate_getprio(rucksack,expected)


def test_get_grroups():
    """check we got a couple groups"""
    result = list(d.get_groups(get_data()))
    assert len(result) == 2

def valid_findbadge(group,expected):
    """can we find the badge?"""
    result = d.find_badge(group)
    if result == expected:
        print(",")
    else:
        print(f"FAIL: {result} instead of {expected}")

def test_findbadge():
    """Run all the findbadges"""
    expectations = ["r","Z"]
    #expectations = [18,52]
    inputs = d.get_groups(get_data())
    for input,expectation in zip(inputs,expectations):
        valid_findbadge(input, expectation)



if __name__ == "__main__":
    print("Testing")
    test_split()
    test_splits()
    test_findcommon()
    test_getprio()
    test_get_grroups()
    test_findbadge()
