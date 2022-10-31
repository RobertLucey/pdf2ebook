import langdetect
from cached_property import cached_property
from boltons.iterutils import strip


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
        return "\n".join(strip(content, ''))
