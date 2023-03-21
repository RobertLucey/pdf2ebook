import argparse

from pdf2ebook import logger

from pdf2ebook.utils import is_local_htmlex_ok, is_docker_installed
from pdf2ebook.pdf import PDF
from pdf2ebook.htmlex_pdf import HTMLEX_PDF


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--in", type=str, dest="in_file", required=True)
    parser.add_argument("--out", type=str, dest="out_file", required=True)
    parser.add_argument(
        "--force-html-ex",
        action="store_true",
        dest="force_html_ex",
    )
    parser.add_argument(
        "--force-html",
        action="store_true",
        dest="force_html",
    )
    parser.add_argument(
        "--force-text",
        action="store_true",
        dest="force_text",
    )
    parser.add_argument(
        "--title",
        type=str,
        dest="title",
        help="title of the book to get metadata from the internet / set metadata on the ebook",
    )
    args = parser.parse_args()

    if not args.force_text:
        args.force_text = None

    if not args.force_html:
        args.force_html = None

    if args.force_html_ex or (
        (is_local_htmlex_ok() or is_docker_installed())
        and not args.force_html
        and not args.force_text
    ):
        pdf = HTMLEX_PDF(
            path=args.in_file,
            title=args.title,
        )
        pdf.to_epub(path=args.out_file)
    else:
        logger.warning("Not using pdf2epubEX which is recommended")
        pdf = PDF(
            path=args.in_file,
            use_html_ex=args.force_html_ex,
            use_html=args.force_html,
            use_text=args.force_text,
            title=args.title,
        )
        pdf.to_epub(path=args.out_file)


if __name__ == "__main__":
    main()
