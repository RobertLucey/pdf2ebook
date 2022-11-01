from unittest import TestCase

from pdf2ebook.text_page import TextPage
from pdf2ebook.pages import Pages


class PagesTest(TestCase):

    def test_detect_header(self):
        pages = Pages()
        for i in range(100):
            pages.append(
                TextPage(0, 'Header\x0csomething\x0cblah\x0cfour\x0cfive\x0csix\x0cseven\x0ceight')
            )

        self.assertEqual(
            pages.detect_header(),
            'Header'
        )

    def test_detect_footer(self):
        pages = Pages()
        for i in range(100):
            pages.append(
                TextPage(0, f'Header\x0csomething\x0cblah\x0cfour\x0cfive\x0c{i}\x0c{i}\x0ceight')
            )

        self.assertEqual(
            pages.detect_footer(),
            'eight'
        )
