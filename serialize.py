from entities import PushCode, ReleaseCode, ShortWord, Word, LongWord


class Decoder:
    """Class to decode bytes into settings"""

    def __init__(self) -> None:
        pass

    def decode(self, data: bytes):
        for cls in [PushCode, ReleaseCode, ShortWord, Word, LongWord]:
            if cls.canParseFrom(data):
                return cls.fromBytes(data)

        raise ValueError("Data cannot be parsed")
