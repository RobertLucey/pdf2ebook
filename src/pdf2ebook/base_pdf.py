import os
import re
import difflib
import unicodedata
from collections import defaultdict

import isbnlib

from pdf2ebook import logger
from pdf2ebook.utils import get_isbn, isbns_from_words


META_CACHE = defaultdict(dict)
ISBN_CACHE = defaultdict(str)
ISBNS_CACHE = defaultdict(list)


class BasePDF:
    @property
    def content_hash(self):
        return hash(sum([page.content_hash for page in self.pages]))

    @property
    def isbn_meta(self):
        if self.content_hash in META_CACHE:
            return META_CACHE[self.content_hash]
        isbn = self.get_isbn()
        if isbn:
            data = isbnlib.meta(isbn)
            META_CACHE[self.content_hash] = data
        return META_CACHE[self.content_hash]

    def get_expected_title(self):
        if self._title:
            return self._title

        # Assert page no removed first

        # Maybe check the first line of the second page too

        filename = os.path.splitext(os.path.basename(self.pdf_path))[0]
        filename = filename.replace("_", " ").lower()
        filename_title = filename
        # if by... remove by... to just get the title
        # FIXME: if by is in the title this confuses things.
        # Maybe see if there's a author name after the by
        filename_title = re.sub("([- ]by[-: ].*)", "", filename_title)

        content_title = ""
        clean_content = self.pages[0].cleaned_text_content.lower()
        found_idx = None
        for idx, line in enumerate(clean_content.split("\n")):
            if line.startswith("by:") or line.startswith("by ") or line == "by":
                found_idx = idx

        if found_idx is not None:
            possible_title = "\n".join(clean_content.split("\n")[:found_idx]).strip()
            logger.debug(f"Guessing the title from page content is: {possible_title}")
            content_title = unicodedata.normalize("NFKD", possible_title.strip())

        if difflib.SequenceMatcher(None, filename_title, content_title).ratio() > 0.4:
            logger.debug("filename_title and content_title close enough")
            return content_title

    def get_isbn(self):
        if self.content_hash in ISBN_CACHE:
            return ISBN_CACHE[self.content_hash]

        for page in self.pages:
            isbn = get_isbn(page.cleaned_text_content)
            if isbn:
                try:
                    isbnlib.meta(isbn)
                except isbnlib._exceptions.NotValidISBNError:
                    logger.warning(f"Not a valid ISBN: {isbn}")
                else:
                    ISBN_CACHE[self.content_hash] = isbn

        if self.content_hash in ISBN_CACHE:
            return ISBN_CACHE[self.content_hash]

        expected_title = self.get_expected_title()
        if expected_title:
            logger.info(f"Guessing the isbn from title: {expected_title}")
            ISBN_CACHE[self.content_hash] = isbnlib.isbn_from_words(expected_title)

        return ISBN_CACHE[self.content_hash]

    def get_isbns(self):
        if self.content_hash in ISBNS_CACHE:
            return ISBNS_CACHE[self.content_hash]

        for page in self.pages:
            isbn = get_isbn(page.cleaned_text_content)
            if isbn:
                try:
                    isbnlib.meta(isbn)
                except isbnlib._exceptions.NotValidISBNError:
                    logger.warning(f"Not a valid ISBN: {isbn}")
                else:
                    ISBNS_CACHE[self.content_hash].append(isbn)

        expected_title = self.get_expected_title()
        if expected_title:
            logger.info(f"Guessing the isbn from title: {expected_title}")
            ISBNS_CACHE[self.content_hash].extend(isbns_from_words(expected_title))

        return ISBNS_CACHE[self.content_hash]

    def get_authors(self):
        isbn = self.get_isbn()
        if isbn:
            return self.isbn_meta.get("Authors", [])
        return []

    def get_title(self):
        if self._title:
            return self._title
        return self.isbn_meta.get("Title", None)

    def get_thumbnail_url(self):
        for isbn in self.get_isbns():
            thumbnail = isbnlib.cover(isbn).get("thumbnail", None)
            if thumbnail:
                return thumbnail

    def get_publisher(self):
        isbn = self.get_isbn()
        if isbn:
            return self.isbn_meta.get("Publisher", None)

    def get_published_date(self):
        isbn = self.get_isbn()
        if isbn:
            return self.isbn_meta.get("Year", None)
