import os
import shutil
import glob

from pdf2ebook import logger


class HTMLEX_PDF:

    ROOT = "/tmp/book"
    META_INF = f"{ROOT}/META-INF"
    OEBPS = f"{ROOT}/OEBPS"
    MIMETYPE = f"{ROOT}/mimetype"
    CONTAINER = f"{META_INF}/container.xml"
    NAV = f"{OEBPS}/nav.xhtml"
    CONTENT = f"{OEBPS}/content.opf"

    def __init__(self, *args, **kwargs):
        self.pdf_path = kwargs["path"]
        self.dot_pages = []
        self.tmp_path = os.path.join('/tmp/', os.path.basename(self.pdf_path))
        shutil.copyfile(self.pdf_path, self.tmp_path)

    @property
    def content_hash(self):
        raise NotImplementedError()

    def modify_pages(self):
        logger.info("Modifying pages")
        for page in sorted(os.listdir()):
            if not page.endswith(".page"):
                continue
            head = """<?xml version=\"1.0\" encoding=\"UTF-8\"?>
<html xmlns:epub=\"http://www.idpf.org/2007/ops\" xmlns=\"http://www.w3.org/1999/xhtml\">
<head>
  <meta charset=\"UTF-8\"/>
  <meta name=\"generator\" content=\"pdf2htmlEX\"/>
  <link rel=\"stylesheet\" type=\"text/css\" href=\"base.min.css\"/>
  <link rel=\"stylesheet\" type=\"text/css\" href=\"style.css\"/>
  <meta name=\"viewport\" content=\"width=900, height=1164\"/>
  <title>title</title>
  </head>
<body>
<div id=\"page-container\">"""
            page_content = open(page, "r").read()
            foot = """</div>
</body>
</html>"""
            content = head + page_content + foot
            with open(page, "w") as f:
                f.write(content)
            logger.debug(f'Move: {page} -> {os.path.splitext(page)[0] + ".xhtml"}')
            os.rename(page, os.path.splitext(page)[0] + ".xhtml")
            self.dot_pages.append((page, page.replace(".page", "").replace("convertedbook", "")))  # FIXME: icky

    def create_structure(self):
        logger.info("Creating structure")
        try:
            shutil.rmtree(self.ROOT)
        except:
            pass

        logger.debug(f'mkdir: {self.ROOT}')
        os.mkdir(self.ROOT)
        logger.debug(f'mkdir: {self.META_INF}')
        os.mkdir(self.META_INF)
        logger.debug(f'mkdir: {self.OEBPS}')
        os.mkdir(self.OEBPS)

    def move_to_oebps(self):
        logger.info("Move to oebps")
        for data in sorted(glob.glob("*.css")):
            logger.debug(f'Move: {data} -> {self.OEBPS}')
            shutil.move(data, self.OEBPS)
        for data in sorted(glob.glob("*.woff")):
            logger.debug(f'Move: {data} -> {self.OEBPS}')
            shutil.move(data, self.OEBPS)
        for data in sorted(glob.glob("*.xhtml")):
            logger.debug(f'Move: {data} -> {self.OEBPS}')
            shutil.move(data, self.OEBPS)

        for data in sorted(glob.glob("*.png")):
            logger.debug(f'Move: {data} -> {self.OEBPS}')
            shutil.move(data, self.OEBPS)
        for data in sorted(glob.glob("*.jpg")):
            logger.debug(f'Move: {data} -> {self.OEBPS}')
            shutil.move(data, self.OEBPS)
        for data in sorted(glob.glob("*.svg")):
            logger.debug(f'Move: {data} -> {self.OEBPS}')
            shutil.move(data, self.OEBPS)

    def write_mimetype(self):
        logger.info("Write mimetype")

        logger.debug(f"Write: {self.MIMETYPE}")
        with open(self.MIMETYPE, "w") as f:
            f.write("application/epub+zip")

    def write_container(self):
        logger.info("Write container")

        logger.debug(f"Write: {self.CONTAINER}")
        with open(self.CONTAINER, "w") as f:
            f.write(
                """<?xml version=\"1.0\" encoding=\"UTF-8\"?>
<container version=\"1.0\" xmlns=\"urn:oasis:names:tc:opendocument:xmlns:container\">
  <rootfiles>
    <rootfile full-path=\"OEBPS/content.opf\" media-type=\"application/oebps-package+xml\"/>
  </rootfiles>
</container>"""
            )

    def write_nav(self):
        logger.info("Write nav")

        logger.debug(f"Write: {self.NAV}")
        with open(self.NAV, "w") as f:
            f.write(
                """<?xml version=\"1.0\" encoding=\"UTF-8\"?>
<html xmlns:epub=\"http://www.idpf.org/2007/ops\"   xmlns=\"http://www.w3.org/1999/xhtml\">
<head>
  <title>title</title>
</head>
<body>
  <nav epub:type=\"toc\" id=\"toc\">
    <ol>
      <li>
        <a href=\"convertedbook0001.xhtml\">Chapter 1 Like This</a>
      </li>
      <li>
        <a href=\"convertedbook0002.xhtml\">Chapter 2 Like This</a>
      </li>
    </ol>
  </nav>
  <nav epub:type=\"landmarks\">
    <ol>
      <li>
        <a epub:type=\"frontmatter\" href=\"convertedbook0001.xhtml\">Cover</a>
      </li>
      <li>
        <a epub:type=\"bodymatter\" href=\"convertedbook0002.xhtml\">Bodymatter</a>
      </li>
    </ol>
  </nav>
  <nav epub:type=\"page-list\" hidden=\"\">
  <ol>"""
            )

            for page in sorted(self.dot_pages):
                logger.debug(f'Add page: href={page[0]}   content={page[1]}')
                f.write(f'   <li>\n    <a href="{page[0]}">{page[1]}</a>\n   </li>')

            f.write(
                """  </ol>
  </nav>
</body>
</html>"""
            )

    def write_content(self):
        logger.info("Write content")

        logger.debug(f'Write: {self.CONTENT}')
        with open(self.CONTENT, "w") as f:
            content = """<?xml version=\"1.0\" encoding=\"UTF-8\"?>
<package xmlns=\"http://www.idpf.org/2007/opf\" prefix=\"rendition: http://www.idpf.org/vocab/rendition/#\" unique-identifier=\"pub-id\" version=\"3.0\">
  <metadata xmlns:dc=\"http://purl.org/dc/elements/1.1/\">
    <dc:identifier id=\"pub-id\">isbn</dc:identifier>
    <dc:title>title</dc:title>
    <dc:creator>author</dc:creator>
    <dc:publisher>publisher</dc:publisher>
    <dc:language>language</dc:language>
    <dc:subject>tags</dc:subject>
    <dc:date>year</dc:date>
    <dc:description>description</dc:description>
    <meta name=\"cover\" content=\"cover-image\"/>
    <meta property=\"dcterms:modified\">date</meta>
    <meta property=\"rendition:layout\">pre-paginated</meta>
    <meta property=\"rendition:spread\">auto</meta>
  </metadata>
  <manifest>"""

            f.write(content)

            for data in sorted(glob.glob(f"{self.OEBPS}/*.xhtml")):
                logger.debug(f'Add page: id={os.path.splitext(os.path.basename(data))[0]}   href={os.path.basename(data)}')
                f.write(
                    f'    <item id="{os.path.splitext(os.path.basename(data))[0]}" href="{os.path.basename(data)}" media-type="application/xhtml+xml"/>\n'
                )

            # TODO: for png, svg, jpg as well as xhtml

            f.write(
                '    <item id="base-min-css" href="base.min.css" media-type="text/css"/>'
            )
            f.write(
                '    <item id="style-css" href="style.css" media-type="text/css"/>'
            )
            f.write(
                '    <item id="cover-image" href="cover.png" media-type="image/png" properties="cover-image"/>'
            )

            f.write(
                '''    <item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>
  </manifest>
  <spine>'''
            )
            for data in sorted(glob.glob(f"{self.OEBPS}/*.xhtml")):
                logger.debug(f'Write spine item: {os.path.splitext(os.path.basename(data))[0]}')
                f.write(
                    f'    <itemref idref="{os.path.splitext(os.path.basename(data))[0]}" properties="rendition:layout-pre-paginated"/>\n'
                )
            f.write(
                '''  </spine>
  <guide>
    <reference type="cover" title="Cover" href="convertedbook0001.xhtml"/>
    <reference type="text" title="Text" href="convertedbook0002.xhtml"/>
  </guide>
</package>'''
            )

    def write_cover(self):
        os.system(f"pdftoppm {self.tmp_path} cover -cropbox -png -f 1 -singlefile")

        logger.debug(f'Move: cover.png -> {self.OEBPS}')
        shutil.move("cover.png", self.OEBPS)

    def to_html(self):
        os.system(
            f"pdf2htmlEX --quiet 1 --embed-css 0 --embed-font 0 --embed-image 0 --embed-javascript 0 --embed-outline 0 --split-pages 1 --page-filename convertedbook%04d.page --css-filename style.css {self.tmp_path}"
        )

    def to_epub(self, path=None):

        self.to_html()
        self.modify_pages()
        self.create_structure()
        self.write_mimetype()
        self.move_to_oebps()
        self.write_container()
        self.write_nav()
        self.write_content()
        self.write_cover()

        # TODO: merge pwd with path

        dir_path = os.path.dirname(os.path.realpath(__file__))

        path_to_out_epub = os.path.join(dir_path, path)

        os.system(
            f"cd /tmp/book && zip -0Xq {path_to_out_epub} ./mimetype && zip -Xr9Dq {path_to_out_epub} ./* -x ./mimetype -x {path_to_out_epub}"
        )

        logger.debug(f"Epub saved: {path_to_out_epub}")
