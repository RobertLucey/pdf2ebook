from unittest import TestCase

from pdf2ebook.utils import window, get_isbn, isbns_from_words, remove_page_no


class UtilsTest(TestCase):
    def test_window(self):
        self.assertEquals(list(window([1, 2, 3], window_size=1)), [(1,), (2,), (3,)])
        self.assertEquals(list(window([1, 2, 3], window_size=2)), [(1, 2), (2, 3)])
        self.assertEquals(list(window([1, 2, 3], window_size=3)), [(1, 2, 3)])
        self.assertEquals(list(window([1, 2, 3], window_size=4)), [])

    def test_get_isbn(self):
        self.assertEquals(
            get_isbn(""" blah 123 23refw"""),
            None,
        )
        self.assertEquals(
            get_isbn(""" blah 123 23refw 978-1-86197-876-9 qdfwe90"""),
            "978-1-86197-876-9",
        )
        self.assertEquals(
            get_isbn(
                """ blah 123 23refw 978-1-86197-876-9 qdfwe90 978-1-86197-876-8"""
            ),
            "978-1-86197-876-9",
        )

    def test_isbns_from_words(self):
        isbns = isbns_from_words("The old man and the sea")
        self.assertGreater(len(isbns), 1)

    def test_remove_page_no(self):
        self.assertEquals(remove_page_no("123 something 123"), "something")
        self.assertEquals(remove_page_no("123 something"), "something")
        self.assertEquals(remove_page_no("something 123"), "something")
