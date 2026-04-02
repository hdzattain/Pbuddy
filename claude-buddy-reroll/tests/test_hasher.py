"""Tests for FNV-1a 32-bit hash implementation."""
import unittest

from buddy_reroll.hasher import fnv1a_32


class TestFnv1a32(unittest.TestCase):
    """Test FNV-1a 32-bit hash with known test vectors."""

    def test_empty_string(self):
        """FNV-1a of empty string should equal offset_basis."""
        result = fnv1a_32("")
        self.assertEqual(result, 2166136261)  # FNV_OFFSET_BASIS

    def test_single_characters(self):
        """Test single character hashes."""
        # Known FNV-1a 32-bit test vectors
        self.assertEqual(fnv1a_32("a"), 0xe40c292c)
        self.assertEqual(fnv1a_32("b"), 0xe70c2de5)
        self.assertEqual(fnv1a_32("c"), 0xe60c2c52)

    def test_known_strings(self):
        """Test known string hashes."""
        # Test vectors verified against our implementation
        self.assertEqual(fnv1a_32("hello"), 0x4f9f2cab)
        self.assertEqual(fnv1a_32("world"), 0x37a3e893)

    def test_deterministic(self):
        """Same input should produce same output."""
        data = "test_user_id"
        hash1 = fnv1a_32(data)
        hash2 = fnv1a_32(data)
        self.assertEqual(hash1, hash2)

    def test_different_inputs_different_outputs(self):
        """Different inputs should likely produce different outputs."""
        hash1 = fnv1a_32("user1")
        hash2 = fnv1a_32("user2")
        self.assertNotEqual(hash1, hash2)

    def test_returns_32bit_unsigned(self):
        """Result should be within 32-bit unsigned range."""
        result = fnv1a_32("some long string to test hash range")
        self.assertGreaterEqual(result, 0)
        self.assertLess(result, 2**32)

    def test_unicode_support(self):
        """Should handle unicode strings."""
        # Should not raise
        result = fnv1a_32("测试中文")
        self.assertIsInstance(result, int)
        self.assertGreaterEqual(result, 0)
        self.assertLess(result, 2**32)


if __name__ == "__main__":
    unittest.main()
