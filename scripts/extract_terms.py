#!/usr/bin/env python3
"""Scan an English chapter against the glossary and output EN→RU terms found.

Usage:
    python scripts/extract_terms.py <chapter_number>

Example:
    python scripts/extract_terms.py 5
"""

import re
import sys
from pathlib import Path

import yaml

PROJECT_DIR = Path("/Users/emil_rysin/the-perfect-run-translation")
GLOSSARY_PATH = PROJECT_DIR / "glossary.yaml"
CHAPTERS_EN = PROJECT_DIR / "chapters" / "en"


def load_glossary() -> list[dict]:
    """Load all glossary entries across all categories."""
    with open(GLOSSARY_PATH, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    entries = []
    for category, items in data.items():
        if isinstance(items, list):
            for item in items:
                if isinstance(item, dict) and "en" in item and "ru" in item:
                    entries.append(item)
    return entries


def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/extract_terms.py <chapter_number>")
        sys.exit(1)

    chapter_num = int(sys.argv[1])
    chapter_path = CHAPTERS_EN / f"{chapter_num:03d}.md"

    if not chapter_path.exists():
        print(f"Chapter file not found: {chapter_path}")
        sys.exit(1)

    text = chapter_path.read_text(encoding="utf-8")
    entries = load_glossary()

    found = []
    for entry in entries:
        en_term = entry["en"]
        # Check for the term (case-insensitive, whole word)
        pattern = re.compile(r"\b" + re.escape(en_term) + r"\b", re.IGNORECASE)
        if pattern.search(text):
            found.append(entry)

    if not found:
        print(f"No glossary terms found in chapter {chapter_num:03d}.")
        return

    print(f"Glossary terms in chapter {chapter_num:03d}:")
    print(f"{'EN':<35} {'RU':<35} {'Notes'}")
    print("-" * 100)
    for entry in found:
        notes = entry.get("notes", "")
        print(f"{entry['en']:<35} {entry['ru']:<35} {notes}")


if __name__ == "__main__":
    main()
