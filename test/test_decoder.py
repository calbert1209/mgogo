import unittest
from serialize import Decoder
from entities import LongWord, PushCode, ReleaseCode, ShortWord, Word

class TestDecoder(unittest.TestCase):
  decoder = Decoder()
  
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