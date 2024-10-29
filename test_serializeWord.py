import unittest
from serializeWord import SerializeShortWord, SerializeWord, SerializeLongWord


class TestSerializeWord(unittest.TestCase):
    serializeWord = SerializeWord()

    def test_word_with_string(self):
        """word should accept a string under 8 characters in length"""
        output = self.serializeWord.word(string="hello")
        self.assertEqual(output, b"_hello")

    def test_word_with_ints(self):
        """word should accept a list of integers under 8 items in length"""
        output = self.serializeWord.word(ints=[1, 2, 3])
        self.assertEqual(output, b"_\x01\x02\x03")

    def test_word_raises_error(self):
        """serializeWord should raise ValueError if arg has length greater than 7"""
        with self.assertRaises(ValueError):
            self.serializeWord.word(string="hello_world")

        with self.assertRaises(ValueError):
            self.serializeWord.word(ints=[1, 2, 3, 4, 5, 6, 7, 8])
            
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

    def test_word_with_string(self):
        """word should accept a string under 16 characters in length"""
        output = self.serializeLongWord.word(string="hello friends")
        self.assertEqual(output, b"$hello friends")

    def test_word_with_ints(self):
        """word should accept a list of integers under 16 items in length"""
        output = self.serializeLongWord.word(
            ints=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
        )
        self.assertEqual(
            output, b"$\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f"
        )

    def test_word_raises_error(self):
        """serializeWord should raise ValueError if arg has length greater than 15"""
        with self.assertRaises(ValueError):
            self.serializeLongWord.word(string="hello_world_hello")

        with self.assertRaises(ValueError):
            self.serializeLongWord.word(
                ints=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
            )
            
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

    def test_word_with_string(self):
        """word should accept a string under 4 characters in length"""
        output = self.serializeShortWord.word(string="hi")
        self.assertEqual(output, b"#hi")

    def test_word_with_ints(self):
        """word should accept a list of integers under 4 items in length"""
        output = self.serializeShortWord.word(ints=[1, 2, 3])
        self.assertEqual(output, b"#\x01\x02\x03")

    def test_word_raises_error(self):
        """serializeWord should raise ValueError if arg has length greater than 3"""
        with self.assertRaises(ValueError):
            self.serializeShortWord.word(string="hello")

        with self.assertRaises(ValueError):
            self.serializeShortWord.word(ints=[1, 2, 3, 4])


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
