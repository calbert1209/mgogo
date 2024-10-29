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
