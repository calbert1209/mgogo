from entities import Array, ParsableAsBytes, ParsableBytesContainer


class Decoder:
    """Class to decode bytes into settings"""

    def __init__(self, fixedLengthClasses: list[ParsableAsBytes]) -> None:
        self._fixedLengthClasses = fixedLengthClasses

    def decode(self, data: bytes):
        for cls in self._fixedLengthClasses:
            if cls.canParseFrom(data):
                return cls.fromBytes(data)
              
        if Array.canParseFrom(data):
            array = Array.fromBytes(data)
            return array.decode(self.decode)

        raise ValueError("Data cannot be parsed")
