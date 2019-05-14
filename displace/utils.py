from itertools import tee


def stepped_grouper(iterable, n, step):
    # TODO better documentation
    """
    Collect data into fixed-length chunks or blocks with given step

    See grouper recipe from https://docs.python.org/3/library/itertools.html
    """
    # stepped_grouper('ABCDEFGHI', 3, 3) --> ADG BEH CFI"

    groups = tee(iterable, n)

    for i, group in enumerate(groups):
        for _ in range(i * step):
            next(group, None)

    return zip(*groups)
