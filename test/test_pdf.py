import os

from unittest import TestCase

from pdf2ebook.pdf import PDF


class AlicePDFTest(TestCase):

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

        self.assertTrue(
            'in Wonderland' in pdf.pages._data[0].text_content
        )

    def test_to_epub(self):
        pdf = PDF(path='test/resources/alice.pdf')
        pdf.load()
        try:
            os.remove('/tmp/test_alice.epub')
        except:
            pass
        pdf.to_epub('/tmp/test_alice.epub')
        self.assertTrue(
            os.path.exists('/tmp/test_alice.epub')
        )


class VortexPDFTest(TestCase):

    def test_to_text(self):
        pass

    def test_to_html(self):
        pdf = PDF(path='test/resources/vortex.pdf')
        pdf.load()
        self.assertEquals(len(pdf.pages), 16)

    def test_pages_context(self):
        pdf = PDF(path='test/resources/vortex.pdf')
        pdf.load()
        self.assertEquals(
            pdf.pages._data[10].next_page.idx,
            pdf.pages._data[11].idx,
        )

    def test_pages_content(self):
        pdf = PDF(path='test/resources/vortex.pdf')
        pdf.load()

        self.assertTrue(
            pdf.pages._data[0].text_content.startswith(
                'INTRODUCING'
            )
        )

    def test_to_epub(self):
        pdf = PDF(path='test/resources/vortex.pdf')
        pdf.load()
        try:
            os.remove('/tmp/test_vortex.epub')
        except:
            pass
        pdf.to_epub('/tmp/test_vortex.epub')


class RoomWithAViewPDFTest(TestCase):

    def test_to_text(self):
        pass

    def test_to_html(self):
        pdf = PDF(path='test/resources/room_with_a_view.pdf')
        pdf.load()
        self.assertEquals(len(pdf.pages), 151)

    def test_pages_context(self):
        pdf = PDF(path='test/resources/room_with_a_view.pdf')
        pdf.load()
        self.assertEquals(
            pdf.pages._data[10].next_page.idx,
            pdf.pages._data[11].idx,
        )

    def test_pages_content(self):
        pdf = PDF(path='test/resources/room_with_a_view.pdf')
        pdf.load()

        self.assertTrue(
            pdf.pages._data[0].text_content.startswith(
                'A ROOM'
            )
        )

    def test_to_epub(self):
        pdf = PDF(path='test/resources/room_with_a_view.pdf')
        pdf.load()
        try:
            os.remove('/tmp/test_room_with_a_view.epub')
        except:
            pass
        pdf.to_epub('/tmp/test_room_with_a_view.epub')
