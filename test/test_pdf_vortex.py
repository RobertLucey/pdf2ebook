import os

from mock import patch
from unittest import TestCase, skip

from pdf2ebook.pdf import PDF


class VortexPDFTest(TestCase):

    PDF_PATH = "test/resources/vortex_blaster.pdf"
    EPUB_NAME = "test_vortex.epub"
    EXPECTED_PAGES = 16

    @skip("Need to get isbn")
    @patch("pdf2ebook.pdf.PDF.use_html_ex", False)
    def test_get_thumbnail_url(self):
        pdf = PDF(path=self.PDF_PATH)
        pdf.load()
        self.assertIsNotNone(pdf.get_thumbnail_url())

    @skip("Need to find author name and check before it")
    @patch("pdf2ebook.pdf.PDF.use_html_ex", False)
    def test_get_expected_title(self):
        pdf = PDF(path=self.PDF_PATH)
        pdf.load()

        contents = []
        for page in pdf.pages:
            contents.append(page)

        last_hash = None
        while last_hash != pdf.content_hash:
            last_hash = pdf.content_hash
            pdf.pages.set_page_number_position()
            header = pdf.pages.detect_header()
            footer = pdf.pages.detect_footer()
            for page in contents:
                page.remove_page_number()
                page.remove_header(header)
                page.remove_footer(footer)

        self.assertEquals(pdf.get_expected_title(), "the vortex blaster")

    @patch("pdf2ebook.pdf.PDF.use_html_ex", False)
    def test_detect_footer(self):
        pdf = PDF(path=self.PDF_PATH)
        pdf.load()
        self.assertEquals(pdf.pages.detect_footer(), None)

    @patch("pdf2ebook.pdf.PDF.use_html_ex", False)
    def test_detect_header(self):
        pdf = PDF(path=self.PDF_PATH)
        pdf.load()
        self.assertEquals(pdf.pages.detect_header(), None)

    @patch("pdf2ebook.pdf.PDF.use_html_ex", False)
    def test_page_number_position(self):
        pdf = PDF(path=self.PDF_PATH)
        pdf.load()
        pdf.pages.set_page_number_position()
        self.assertEquals(pdf.pages[0].page_number_position, None)

    @patch("pdf2ebook.pdf.PDF.use_html_ex", False)
    def test_pages_content(self):
        pdf = PDF(path=self.PDF_PATH)
        pdf.load()

        self.assertEqual(
            pdf.pages._data[0].text_content,
            """INTRODUCING "Storm" Cloud, who, through tragedy, is destined to become the most noted figure in the
galaxy—

The Vortex Blaster
***

E. E. SMITH, Ph.D.
Author of "The Skylark,""Skylark Three,""The Skylark of Valeron," the Lensman stories, etc.
Comet
Published in July 1941
epubBooks.com

""",
        )

    @patch("pdf2ebook.pdf.PDF.use_html_ex", False)
    def test_pages_cleaned_content(self):
        pdf = PDF(path=self.PDF_PATH)
        pdf.load()

        self.assertEquals(
            pdf.pages._data[0].cleaned_text_content,
            """INTRODUCING "Storm" Cloud, who, through tragedy, is destined to become the most noted figure in the
galaxy—

The Vortex Blaster
***

E. E. SMITH, Ph.D.
Author of "The Skylark,""Skylark Three,""The Skylark of Valeron," the Lensman stories, etc.
Comet
Published in July 1941
epubBooks.com""",
        )

    @patch("pdf2ebook.pdf.PDF.use_html_ex", False)
    def test_pages_context(self):
        pdf = PDF(path=self.PDF_PATH)
        pdf.load()
        for i in range(len(pdf.pages)):
            if i == len(pdf.pages) - 1:
                self.assertEquals(
                    pdf.pages._data[i].next_page,
                    None,
                )
            else:
                self.assertEquals(
                    pdf.pages._data[i].next_page.idx,
                    pdf.pages._data[i + 1].idx,
                )

    @patch("pdf2ebook.pdf.PDF.use_html_ex", False)
    def test_to_epub(self):
        pdf = PDF(path=self.PDF_PATH)
        pdf.load()
        try:
            os.remove(f"/tmp/{self.EPUB_NAME}")
        except:
            pass
        pdf.to_epub(f"/tmp/{self.EPUB_NAME}")
        self.assertTrue(os.path.exists(f"/tmp/{self.EPUB_NAME}"))

    @patch("pdf2ebook.pdf.PDF.use_html_ex", False)
    def test_to_html(self):
        pdf = PDF(path=self.PDF_PATH)
        pdf.load()
        self.assertEquals(len(pdf.pages), self.EXPECTED_PAGES)
        self.assertGreater(os.path.getsize(f"/tmp/{self.EPUB_NAME}"), 0)


class VortexPDFTest_EX(TestCase):

    PDF_PATH = "test/resources/vortex_blaster.pdf"
    EPUB_NAME = "test_vortex.epub"
    EXPECTED_PAGES = 17

    def test_text_lines(self):
        pdf = PDF(path=self.PDF_PATH)
        pdf.load()
        self.assertEquals(
            list(pdf.pages[0].text_lines),
            [
                'INTRODUCING "Storm" Cloud, who, through tragedy, is destined to become the most noted figure in the',
                "galaxy—",
                "The Vortex Blaster",
                "***",
                "E. E. SMITH, Ph.D.",
                'Author of "The Skylark,""Skylark Three,""The Skylark of Valeron," the Lensman stories, etc.',
                "Comet",
                "Published in July 1941",
                "epubBooks.com",
                "",
                "",
            ],
        )

    def test_page_numbers(self):
        pdf = PDF(path=self.PDF_PATH)
        pdf.load()
        self.assertEquals(len(pdf.pages), self.EXPECTED_PAGES)

    def test_pages_context(self):
        pdf = PDF(path=self.PDF_PATH)
        pdf.load()
        for i in range(len(pdf.pages)):
            if i == len(pdf.pages) - 1:
                self.assertEquals(
                    pdf.pages._data[i].next_page,
                    None,
                )
            else:
                self.assertEquals(
                    pdf.pages._data[i].next_page.idx,
                    pdf.pages._data[i + 1].idx,
                )

    def test_strip_whitespace(self):
        pdf = PDF(path=self.PDF_PATH)
        pdf.load()
        pdf.pages[0].strip_whitespace()

        self.assertEquals(
            list(pdf.pages[0].text_lines),
            [
                'INTRODUCING "Storm" Cloud, who, through tragedy, is destined to become the most noted figure in the',
                "galaxy—",
                "The Vortex Blaster",
                "***",
                "E. E. SMITH, Ph.D.",
                'Author of "The Skylark,""Skylark Three,""The Skylark of Valeron," the Lensman stories, etc.',
                "Comet",
                "Published in July 1941",
                "epubBooks.com",
            ],
        )
