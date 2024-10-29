import unittest
from stuff import Serialize

class TestSerialize(unittest.TestCase):
    def test_word_with_string(self):
        """word should accept a string"""
        self.assertEqual(Serialize.word(string='hello'), b'_hello')

    def test_word_with_ints(self):
        """word should accept a list of integers"""
        self.assertEqual(Serialize.word(ints=[1,2,3]), b'_\x01\x02\x03')

    def test_word_raises_error(self):
        """serializeWord should raise ValueError if word is longer than 7 characters"""
        with self.assertRaises(ValueError):
            Serialize.word(string='hello_world')

        with self.assertRaises(ValueError):
            Serialize.word(ints=[1,2,3,4,5,6,7,8])

if __name__ == "__main__":
    unittest.main()