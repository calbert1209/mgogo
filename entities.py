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

class ParsableAsBytes:
  @staticmethod
  def fromBytes(data: bytes) -> 'ParsableAsBytes':
    raise NotImplementedError()
  
  def canParseFrom(data: bytes) -> bool:
    raise NotImplementedError()

class ParsableBytesContainer:
    def __init(self) -> None:
        pass
      
    def decode(self, decoder):
        raise NotImplementedError()
class PushCode(ParsableAsBytes):
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


class ReleaseCode(ParsableAsBytes):
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


class ShortWord(ParsableAsBytes):
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


class Word(ParsableAsBytes):
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


class LongWord(ParsableAsBytes):
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


class Array(ParsableAsBytes, ParsableBytesContainer):
    _prefix = Prefix.ARRAY
    _items = None
    _length = -1

    def __init__(self, length: int, contents: bytes) -> None:
        self.contents = contents
        self._length = length
        
    def __isItemPrefix(self, byte: int) -> bool:
        first = self.contents[0]
        if first == ord(Prefix.PCODE) or byte == ord(Prefix.RCODE):
            return byte == ord(Prefix.PCODE) or byte == ord(Prefix.RCODE)
        
        return byte == first
        
    def __splitKeyCodeContents(self) -> list[bytes]:
        output = []
        item = b""
        for byte in self.contents:
            if self.__isItemPrefix(byte):
                # push any existing item to output
                if len(item) > 0:
                    output.append(item)
                    item = b""
                    
            item += bytes([byte])
              
        if (len(item) > 0):
            output.append(item)
                
        return output

    @property
    def items(self) -> list[bytes]:
        if self._items is None:
            self._items = self.__splitKeyCodeContents()

        return self._items
      
    def decode(self, decoder):
        return [decoder(item) for item in self.items]
          
    @property
    def length(self) -> int:
        return self._length

    @staticmethod
    def fromBytes(data: bytes):
        length = data[1]
        return Array(length=length, contents=data[2:])

    @staticmethod
    def canParseFrom(data: bytes) -> bool:
        return data[0] == ord(Array._prefix)