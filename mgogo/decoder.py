from containers.parsableByteContainer import ParsableBytesContainer
from scalars.parsableAsBytes import ParsableAsBytes
from mgogo.prefix import Prefix


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
