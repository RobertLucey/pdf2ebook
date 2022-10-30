import argparse

from pdf2ebook.pdf import PDF


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--in", type=str, dest="in_file", required=True)
    parser.add_argument("--out", type=str, dest="out_file", required=True)
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
    args = parser.parse_args()

    if not args.force_text:
        args.force_text = None

    if not args.force_html:
        args.force_html = None

    pdf = PDF(path=args.in_file, use_html=args.force_html, use_text=args.force_text)
    pdf.to_epub(path=args.out_file)


if __name__ == "__main__":
    main()
