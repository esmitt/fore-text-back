class TextTTF:
    def __init__(self, text: str):
        self._text = text

    def get_text(self) -> str:
        return self._text

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value: str):
        self._text = value

