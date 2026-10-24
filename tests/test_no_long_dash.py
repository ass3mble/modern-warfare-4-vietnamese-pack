"""Prevent long dash punctuation in text published in this repository.

Prefer the ordinary ASCII hyphen, U+002D, for prose and headings.
Archive payload chunks (*.b64) contain compressed translation data and
are intentionally not changed by formatting rules.
"""

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROHIBITED = {chr(code) for code in (0x2012, 0x2013, 0x2014, 0x2015)}
PROHIBITED_ENTITIES = ("&mdash;", "&ndash;", "&#8212;", "&#8211;",
                       "&#x2014;", "&#x2013;")
TEXT_SUFFIXES = {".md", ".py", ".bat", ".ps1", ".json", ".txt", ".yaml", ".yml", ".toml", ".ini"}
EXTRA_TEXT_FILES = {".gitignore", ".gitattributes", "LICENSE"}


class TextStyleTests(unittest.TestCase):
    def test_no_long_dash_punctuation_in_repository_content(self):
        violations = []
        for path in sorted(ROOT.rglob("*")):
            if not path.is_file():
                continue
            if any(part in {".git", ".venv", "__pycache__"} for part in path.relative_to(ROOT).parts):
                continue
            if path.suffix.lower() not in TEXT_SUFFIXES and path.name not in EXTRA_TEXT_FILES:
                continue
            body = path.read_text(encoding="utf-8")
            for line_number, line in enumerate(body.splitlines(), 1):
                if any(ch in line for ch in PROHIBITED):
                    violations.append(f"{path.relative_to(ROOT)}:{line_number}")
                if any(entity in line.lower() for entity in PROHIBITED_ENTITIES):
                    violations.append(f"{path.relative_to(ROOT)}:{line_number} (HTML entity)")
        self.assertFalse(violations, "Replace long dash punctuation with a normal '-' in: " +
                         ", ".join(violations))


if __name__ == "__main__":
    unittest.main()
