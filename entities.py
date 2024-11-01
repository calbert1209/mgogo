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


class PushCode:
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


class ReleaseCode:
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


class ShortWord:
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


class Word:
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


class LongWord:
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