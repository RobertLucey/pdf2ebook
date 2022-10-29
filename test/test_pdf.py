from unittest import TestCase

from pdf2ebook.pdf import PDF


class PDFTest(TestCase):

    def test_to_text(self):
        pass

    def test_to_html(self):
        pdf = PDF(path='test/resources/alice.pdf')
        pdf.load()
        self.assertEquals(len(pdf.pages), 21)

    def test_pages_context(self):
        pdf = PDF(path='test/resources/alice.pdf')
        pdf.load()
        self.assertEquals(
            pdf.pages._data[10].next_page.idx,
            pdf.pages._data[11].idx,
        )

    def test_pages_content(self):
        pdf = PDF(path='test/resources/alice.pdf')
        pdf.load()

        self.assertTrue(
            pdf.pages._data[0].text_content.startswith(
                '1'
            )
        )
        pdf.pages._data[0].text_content[21:35]

        self.assertTrue(
            'in Wonderland' in pdf.pages._data[0].text_content
        )

    def test_to_epub(self):
        pdf = PDF(path='test/resources/alice.pdf')
        pdf.load()
        pdf.to_epub('/tmp/test.epub')
