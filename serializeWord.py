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
    
    def word(self, **kwargs) -> bytes:
        string = kwargs.get('string')
        ints = kwargs.get('ints')
        if string is not None:
          return self.__strToWord(string)
        
        if ints is not None:
          return self.__intsToWord(ints)
        
class SerializeShortWord(BaseWord):
    def __init__(self):
        super().__init__('#', 3)
    
    def word(self, **kwargs) -> bytes:
        return super().word(**kwargs)
      
class SerializeWord(BaseWord):
    def __init__(self):
        super().__init__('_', 7)
    
    def word(self, **kwargs) -> bytes:
        return super().word(**kwargs)
      
class SerializeLongWord(BaseWord):
    def __init__(self):
        super().__init__('$', 15)
    
    def word(self, **kwargs) -> bytes:
        return super().word(**kwargs)
      
