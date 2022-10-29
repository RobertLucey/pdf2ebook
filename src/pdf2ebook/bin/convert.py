import argparse

from pdf2ebook.pdf import PDF


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--in", type=str, dest="in_file", required=True)
    parser.add_argument("--out", type=str, dest="out_file", required=True)
    args = parser.parse_args()

    pdf = PDF(path=args.in_file)
    pdf.load()
    pdf.to_epub(path=args.out_file)


if __name__ == "__main__":
    main()
