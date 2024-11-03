class ParsableAsBytes:
    @staticmethod
    def fromBytes(data: bytes) -> "ParsableAsBytes":
        raise NotImplementedError()

    def canParseFrom(data: bytes) -> bool:
        raise NotImplementedError()
