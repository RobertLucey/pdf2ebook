from itertools import islice


def clean_string(string):
    string = string.replace("\x0c", "")
    return string.encode("ascii", errors="ignore").decode().strip()


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
