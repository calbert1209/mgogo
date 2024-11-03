from scalars.parsableAsBytes import ParsableAsBytes


class ParsableBytesContainer:
    @staticmethod
    def fromBytes(data: bytes, decode) -> "ParsableAsBytes":
        raise NotImplementedError()

    @staticmethod
    def canParseFrom(data: bytes) -> bool:
        raise NotImplementedError()
