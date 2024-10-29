import unittest
from serializeKeyCode import SerializePushCode, SerializeReleaseCode

class TestSerializePushCode(unittest.TestCase):
    serializer = SerializePushCode()
    def test_fromInts(self):
        """fromInts should return a push code from a list of integers"""
        output = self.serializer.fromInt(2)
        self.assertEqual(output, b"+\x02")
    
    def test_toInt(self):
        """toInt should return an integer from a push code"""
        output = self.serializer.toInt(b"+\x02")
        self.assertEqual(output, 2)
        
    def test_toInt_raises_error(self):
        """toInt should raise ValueError if code is invalid length"""
        with self.assertRaises(ValueError):
            self.serializer.toInt(b"+")
            
        with self.assertRaises(ValueError):
            self.serializer.toInt(b"+\x02\x03")
            
    def test_toInt_raises_error(self): 
        """toInt should raise ValueError if code does not start with prefix"""
        with self.assertRaises(ValueError):
            self.serializer.toInt(b"-\x02")
            
class TestSerializeReleaseCode(unittest.TestCase):
    serializer = SerializeReleaseCode()
  
    def test_fromInts(self):
        """fromInts should return a release code from a list of integers"""
        output = self.serializer.fromInt(2)
        self.assertEqual(output, b"-\x02")
    
    def test_toInt(self):
        """toInt should return an integer from a release code"""
        output = self.serializer.toInt(b"-\x02")
        self.assertEqual(output, 2)
        
    def test_toInt_raises_error(self):
        """toInt should raise ValueError if code is invalid length"""
        with self.assertRaises(ValueError):
            self.serializer.toInt(b"-")
            
        with self.assertRaises(ValueError):
            self.serializer.toInt(b"-\x02\x03")
            
    def test_toInt_raises_error(self): 
        """toInt should raise ValueError if code does not start with prefix"""
        with self.assertRaises(ValueError):
            self.serializer.toInt(b"+\x02")
            
def makeSuite():
    tests = [
        TestSerializePushCode(key)
        for key in TestSerializePushCode.__dict__.keys()
        if key.startswith("test")
    ]
    tests += [
        TestSerializeReleaseCode(key)
        for key in TestSerializeReleaseCode.__dict__.keys()
        if key.startswith("test")
    ]
    return unittest.TestSuite(tests)


if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(makeSuite())