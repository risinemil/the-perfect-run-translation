#!/usr/bin/env python3
"""Extract epub chapters to individual Markdown files.

Phase 1 of The Perfect Run translation workflow.
Reads XHTML chapter files from the extracted epub and converts them to Markdown,
preserving formatting (bold, italic, headers, tables, block quotes, hr, images).
"""

import json
import re
import shutil
from pathlib import Path

from bs4 import BeautifulSoup
from markdownify import markdownify as md

EXTRACT_DIR = Path("/private/tmp/tpr_extract/OEBPS")
TEXT_DIR = EXTRACT_DIR / "Text"
PROJECT_DIR = Path("/Users/emil_rysin/the-perfect-run-translation")
CHAPTERS_EN = PROJECT_DIR / "chapters" / "en"
ASSETS_DIR = PROJECT_DIR / "assets"


def extract_title_from_filename(filename: str) -> str:
    """Extract human-readable title from filename like '0001_2_The_Save_Point.xhtml'."""
    name = filename.replace(".xhtml", "")
    name = re.sub(r"^\d+_\d+_", "", name)
    name = name.replace("_", " ")
    return name


def convert_chapter(xhtml_path: Path) -> tuple[str, str]:
    """Convert an XHTML chapter file to Markdown. Returns (title, markdown_content)."""
    with open(xhtml_path, "r", encoding="utf-8") as f:
        html = f.read()

    soup = BeautifulSoup(html, "lxml")
    body = soup.find("body")
    if not body:
        return "", ""

    h1 = body.find("h1")
    title = h1.get_text(strip=True) if h1 else extract_title_from_filename(xhtml_path.name)

    markdown = md(str(body), heading_style="ATX", bullets="-", strip=["script", "style"])

    markdown = re.sub(r"\n{3,}", "\n\n", markdown)
    markdown = markdown.strip() + "\n"

    return title, markdown


def main():
    CHAPTERS_EN.mkdir(parents=True, exist_ok=True)
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)

    xhtml_files = sorted(
        f for f in TEXT_DIR.iterdir()
        if f.suffix == ".xhtml" and f.name != "Cover.xhtml"
    )

    print(f"Found {len(xhtml_files)} chapter files")

    manifest = {"chapters": []}

    for i, xhtml_path in enumerate(xhtml_files):
        chapter_num = f"{i:03d}"
        out_path = CHAPTERS_EN / f"{chapter_num}.md"

        title, markdown = convert_chapter(xhtml_path)
        if not markdown:
            print(f"  WARNING: Empty content for {xhtml_path.name}")
            continue

        with open(out_path, "w", encoding="utf-8") as f:
            f.write(markdown)

        manifest["chapters"].append({
            "file": f"{chapter_num}.md",
            "title_en": title,
            "title_ru": "",
            "source_file": xhtml_path.name,
        })

        if (i + 1) % 25 == 0:
            print(f"  Processed {i + 1}/{len(xhtml_files)} chapters")

    manifest_path = PROJECT_DIR / "chapters" / "manifest.json"
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    print(f"\nDone! Extracted {len(manifest['chapters'])} chapters to {CHAPTERS_EN}")
    print(f"Manifest written to {manifest_path}")

    # Copy assets
    images_dir = EXTRACT_DIR / "Images"
    if images_dir.exists():
        for img in images_dir.iterdir():
            shutil.copy2(img, ASSETS_DIR / img.name)
        print(f"Copied {len(list(images_dir.iterdir()))} images to {ASSETS_DIR}")

    styles_dir = EXTRACT_DIR / "Styles"
    if styles_dir.exists():
        for css in styles_dir.iterdir():
            shutil.copy2(css, ASSETS_DIR / css.name)
        print(f"Copied CSS to {ASSETS_DIR}")

    cover = EXTRACT_DIR / "Text" / "Cover.xhtml"
    if cover.exists():
        shutil.copy2(cover, ASSETS_DIR / "Cover.xhtml")

    for meta_file in ["content.opf", "toc.ncx"]:
        src = EXTRACT_DIR / meta_file
        if src.exists():
            shutil.copy2(src, ASSETS_DIR / meta_file)

    print("Assets copied.")


if __name__ == "__main__":
    main()
