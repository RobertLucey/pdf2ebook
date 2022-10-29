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
