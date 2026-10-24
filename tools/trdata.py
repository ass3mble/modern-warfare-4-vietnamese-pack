#!/usr/bin/env python3
"""Offline, source-only validator for a length-prefixed UTF-8 EN/VI dictionary.

No game APIs, injection, external libraries or installation behavior.
Format: little-endian u32 row count, repeated u16+utf8 EN / u16+utf8 VI.
"""
import argparse
import csv
import hashlib
import re
import struct
import unicodedata
from pathlib import Path

TOKEN = re.compile(
    r"\^?#x[0-9A-Fa-f]+\.#x[0-9A-Fa-f]+\^?|"
    r"\^F[^^\r\n]+\^|\^\.[0-9]+|\^\$|\^\^[A-Za-z]|"
    r"\^[0-9A-Za-z%+$]|&&[0-9]+|\[\{[^}]*\}\]|\{[^{}]+\}|"
    r"%[-\d.]*[a-zA-Z]"
)


def digest(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def parse(data):
    if len(data) < 4:
        raise ValueError("Header missing")
    count = struct.unpack_from("<I", data)[0]
    if count > 1_000_000:
        raise ValueError("Unreasonable entry count")
    pos, result = 4, []
    for index in range(count):
        pair = []
        for field in ("English", "Vietnamese"):
            if pos + 2 > len(data):
                raise ValueError(f"Truncated length at {index} {field}")
            size = struct.unpack_from("<H", data, pos)[0]
            pos += 2
            if pos + size > len(data):
                raise ValueError(f"Truncated contents at {index} {field}")
            try:
                value = data[pos:pos + size].decode("utf-8", errors="strict")
            except UnicodeDecodeError as error:
                raise ValueError(f"Invalid UTF-8 at {index} {field}") from error
            pos += size
            pair.append(value)
        result.append(tuple(pair))
    if pos != len(data):
        raise ValueError("Unexpected trailing bytes")
    return result


def pack(rows):
    out = bytearray(struct.pack("<I", len(rows)))
    for index, (english, translation) in enumerate(rows):
        for field in (english, translation):
            raw = field.encode("utf-8")
            if not 0 < len(raw) <= 65535:
                raise ValueError(f"Invalid UTF-8 field length at {index}")
            out.extend(struct.pack("<H", len(raw)))
            out.extend(raw)
    return bytes(out)


def read_rows(path, expect_count=None):
    payload = Path(path).read_bytes()
    rows = parse(payload)
    if pack(rows) != payload:
        raise ValueError("Dictionary failed exact round-trip validation")
    if expect_count is not None and len(rows) != expect_count:
        raise ValueError(f"Count mismatch: got {len(rows)}, expected {expect_count}")
    if len(set(en for en, _ in rows)) != len(rows):
        raise ValueError("Duplicate source strings: IDs may not be unambiguous")
    return rows


def read_review(path):
    with Path(path).open("r", encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        required = {"id", "EN_exact", "installed_VI_exact", "candidate_VI_exact"}
        if not reader.fieldnames or not required.issubset(reader.fieldnames):
            raise ValueError("Review CSV requires id, EN_exact, installed_VI_exact, candidate_VI_exact")
        changes = {}
        for record in reader:
            index = int(record["id"])
            if index in changes:
                raise ValueError(f"Duplicate reviewed ID {index}")
            changes[index] = record
    if not changes:
        raise ValueError("Empty review")
    return changes


def check_change(old, new, index):
    if not unicodedata.is_normalized("NFC", new):
        raise ValueError(f"Non-NFC Vietnamese text at ID {index}")
    if any(ch == "\x00" for ch in new):
        raise ValueError(f"Null byte at ID {index}")
    if (old.count("\n"), old.count("\r")) != (new.count("\n"), new.count("\r")):
        raise ValueError(f"Line break count changed at ID {index}")
    if TOKEN.findall(old) != TOKEN.findall(new):
        raise ValueError(f"Control placeholders changed at ID {index}")


def apply_review(rows, changes):
    changed = list(rows)
    for index, record in sorted(changes.items()):
        if not 0 <= index < len(rows):
            raise ValueError(f"Unknown ID {index}")
        en, vi = rows[index]
        if en != record["EN_exact"] or vi != record["installed_VI_exact"]:
            raise ValueError(f"Original source/translation drift at ID {index}")
        proposal = record["candidate_VI_exact"]
        if proposal == vi:
            raise ValueError(f"Unchanged proposal at ID {index}")
        check_change(vi, proposal, index)
        changed[index] = (en, proposal)
    return changed


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    inspect = sub.add_parser("inspect", help="Read-only dictionary integrity inspection")
    inspect.add_argument("source")
    inspect.add_argument("--expect-count", type=int)
    build = sub.add_parser("build", help="Build a new candidate in a separate file")
    build.add_argument("source")
    build.add_argument("review")
    build.add_argument("--base-sha", required=True)
    build.add_argument("--out", required=True)
    build.add_argument("--expect-count", type=int)
    verify = sub.add_parser("verify", help="Independently compare candidate to base and review")
    verify.add_argument("source")
    verify.add_argument("candidate")
    verify.add_argument("--review", required=True)
    args = parser.parse_args()
    if args.command == "inspect":
        rows = read_rows(args.source, args.expect_count)
        print(f"PASS: {len(rows)} rows, sha256={digest(args.source)}")
    elif args.command == "build":
        src = Path(args.source).resolve()
        dst = Path(args.out).resolve()
        if src == dst:
            raise ValueError("Refusing to overwrite source")
        if dst.exists():
            raise FileExistsError(f"Output already exists: {dst}")
        if digest(src).lower() != args.base_sha.lower():
            raise ValueError("SHA-256 pin mismatch; refusing to build")
        rows = read_rows(src, args.expect_count)
        revised = apply_review(rows, read_review(args.review))
        if digest(src).lower() != args.base_sha.lower():
            raise ValueError("Source changed during review")
        payload = pack(revised)
        if parse(payload) != revised:
            raise ValueError("Candidate failed round trip")
        # Exclusive-create prevents overwriting an existing stage.
        with dst.open("xb") as stream:
            stream.write(payload)
        print(f"PASS: detached {len(revised)}-entry candidate: {dst}; sha256={digest(dst)}")
    else:
        original = read_rows(args.source)
        candidate = read_rows(args.candidate)
        if len(original) != len(candidate):
            raise ValueError("Entry count changed")
        changes = read_review(args.review)
        expected = apply_review(original, changes)
        if expected != candidate:
            raise ValueError("Candidate differs from reviewed changes")
        print(f"PASS: {len(changes)} exact reviewed modifications; other entries preserved")


if __name__ == "__main__":
    main()
