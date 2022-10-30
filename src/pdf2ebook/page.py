import os
from io import StringIO
import shutil

import bs4
import langdetect
from cached_property import cached_property

from ebooklib import epub
from ebooklib.utils import create_pagebreak

from pdf2ebook import logger
from pdf2ebook.w2n import word_to_num


class GenericPage:
    @cached_property
    def lang(self):
        try:
            lang = langdetect.detect(self.text_content[:1000])
        except langdetect.lang_detect_exception.LangDetectException:
            lang = None

        return lang


class Page(GenericPage):
    def __init__(self, idx, content):
        self.idx = idx
        self.next_page = None
        self.content = content

    @property
    def text_content(self):
        if self.next_page is not None:
            return "\n".join(self.content.split("\x0c")[self.idx : self.next_page.idx])
        return "\n".join(self.content.split("\x0c")[self.idx :])

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


class HTMLPage(GenericPage):
    def __init__(self, idx, content):
        self.idx = idx
        self.next_page = None

        soup = bs4.BeautifulSoup(StringIO(content), "html.parser")

        try:
            soup.hr.decompose()
        except:
            logger.warning("No hr tags found, expecting a single page document")

        self.content = str(soup)

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
