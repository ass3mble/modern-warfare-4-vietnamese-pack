#!/usr/bin/env python3
"""Offline Windows MW4 Vietnamese installer with hash pin and exact backup.

Requires only Python 3 standard library, never runs the game or native files.
Output package contains only VI text; installed game supplies English keys.
"""
from __future__ import annotations

import argparse
import base64
import gzip
import hashlib
import json
import os
import shutil
import struct
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PACK = ROOT / "pack"
ENC = "utf-8"


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as inp:
        for block in iter(lambda: inp.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def get_pack():
    manifest = json.loads((PACK / "manifest.json").read_text(ENC))
    if manifest.get("format") != "mw4-vi-only-overlay-v1":
        raise ValueError("Unknown or invalid localization package")
    encoded = []
    for i, name in enumerate(manifest["chunks"]):
        if not name.startswith("v6157.part") or not name.endswith(".b64") or Path(name).name != name:
            raise ValueError("Unsafe chunk name")
        part = (PACK / name).read_text("ascii").strip()
        if len(part) != manifest["chunk_byte_length"][i]:
            raise ValueError(f"Damaged chunk {name}")
        encoded.append(part)
    joined = "".join(encoded)
    if sha(joined.encode("ascii")) != manifest["encoded_sha256"]:
        raise ValueError("Checksum mismatch on distributed text chunks")
    zipped = base64.b64decode(joined, validate=True)
    if sha(zipped) != manifest["gzip_sha256"]:
        raise ValueError("Checksum mismatch on compressed localization")
    pack = json.loads(gzip.decompress(zipped).decode(ENC))
    if (pack["format"], pack["english_key_count"],
        pack["english_fingerprint_sha256"], pack["expected_installed_sha256"]) != (
            manifest["format"], manifest["game_dictionary_count"],
            manifest["english_fingerprint_sha256"], manifest["expected_installed_sha256"]):
        raise ValueError("Package manifest conflicts with translation contents")
    if len(pack["vi_strings"]) != manifest["game_dictionary_count"]:
        raise ValueError("Incomplete Vietnamese translation pack")
    return manifest, pack["vi_strings"]


def rebuild(original: bytes, vi: list[str], expected_count: int):
    if len(original) < 4:
        raise ValueError("Invalid source dictionary")
    count = struct.unpack_from("<I", original, 0)[0]
    if count != expected_count:
        raise ValueError(f"Unsupported game update: dictionary has {count} keys, expected {expected_count}")
    out = bytearray(struct.pack("<I", count))
    en_hasher = hashlib.sha256()
    en_hasher.update(struct.pack("<I", count))
    pos = 4
    for idx in range(count):
        if pos + 2 > len(original):
            raise ValueError("Invalid English field length")
        n = struct.unpack_from("<H", original, pos)[0]
        pos += 2
        if not n or pos + n > len(original):
            raise ValueError("Invalid English field data")
        en = original[pos:pos+n]
        en.decode(ENC, errors="strict")
        length_prefix = struct.pack("<H", n)
        out.extend(length_prefix)
        out.extend(en)
        en_hasher.update(length_prefix)
        en_hasher.update(en)
        pos += n
        if pos + 2 > len(original):
            raise ValueError("Invalid old translation length")
        current_length = struct.unpack_from("<H", original, pos)[0]
        pos += 2
        if pos + current_length > len(original):
            raise ValueError("Invalid old translation field")
        original[pos:pos+current_length].decode(ENC, errors="strict")
        pos += current_length
        target = vi[idx].encode(ENC, errors="strict")
        if not 0 < len(target) <= 65535:
            raise ValueError(f"Invalid Vietnamese text size at key {idx}")
        out.extend(struct.pack("<H", len(target)))
        out.extend(target)
    if pos != len(original):
        raise ValueError("Trailing bytes in game dictionary")
    return bytes(out), en_hasher.hexdigest()


def game_running():
    if os.name != "nt":
        return False
    try:
        import subprocess
        cp = subprocess.run(["tasklist", "/FO", "CSV", "/NH"],
                            check=False, capture_output=True, text=True,
                            timeout=10)
        names = ("sp26-cod.exe", "cod.exe", "modernwarfare.exe")
        return any(f'"{n}"' in cp.stdout.lower() for n in names)
    except (OSError, Exception):
        # Fail closed if unable to verify game exit.
        raise RuntimeError("Unable to determine whether the game is running")


def choose_folder(value: str | None) -> Path:
    if value:
        return Path(value.strip().strip('"')).expanduser().resolve()
    if (ROOT / "sp26" / "trdata2.bin").is_file():
        return ROOT
    try:
        import tkinter
        from tkinter import filedialog
        window = tkinter.Tk()
        window.withdraw()
        selected = filedialog.askdirectory(title="Select game folder containing sp26")
        window.destroy()
        if selected:
            return Path(selected).resolve()
    except Exception:
        pass
    return Path(input("Paste GAME folder path containing sp26: ").strip().strip('"')).expanduser().resolve()


def install(game_dir: Path, verify_only=False):
    manifest, vi = get_pack()
    live = game_dir / "sp26" / "trdata2.bin"
    if not live.is_file():
        raise FileNotFoundError(f"Game dictionary not found: {live}")
    if game_running():
        raise RuntimeError("Game is running. Close it completely before installation")
    original = live.read_bytes()
    original_sha = sha(original)
    if original_sha == manifest["expected_installed_sha256"]:
        print("ALREADY INSTALLED: V6.157 is byte-for-byte identical")
        return
    assembled, en_digest = rebuild(original, vi, manifest["game_dictionary_count"])
    if en_digest != manifest["english_fingerprint_sha256"]:
        raise ValueError("Incompatible English-key corpus; different game build. Nothing changed")
    candidate_sha = sha(assembled)
    if candidate_sha != manifest["expected_installed_sha256"]:
        raise ValueError("Expected installed SHA differs; patch rejected")
    print("SOURCE COMPATIBILITY: PASS (40,085 keys)")
    print("CANDIDATE SHA256:", candidate_sha)
    if verify_only:
        print("VERIFY-ONLY SUCCESS: no files changed")
        return
    if sha_file(live) != original_sha:
        raise RuntimeError("Game dictionary changed during verification")
    stamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    backup = Path(f"{live}.BACKUP-{stamp}-{original_sha[:12]}")
    stage = Path(f"{live}.STAGING-{stamp}-{os.getpid()}")
    if backup.exists() or stage.exists():
        raise FileExistsError("Backup or temporary name collision")
    with stage.open("xb") as f:
        f.write(assembled)
        f.flush()
        os.fsync(f.fileno())
    try:
        if sha_file(stage) != candidate_sha:
            raise ValueError("Staged candidate failed checksum verification")
        if sha_file(live) != original_sha or game_running():
            raise RuntimeError("The game started or dictionary changed. Aborting")
        with backup.open("xb") as f:
            f.write(original)
            f.flush()
            os.fsync(f.fileno())
        if sha_file(backup) != original_sha:
            raise RuntimeError("Backup failed integrity validation")
        if sha_file(live) != original_sha:
            raise RuntimeError("Original file changed after backup. Aborting")
        # Atomic rename in same volume. The backed-up original is never deleted.
        os.replace(stage, live)
        if sha_file(live) != candidate_sha:
            raise RuntimeError("Postinstall SHA mismatch. Restore from verified backup")
        if sha_file(backup) != original_sha:
            raise RuntimeError("Backup has been unexpectedly changed")
    finally:
        if stage.exists():
            stage.unlink()
    print("SUCCESS: Installed Vietnamese localization V6.157")
    print("BACKUP (keep this file):", backup)
    print("Installed SHA256:", candidate_sha)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--game-dir", default=None)
    parser.add_argument("--verify-only", action="store_true")
    args = parser.parse_args()
    print("=== Modern Warfare 4 Vietnamese Pack V6.157 ===")
    try:
        install(choose_folder(args.game_dir), args.verify_only)
    except Exception as exc:
        print("STOP:", str(exc))
        print("No game executable or native DLL/FF was changed.")
        sys.exit(1)


if __name__ == "__main__":
    main()
