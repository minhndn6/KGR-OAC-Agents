"""
decode_double_json.py — small utility to handle double-JSON-encoded strings.

Usage (CLI):
    python decode_double_json.py <file_path>

Prints top-level keys of the decoded object.
"""
import json
import sys
from pathlib import Path


def decode(text: str):
    """JSON-parse once; if result is still a str, parse again. Returns the object."""
    obj = json.loads(text)
    if isinstance(obj, str):
        obj = json.loads(obj)
    return obj


def main():
    if len(sys.argv) < 2:
        print("Usage: python decode_double_json.py <file_path>")
        sys.exit(1)

    path = Path(sys.argv[1])
    if not path.exists():
        print(f"ERROR: file not found: {path}")
        sys.exit(1)

    text = path.read_text(encoding="utf-8")
    obj = decode(text)

    if isinstance(obj, dict):
        print(f"Top-level keys ({len(obj)}):")
        for k in obj:
            print(f"  {k}")
    elif isinstance(obj, list):
        print(f"Top-level list with {len(obj)} items.")
    else:
        print(f"Decoded value: {obj!r}")


if __name__ == "__main__":
    main()
