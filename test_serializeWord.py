import unittest
from serializeWord import SerializeShortWord, SerializeWord, SerializeLongWord


class TestSerializeWord(unittest.TestCase):
    serializeWord = SerializeWord()

    def test_fromInts(self):
        """fromInts should return a word from a list of integers"""
        output = self.serializeWord.fromInts([1, 2, 3])
        self.assertEqual(output, b"_\x01\x02\x03")
        
    def test_fromInts_raises_error(self):
        """fromInts should raise ValueError if word is too long"""
        with self.assertRaises(ValueError):
            self.serializeWord.fromInts([1, 2, 3, 4, 5, 6, 7, 8])
        
    def test_fromString(self):
        """fromString should return a word from a string"""
        output = self.serializeWord.fromString("hello")
        self.assertEqual(output, b"_hello")
            
    def test_fromString_raises_error(self):
        """fromString should raise ValueError if word is too long"""
        with self.assertRaises(ValueError):
            self.serializeWord.fromString("hello friends")
            
    def test_toInts(self):
        """toInts should return a list of integers from a word"""
        output = self.serializeWord.toInts(b"_\x01\x02\x03")
        self.assertEqual(output, [1, 2, 3])
        
    def test_toInts_raises_error(self):
        """toInts should raise ValueError if word does not start with prefix"""
        with self.assertRaises(ValueError):
            self.serializeWord.toInts(b"#\x01\x02\x03")
    
    def test_toString(self):
        """toString should return a string from a word"""
        output = self.serializeWord.toString(b"_hello")
        self.assertEqual(output, "hello")
        
    def test_toString_raises_error(self):
        """toString should raise ValueError if word does not start with prefix"""
        with self.assertRaises(ValueError):
            self.serializeWord.toString(b"#hello")


class TestSerializeLongWord(unittest.TestCase):
    serializeLongWord = SerializeLongWord()

    def test_fromInts(self):
        """fromInts should return a word from a list of integers"""
        output = self.serializeLongWord.fromInts([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])
        self.assertEqual(output, b"$\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f")
        
    def test_fromInts_raises_error(self):
        """fromInts should raise ValueError if word is too long"""
        with self.assertRaises(ValueError):
            self.serializeLongWord.fromInts([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])
        
    def test_fromString(self):
        """fromString should return a word from a string"""
        output = self.serializeLongWord.fromString("hello friends")
        self.assertEqual(output, b"$hello friends")
        
    def test_fromString_raises_error(self):
        """fromString should raise ValueError if word is too long"""
        with self.assertRaises(ValueError):
            self.serializeLongWord.fromString("hello friends and family")
            
    def test_toInts(self):
        """toInts should return a list of integers from a word"""
        output = self.serializeLongWord.toInts(b"$\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f")
        self.assertEqual(output, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])
        
    def test_toInts_raises_error(self):
        """toInts should raise ValueError if word does not start with prefix"""
        with self.assertRaises(ValueError):
            self.serializeLongWord.toInts(b"_\x01\x02\x03")
            
    def test_toString(self):
        """toString should return a string from a word"""
        output = self.serializeLongWord.toString(b"$hello friends")
        self.assertEqual(output, "hello friends")
        
    def test_toString_raises_error(self):
        """toString should raise ValueError if word does not start with prefix"""
        with self.assertRaises(ValueError):
            self.serializeLongWord.toString(b"#hello friends")


class TestSerializeShortWord(unittest.TestCase):
    serializeShortWord = SerializeShortWord()

    def test_fromInts(self):
        """fromInts should return a word from a list of integers"""
        output = self.serializeShortWord.fromInts([1, 2, 3])
        self.assertEqual(output, b"#\x01\x02\x03")
        
    def test_fromInts_raises_error(self):
        """fromInts should raise ValueError if word is too long"""
        with self.assertRaises(ValueError):
            self.serializeShortWord.fromInts([1, 2, 3, 4])
    
    def test_fromString(self):
        """fromString should return a word from a string"""
        output = self.serializeShortWord.fromString("hi")
        self.assertEqual(output, b"#hi")
        
    def test_fromString_raises_error(self):
        """fromString should raise ValueError if word is too long"""
        with self.assertRaises(ValueError):
            self.serializeShortWord.fromString("hello")
        
    def test_toInts(self):
        """toInts should return a list of integers from a word"""
        output = self.serializeShortWord.toInts(b"#\x01\x02\x03")
        self.assertEqual(output, [1, 2, 3])
        
    def test_toInts_raises_error(self):
        """toInts should raise ValueError if word does not start with prefix"""
        with self.assertRaises(ValueError):
            self.serializeShortWord.toInts(b"_\x01\x02\x03")
            
    def test_toString(self):
        """toString should return a string from a word"""
        output = self.serializeShortWord.toString(b"#hi")
        self.assertEqual(output, "hi")
        
    def test_toString_raises_error(self):
        """toString should raise ValueError if word does not start with prefix"""
        with self.assertRaises(ValueError):
            self.serializeShortWord.toString(b"_hi")


def makeSuite():
    tests = [
        TestSerializeWord(key)
        for key in TestSerializeWord.__dict__.keys()
        if key.startswith("test")
    ]
    tests += [
        TestSerializeLongWord(key)
        for key in TestSerializeLongWord.__dict__.keys()
        if key.startswith("test")
    ]
    tests += [
        TestSerializeShortWord(key)
        for key in TestSerializeShortWord.__dict__.keys()
        if key.startswith("test")
    ]
    return unittest.TestSuite(tests)


if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(makeSuite())
