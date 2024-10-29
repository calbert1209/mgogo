class BaseWord:
    def __init__(self, prefix: str, limit: int):
        self._prefix = prefix
        self._limit = limit

    def __strToWord(self, string: str) -> bytes:
        if len(string) > self._limit:
            raise ValueError(f"string is longer than {self._limit} characters")
        return bytes(f"{self._prefix}{string}",'utf-8')
    

    def __intsToWord(self, ints: list[int]) -> bytes:
        if len(ints) > self._limit:
            raise ValueError(f"Integer list is longer than {self._limit} characters")
        return bytes(self._prefix, 'utf-8') + bytes(ints)
        
    def fromString(self, string: str) -> bytes:
        return self.__strToWord(string)
      
    def fromInts(self, ints: list[int]) -> bytes:
        return self.__intsToWord(ints)
        
    def toInts(self, word: bytes) -> list[int]:
        if word[0] != ord(self._prefix):
            raise ValueError(f"Word does not start with {self._prefix}")
        return list(word[1:])
      
    def toString(self, word: bytes) -> str:
        if word[0] != ord(self._prefix):
            raise ValueError(f"Word does not start with {self._prefix}")
        return word[1:].decode('utf-8')
      
        
class SerializeShortWord(BaseWord):
    def __init__(self):
        super().__init__('#', 3)
    
    def fromInts(self, ints: list[int]) -> bytes:
        return super().fromInts(ints)
      
    def fromString(self, string: str) -> bytes:
        return super().fromString(string)
      
    def toInts(self, word: bytes) -> list[int]:
        return super().toInts(word)
      
    def toString(self, word: bytes) -> str:
        return super().toString(word)
      
class SerializeWord(BaseWord):
    def __init__(self):
        super().__init__('_', 7)
    
    def fromInts(self, ints: list[int]) -> bytes:
        return super().fromInts(ints)
      
    def fromString(self, string: str) -> bytes:
        return super().fromString(string)
      
    def toInts(self, word: bytes) -> list[int]:
        return super().toInts(word)
      
    def toString(self, word: bytes) -> str:
        return super().toString(word)
      
class SerializeLongWord(BaseWord):
    def __init__(self):
        super().__init__('$', 15)
    
    def fromInts(self, ints: list[int]) -> bytes:
        return super().fromInts(ints)
      
    def fromString(self, string: str) -> bytes:
        return super().fromString(string)
  
    def toInts(self, word: bytes) -> list[int]:
        return super().toInts(word)
      
    def toString(self, word: bytes) -> str:
        return super().toString(word)
