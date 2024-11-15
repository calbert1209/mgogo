from prefix import Prefix
from scalars.parsableAsBytes import ParsableAsBytes


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
