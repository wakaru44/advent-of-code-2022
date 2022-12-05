

import dayone as d


def test_importing():
    expect = 265
    result = len(d.get_input())
    if result != expect:
        print (f"FAIL. {result} but expected {expect}")
    else:
        print(".")

def test_sumup():
    expect = 6
    result = d.sumup([1,2,3])
    if result != expect:
        print (f"FAIL. {result} but expected {expect}")
    else:
        print(".")

def test_top3():
    expect = [7,8,9] # Because seven ate nine
    result = d.top3([9,8,7,1,2,3])
    if result != expect:
        print (f"FAIL. {result} but expected {expect}")
    else:
        print(".")


if __name__ == "__main__":
    test_importing()
    test_sumup()
    test_top3()