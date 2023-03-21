import os

from mock import patch
from unittest import TestCase

from pdf2ebook.pdf import PDF


class MobyDickPDFTest(TestCase):
    PDF_PATH = "test/resources/moby_dick.pdf"
    EPUB_NAME = "test_moby_dick.epub"
    EXPECTED_PAGES = 7

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

        self.assertEquals(pdf.get_expected_title(), "moby dick")

    def test_detect_footer(self):
        pdf = PDF(path=self.PDF_PATH)
        pdf.load()
        self.assertEquals(
            pdf.pages.detect_footer(), "Created for Lit2Go on the web at etc.usf.edu"
        )

    def test_detect_header(self):
        pdf = PDF(path=self.PDF_PATH)
        pdf.load()
        self.assertEquals(
            pdf.pages.detect_header(), "Moby Dick:\xa0Chapter 1\xa0by Herman Melville"
        )

    def test_remove_page_number(self):
        pdf = PDF(path=self.PDF_PATH)
        pdf.load()

        last_hash = None
        while last_hash != pdf.content_hash:
            last_hash = pdf.content_hash
            pdf.pages.set_page_number_position()
            header = pdf.pages.detect_header()
            footer = pdf.pages.detect_footer()
            for page in pdf.pages:
                page.remove_page_number()
                page.remove_header(header)
                page.remove_footer(footer)

        pdf.pages.set_page_number_position()
        self.assertEquals(
            pdf.pages[1].content,
            """Circumambulate the city of a dreamy Sabbath afternoon. Go from <br/>Corlears Hook to Coenties Slip, and from thence, by Whitehall, <br/>northward. What do you see?- Posted like silent sentinels all around the <br/>town, stand thousands upon thousands of mortal men fixed in ocean <br/>reveries. Some leaning against the spiles; some seated upon the pier-<br/>heads; some looking over the bulwarks of ships from China; some high <br/>aloft in the rigging, as if striving to get a still better seaward peep. But <br/>these are all landsmen; of week days pent up in lath and plaster- tied to <br/>counters, nailed to benches, clinched to desks. How then is this? Are the <br/>green fields gone? What do they here?<br/>
But look! here come more crowds, pacing straight for the water, and <br/>seemingly bound for a dive. Strange! Nothing will content them but the <br/>extremest limit of the land; loitering under the shady lee of yonder <br/>warehouses will not suffice. No. They must get just as nigh the water as <br/>they possibly can without falling And there they stand- miles of them- <br/>leagues. Inlanders all, they come from lanes and alleys, streets avenues- <br/>north, east, south, and west. Yet here they all unite. Tell me, does the <br/>magnetic virtue of the needles of the compasses of all those ships attract <br/>them thither?<br/>
Once more. Say you are in the country; in some high land of lakes. Take <br/>almost any path you please, and ten to one it carries you down in a dale, <br/>and leaves you there by a pool in the stream. There is magic in it. Let the <br/>most absent-minded of men be plunged in his deepest reveries- stand <br/>that man on his legs, set his feet a-going, and he will infallibly lead you <br/>to water, if water there be in all that region. Should you ever be athirst in <br/>the great American desert, try this experiment, if your caravan happen to <br/>be supplied with a metaphysical professor. Yes, as every one knows, <br/>meditation and water are wedded for ever.<br/>
But here is an artist. He desires to paint you the dreamiest, shadiest, <br/>quietest, most enchanting bit of romantic landscape in all the valley of <br/>the Saco. What is the chief element he employs? There stand his trees, <br/>""",
        )

    def test_page_number_position(self):
        pdf = PDF(path=self.PDF_PATH)
        pdf.load()

        last_hash = None
        while last_hash != pdf.content_hash:
            last_hash = pdf.content_hash
            pdf.pages.set_page_number_position()
            header = pdf.pages.detect_header()
            footer = pdf.pages.detect_footer()
            for page in pdf.pages:
                page.remove_page_number()
                page.remove_header(header)
                page.remove_footer(footer)

        pdf.pages.set_page_number_position()
        self.assertEquals(pdf.pages[0].page_number_position, "bottom")

    def test_pages_content(self):
        pdf = PDF(path=self.PDF_PATH)
        pdf.load()

        self.assertEquals(
            pdf.pages._data[1].text_content,
            """Moby Dick: Chapter 1 by Herman Melville
Circumambulate the city of a dreamy Sabbath afternoon. Go from Corlears Hook to Coenties Slip, and from thence, by Whitehall, northward. What do you see?- Posted like silent sentinels all around the town, stand thousands upon thousands of mortal men fixed in ocean reveries. Some leaning against the spiles; some seated upon the pier-heads; some looking over the bulwarks of ships from China; some high aloft in the rigging, as if striving to get a still better seaward peep. But these are all landsmen; of week days pent up in lath and plaster- tied to counters, nailed to benches, clinched to desks. How then is this? Are the green fields gone? What do they here?
But look! here come more crowds, pacing straight for the water, and seemingly bound for a dive. Strange! Nothing will content them but the extremest limit of the land; loitering under the shady lee of yonder warehouses will not suffice. No. They must get just as nigh the water as they possibly can without falling And there they stand- miles of them- leagues. Inlanders all, they come from lanes and alleys, streets avenues- north, east, south, and west. Yet here they all unite. Tell me, does the magnetic virtue of the needles of the compasses of all those ships attract them thither?
Once more. Say you are in the country; in some high land of lakes. Take almost any path you please, and ten to one it carries you down in a dale, and leaves you there by a pool in the stream. There is magic in it. Let the most absent-minded of men be plunged in his deepest reveries- stand that man on his legs, set his feet a-going, and he will infallibly lead you to water, if water there be in all that region. Should you ever be athirst in the great American desert, try this experiment, if your caravan happen to be supplied with a metaphysical professor. Yes, as every one knows, meditation and water are wedded for ever.
But here is an artist. He desires to paint you the dreamiest, shadiest, quietest, most enchanting bit of romantic landscape in all the valley of the Saco. What is the chief element he employs? There stand his trees, 
2
Created for Lit2Go on the web at etc.usf.edu""",
        )

    def test_pages_cleaned_content(self):
        pdf = PDF(path=self.PDF_PATH)
        pdf.load()

        self.assertEquals(
            pdf.pages._data[1].cleaned_text_content,
            """Moby Dick: Chapter 1 by Herman Melville
Circumambulate the city of a dreamy Sabbath afternoon. Go from Corlears Hook to Coenties Slip, and from thence, by Whitehall, northward. What do you see?- Posted like silent sentinels all around the town, stand thousands upon thousands of mortal men fixed in ocean reveries. Some leaning against the spiles; some seated upon the pier-heads; some looking over the bulwarks of ships from China; some high aloft in the rigging, as if striving to get a still better seaward peep. But these are all landsmen; of week days pent up in lath and plaster- tied to counters, nailed to benches, clinched to desks. How then is this? Are the green fields gone? What do they here?
But look! here come more crowds, pacing straight for the water, and seemingly bound for a dive. Strange! Nothing will content them but the extremest limit of the land; loitering under the shady lee of yonder warehouses will not suffice. No. They must get just as nigh the water as they possibly can without falling And there they stand- miles of them- leagues. Inlanders all, they come from lanes and alleys, streets avenues- north, east, south, and west. Yet here they all unite. Tell me, does the magnetic virtue of the needles of the compasses of all those ships attract them thither?
Once more. Say you are in the country; in some high land of lakes. Take almost any path you please, and ten to one it carries you down in a dale, and leaves you there by a pool in the stream. There is magic in it. Let the most absent-minded of men be plunged in his deepest reveries- stand that man on his legs, set his feet a-going, and he will infallibly lead you to water, if water there be in all that region. Should you ever be athirst in the great American desert, try this experiment, if your caravan happen to be supplied with a metaphysical professor. Yes, as every one knows, meditation and water are wedded for ever.
But here is an artist. He desires to paint you the dreamiest, shadiest, quietest, most enchanting bit of romantic landscape in all the valley of the Saco. What is the chief element he employs? There stand his trees,
2
Created for Lit2Go on the web at etc.usf.edu""",
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
            os.remove(f"/tmp/{self.EPUB_NAME}")
        except:
            pass
        pdf.to_epub(f"/tmp/{self.EPUB_NAME}")
        self.assertTrue(os.path.exists(f"/tmp/{self.EPUB_NAME}"))

    def test_to_html(self):
        pdf = PDF(path=self.PDF_PATH)
        pdf.load()
        self.assertEquals(len(pdf.pages), self.EXPECTED_PAGES)
        self.assertGreater(os.path.getsize(f"/tmp/{self.EPUB_NAME}"), 0)
