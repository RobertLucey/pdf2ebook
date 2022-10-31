import re
from itertools import islice


def window(sequence, window_size=2):
    """
    Returns a sliding window (of width n) over data from the iterable
    """
    seq_iterator = iter(sequence)
    result = tuple(islice(seq_iterator, window_size))
    if len(result) == window_size:
        yield result
    for elem in seq_iterator:
        result = result[1:] + (elem,)
        yield result


def remove_page_no(content):
    # bit risky, should be told if to remove from start or end
    return re.sub("(^\d+)|(\d+$)", "", content)
