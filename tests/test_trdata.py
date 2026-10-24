"""Synthetic-only regression tests: no copyrighted game files required."""
import importlib.util
import struct
import unittest
from pathlib import Path

MODULE = Path(__file__).resolve().parents[1] / "tools" / "trdata.py"
spec = importlib.util.spec_from_file_location("trdata", MODULE)
trdata = importlib.util.module_from_spec(spec)
spec.loader.exec_module(trdata)


class DictionaryTests(unittest.TestCase):
    def setUp(self):
        self.rows = [
            ("HELLO", "Xin chào"),
            ("Press [{+attack}] now!", "Nhấn [{+attack}] ngay!"),
            ("Line one\nLine two", "Dòng một\nDòng hai"),
        ]

    def test_binary_round_trip(self):
        payload = trdata.pack(self.rows)
        self.assertEqual(trdata.parse(payload), self.rows)
        self.assertEqual(struct.unpack_from("<I", payload)[0], 3)

    def test_parse_rejects_truncated_or_trailing(self):
        data = trdata.pack(self.rows)
        for broken in (data[:-1], data + b"x", b"\x01\x00"):
            with self.assertRaises(ValueError):
                trdata.parse(broken)

    def test_exact_review_changes_only_one_index(self):
        changes = {0: {
            "id": "0", "EN_exact": "HELLO",
            "installed_VI_exact": "Xin chào", "candidate_VI_exact": "Chào bạn"
        }}
        revised = trdata.apply_review(self.rows, changes)
        self.assertEqual(revised[0], ("HELLO", "Chào bạn"))
        self.assertEqual(revised[1:], self.rows[1:])

    def test_reject_source_drift(self):
        changes = {0: {
            "id": "0", "EN_exact": "WRONG",
            "installed_VI_exact": "Xin chào", "candidate_VI_exact": "Chào bạn"
        }}
        with self.assertRaises(ValueError):
            trdata.apply_review(self.rows, changes)

    def test_reject_placeholder_changes(self):
        with self.assertRaises(ValueError):
            trdata.check_change("Nhấn [{+attack}] đi", "Nhấn [{+reload}] đi", 1)

    def test_reject_newline_changes(self):
        with self.assertRaises(ValueError):
            trdata.check_change("Dòng một\nDòng hai", "Dòng một Dòng hai", 2)

    def test_reject_non_nfc(self):
        with self.assertRaises(ValueError):
            trdata.check_change("Đúng", "Du\u0301ng", 3)

    def test_utf8_errors(self):
        with self.assertRaises(ValueError):
            trdata.parse(struct.pack("<IHH", 1, 1, 0xFFFF))


if __name__ == "__main__":
    unittest.main()
