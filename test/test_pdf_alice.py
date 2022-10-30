import os

from unittest import TestCase

from pdf2ebook.pdf import PDF


class AlicePDFTest(TestCase):

    PDF_PATH = 'test/resources/alice.pdf'
    EPUB_NAME = 'test_alice.epub'
    EXPECTED_PAGES = 21

    def test_pages_content(self):
        pdf = PDF(path=self.PDF_PATH)
        pdf.load()

        self.assertEquals(
            pdf.pages._data[0].text_content,
            '''1
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
feel very sleepy and stupid), whether the pleasure of making a daisy-chain would be'''
        )

    def test_pages_cleaned_content(self):
        pdf = PDF(path=self.PDF_PATH)
        pdf.load()

        self.assertEquals(
            pdf.pages._data[0].cleaned_text_content,
            '''1
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
feel very sleepy and stupid), whether the pleasure of making a daisy-chain would be'''
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
