import unittest
from serialize import Decoder
from entities import Array, LongWord, PushCode, ReleaseCode, ShortWord, Word

fixedLengthClasses = [PushCode, ReleaseCode, ShortWord, Word, LongWord]
containerClasses = [Array]
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