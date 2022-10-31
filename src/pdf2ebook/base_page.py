import langdetect
from cached_property import cached_property
from boltons.iterutils import strip

from pdf2ebook.utils import remove_page_no


class BasePage:
    @cached_property
    def lang(self):
        try:
            lang = langdetect.detect(self.text_content[:1000])
        except langdetect.lang_detect_exception.LangDetectException:
            lang = None

        return lang

    @property
    def cleaned_text_content(self):
        content = []
        for line in self.text_content.split("\n"):
            content.append(line.strip())
        return "\n".join(strip(content, ""))

    def get_text_content_without_page_no(self, position):
        if position is None:
            return

        if position == "bottom":
            return "\n".join(
                strip(
                    self.cleaned_text_content.split("\n")[:-1]
                    + [remove_page_no(self.cleaned_text_content.split("\n")[-1])],
                    "",
                )
            )
        elif position == "top":
            return "\n".join(
                strip(
                    [remove_page_no(self.cleaned_text_content.split("\n")[0])]
                    + self.cleaned_text_content.split("\n")[1:],
                    "",
                )
            )
