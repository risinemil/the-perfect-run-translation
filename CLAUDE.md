# The Perfect Run — Translation Project

English to Russian translation of Maxime J. Durand's "The Perfect Run".

## Structure

```
chapters/en/     — 130 English chapter files (000.md–129.md)
chapters/ru/     — Russian translations (to be created)
chapters/manifest.json — chapter metadata
glossary.yaml    — term consistency glossary (source of truth)
SKILL.md         — translation workflow and guidelines
assets/          — images, CSS from epub
scripts/         — extraction and validation tools
reviews/         — translation QA documents
```

## Skills

- `/translate <chapter_number>` — translates a chapter from English to Russian following all guidelines

## Key Commands

```bash
source .venv/bin/activate  # activate Python environment
python scripts/extract_terms.py <N>   # pre-translation glossary scan
python scripts/validate_terms.py <N>  # post-translation blacklist check
```

## Rules

- Always check glossary.yaml for term consistency
- Never change glossary terms without updating all translated chapters
