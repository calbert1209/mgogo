
from containers.keyCommand import KeyCommand
from containers.parsableByteContainer import ParsableBytesContainer
from prefix import Prefix
from scalars import LongWord


class PadPage(ParsableBytesContainer):
    _prefix = Prefix.PAGE

    def __init__(self, label: LongWord, commands: list[KeyCommand]):
        self._label = label
        self._commands = commands

    @property
    def label(self):
        self._label

    @property
    def commands(self):
        return self._commands

    @staticmethod
    def fromBytes(data: bytes, decode):
        labelStart = 1
        commandsStart = labelStart + LongWord.length
        label = decode(data[labelStart:commandsStart])
        commands = decode(data[commandsStart:])
        return PadPage(label, commands)

    @staticmethod
    def canParseFrom(data: bytes) -> bool:
        if data[0] != ord(PadPage._prefix):
            return False

        if data[1] != ord(Prefix.LWORD):
            return False

        if data[1 + LongWord.length] != ord(Prefix.ARRAY):
            return False

        return True