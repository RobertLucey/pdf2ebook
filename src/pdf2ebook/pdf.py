import os
import re
import difflib
import unicodedata
from io import StringIO

import isbnlib
import bs4
from ebooklib import epub
from ebooklib.plugins import standard
from cached_property import cached_property

from pdf2ebook import logger
from pdf2ebook.text_page import TextPage
from pdf2ebook.html_page import HTMLPage
from pdf2ebook.pages import Pages
from pdf2ebook.utils import window, get_isbn, isbns_from_words


class PDF:
    def __init__(self, *args, **kwargs):
        self.pdf_path = kwargs["path"]
        self._title = kwargs.get("title", None)
        self._use_text = kwargs.get("use_text", None)
        self._use_html = kwargs.get("use_html", None)

        self.text_content = None

        self.text_file = None
        self.html_file = None

        self.loaded = False

    def get_expected_title(self):
        if self._title:
            return self._title

        # Assert page no removed first

        # Maybe check the first line of the second page too

        filename = os.path.splitext(os.path.basename(self.pdf_path))[0]
        filename = filename.replace("_", " ").lower()
        filename_title = filename
        # if by... remove by... to just get the title
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
        for page in self.pages:
            isbn = get_isbn(page.cleaned_text_content)
            if isbn:
                try:
                    isbnlib.meta(isbn)
                except isbnlib._exceptions.NotValidISBNError:
                    logger.warning(f"Not a valid ISBN: {isbn}")
                else:
                    return isbn

        expected_title = self.get_expected_title()
        if expected_title:
            logger.info(f"Guessing the isbn from title: {expected_title}")
            return isbnlib.isbn_from_words(expected_title)

    def get_isbns(self):

        isbns = []

        for page in self.pages:
            isbn = get_isbn(page.cleaned_text_content)
            if isbn:
                try:
                    isbnlib.meta(isbn)
                except isbnlib._exceptions.NotValidISBNError:
                    logger.warning(f"Not a valid ISBN: {isbn}")
                else:
                    isbns.append(isbn)

        expected_title = self.get_expected_title()
        if expected_title:
            logger.info(f"Guessing the isbn from title: {expected_title}")
            isbns.extend(isbns_from_words(expected_title))

        return list(set(isbns))

    def get_authors(self):
        isbn = self.get_isbn()
        if isbn:
            meta = isbnlib.meta(isbn)
            if meta.get("Authors", None):
                return meta["Authors"]
        return []

    def get_title(self):
        if self._title:
            return self._title

        isbn = self.get_isbn()
        if isbn:
            meta = isbnlib.meta(isbn)
            if meta.get("Title", None):
                return meta["Title"]

    def set_title(self, book):
        title = self.get_title()
        if title:
            book.set_title(title)
        else:
            book.set_title(os.path.splitext(os.path.basename(self.pdf_path))[0])
        return book

    def set_authors(self, book):
        isbn = self.get_isbn()
        if isbn:
            for author in self.get_authors():
                book.add_author(author)
        return book

    def set_identifier(self, book):
        isbn = self.get_isbn()
        if isbn:
            book.set_identifier(isbn)
        return book

    def get_thumbnail_url(self):
        for isbn in self.get_isbns():
            thumbnail = isbnlib.cover(isbn).get("thumbnail", None)
            if thumbnail:
                return thumbnail

    def to_epub(self, path=None):
        self.load()

        if self.use_text:
            logger.warning("Only using text, images will not be included")

        book = epub.EpubBook()

        if self.use_html:
            for page in self.pages:
                for image in page.images:
                    book.add_item(image)

        for i in range(10):  # FIXME: hacky
            self.pages.set_page_number_position()
            header = self.pages.detect_header()
            footer = self.pages.detect_footer()
            for page in self.pages:
                page.remove_page_number()
                page.remove_header(header)
                page.remove_footer(footer)

        for page in self.pages:
            if (
                bs4.BeautifulSoup(
                    StringIO(page.epub_content.content), "html.parser"
                ).text
                == ""
                and bs4.BeautifulSoup(
                    StringIO(page.epub_content.content), "html.parser"
                ).find("img")
                is None
            ):
                continue
            page.strip_whitespace()
            book.add_item(page.epub_content)

        book.add_item(epub.EpubNcx())
        book.add_item(epub.EpubNav())

        book.spine = ["nav"] + [c.epub_content for c in self.pages]

        langs = [page.lang for page in self.pages]
        lang = max(set(langs), key=langs.count)
        if lang is None:
            logger.warning("Could not detect language")
        else:
            logger.debug(f"Language detected: {lang}")
            book.set_language(lang)

        book = self.set_identifier(book)
        book = self.set_authors(book)
        book = self.set_title(book)

        opts = {"plugins": [standard.SyntaxPlugin()]}
        epub.write_epub(path, book, opts)
        logger.debug(f"Epub saved: {path}")

    def load_text(self):
        self.text_file = self.pdf_path + ".txt"

        os.system(f"pdftotext '{self.pdf_path}' '{self.text_file}'")

        if not os.path.exists(self.text_file):
            logger.error("Could not convert pdf to text: %s" % (self.text_file))
            return

        self.text_content = open(self.text_file, "r").read()

    def load_html(self):
        self.html_file = self.pdf_path.replace(".pdf", "s.html")

        os.system(f"pdftohtml -q '{self.pdf_path}'")

        if not os.path.exists(self.html_file):
            logger.error("Could not convert pdf to html: %s" % (self.html_file))
            self.loaded = True
            return

    def load(self):
        if self.loaded:
            return

        self.load_text()
        self.load_html()

    @property
    def use_text(self):
        if self._use_text is not None:
            return self._use_text

        if not self.use_html:
            return True

        return False

    @property
    def use_html(self):
        if self._use_html is not None:
            return self._use_html

        soup = bs4.BeautifulSoup(open(self.html_file), "html.parser")

        if len(soup.text.split(" ")) > 2000:
            return True

        return False

    @cached_property
    def pages(self):
        self.load()

        # TODO Find contents / table of contents and start after that. Who needs acks
        pages = Pages()

        if self.use_text:
            logger.debug("Generating pages using only text")
            # TODO: if all the content looks to be in html, use that rather than text
            for idx, (p, c, n) in enumerate(
                window(self.text_content.split("\x0c"), window_size=3)
            ):
                pages.append(TextPage(idx, self.text_content))

        elif self.use_html:
            logger.debug("Generating pages using html")

            soup = bs4.BeautifulSoup(open(self.html_file), "html.parser")
            html_content = open(self.html_file, "r").read()
            body = soup.find("body")
            breaks = body.find_all("hr")

            page_idx = 0

            pages.append(
                HTMLPage(
                    page_idx,
                    "\n".join(
                        html_content.split("\n")[body.sourceline : breaks[0].sourceline]
                    ),
                )
            )
            for idx, (i, j) in enumerate(window(breaks, window_size=2)):
                pages.append(
                    HTMLPage(
                        idx + 1,
                        "\n".join(
                            html_content.split("\n")[i.sourceline : j.sourceline]
                        ),
                    )
                )
        else:
            raise Exception("Could not convert")

        pages.set_context()

        logger.debug(f"Generated {len(pages)} pages")

        return pages
