import difflib

from ebooklib import epub
from ebooklib.utils import create_pagebreak

from pdf2ebook.base_page import BasePage
from pdf2ebook.w2n import word_to_num


class TextPage(BasePage):
    def __init__(self, idx, content):
        self.idx = idx
        self.next_page = None
        self.content = content

        if self.next_page is not None:
            self.raw_content = "\n".join(
                self.content.split("\x0c")[self.idx : self.next_page.idx]
            )
        else:
            self.raw_content = "\n".join(self.content.split("\x0c")[self.idx :])

        super(TextPage, self).__init__()

    @property
    def text_content(self):
        return self.raw_content

    @property
    def page_no(self):
        # Page number and written page number different
        # this is what's written on the page, not the actual index of the page in pages

        # TODO: find if at the top or bottom. Be told from pages when adding context
        # Also need to remove author name if first or last phrase
        first_line = self.text_content.strip().split("\n")[0]
        last_line = self.text_content.strip().split("\n")[-1]

        first_line_num = None
        try:
            first_line_num = word_to_num(first_line)
        except:
            pass

        last_line_num = None
        try:
            last_line_num = word_to_num(last_line)
        except:
            pass

        if first_line.isdigit():
            return int(first_line)
        elif last_line.isdigit():
            return int(last_line)
        elif first_line_num:
            return first_line_num
        elif last_line_num:
            return last_line_num
        else:
            return None

    @property
    def html_content(self):
        content = ""
        for para in self.text_content.split("\n\n"):
            content += "<p>" + para + "</p>"
        return content

    @property
    def epub_content(self):
        # need a different content that strips headers and footers
        epub_page = epub.EpubHtml(
            title=f"title_{self.idx}",
            file_name=f"page_{self.idx}.xhtml",
            lang=self.lang,
            uid=str(self.idx),
        )
        epub_page.content = self.html_content
        epub_page.content += create_pagebreak(f"p_{self.idx}")
        return epub_page

    def remove_page_number(self):
        self.raw_content = self.text_content_without_page_no

    def remove_header(self, header):
        if not header:
            return
        content = []
        for idx, line in enumerate(self.text_content.split("\n")):
            if idx < 5:
                if difflib.SequenceMatcher(None, line, header).ratio() > 0.8:
                    pass
                else:
                    content.append(line)
            else:
                content.append(line)

        if content:
            self.raw_content = "\n".join(content)

    def remove_footer(self, footer):
        if not footer:
            return
        content = []
        for idx, line in enumerate(reversed(self.text_content.split("\n"))):
            if idx < 5:
                if difflib.SequenceMatcher(None, line, footer).ratio() > 0.8:
                    pass
                else:
                    content.append(line)
            else:
                content.append(line)

        if content:
            self.raw_content = "\n".join(reversed(content))

    def set_next_page(self, next_page):
        self.next_page = next_page
        if self.next_page is not None:
            self.raw_content = "\n".join(
                self.content.split("\x0c")[self.idx : self.next_page.idx]
            )
        else:
            self.raw_content = "\n".join(self.content.split("\x0c")[self.idx :])
