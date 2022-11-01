import os

from unittest import TestCase

from pdf2ebook.pdf import PDF


class VortexPDFTest(TestCase):

    PDF_PATH = 'test/resources/vortex.pdf'
    EPUB_NAME = 'test_vortex.epub'
    EXPECTED_PAGES = 16

    def test_detect_footer(self):
        pdf = PDF(path=self.PDF_PATH)
        pdf.load()
        self.assertEquals(
            pdf.pages.detect_footer(),
            None
        )

    def test_detect_header(self):
        pdf = PDF(path=self.PDF_PATH)
        pdf.load()
        self.assertEquals(
            pdf.pages.detect_header(),
            None
        )

    def test_page_number_position(self):
        pdf = PDF(path=self.PDF_PATH)
        pdf.load()
        pdf.pages.set_page_number_position()
        self.assertEquals(
            pdf.pages[0].page_number_position,
            None
        )

    def test_pages_content(self):
        pdf = PDF(path=self.PDF_PATH)
        pdf.load()

        self.assertEqual(
            pdf.pages._data[0].text_content,
            '''INTRODUCING "Storm" Cloud, who, through tragedy, is destined to become the most noted figure in the
galaxy—

The Vortex Blaster
***

E. E. SMITH, Ph.D.
Author of "The Skylark,""Skylark Three,""The Skylark of Valeron," the Lensman stories, etc.
Comet
Published in July 1941
epubBooks.com

'''
        )

    def test_pages_cleaned_content(self):
        pdf = PDF(path=self.PDF_PATH)
        pdf.load()

        self.assertEquals(
            pdf.pages._data[0].cleaned_text_content,
            '''INTRODUCING "Storm" Cloud, who, through tragedy, is destined to become the most noted figure in the
galaxy—

The Vortex Blaster
***

E. E. SMITH, Ph.D.
Author of "The Skylark,""Skylark Three,""The Skylark of Valeron," the Lensman stories, etc.
Comet
Published in July 1941
epubBooks.com'''
        )

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

    def test_to_epub(self):
        pdf = PDF(path=self.PDF_PATH)
        pdf.load()
        try:
            os.remove(f'/tmp/{self.EPUB_NAME}')
        except:
            pass
        pdf.to_epub(f'/tmp/{self.EPUB_NAME}')
        self.assertTrue(
            os.path.exists(f'/tmp/{self.EPUB_NAME}')
        )

    def test_to_html(self):
        pdf = PDF(path=self.PDF_PATH)
        pdf.load()
        self.assertEquals(len(pdf.pages), self.EXPECTED_PAGES)
        self.assertGreater(
            os.path.getsize(f'/tmp/{self.EPUB_NAME}'),
            0
        )
