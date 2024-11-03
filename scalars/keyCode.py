
from prefix import Prefix
from scalars.parsableAsBytes import ParsableAsBytes


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
