import os

from mock import patch
from unittest import TestCase

from pdf2ebook.pdf import PDF


class AlicePDFTest(TestCase):
    PDF_PATH = "test/resources/alice_in_wonderland.pdf"
    EPUB_NAME = "test_alice.epub"
    EXPECTED_PAGES = 21

    def test_get_thumbnail_url(self):
        pdf = PDF(path=self.PDF_PATH)
        pdf.load()
        self.assertIsNotNone(pdf.get_thumbnail_url())

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

        self.assertEqual(pdf.get_expected_title(), "alice's adventures in wonderland")

    def test_detect_footer(self):
        pdf = PDF(path=self.PDF_PATH)
        pdf.load()
        self.assertEqual(pdf.pages.detect_footer(), None)

    def test_detect_header(self):
        pdf = PDF(path=self.PDF_PATH)
        pdf.load()
        self.assertEqual(pdf.pages.detect_header(), None)

    def test_remove_page_number(self):
        pdf = PDF(path=self.PDF_PATH)
        pdf.load()
        pdf.pages.set_page_number_position()
        pdf.pages[0].remove_page_number()
        self.assertEqual(
            pdf.pages[0].content,
            """<b>Alice's Adventures in Wonderland </b><br/>
<b>by </b><br/>
<b>Lewis Carroll </b><br/>
 <br/>
<b>CHAPTER I</b> <br/>
  <br/>
<i><b>DOWN THE RABBIT-HOLE</b></i> <br/>
    <br/>
ALICE was beginning to get very tired of sitting by her sister on the bank and of having <br/>
nothing to do: once or twice she had peeped into the book her sister was reading, but it <br/>
had no pictures or conversations in it, "and what is the use of a book," thought Alice, <br/>
"without pictures or conversations?'   <br/>
So she was considering, in her own mind (as well as she could, for the hot day made her <br/>
feel very sleepy and stupid), whether the pleasure of making a daisy-chain would be <br/>""",
        )

    def test_page_number_position(self):
        pdf = PDF(path=self.PDF_PATH)
        pdf.load()
        pdf.pages.set_page_number_position()
        self.assertEqual(pdf.pages[0].page_number_position, "top")

    def test_page_without_page_no(self):
        pdf = PDF(path=self.PDF_PATH)
        pdf.load()
        pdf.pages.set_page_number_position()
        self.assertEqual(
            pdf.pages[0].text_content_without_page_no,
            """Alice's Adventures in Wonderland
by
Lewis Carroll

CHAPTER I

DOWN THE RABBIT-HOLE

ALICE was beginning to get very tired of sitting by her sister on the bank and of having
nothing to do: once or twice she had peeped into the book her sister was reading, but it
had no pictures or conversations in it, "and what is the use of a book," thought Alice,
"without pictures or conversations?'
So she was considering, in her own mind (as well as she could, for the hot day made her
feel very sleepy and stupid), whether the pleasure of making a daisy-chain would be""",
        )

    def test_pages_content(self):
        pdf = PDF(path=self.PDF_PATH)
        pdf.load()

        self.assertEqual(
            pdf.pages._data[0].text_content,
            """1
Alice's Adventures in Wonderland 
by 
Lewis Carroll 
 
CHAPTER I 
  
DOWN THE RABBIT-HOLE 
    
ALICE was beginning to get very tired of sitting by her sister on the bank and of having 
nothing to do: once or twice she had peeped into the book her sister was reading, but it 
had no pictures or conversations in it, "and what is the use of a book," thought Alice, 
"without pictures or conversations?'   
So she was considering, in her own mind (as well as she could, for the hot day made her 
feel very sleepy and stupid), whether the pleasure of making a daisy-chain would be""",
        )

    def test_pages_cleaned_content(self):
        pdf = PDF(path=self.PDF_PATH)
        pdf.load()

        self.assertEqual(
            pdf.pages._data[0].cleaned_text_content,
            """1
Alice's Adventures in Wonderland
by
Lewis Carroll

CHAPTER I

DOWN THE RABBIT-HOLE

ALICE was beginning to get very tired of sitting by her sister on the bank and of having
nothing to do: once or twice she had peeped into the book her sister was reading, but it
had no pictures or conversations in it, "and what is the use of a book," thought Alice,
"without pictures or conversations?'
So she was considering, in her own mind (as well as she could, for the hot day made her
feel very sleepy and stupid), whether the pleasure of making a daisy-chain would be""",
        )

    def test_pages_context(self):
        pdf = PDF(path=self.PDF_PATH)
        pdf.load()
        for i in range(len(pdf.pages)):
            if i == len(pdf.pages) - 1:
                self.assertEqual(
                    pdf.pages._data[i].next_page,
                    None,
                )
            else:
                self.assertEqual(
                    pdf.pages._data[i].next_page.idx,
                    pdf.pages._data[i + 1].idx,
                )

    def test_to_epub(self):
        pdf = PDF(path=self.PDF_PATH)
        pdf.load()
        try:
            os.remove(f"/tmp/{self.EPUB_NAME}")
        except:
            pass
        pdf.to_epub(f"/tmp/{self.EPUB_NAME}")
        self.assertTrue(os.path.exists(f"/tmp/{self.EPUB_NAME}"))
        self.assertGreater(os.path.getsize(f"/tmp/{self.EPUB_NAME}"), 0)

    def test_to_html(self):
        pdf = PDF(path=self.PDF_PATH)
        pdf.load()
        self.assertEqual(len(pdf.pages), self.EXPECTED_PAGES)
