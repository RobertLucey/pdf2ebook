from io import StringIO

import bs4

from pdf2ebook import logger
from pdf2ebook.base_page import BasePage


class HTMLExPage(BasePage):
    def __init__(self, idx, content, head=None):
        self.idx = idx
        self.next_page = None

        self.dups_removed = False

        self.head = head

        self.content = content

        super(HTMLExPage, self).__init__()

    @property
    def content_hash(self):
        self.remove_dups()
        return hash(self.content)

    @property
    def html_content(self):
        self.remove_dups()
        # TODO
        self.content.img.decompose()
        print(self.content.text.replace("", " "))

        # each div is a line
        return None

    @property
    def lines(self):
        self.remove_dups()
        for line in self.content.find_all("div"):
            yield line

    @property
    def text_lines(self):
        self.remove_dups()
        for line in self.content.find_all("div"):
            yield line.text.replace("", " ").strip()

    def remove_dups(self):
        if self.dups_removed:
            return
        content = self.content.find_all("div")[2:]
        self.content = bs4.BeautifulSoup(
            StringIO("".join([str(c) for c in content])), "html.parser"
        )
        self.dups_removed = True

    def strip_whitespace(self):
        self.remove_dups()
        content = []
        collect = False
        for line in self.content.find_all("div"):
            if collect:
                content.append(line)
            else:
                if not line.text.strip():  # or img
                    continue
                else:
                    collect = True
                    content.append(line)

        if content:
            self.content = bs4.BeautifulSoup(
                StringIO("".join([str(c) for c in content])), "html.parser"
            )

        content = []
        collect = False
        for line in reversed(self.content.find_all("div")):
            if collect:
                content.append(line)
            else:
                if not line.text.strip():  # or img
                    continue
                else:
                    collect = True
                    content.append(line)
        if content:
            self.content = bs4.BeautifulSoup(
                StringIO("".join(reversed([str(c) for c in content]))), "html.parser"
            )
