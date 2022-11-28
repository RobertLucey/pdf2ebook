import os

from mock import patch
from unittest import TestCase, skip

from pdf2ebook.htmlex_pdf import HTMLEX_PDF


class AlicePDFEXTest(TestCase):

    PDF_PATH = "test/resources/alice_in_wonderland.pdf"
    EPUB_NAME = "test_alice.epub"
    EXPECTED_PAGES = 21

    def test_get_thumbnail_url(self):
        pdf = HTMLEX_PDF(path=self.PDF_PATH)
        pdf.to_epub(path=f"/tmp/{self.EPUB_NAME}")
        self.assertIsNotNone(pdf.get_thumbnail_url())

    @skip("page number functionality not yet implemented")
    def test_get_expected_title(self):
        pdf = HTMLEX_PDF(path=self.PDF_PATH)
        pdf.to_epub(path=f"/tmp/{self.EPUB_NAME}")

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

        self.assertEquals(pdf.get_expected_title(), "alice's adventures in wonderland")

    def test_detect_footer(self):
        pdf = HTMLEX_PDF(path=self.PDF_PATH)
        pdf.to_epub(path=f"/tmp/{self.EPUB_NAME}")
        self.assertEquals(pdf.pages.detect_footer(), None)

    def test_detect_header(self):
        pdf = HTMLEX_PDF(path=self.PDF_PATH)
        pdf.to_epub(path=f"/tmp/{self.EPUB_NAME}")
        self.assertEquals(pdf.pages.detect_header(), None)

    @skip("complex xml, skipping for now")
    def test_remove_page_number(self):
        pdf = HTMLEX_PDF(path=self.PDF_PATH)
        pdf.to_epub(path=f"/tmp/{self.EPUB_NAME}")
        pdf.pages.set_page_number_position()
        pdf.pages[0].remove_page_number()
        self.assertEquals(
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

    @skip("page number functionality not yet implemented")
    def test_page_number_position(self):
        pdf = HTMLEX_PDF(path=self.PDF_PATH)
        pdf.to_epub(path=f"/tmp/{self.EPUB_NAME}")
        pdf.pages.set_page_number_position()
        self.assertEquals(pdf.pages[0].page_number_position, "top")

    @skip("page number functionality not yet implemented")
    def test_page_without_page_no(self):
        pdf = HTMLEX_PDF(path=self.PDF_PATH)
        pdf.to_epub(path=f"/tmp/{self.EPUB_NAME}")
        pdf.pages.set_page_number_position()
        self.assertEquals(
            pdf.pages[0].text_content_without_page_no.strip(),
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
        pdf = HTMLEX_PDF(path=self.PDF_PATH)
        pdf.to_epub(path=f"/tmp/{self.EPUB_NAME}")

        self.assertEquals(
            pdf.pages._data[0].text_content.strip().replace("\xa0", " "),
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
feel very sleepy and stupid), whether the pleasure of making a daisy-chain would be""".replace(
                "\xa0", " "
            ),
        )

    def test_pages_cleaned_content(self):
        pdf = HTMLEX_PDF(path=self.PDF_PATH)
        pdf.to_epub(path=f"/tmp/{self.EPUB_NAME}")

        self.assertEquals(
            pdf.pages._data[0].cleaned_text_content.strip().replace("\xa0", " "),
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
feel very sleepy and stupid), whether the pleasure of making a daisy-chain would be""".replace(
                "\xa0", " "
            ),
        )

    def test_pages_context(self):
        # TODO: need to set_context at some point
        pdf = HTMLEX_PDF(path=self.PDF_PATH)
        pdf.to_epub(path=f"/tmp/{self.EPUB_NAME}")
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
        pdf = HTMLEX_PDF(path=self.PDF_PATH)
        pdf.to_epub(path=f"/tmp/{self.EPUB_NAME}")
        try:
            os.remove(f"/tmp/{self.EPUB_NAME}")
        except:
            pass
        pdf.to_epub(f"/tmp/{self.EPUB_NAME}")
        self.assertTrue(os.path.exists(f"/tmp/{self.EPUB_NAME}"))

    def test_to_html(self):
        pdf = HTMLEX_PDF(path=self.PDF_PATH)
        pdf.to_epub(path=f"/tmp/{self.EPUB_NAME}")
        self.assertEquals(len(pdf.pages), self.EXPECTED_PAGES)
        self.assertGreater(os.path.getsize(f"/tmp/{self.EPUB_NAME}"), 0)
