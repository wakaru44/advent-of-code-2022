import daytoo as d

def test_sum():
    expect = 0
    result = 0

    if result != expect:
        print (f"FAIL. {result} but expected {expect}")
    else:
        print(".")

test_data = """A Y
    B X
    C Z"""

def get_data():
    """"return test data in a list"""
    clean =  [ l.strip() for l in test_data.split("\n") ]
    return clean

def test_english():
    """check that we read english on the combo"""
    expect = ("rock","paper")
    result = d.convert("A Y")

    if result != expect:
        print (f"FAIL. {result} but expected {expect}")
    else:
        print(".")

def test_draw():
    """check that we read english on the combo"""
    expect = ("rock","rock")
    result = d.convert("A X")

    if result != expect:
        print (f"FAIL. {result} but expected {expect}")
    else:
        print(".")

def test_draw_not():
    """validate that we don't process bad data"""
    try:
        d.is_draw("A Y")
    except Exception:
        print(".")

def test_score():
    """check the scores are correct with all test data"""
    for pair in get_data():
        result = d.get_score(d.convert(pair))
        print(result)

def test_iswin():
    """validate that we register a win"""
    for pair in get_data():
        result = d.is_win(d.convert(pair))
        print(result)

    
if __name__ == "__main__":
    print("Testing:")
    test_english()
    test_draw()
    test_score()
    test_draw_not()
    test_iswin()
