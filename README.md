PDF2EBook
=========

Convert pdfs to an epub, geared towards books. Adds cover, metadata like author / title / isbn


Dependencies
------------

Poppler - `sudo apt install libpoppler-cpp-dev`

PDFToHTML - `sudo apt install pdftohtml`

pdf2epubEX (recommended) - https://github.com/dodeeric/pdf2epubEX

Docker (if you don't want to install pdf2epubEX directly)


Installation
------------

`pip install pdf2ebook`


Usage
-----

`pdf2epub --in something.pdf --out other.epub --title "Optional but helpful title"`
