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
