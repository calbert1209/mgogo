class SerializeKeyCode:
    _length = 2

    def __init__(self, prefix: str):
        self._prefix = prefix

    def fromInt(self, n: int) -> bytes:
        return bytes(f"{self._prefix}", "utf-8") + bytes([n])

    def toInt(self, code: bytes) -> int:
        if code[0] != ord(self._prefix):
            raise ValueError(f"Code does not start with {self._prefix}")

        if len(code) != self._length:
            raise ValueError("Code is invalid length")

        return code[1]


class SerializePushCode(SerializeKeyCode):
    def __init__(self):
        super().__init__("+")

    def fromInt(self, n: int) -> bytes:
        return super().fromInt(n)

    def toInt(self, code: bytes) -> int:
        return super().toInt(code)


class SerializeReleaseCode(SerializeKeyCode):
    def __init__(self):
        super().__init__("-")

    def fromInt(self, n: int) -> bytes:
        return super().fromInt(n)

    def toInt(self, code: bytes) -> int:
        return super().toInt(code)
