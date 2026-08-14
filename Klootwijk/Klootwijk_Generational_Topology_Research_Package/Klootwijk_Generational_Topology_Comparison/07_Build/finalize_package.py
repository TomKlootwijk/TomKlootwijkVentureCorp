#!/usr/bin/env python3
"""Create a deterministic package manifest and SHA-256 checksum list."""
from __future__ import annotations

import csv
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "MANIFEST.csv"
CHECKSUMS = ROOT / "SHA256SUMS.txt"

EXCLUDED_NAMES = {MANIFEST.name, CHECKSUMS.name}
EXCLUDED_PARTS = {"__pycache__"}
EXCLUDED_SUFFIXES = {".pyc", ".tmp", ".lock"}


def eligible(path: Path) -> bool:
    rel = path.relative_to(ROOT)
    if path.name in EXCLUDED_NAMES:
        return False
    if any(part in EXCLUDED_PARTS for part in rel.parts):
        return False
    if path.suffix in EXCLUDED_SUFFIXES:
        return False
    return path.is_file()


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def category(rel: Path) -> str:
    return rel.parts[0] if len(rel.parts) > 1 else "package-root"


def main() -> None:
    files = sorted((p for p in ROOT.rglob("*") if eligible(p)), key=lambda p: p.as_posix())
    with MANIFEST.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["relative_path", "bytes", "category"])
        for path in files:
            rel = path.relative_to(ROOT)
            w.writerow([rel.as_posix(), path.stat().st_size, category(rel)])

    checksum_files = sorted(
        [p for p in ROOT.rglob("*") if eligible(p)] + [MANIFEST],
        key=lambda p: p.relative_to(ROOT).as_posix(),
    )
    with CHECKSUMS.open("w", encoding="utf-8") as f:
        for path in checksum_files:
            f.write(f"{sha256(path)}  {path.relative_to(ROOT).as_posix()}\n")

    print(f"Manifest entries: {len(files)}")
    print(MANIFEST)
    print(CHECKSUMS)


if __name__ == "__main__":
    main()
