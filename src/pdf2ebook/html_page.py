import re
import difflib
import os
from io import StringIO
import shutil

import bs4

from ebooklib import epub
from ebooklib.utils import create_pagebreak

from pdf2ebook import logger
from pdf2ebook.base_page import BasePage


class HTMLPage(BasePage):
    def __init__(self, idx, content):
        self.idx = idx
        self.next_page = None

        soup = bs4.BeautifulSoup(StringIO(content), "html.parser")

        try:
            soup.hr.decompose()
        except:
            logger.warning("No hr tags found, expecting a single page document")

        self.content = str(soup)

        super(HTMLPage, self).__init__()

    @property
    def images(self):
        soup = bs4.BeautifulSoup(StringIO(self.content), "html.parser")
        imgs = soup.find_all("img")
        logger.debug(f"Found {len(imgs)} images in page {self.idx}")

        images = []
        for idx, img in enumerate(imgs):
            epub_image = epub.EpubImage()

            real_path = img["src"]

            new_path = os.path.basename(real_path)
            try:
                shutil.copy(real_path, new_path)
            except Exception as ex:
                logger.debug(
                    f'Could not copy image "{real_path}" -> "{new_path}": {ex}'
                )

            try:
                image_content = open(new_path, "rb").read()
            except:
                logger.error(f"Could not get image content from path: {new_path}")
            else:
                epub_image.uid = f"image_{self.idx}_{idx}"
                epub_image.file_name = new_path
                epub_image.media_type = "image/png"  # TODO: detect
                epub_image.set_content(image_content)
                images.append(epub_image)

        return images

    @property
    def text_content(self):
        soup = bs4.BeautifulSoup(StringIO(self.content), "html.parser")
        return soup.text.strip()

    @property
    def page_no(self):
        raise NotImplementedError()

    @property
    def html_content(self):
        soup = bs4.BeautifulSoup(StringIO(self.content), "html.parser")
        for img in soup.find_all("img"):
            img["src"] = os.path.basename(img["src"])
        self.content = str(soup)
        return self.content

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

    def remove_header(self, header):
        if not header:
            return
        # might need to remove tags
        soup = bs4.BeautifulSoup(StringIO(self.content), "html.parser")
        lines = str(soup).split("\n")
        content = []
        collect = False
        for line in lines:
            if collect:
                content.append(line)
            else:
                soup_line = bs4.BeautifulSoup(StringIO(line), "html.parser")
                if (
                    difflib.SequenceMatcher(
                        None, soup_line.text.strip(), header
                    ).ratio()
                    > 0.8
                ):
                    collect = True
        if content:
            self.content = "\n".join(content)

    def remove_footer(self, footer):
        if not footer:
            return
        # might need to remove tags
        soup = bs4.BeautifulSoup(StringIO(self.content), "html.parser")
        lines = str(soup).split("\n")
        content = []
        collect = False
        for line in reversed(lines):
            if collect:
                content.append(line)
            else:
                soup_line = bs4.BeautifulSoup(StringIO(line), "html.parser")
                if (
                    difflib.SequenceMatcher(
                        None, soup_line.text.strip(), footer
                    ).ratio()
                    > 0.8
                ):
                    collect = True
        if content:
            self.content = "\n".join(reversed(content))

    def remove_page_number(self):
        if self.included_page_no is None:
            return

        # find the number from text and remove from html
        soup = bs4.BeautifulSoup(StringIO(self.content), "html.parser")
        lines = str(soup).split("\n")

        if self.page_number_position == "top":
            content = []
            collect = False
            for line in lines:
                if collect:
                    content.append(line)
                else:
                    text_line = bs4.BeautifulSoup(
                        StringIO(line), "html.parser"
                    ).text.strip()
                    if text_line.startswith(self.included_page_no):
                        content.append(
                            re.sub("(^\d+)", "", text_line)
                        )  # FIXME: this removes html elements
                        collect = True
            if content:
                self.content = "\n".join(content)
        elif self.page_number_position == "bottom":
            content = []
            collect = False
            for line in reversed(lines):
                if collect:
                    content.append(line)
                else:
                    text_line = bs4.BeautifulSoup(
                        StringIO(line), "html.parser"
                    ).text.strip()
                    if text_line.startswith(self.included_page_no):
                        content.append(
                            re.sub("(^\d+)", "", text_line)
                        )  # FIXME: this removes html elements
                        collect = True
            if content:
                self.content = "\n".join(reversed(content))

        self.strip_whitespace()

    def strip_whitespace(self):
        soup = bs4.BeautifulSoup(StringIO(self.content), "html.parser")
        lines = str(soup).split("\n")
        content = []
        collect = False
        for line in lines:
            if collect:
                content.append(line)
            else:
                soup_line = bs4.BeautifulSoup(StringIO(line), "html.parser")
                if soup_line.text.strip() == "":
                    collect = True
        if content:
            self.content = "\n".join(content)

        soup = bs4.BeautifulSoup(StringIO(self.content), "html.parser")
        lines = str(soup).split("\n")
        content = []
        collect = False
        for line in reversed(lines):
            if collect:
                content.append(line)
            else:
                soup_line = bs4.BeautifulSoup(StringIO(line), "html.parser")
                if soup_line.text.strip() == "":
                    collect = True
        if content:
            self.content = "\n".join(reversed(content))
