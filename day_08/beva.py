
title =     "\nDay 08 Part 1:"
total = sum(
        [
            not bool(
                [x for x in treeone[r][:c] if x >= treeone[r][c]]
                and [x for x in treeone[r][c + 1 :] if x >= treeone[r][c]]
                and [x[c] for i, x in enumerate(treeone) if x[c] >= treeone[r][c] and i < r]
                and [x[c] for i, x in enumerate(treeone) if x[c] >= treeone[r][c] and i > r]
            )
            for treeone in [[[int(y) for y in line] for line in open('input.csv').read().split("\n")]]
            for r in range(len(treeone))
            for c in range(len(treeone[r]))
        ]
    )

print(title, total)