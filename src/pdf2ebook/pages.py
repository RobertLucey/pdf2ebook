import re
from collections import Counter

from pdf2ebook import logger
from pdf2ebook.utils import window


class Pages:
    def __init__(self, *args, **kwargs):
        self._data = []

    def append(self, item):
        self._data.append(item)

    def __len__(self):
        return len(self._data)

    def __getitem__(self, i):
        return self._data[i]

    def __iter__(self):
        return (i for i in self._data)

    def set_context(self):
        for one, two in window(self._data, window_size=2):
            one.set_next_page(two)

    def detect_header(self):
        lines = []
        for page in self:
            lines.extend(
                [
                    i
                    for i in page.cleaned_text_content.split("\n")[:3]
                    if i  # FIXME: shouldn't need to check, cleaned data should be stripped
                ]
            )
        if len(Counter(lines).most_common(1)):
            line, count = Counter(lines).most_common(1)[0]
            # look over the first x lines and watch for similarities
            if count > len(self) / 4:
                logger.debug(f"Detected header: {line}")
                return line

    def detect_footer(self):
        lines = []
        for page in self:
            lines.extend(
                [
                    i
                    for i in page.cleaned_text_content.split("\n")[-3:]
                    if i  # FIXME: shouldn't need to check, cleaned data should be stripped
                ]
            )

        if len(Counter(lines).most_common(1)):
            line, count = Counter(lines).most_common(1)[0]
            # look over the first x lines and watch for similarities
            if count > len(self) / 4:
                logger.debug(f"Detected footer: {line}")
                return line

    def set_page_number_position(self):

        # FIXME: For html use tag context rather than just text

        # TODO: Need to remove headers / footers in some cases

        top_matches = 0
        for page in self:
            first_line = page.cleaned_text_content.split("\n")[0]
            if re.match("^\d+", first_line) or re.match("\d+$", first_line):
                top_matches += 1

        bottom_matches = 0
        for page in self:
            last_line = page.cleaned_text_content.split("\n")[-1]
            if re.match("^\d+", last_line) or re.match("\d+$", last_line):
                bottom_matches += 1

        # make sure 50% of pages follow the pattern
        if top_matches > len(self) / 2 and bottom_matches < len(self) / 2:
            for page in self:
                page.page_number_position = "top"
        elif bottom_matches > len(self) / 2 and top_matches < len(self) / 2:
            for page in self:
                page.page_number_position = "bottom"
