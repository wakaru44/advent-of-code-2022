import daytoob as d


def test_sum():
    expect = 0
    result = 0

    if result != expect:
        print(f"FAIL. {result} but expected {expect}")
    else:
        print(".")


test_data = """A Y
    B X
    C Z"""


def get_data():
    """"return test data in a list"""
    clean = [l.strip() for l in test_data.split("\n")]
    return clean


def test_english():
    """check that we read english on the combo"""
    expect = ("rock", "draw")
    result = d.convert("A Y")
    if result != expect:
        print(f"FAIL. {result} but expected {expect}")
    else:
        print(".")


def test_myshape():
    """validate that we know our shape for a win-lose situation"""
    expect = "rock"
    result = d.get_shape(("paper", "lose"))
    assert expect == result
    if result != expect:
        print(f"FAIL. {result} but expected {expect}")
    else:
        print(".")


def test_score():
    """check the scores are correct with all test data"""
    for pair, expected in zip(get_data(), [4, 1, 7]):
        result = d.get_score(d.convert(pair))
        if result != expected:
            print(f"FAIL. {result} but expected {expected}")
        else:
            print(".")


if __name__ == "__main__":
    print("Testing:")
    test_english()
    test_myshape()
    test_score()
