import re
from itertools import islice

try:  # pragma: no cover
    from urllib.parse import quote
except ImportError:  # pragma: no cover
    from urllib import quote

from isbnlib._core import get_isbnlike
from isbnlib.dev import webservice

ISBN_REGEX = r"978[0-9\-]+"
ISBN_PATTERN = re.compile(ISBN_REGEX, re.UNICODE)


def get_isbn(text):
    matches = ISBN_PATTERN.findall(text)
    if matches:
        return matches[0]


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
    return re.sub("(^\d+)|(\d+$)", "", content).strip()


def isbns_from_words(words):
    """Use Google to get an ISBN from words from title and author's name."""
    service_url = "http://www.google.com/search?q=ISBN+"
    search_url = service_url + quote(words.replace(" ", "+"))

    user_agent = "w3m/0.5.3"

    content = webservice.query(
        search_url,
        user_agent=user_agent,
        appheaders={
            "Content-Type": 'text/plain; charset="UTF-8"',
            "Content-Transfer-Encoding": "Quoted-Printable",
        },
    )
    return get_isbnlike(content)
