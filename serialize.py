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

class PushCode:
  _prefix = Prefix.PCODE
  value = 0
  def __init__(self, value: int) -> None:
    self.value = value
  
  def toBytes(self) -> bytes:
    return f"{self._prefix}{self.value}".encode()
  
  @staticmethod
  def fromBytes(data: bytes):
    return PushCode(int(data[1]))
  
  @staticmethod
  def isPushCode(data: bytes) -> bool:
    if len(data) != 2:
      return False

    return data[0] == PushCode._prefix.encode()[0]
  

class ReleaseCode:
  _prefix = Prefix.RCODE
  value = 0
  def __init__(self, value: int) -> None:
    self.value = value
  
  def toBytes(self) -> bytes:
    return f"{self._prefix}{self.value}".encode()
  
  @staticmethod
  def fromBytes(data: bytes):
    return ReleaseCode(int(data[1]))
  
  @staticmethod
  def isReleaseCode(data: bytes) -> bool:
    if len(data) != 2:
      return False

    return data[0] == ReleaseCode._prefix.encode()[0]
  


def keyCodeFactory(data: bytes) -> PushCode | ReleaseCode:
  """Factory method to create either a PushCode or ReleaseCode object"""
  if PushCode.isPushCode(data):
    return PushCode.fromBytes(data)
  elif ReleaseCode.isReleaseCode(data):
    return ReleaseCode.fromBytes(data)
  else:
    raise ValueError("Data cannot be parsed")


class Decoder:
  """Class to decode bytes into settings"""
  def __init__(self) -> None:
     pass
   
  def decode(self, data: bytes):
    return keyCodeFactory(data)