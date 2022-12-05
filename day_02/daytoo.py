

words = {
    "A": "rock",
    "B": "paper",
    "C": "scissor",
    "X": "rock",
    "Y": "paper",
    "Z": "scissor",
}

new_words = {
    "A": "rock",
    "B": "paper",
    "C": "scissor",
    "X": "lose",
    "Y": "draw",
    "Z": "win",
}

score_map = {
    "win": 6,
    "draw": 3,
    "lose": 0
}

shape_score = {
    "rock": 1,
    "paper": 2,
    "scissor": 3,
}

win_combo = [ ("rock","paper"), ("scissor","rock"), ("paper","scissor") ]


def convert (pair):
    """ for a combo, find out the names in english """
    return tuple(map(lambda x: words[x], pair.split(" ")))

def is_draw(combo):
    if "X" in combo or "Y" in combo or "Z" in combo:
        raise Exception("FUck u")
    return combo[0]==combo[1]

def is_win(combo):
    if "X" in combo or "Y" in combo or "Z" in combo:
        raise Exception("FUck u")
    return combo in win_combo

def get_score(combo):
    """Get scores with the old system"""
    score = 0
    if is_win(combo):
        score += score_map["win"]
    if is_draw(combo):
        score += score_map["draw"]
    score += shape_score[combo[1]] # add the shape score
    return score

def get_new_score(combo):
    """Get the scores, with the new system."""


def get_data(fname = "input.csv"):
    """get the data as an iterable"""
    with open(fname,"r") as fh:
        for line in fh:
            yield line.strip()


def get_total(data):
    return sum(
        map(
            lambda x: get_score(convert(x)),
            get_data()
            )
    )

if __name__ == "__main__":
    print(get_total(get_data()))