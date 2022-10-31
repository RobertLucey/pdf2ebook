import re

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
            one.next_page = two

    @property
    def page_number_position(self):

        # TODO: Need to remove headers / footers in some cases

        top_matches = 0
        for page in self:
            first_line = page.cleaned_text_content.split('\n')[0]
            if re.match('^\d+', first_line) or re.match('\d+$', first_line):
                top_matches += 1

        bottom_matches = 0
        for page in self:
            last_line = page.cleaned_text_content.split('\n')[-1]
            if re.match('^\d+', last_line) or re.match('\d+$', last_line):
                bottom_matches += 1

        # make sure 50% of pages follow the pattern
        if top_matches > len(self) / 2 and bottom_matches < len(self) / 2:
            return 'top'
        elif bottom_matches > len(self) / 2 and top_matches < len(self) / 2:
            return 'bottom'
