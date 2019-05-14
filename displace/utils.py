from itertools import tee, islice


def nwise(iterable, n, step):
    """
    Iterate over iterable n elements at a time, apart from each other by step

    nwise("ABCDEFGHI", 3, 3) --> ADG, BEH, CFI

    nwise(range(4), 2, 1) <--> pairwise(range(4))

    See pairwise recipe from https://docs.python.org/3/library/itertools.html
    """

    groups = tee(iterable, n)

    # Advance each iterator by it's index times the step
    groups = (islice(g, i * step, None) for i, g in enumerate(groups))

    return zip(*groups)
