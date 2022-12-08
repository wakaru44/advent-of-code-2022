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
        lista = test_data.split('\n')
        it = itertools.islice(lista, len(lista))
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
    Given a stream of data, pull the next command with it's output.

    >>> commands = list(get_command(get_data(test_data=test_data)))
    >>> len(commands)
    10
    """
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
    # and we should yield the last and final command
    yield command


def process_ls(cur=None, command=None, tree=None):
    """
    Given the output of an ls command, build the tree.

    >>> tree = {'root': ['dir a'], 'root.a': []}
    >>> commands = list(get_command(get_data(test_data=test_data)))
    >>> len(commands)
    10
    >>> command = ['$ ls','dir b','12313 foo.txt']
    >>> process_ls('root', command, tree)
    ('root', {'root': ['dir a', 'dir b', '12313 foo.txt'], 'root.a': [], 'root.b': []})
    """

    # We need the tree, otherwise we can't do anything.
    assert tree is not None
    assert cur is not None  # We need the cursor to see where we are.
    for entry in command[1:]:
        if entry.startswith('dir'):
            tree = add_dir(cur, entry, tree)
        else:
            tree = add_file(cur, entry, tree)
    return (cur, tree)


def process_cd(cur=None, command=None, tree=None):
    """
    Given a CD command, figure out what to do.

    >>> tree = {'root': ['dir a'], 'root.a': []}
    >>> process_cd('root',['cd a'], tree)
    ('root.a', {'root': ['dir a'], 'root.a': []})

    >>> tree = {'root': ['dir a'], 'root.a': []}
    >>> process_cd('root.a',['cd ..'], tree)
    ('root', {'root': ['dir a'], 'root.a': []})

    >>> tree = {'root': ['dir a'], 'root.a': []}
    >>> process_cd('root.a.b.c',['cd /'], tree)
    ('root', {'root': ['dir a'], 'root.a': []})
    """
    dest = command[0].split(' ').pop()
    #print("DEBUG CD",command)
    #print("DEBUG CD",dest)
    if dest == '..' or dest == '/':
        cur = cd_outof(cur, dest, tree)
    else:
        cur = cd_into(cur, dest, tree)
    return (cur, tree)


def cd_into(cur=None, target=None, tree=None):
    """
    Given the output of a cd command, update the cursor to it.

    >>> tree = {'root': []}
    >>> tree = add_dir('root','a',tree)
    >>> cd_into('root', 'a', tree)
    'root.a'
    """
    return cur+'.' + target


def cd_outof(cur=None, target=None, tree=None):
    """
    Get out of this folder, to root or previous.

    >>> tree = {'root': []}
    >>> tree = add_dir('root','dir a',tree)
    >>> cd_outof('root.a', '..', tree)
    'root'

    >>> tree = {'root': []}
    >>> tree = add_dir('root','dir a',tree)
    >>> cd_outof('root', '..', tree)
    'root'

    >>> tree = {'root': []}
    >>> tree = add_dir('root','dir a',tree)
    >>> cd_outof('root.a.b.c', '..', tree)
    'root.a.b'

    >>> tree = {'root': []}
    >>> tree = add_dir('root','dir a',tree)
    >>> cd_outof('root.a.b.c', '/', tree)
    'root'
    """
    # check we don't go further than root.
    # check that / takes us to root.
    chunks = cur.split('.')
    prev = chunks[:-1]
    if prev == []:
        prev = ['root']
    if target == '/':
        prev = ['root']
    return ".".join(prev)


def add_file(cur, entry, tree):
    """
    Given the curretn branch, add a file to it.

    >>> tree = {'root': [],'root.a':[]}
    >>> tree = add_file('root', '1234 bar',tree)
    """
    tree[cur].append(entry)
    return tree


def add_dir(cur, entry, tree):
    """
    Given the current branch of the tree, return the branch with a new dir.

    >>> tree = {'root': []}
    >>> add_dir('root','dir a',tree)
    {'root': ['dir a'], 'root.a': []}

    """
    dirname = entry.split(' ').pop()
    tree[cur].append(entry)
    tree[cur+'.'+dirname] = []
    return tree


def build_tree(commands, tree):
    """
    Build the tree from the list of all commands

    >>> commands = get_command(get_data(test_data=test_data))
    >>> tree = {'root': []}
    >>> tree = build_tree(commands,tree)
    >>> tree
    {'root': ['dir a', '14848514 b.txt', '8504156 c.dat', 'dir d'], 'root.a': ['dir e', '29116 f', '2557 g', '62596 h.lst'], 'root.d': ['4060174 j', '8033020 d.log', '5626152 d.ext', '7214296 k'], 'root.a.e': ['584 i']}

    """
    mapper = {
        'cd': process_cd,
        'ls': process_ls,
    }
    cur = 'root'
    for command in commands:
        hint = command[0].split(' ')[1]
        (cur, tree) = mapper[hint](cur, command, tree)
    return tree


def size_dir(cur, tree):
    """
    Get the size of the dir.
    >>> commands = get_command(get_data(test_data=test_data))
    >>> tree = {'root': []}
    >>> tree = build_tree(commands,tree)
    >>> size_dir('root.a',tree)
    94853
    """
    files = filter(
        lambda x: not x.startswith('dir'),
        tree[cur]
    )
    dirs = filter(
        lambda x: x.startswith('dir'),
        tree[cur]
    )
    size_files = sum(map(
        lambda x: int(x.split(' ')[0]),
        files
    ))
    size_dirs = sum(map(
        lambda x: size_dir(cur+'.'+x.split(' ')[1], tree),
        dirs
    ))

    return size_files + size_dirs


def pd(k):
    """given a path, adjust it to whitespaces"""
    chunks = k.split('.')
    dirname = chunks.pop()
    spaces = "  "*len(chunks)
    return spaces+dirname


def pl(k, v):
    """given a bunch of files, and a path, print with padding."""
    spacer = "  " * len(k.split('.'))
    all = []
    for file in v:
        all.append(spacer+file)
    return "\n".join(all)


def pretty_tree(tree):
    """
    Pretty print the tree

    >>> tree = {'root': [],'root.a':['123 file']}
    root
     dir a
      123 file

    """
    cur = 'root'
    print(cur)
    print(tree[cur])
    for k in sorted(tree.keys()):
        print(pd(k))
        print(pl(k, tree[k]))
    return "---"

def part1(data):
    commands = get_command(data)
    tree = {'root': []}  # The initial tree
    tree = build_tree(commands, tree)
    sizes = []
    for dir in tree.keys():
        sizes.append((dir, size_dir(dir, tree)))

    return sum(list(map(
        lambda x: x[1],
        filter(
            lambda x: x[1] <= 100000,
            sizes
        ))))
    return "Thanks"


def part2(data):
    commands = get_command(data)
    tree = {'root': []}  # The initial tree
    tree = build_tree(commands, tree)
    sizes = {}
    for dir in tree.keys():
        sizes[dir] = size_dir(dir, tree)

    minimum = 30000000 # 30 MB
    total = 70000000 # 70MB
    available = total - sizes['root']
    required = minimum - available
    print("AVIL", available)

    return min(list(
        filter(
            lambda x: x >= required,
            sizes.values()
        )))


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    print("Results:")
    print(part1(get_data()))
    print(part2(get_data()))
