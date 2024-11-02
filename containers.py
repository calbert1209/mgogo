from prefix import Prefix
from scalars import ParsableAsBytes, PushCode, ReleaseCode, ShortWord, Word


class ParsableBytesContainer:
    def __init(self) -> None:
        pass

    @staticmethod
    def fromBytes(data: bytes, decode) -> "ParsableAsBytes":
        raise NotImplementedError()

    @staticmethod
    def canParseFrom(data: bytes) -> bool:
        raise NotImplementedError()


class Array(ParsableBytesContainer):
    _prefix = Prefix.ARRAY
    _items = None
    _length = -1

    def __init__(self, length: int, items: ParsableAsBytes) -> None:
        self._length = length
        self._items = items

    @staticmethod
    def __isItemPrefix(first: int, byte: int) -> bool:
        if first == ord(Prefix.PCODE) or first == ord(Prefix.RCODE):
            return byte == ord(Prefix.PCODE) or byte == ord(Prefix.RCODE)

        return byte == first

    @staticmethod
    def __parseContents(contents) -> list[bytes]:
        first = contents[0]
        output = []
        item = b""
        for byte in contents:
            if Array.__isItemPrefix(first, byte):
                # push any existing item to output
                if len(item) > 0:
                    output.append(item)
                    item = b""

            item += bytes([byte])

        if len(item) > 0:
            output.append(item)

        return output

    @property
    def length(self) -> int:
        return self._length

    @property
    def items(self) -> list[ParsableAsBytes]:
        return self._items

    @staticmethod
    def fromBytes(data: bytes, decode):
        length = data[1]
        contents = data[2:]
        items = [decode(item) for item in Array.__parseContents(contents)]
        if len(items) != length:
            raise ValueError("Array length does not match items' length")

        return Array(length=length, items=items)

    @staticmethod
    def canParseFrom(data: bytes) -> bool:
        return data[0] == ord(Array._prefix)


class KeyCommand(ParsableBytesContainer):
    _label: Word
    _color: ShortWord
    _codes: list

    def __init(self, label: str, color: tuple[int, int, int], codes: list) -> None:
        super().__init()
        self._label = label
        self._color = color
        self._codes = codes

    @staticmethod
    def fromBytes(data: bytes, decode):
        colorStart = Word.length
        keyCodesStart = colorStart + ShortWord.length
        label = decode(data[1:colorStart])
        color = decode(data[colorStart, keyCodesStart])
        codes = decode(data[keyCodesStart:])
        return KeyCommand(label, color, codes)
