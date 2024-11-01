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


class ParsableBytesContainer:
    def __init(self) -> None:
        pass

    @staticmethod
    def fromBytes(data: bytes, decoder) -> "ParsableAsBytes":
        raise NotImplementedError()

    @staticmethod
    def canParseFrom(data: bytes) -> bool:
        raise NotImplementedError()


class PushCode(ParsableAsBytes):
    _prefix = Prefix.PCODE
    _length = 2
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
        if len(data) != PushCode._length:
            return False

        return data[0] == PushCode._prefix.encode()[0]


class ReleaseCode(ParsableAsBytes):
    _prefix = Prefix.RCODE
    _length = 2
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
        if len(data) != ReleaseCode._length:
            return False

        return data[0] == ReleaseCode._prefix.encode()[0]


class ShortWord(ParsableAsBytes):
    _prefix = Prefix.SWORD
    _length = 4

    def __init__(self, value: bytes) -> None:
        self.value = value

    def toInts(self) -> list[int]:
        return [int(i) for i in self.value.split()]

    @staticmethod
    def fromBytes(data: bytes):
        return ShortWord(data[1:])

    @staticmethod
    def canParseFrom(data: bytes) -> bool:
        if len(data) != ShortWord._length:
            return False

        return data[0] == ord(ShortWord._prefix)


class Word(ParsableAsBytes):
    _prefix = Prefix.WORD
    _length = 8

    def __init__(self, value: bytes) -> None:
        self.value = value

    def toInts(self) -> list[int]:
        return [int(i) for i in self.value.split()]

    def toString(self) -> str:
        return self.value.decode()

    @staticmethod
    def fromBytes(data: bytes):
        return Word(data[1:])

    @staticmethod
    def canParseFrom(data: bytes) -> bool:
        if len(data) != Word._length:
            return False

        return data[0] == ord(Word._prefix)


class LongWord(ParsableAsBytes):
    _prefix = Prefix.LWORD
    _length = 16

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
        if len(data) != LongWord._length:
            return False

        return data[0] == ord(LongWord._prefix)


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
    def fromBytes(data: bytes, decoder):
        length = data[1]
        contents = data[2:]
        items = [decoder(item) for item in Array.__parseContents(contents)]
        if len(items) != length:
            raise ValueError("Array length does not match items' length")

        return Array(length=length, items=items)

    @staticmethod
    def canParseFrom(data: bytes) -> bool:
        return data[0] == ord(Array._prefix)
