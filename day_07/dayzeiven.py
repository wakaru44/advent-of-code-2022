import itertools

test_data = """
$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
"""


def get_data(fname="input.csv", test_data=None):
    """
    Load the file, and process the data a little bit.
    Return Just the lines.

    >>> get_data(test_data=test_data).__next__()   # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    '$ cd /'


    """
    if test_data is not None:
        it = test_data.split("\n")
    else:
        it = open(fname, "r")
    for line in it:
        cline = line.strip()
        if cline != '':  # if the line is empty, ignore it.
            try:
                yield cline
            except ValueError as e:
                print(f"FUCK {e}")
                print("cline:", cline)
        else:
            continue
    if test_data is None:
        it.close()  # we are not using with, so we must close manually.


def get_command(data):
    """
    Given a stream of data, pull the next command with it's output."""
    command = list(itertools.islice(data, 1))  # get the first command.
    output = None
    previous = None
    for next in data:
        # take the next command, if it's output, put it together.
        if previous is not None:
            # The previous command was also a command, s oit goes on the next output.
            command = [previous]
            previous = None  # and we reset the previous holder.
        if next.startswith('$'):
            # then it's a command, not output. save it for later, and return the lot.
            previous = next
            yield command
            command = []  # reset just in case? sholud reset in the prev. if.
        else:
            # Then it's output, should be appended.
            command.append(next)
    # print ("OH SHIT") # Should we even get here? yes, is natural.


def process_ls(output, tree=None, curs=None):
    """
    Given the output of an ls command, build the tree.

   # >>> tree = {'root': {'files':[],'dirs':{}}}
    #>>> process_ls(['$ ls','123 foo'], tree)
    {"root":[(123,'foo')]}

    """
    assert tree is not None  # We need the tree, otherwise we can't do anything.
    assert curs is not None  # We need the cursor to see where we are.
    # return a dict with the folders as keys, files as tuples with size, dirs as tuples with no size.
    for entry in output[1:]:
        if entry.startswith('dir'):
            add_dir(entry, tree)
        else:
            add_file(entry, tree)

    return tree


def insert_entry(curs, tree):
    """ Insert an entry inside a tree??"""
    return tree


def add_file(entry, tree):
    """
    Given the curretn branch, add a file to it.

    >>> tree = {'root': {'files':[],'dirs':{}}}
    >>> tree['root'] = add_dir('foo',tree['root'])
    >>> tree
    {'root': {'files': [], 'dirs': {'foo': {'files': [], 'dirs': {}}}}}
    >>> tree['root']['dirs']['foo'] = add_file('1234 bar',tree['root']['dirs']['foo'])
    >>> tree
    {'root': {'files': [], 'dirs': {'foo': {'files': ['1234 bar'], 'dirs': {}}}}}

    """
    tree['files'].append(entry)
    return tree


def add_dir(entry, tree):
    """
    Given the current branch of the tree, return the branch with a new dir.

    >>> tree = {'root': {'files':[],'dirs':{}}}
    >>> tree['root'] = add_dir('foo',tree['root'])
    >>> tree
    {'root': {'files': [], 'dirs': {'foo': {'files': [], 'dirs': {}}}}}

    """
    tree['dirs'][entry] = {'files': [], 'dirs': {}}
    return tree


def part1(data):
    pass


def part2(data):
    pass


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    print("Results:")
    print(part1(get_data()))
    print(part2(get_data()))
