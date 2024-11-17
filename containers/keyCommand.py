
from containers.parsableByteContainer import ParsableBytesContainer
from mgogo.prefix import Prefix
from scalars.word import ShortWord, Word


class KeyCommand(ParsableBytesContainer):
    _prefix = Prefix.COMM
    _label: Word
    _color: ShortWord
    _codes: list

    def __init__(self, label: str, color: tuple[int, int, int], codes: list) -> None:
        self._label = label
        self._color = color
        self._codes = codes

    @property
    def label(self):
        return self._label

    @property
    def color(self):
        return self._color

    @property
    def codes(self):
        return self._codes

    @staticmethod
    def fromBytes(data: bytes, decode):
        colorStart = Word.length + 1
        keyCodesStart = colorStart + ShortWord.length
        label = decode(data[1:colorStart])
        color = decode(data[colorStart:keyCodesStart])
        codes = decode(data[keyCodesStart:])
        return KeyCommand(label, color, codes)

    @staticmethod
    def canParseFrom(data: bytes) -> bool:
        if data[0] != ord(KeyCommand._prefix):
            return False

        if data[1] != ord(Prefix.WORD):
            return False

        if data[1 + Word.length] != ord(Prefix.SWORD):
            return False

        if data[1 + Word.length + ShortWord.length] != ord(Prefix.ARRAY):
            return False

        return True
