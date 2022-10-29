import os
from io import StringIO

import bs4
from ebooklib import epub
from ebooklib.plugins import standard

from pdf2ebook.page import Page, HTMLPage
from pdf2ebook.pages import Pages
from pdf2ebook.utils import window


class PDF:
    def __init__(self, *args, **kwargs):

        self.pdf_path = kwargs["path"]
        self.text_content = None

        self._use_text = kwargs.get("use_text", None)
        self._use_html = kwargs.get("use_html", None)

        self.text_file = None
        self.html_file = None

    def to_epub(self, path=None):
        book = epub.EpubBook()

        # add metadata
        book.set_title(os.path.splitext(os.path.basename(self.pdf_path))[0])
        book.set_language("en")  # TODO: detect

        book.add_author("")

        contents = []
        for page in self.pages:
            contents.append(page)

        if self.use_html:
            for page in contents:
                for image in page.images:
                    book.add_item(image)

        for page in contents:
            book.add_item(page.epub_content)

        book.add_item(epub.EpubNcx())
        book.add_item(epub.EpubNav())

        book.spine = ["nav"] + [c.epub_content for c in contents]

        opts = {"plugins": [standard.SyntaxPlugin()]}
        epub.write_epub(path, book, opts)

    def load_text(self):
        self.text_file = self.pdf_path + ".txt"

        if not os.path.exists(self.text_file):
            os.system(f"pdftotext '{self.pdf_path}' '{self.text_file}'")

        if not os.path.exists(self.text_file):
            print("Could not convert pdf to text: %s" % (self.text_file))
            return

        self.text_content = open(self.text_file, "r").read()

    def load_html(self):
        self.html_file = self.pdf_path.replace(".pdf", "s.html")

        if not os.path.exists(self.html_file):
            os.system(f"pdftohtml '{self.pdf_path}'")

        if not os.path.exists(self.html_file):
            print("Could not convert pdf to html: %s" % (self.html_file))
            self.loaded = True
            return

    def load(self):
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

    @property
    def pages(self):
        # assume pages are numbered with newlines padding

        # TODO Find contents / table of contents and start after that. Who needs acks
        pages = Pages()

        if self.use_text:
            # TODO: if all the content looks to be in html, use that rather than text
            for idx, (p, c, n) in enumerate(
                window(self.text_content.split("\x0c"), window_size=3)
            ):
                pages.append(Page(idx, self.text_content))

        elif self.use_html:

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

        return pages
