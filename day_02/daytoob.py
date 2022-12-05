

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

win_combo = {
    "rock": "paper",
    "scissor": "rock",
    "paper": "scissor"
}

# The losing combo for a given shape
lose_combo = {
    "rock": "scissor",
    "scissor": "paper",
    "paper": "rock"
}


def convert(pair):
    """ for a combo, find out the names in english """
    return tuple(map(lambda x: new_words[x], pair.split(" ")))


def get_shape(combo):
    """Return my shape for a given combo"""
    her_shape = combo[0]
    result = combo[1]
    if result=="win":
        return win_combo[her_shape]
    elif result == "draw":
        return her_shape
    else:
        return lose_combo[her_shape]

def get_score(combo):
    """Get scores with the old system"""
    score = 0
    result = combo[1]
    score += score_map[result]
    score += shape_score[get_shape(combo)]  # add the shape score
    return score


def get_data(fname="input.csv"):
    """get the data as an iterable"""
    with open(fname, "r") as fh:
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
