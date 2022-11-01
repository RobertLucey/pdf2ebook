import os

from unittest import TestCase

from pdf2ebook.pdf import PDF


class RoomWithAViewPDFTest(TestCase):

    PDF_PATH = 'test/resources/room_with_a_view.pdf'
    EPUB_NAME = 'test_room_with_a_view.epub'
    EXPECTED_PAGES = 151

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
            'bottom'
        )

    def test_pages_content(self):
        pdf = PDF(path=self.PDF_PATH)
        pdf.load()

        self.assertEquals(
            pdf.pages._data[0].text_content,
            """A ROOM WITH A VIEW 
  
by E. M. Forster 
  
 
 
  
 
This free e-book was created and is distributed not-for-profit 
by Candida Martinelli of 
Candida Martinelli’s Italophile Site"""
        )

    def test_pages_cleaned_content(self):
        pdf = PDF(path=self.PDF_PATH)
        pdf.load()

        self.assertEquals(
            pdf.pages._data[0].cleaned_text_content,
            """A ROOM WITH A VIEW

by E. M. Forster





This free e-book was created and is distributed not-for-profit
by Candida Martinelli of
Candida Martinelli’s Italophile Site"""
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
        self.assertGreater(
            os.path.getsize(f'/tmp/{self.EPUB_NAME}'),
            0
        )

    def test_to_html(self):
        pdf = PDF(path=self.PDF_PATH)
        pdf.load()
        self.assertEquals(len(pdf.pages), self.EXPECTED_PAGES)
