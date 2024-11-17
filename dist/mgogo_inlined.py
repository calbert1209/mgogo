class Prefix:
    """Enum-like class for the prefix of the serialized words"""

    SWORD = "#"
    WORD = "_"
    LWORD = "$"
    PCODE = "+"
    RCODE = "-"

    ARRAY = "*"
    COMM = "<"
    PAGE = "["

    END = "\n"


class ParsableAsBytes:
    @staticmethod
    def fromBytes(data: bytes) -> "ParsableAsBytes":
        raise NotImplementedError()

    def canParseFrom(data: bytes) -> bool:
        raise NotImplementedError()


class PushCode(ParsableAsBytes):
    _prefix = Prefix.PCODE
    length = 2
    value = 0

    def __init__(self, value: int) -> None:
        self.value = value

    def toBytes(self) -> bytes:
        return f"{self._prefix}{self.value}".encode()

    @staticmethod
    def fromBytes(data: bytes):
        return PushCode(int(data[1]))

    @staticmethod
    def canParseFrom(data: bytes) -> bool:
        if len(data) != PushCode.length:
            return False

        return data[0] == PushCode._prefix.encode()[0]


class ReleaseCode(ParsableAsBytes):
    _prefix = Prefix.RCODE
    length = 2
    value = 0

    def __init__(self, value: int) -> None:
        self.value = value

    def toBytes(self) -> bytes:
        return f"{self._prefix}{self.value}".encode()

    @staticmethod
    def fromBytes(data: bytes):
        return ReleaseCode(int(data[1]))

    @staticmethod
    def canParseFrom(data: bytes) -> bool:
        if len(data) != ReleaseCode.length:
            return False

        return data[0] == ReleaseCode._prefix.encode()[0]


class ShortWord(ParsableAsBytes):
    _prefix = Prefix.SWORD
    length = 4

    def __init__(self, value: bytes) -> None:
        self.value = value

    def toInts(self) -> list[int]:
        return [int(i) for i in self.value]

    @staticmethod
    def fromBytes(data: bytes):
        return ShortWord(data[1:])

    @staticmethod
    def canParseFrom(data: bytes) -> bool:
        if len(data) != ShortWord.length:
            return False

        return data[0] == ord(ShortWord._prefix)


class Word(ParsableAsBytes):
    _prefix = Prefix.WORD
    length = 8

    def __init__(self, value: bytes) -> None:
        self.value = value

    def toInts(self) -> list[int]:
        return [int(i) for i in self.value.split()]

    def toString(self) -> str:
        return self.value.decode()

    def toTrimmed(self) -> str:
        return self.toString().strip()

    @staticmethod
    def fromBytes(data: bytes):
        return Word(data[1:])

    @staticmethod
    def canParseFrom(data: bytes) -> bool:
        if len(data) != Word.length:
            return False

        return data[0] == ord(Word._prefix)


class LongWord(ParsableAsBytes):
    _prefix = Prefix.LWORD
    length = 16

    def __init__(self, value: bytes) -> None:
        self.value = value

    def toInts(self) -> list[int]:
        return [int(i) for i in self.value.split()]

    def toString(self) -> str:
        return self.value.decode()

    @staticmethod
    def fromBytes(data: bytes):
        return LongWord(data[1:])

    @staticmethod
    def canParseFrom(data: bytes) -> bool:
        if len(data) != LongWord.length:
            return False

        return data[0] == ord(LongWord._prefix)


class ParsableBytesContainer:
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

    def __init__(self, length: int, items: ParsableBytesContainer) -> None:
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
    def fromBytes(data: bytes, decode) -> "Array":
        length = data[1]
        contents = data[2:]
        items = [decode(item) for item in Array.__parseContents(contents)]
        if len(items) != length:
            print(f"items{len(items)} declared: {length}")
            raise ValueError("Array length does not match items' length")

        return Array(length=length, items=items)

    @staticmethod
    def canParseFrom(data: bytes) -> bool:
        return data[0] == ord(Array._prefix)


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


class PadPage(ParsableBytesContainer):
    _prefix = Prefix.PAGE

    def __init__(self, label: LongWord, commands: Array):
        self._label = label
        self._commands = commands

    @property
    def label(self):
        return self._label

    @property
    def commands(self):
        return self._commands

    @staticmethod
    def fromBytes(data: bytes, decode):
        labelStart = 1
        commandsStart = labelStart + LongWord.length
        label = decode(data[labelStart:commandsStart])
        commands = decode(data[commandsStart:])
        return PadPage(label, commands)

    @staticmethod
    def canParseFrom(data: bytes) -> bool:
        if data[0] != ord(PadPage._prefix):
            return False

        if data[1] != ord(Prefix.LWORD):
            return False

        if data[1 + LongWord.length] != ord(Prefix.ARRAY):
            return False

        return True


class Decoder:
    """Class to decode bytes into settings"""

    def __init__(
        self,
        fixedLengthClasses: list[ParsableAsBytes],
        containerClasses: list[ParsableBytesContainer],
    ) -> None:
        self._fixedLengthClasses = fixedLengthClasses
        self._containerClasses = containerClasses

    def decode(self, data: bytes):
        for cls in self._fixedLengthClasses:
            if cls.canParseFrom(data):
                return cls.fromBytes(data)

        for cls in self._containerClasses:
            if cls.canParseFrom(data):
                return cls.fromBytes(data, self.decode)

        raise ValueError("Data cannot be parsed")

    def trim(self, nvmData: bytes) -> bytes:
        return nvmData.split(Prefix.END.encode())[0]
