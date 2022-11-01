import os

from unittest import TestCase, skip

from PIL import Image

from pdf2ebook.text_page import TextPage
from pdf2ebook.html_page import HTMLPage
from pdf2ebook.base_page import BasePage


class BasePageTest(TestCase):

    def test_lang(self):
        page = BasePage()
        page.text_content = 'This program converts files of one format into another'
        self.assertEqual(
            page.lang,
            'en'
        )

        page = BasePage()
        page.text_content = "Ce programme convertit les fichiers d'un format dans un autre"
        self.assertEqual(
            page.lang,
            'fr'
        )

        page = BasePage()
        page.text_content = ""
        self.assertEqual(
            page.lang,
            None
        )


class TextPageTest(TestCase):

    def test_remove_footer(self):
        page = TextPage(0, 'something blah blah\x0cother stuff\x0cFooter')
        page.remove_header('Footer')

        self.assertEqual(
            page.text_content,
            'something blah blah\nother stuff'
        )

    def test_remove_header(self):
        page = TextPage(0, 'Header\x0csomething blah blah\x0cother stuff')
        page.remove_header('Header')

        self.assertEqual(
            page.text_content,
            'something blah blah\nother stuff'
        )

    def test_text_content(self):
        first = TextPage(1, 'one\x0ctwo\x0cthree\x0cfour\x0cfive\x0csix\x0cseven\x0ceight')
        second = TextPage(4, '')
        first.set_next_page(second)
        self.assertEqual(
            first.text_content,
            'two\nthree\nfour'
        )

        first = TextPage(1, 'one\x0ctwo\x0cthree\x0cfour\x0cfive\x0csix\x0cseven\x0ceight')
        first.set_next_page(None)
        self.assertEqual(
            first.text_content,
            'two\nthree\nfour\nfive\nsix\nseven\neight'
        )

    def test_page_no(self):
        first = TextPage(0, 'blah blah blah')
        self.assertEqual(
            first.page_no,
            None
        )

        first = TextPage(0, '2\nblah blah blah')
        self.assertEqual(
            first.page_no,
            2
        )

        first = TextPage(0, 'two\nblah blah blah')
        self.assertEqual(
            first.page_no,
            2
        )

        first = TextPage(0, 'blah\nblah blah blah\n2')
        self.assertEqual(
            first.page_no,
            2
        )

        first = TextPage(0, 'blah\nblah blah blah\ntwo')
        self.assertEqual(
            first.page_no,
            2
        )

    def test_html_content(self):
        first = TextPage(0, 'blah\n\nblah blah blah')
        self.assertEqual(
            first.html_content,
            '<p>blah</p><p>blah blah blah</p>'
        )

    def test_epub_content(self):
        first = TextPage(0, 'blah\n\nblah blah blah')
        self.assertEqual(
            first.epub_content.content,
            '<p>blah</p><p>blah blah blah</p><span xmlns:epub="http://www.idpf.org/2007/ops" epub:type="pagebreak" title="p_0" id="p_0"/>'
        )


class HTMLPageTest(TestCase):

    def test_images(self):
        try:
            os.remove("/tmp/pdf2ebook_test_images.png")
        except:
            pass

        image = Image.new('RGB', (1, 1))
        image.save("/tmp/pdf2ebook_test_images.png", "PNG")

        page = HTMLPage(0, '<img src="/tmp/pdf2ebook_test_images.png"></img>')
        self.assertEqual(
            len(page.images),
            1
        )

    @skip('Need to implement')
    def test_page_no(self):
        pass

    def test_html_content(self):
        page = HTMLPage(0, '<p>something something</p>')
        self.assertEqual(
            page.html_content,
            '<p>something something</p>'
        )

        page = HTMLPage(0, '<p>something something</p><img src="/tmp/test_images.png"></img>')
        self.assertEqual(
            page.html_content,
            '<p>something something</p><img src="test_images.png"/>'
        )

    def test_remove_header(self):
        page = HTMLPage(0, '<p>something</p>\nBlah blah</br>')
        page.remove_header('something')
        self.assertEquals(
            page.text_content,
            'Blah blah'
        )

    def test_remove_footer(self):
        page = HTMLPage(0, '<p>something</p>\nBlah blah</br>')
        page.remove_footer('Blah blah')
        self.assertEquals(
            page.text_content,
            'something'
        )
