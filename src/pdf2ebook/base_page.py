import re

import langdetect
from cached_property import cached_property
from boltons.iterutils import strip

from pdf2ebook.utils import remove_page_no


class BasePage:
    def __init__(self, *args, **kwargs):
        self.page_number_position = kwargs.get("page_number_position", None)

    @cached_property
    def lang(self):
        try:
            lang = langdetect.detect(self.text_content[:1000])
        except langdetect.lang_detect_exception.LangDetectException:
            lang = None

        return lang

    @property
    def cleaned_text_content(self):
        # FIXME: remove newlines at start and end
        content = []
        for line in self.text_content.split("\n"):
            content.append(line.strip())
        return "\n".join(strip(content, ""))

    @property
    def included_page_no(self):
        if self.page_number_position == "bottom":
            line = self.cleaned_text_content.split("\n")[-1].strip()
            matched = re.match("^\d+", line)
            if matched:
                return matched.group()
        elif self.page_number_position == "top":
            line = self.cleaned_text_content.split("\n")[0].strip()
            matched = re.match("\d+$", line)
            if matched:
                return matched.group()

    @property
    def text_content_without_page_no(self):
        if self.page_number_position == "bottom":
            return "\n".join(
                strip(
                    self.cleaned_text_content.split("\n")[:-1]
                    + [remove_page_no(self.cleaned_text_content.split("\n")[-1])],
                    "",
                )
            )
        elif self.page_number_position == "top":
            return "\n".join(
                strip(
                    [remove_page_no(self.cleaned_text_content.split("\n")[0])]
                    + self.cleaned_text_content.split("\n")[1:],
                    "",
                )
            )
        return self.cleaned_text_content

    def set_next_page(self, next_page):
        self.next_page = next_page
