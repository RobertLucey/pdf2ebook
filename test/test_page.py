from unittest import TestCase

from pdf2ebook.page import Page, HTMLPage, GenericPage


class GenericPageTest(TestCase):

    def test_lang(self):
        page = GenericPage()
        page.text_content = 'This program converts files of one format into another'
        self.assertEqual(
            page.lang,
            'en'
        )

        page = GenericPage()
        page.text_content = "Ce programme convertit les fichiers d'un format dans un autre"
        self.assertEqual(
            page.lang,
            'fr'
        )


class PageTest(TestCase):

    def test_text_content(self):
        first = Page(1, 'one\x0ctwo\x0cthree\x0cfour\x0cfive\x0csix\x0cseven\x0ceight')
        second = Page(4, '')
        first.next_page = second
        self.assertEqual(
            first.text_content,
            'two\nthree\nfour'
        )

        first = Page(1, 'one\x0ctwo\x0cthree\x0cfour\x0cfive\x0csix\x0cseven\x0ceight')
        first.next_page = None
        self.assertEqual(
            first.text_content,
            'two\nthree\nfour\nfive\nsix\nseven\neight'
        )

    def test_page_no(self):
        first = Page(0, '2\nblah blah blah')
        self.assertEqual(
            first.page_no,
            2
        )

        first = Page(0, 'two\nblah blah blah')
        self.assertEqual(
            first.page_no,
            2
        )

        first = Page(0, 'blah\nblah blah blah\n2')
        self.assertEqual(
            first.page_no,
            2
        )

        first = Page(0, 'blah\nblah blah blah\ntwo')
        self.assertEqual(
            first.page_no,
            2
        )
