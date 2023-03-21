import re
import os
from shutil import which
from itertools import islice
from urllib.request import urlopen

import bs4
from googlesearch import search

from pdf2ebook import logger


try:  # pragma: no cover
    from urllib.parse import quote
except ImportError:  # pragma: no cover
    from urllib import quote

from isbnlib._core import get_isbnlike
from isbnlib.dev import webservice

ISBN_REGEX = r"978[0-9\-]+"
ISBN_PATTERN = re.compile(ISBN_REGEX, re.UNICODE)


def get_isbn(text):
    isbns = get_isbns(text)
    if isbns:
        return isbns[0]


def get_isbns(text):
    text = re.sub(r"\s+", "", text, flags=re.UNICODE)
    matches = ISBN_PATTERN.findall(text)
    for match in matches:
        while match.endswith("-"):
            match = match[:-1]
    return matches


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


def is_local_htmlex_ok():
    if not which("pdf2htmlEX"):
        return

    return os.system("pdf2htmlEX --version") == 0


def is_docker_installed():
    return bool(which("docker"))


def get_isbn_from_content(content, engine="google"):
    for url_result in search(content, stop=10):
        url_isbn = get_isbn(url_result)
        if url_isbn:
            return url_isbn

        # if it ends in .pdf we can skip, likely what we have
        if url_result.endswith(".pdf"):
            continue

        try:
            source = urlopen(url_result)
            soup = bs4.BeautifulSoup(source, "html.parser")

            title_isbn = get_isbn(soup.title.text)
            if title_isbn:
                return title_isbn

            content_isbns = get_isbns(soup.text)
            if len(content_isbns) > 1:
                # TODO: be smarter, may ref other books
                pass
            elif len(content_isbns) == 1:
                return content_isbns[0]
        except Exception as ex:
            logger.warning(f"Could not search for isbn from content: {ex}")
