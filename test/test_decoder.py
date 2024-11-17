import unittest
from scalars.word import LongWord, ShortWord, Word
from scalars.keyCode import PushCode, ReleaseCode
from containers.array import Array
from containers.keyCommand import KeyCommand
from containers.padPage import PadPage

from decoder import Decoder

fixedLengthClasses = [PushCode, ReleaseCode, ShortWord, Word, LongWord]
containerClasses = [Array, KeyCommand, PadPage]


class TestStaticLengthDecoder(unittest.TestCase):
    decoder = Decoder(fixedLengthClasses, containerClasses)

    def test_decode_push_code(self):
        """decode should return a PushCode object from a push code"""
        output = self.decoder.decode(b"+\x02")
        self.assertIsInstance(output, PushCode)
        self.assertEqual(output.value, 2)

    def test_decode_release_code(self):
        """decode should return a ReleaseCode object from a push code"""
        output = self.decoder.decode(b"-\xff")
        self.assertIsInstance(output, ReleaseCode)
        self.assertEqual(output.value, 255)

    def test_decode_raises_error(self):
        """decode should raise ValueError if code is invalid length"""
        with self.assertRaises(ValueError):
            self.decoder.decode(b"+")

        with self.assertRaises(ValueError):
            self.decoder.decode(b"+\x02\x03")

    def test_decode_short_word(self):
        """decode should return a ShortWord object from a short word"""
        output = self.decoder.decode(b"#\xff\x80\x00")
        self.assertIsInstance(output, ShortWord)
        self.assertEqual(output.value, b"\xff\x80\x00")

    def test_decode_raises_error_short_word(self):
        """decode should raise ValueError if short word is invalid length"""
        with self.assertRaises(ValueError):
            self.decoder.decode(b"#\xff\x80")

        with self.assertRaises(ValueError):
            self.decoder.decode(b"#\xff\x80\x00\x00")

    def test_decode_word(self):
        """decode should return a Word object from a word"""
        output = self.decoder.decode(b"_Hello  ")
        self.assertIsInstance(output, Word)
        self.assertEqual(output.value, b"Hello  ")

    def test_decode_raises_error_word(self):
        """decode should raise ValueError if word is invalid length"""
        with self.assertRaises(ValueError):
            self.decoder.decode(b"_HelloWorld")

        with self.assertRaises(ValueError):
            self.decoder.decode(b"_Helloo")

    def test_decode_long_word(self):
        """decode should return a LongWord object from a long word"""
        output = self.decoder.decode(b"$Hello my friend")
        self.assertIsInstance(output, LongWord)
        self.assertEqual(output.value, b"Hello my friend")

    def test_decode_raises_error_long_word(self):
        """decode should raise ValueError if long word is invalid length"""
        with self.assertRaises(ValueError):
            self.decoder.decode(b"$Hello friend")

        with self.assertRaises(ValueError):
            self.decoder.decode(b"$Hello my good friend")


class TestArrayDecoder(unittest.TestCase):
    decoder = Decoder(fixedLengthClasses, containerClasses)

    def test_decode_keycode_array(self):
        """decode should return an array of objects from an array"""
        output = self.decoder.decode(b"*\x03+\x02+\x03-\x04")
        items = output.items
        self.assertEqual(len(items), 3)
        self.assertIsInstance(items[0], PushCode)
        self.assertIsInstance(items[1], PushCode)
        self.assertIsInstance(items[2], ReleaseCode)
        self.assertEqual(items[0].value, 2)
        self.assertEqual(items[1].value, 3)
        self.assertEqual(items[2].value, 4)

    def test_decode_short_word_array(self):
        """decode should return an array of objects from an array"""
        output = self.decoder.decode(b"*\x02#\xff\x80\x00#\x00\xff\x00")
        items = output.items
        self.assertEqual(len(items), 2)
        self.assertEqual(output.length, 2)

        for item in items:
            self.assertIsInstance(item, ShortWord)

        self.assertEqual(items[0].value, b"\xff\x80\x00")
        self.assertEqual(items[1].value, b"\x00\xff\x00")

    def test_decode_word_array(self):
        """decode should return an array of objects from an array"""
        output = self.decoder.decode(b"*\x02_Hello  _World  ")
        items = output.items
        self.assertEqual(len(items), 2)
        self.assertEqual(output.length, 2)

        for item in items:
            self.assertIsInstance(item, Word)

        self.assertEqual(items[0].value, b"Hello  ")
        self.assertEqual(items[1].value, b"World  ")

    def test_decode_long_word_array(self):
        """decode should return an array of objects from an array"""
        output = self.decoder.decode(b"*\x02$Hello my friend$Goodbye world! ")
        items = output.items
        self.assertEqual(len(items), 2)
        self.assertEqual(output.length, 2)

        for item in items:
            self.assertIsInstance(item, LongWord)

        self.assertEqual(items[0].value, b"Hello my friend")
        self.assertEqual(items[1].value, b"Goodbye world! ")

    copy = b"<_COPY   #\xff\x80\x00*\x02+\x45+\x44"
    paste = b"<_PASTE  #\x00\xff\x00*\x02+\x45+\x47"
    cut = b"<_CUT    #\x00\x00\xff*\x02+\x66+\x67"

    def test_decode_key_command_copy(self):
        """decode should return a key command object from bytes"""
        output = self.decoder.decode(self.copy)

        self.assertIsInstance(output, KeyCommand)
        self.assertEqual(output.label.toString(), "COPY   ")
        self.assertEqual(output.color.toInts(), [255, 128, 0])
        self.assertEqual(output.codes.length, 2)
        self.assertListEqual(
            [x.value for x in output.codes.items], [0x45, 0x44])

    def test_decode_key_command_paste(self):
        """decode should return a key command object from bytes"""
        output = self.decoder.decode(self.paste)

        self.assertIsInstance(output, KeyCommand)
        self.assertEqual(output.label.toTrimmed(), "PASTE")
        self.assertEqual(output.color.toInts(), [0, 255, 0])
        self.assertEqual(output.codes.length, 2)
        self.assertListEqual(
            [x.value for x in output.codes.items], [0x45, 0x47])

    padPage = \
        b"[$FIRSTPAGE      " +\
        b"*\x03" +\
        b"<_COPY   #\xff\x80\x00*\x02+\x45+\x44" +\
        b"<_PASTE  #\x00\xff\x00*\x02+\x45+\x47" +\
        b"<_CUT    #\x00\x00\xff*\x02+\x66+\x67"

    def test_decode_pad_page(self):
        """decode should return a pad page object from bytes"""
        output = self.decoder.decode(self.padPage)
        self.assertIsInstance(output, PadPage)
        self.assertEqual(output.label.toString(), "FIRSTPAGE      ")
        self.assertEqual(len(output.commands.items), 3)
        for item in output.commands.items:
            self.assertIsInstance(item, KeyCommand)

    padPagesArray = \
        b"*\x02" +\
        b"[$FIRSTPAGE      " +\
        b"*\x03" +\
        b"<_COPY   #\xff\x80\x00*\x02+\x45+\x44" +\
        b"<_PASTE  #\x00\xff\x00*\x02+\x45+\x47" +\
        b"<_CUT    #\x00\x00\xff*\x02+\x66+\x67" +\
        b"[$SECONdPAGE     " +\
        b"*\x04" +\
        b"<_FOO    #\xff\x80\x00*\x02+\x45+\x44" +\
        b"<_BAR    #\x00\xff\x00*\x02+\x45+\x47" +\
        b"<_BAZ    #\x00\x00\xff*\x02+\x66+\x67" +\
        b"<_BUZ    #\xff\x00\x00*\x03+\x66+\x67-\x67"

    def test_decode_pad_pages_array(self):
        """decode should return an array of pad page objects from bytes"""
        output = self.decoder.decode(self.padPagesArray)
        pages = output.items
        self.assertIsInstance(output, Array)
        self.assertEqual(len(pages), 2)

        self.assertIsInstance(pages[0], PadPage)
        self.assertEqual(len(pages[1].commands.items), 4)

    def test_trim_nvm_bytes(self):
        mockNvmBytes = self.padPagesArray + b"\n\22\23\22\23\22\23\n\0\0\0\0\0"
        output = self.decoder.trim(mockNvmBytes)
        self.assertEqual(len(self.padPagesArray), len(output))
        self.assertEqual(Array.canParseFrom(output), True)
