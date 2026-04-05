#!/usr/bin/env python3
"""Validate a translated chapter against known-bad translations (blacklist).

Usage:
    python scripts/validate_terms.py <chapter_number>
"""

import re
import sys
from pathlib import Path

PROJECT_DIR = Path("/Users/emil_rysin/the-perfect-run-translation")
CHAPTERS_RU = PROJECT_DIR / "chapters" / "ru"

# Known-bad translations: (regex_pattern, explanation)
# Add entries as translation progresses and mistakes are identified.
BLACKLIST: list[tuple[str, str]] = [
    # Example entries — populate as the project discovers recurring mistakes:
    # (r"\bисключени[еяю]\b", "Lore-related 'Exclusion' should not use 'исключение'"),
]


def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/validate_terms.py <chapter_number>")
        sys.exit(1)

    chapter_num = int(sys.argv[1])
    chapter_path = CHAPTERS_RU / f"{chapter_num:03d}.md"

    if not chapter_path.exists():
        print(f"Translated chapter not found: {chapter_path}")
        sys.exit(1)

    text = chapter_path.read_text(encoding="utf-8")
    issues = []

    for pattern, explanation in BLACKLIST:
        for match in re.finditer(pattern, text, re.IGNORECASE):
            line_num = text[:match.start()].count("\n") + 1
            issues.append((line_num, match.group(), explanation))

    if not issues:
        print(f"Chapter {chapter_num:03d}: No blacklist violations found.")
    else:
        print(f"Chapter {chapter_num:03d}: {len(issues)} blacklist violation(s):")
        for line_num, matched, explanation in issues:
            print(f"  Line {line_num}: '{matched}' — {explanation}")


if __name__ == "__main__":
    main()
