import unittest
from serialize import Decoder, PushCode, ReleaseCode

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