---
name: translate
description: Translate a chapter of The Perfect Run from English to Russian. Takes a chapter number as argument.
argument-hint: "[chapter-number]"
---

# The Perfect Run — English to Russian Translation

You are translating chapter $ARGUMENTS of "The Perfect Run" by Maxime J. Durand.

## Workflow

1. **Extract glossary terms** for this chapter:
   ```bash
   source .venv/bin/activate && python scripts/extract_terms.py $ARGUMENTS
   ```
2. **Read the English chapter**: `chapters/en/<chapter_number_padded>.md` (zero-padded to 3 digits, e.g. chapter 5 → `005.md`)
3. **Use the extract_terms output as your glossary reference.** Do NOT read the full `glossary.yaml` — the extract already gives you all relevant EN→RU terms. Only open `glossary.yaml` if you need to add a new term.
4. **Translate** the full chapter into Russian, following all guidelines below.
5. **Write** the translation to `chapters/ru/<chapter_number_padded>.md`
6. **Validate** the translation:
   ```bash
   source .venv/bin/activate && python scripts/validate_terms.py $ARGUMENTS
   ```
7. **Update `chapters/manifest.json`** — fill in the `title_ru` field for this chapter.
8. **Report new terms.** If the chapter introduces names, places, aliases, or recurring terms not in the glossary, **do NOT add them to `glossary.yaml` yourself.** Instead, write a file `chapters/ru/<chapter_number_padded>.terms.md` listing each new term as an EN→RU pair with a short note. Example:
   ```
   - Fisty → Фисти — Ryan's pisto-gauntlet name. Transliterated (proper noun).
   - Blower → Поддувала — Ryan's nickname for Sarin. Preserves double meaning.
   ```
   The orchestrating agent will consolidate terms across chapters, resolve conflicts, and update the glossary.

## Core Principle

**«Если фраза звучит как перевод — она плохая.»** Always prefer natural Russian over literal accuracy. Find the Russian way to say it, not Russian words for the English.

## Glossary (`glossary.yaml`)

The glossary is the single source of truth for term consistency. Extracted terms are **mandatory, non-negotiable** — use them exactly as given.

### Rules

- **Transliterate** character names and place names by default (Райан, Нью-Ром).
- Where a name has obvious semantic meaning relevant to the story, add a translator's note in brackets on first occurrence, e.g.: `Квиксейв [быстрое сохранение]`.
- Do NOT add translator's notes for every name — only where the meaning is plot-relevant.
- NEVER change an existing glossary translation without updating all already-translated chapters.

## Style

- **Match the author's register.** The Perfect Run shifts between comedic action, tense thriller scenes, emotional flashbacks, and sci-fi exposition. The Russian text must follow these shifts naturally.
- **Ryan's voice** is irreverent, pop-culture-obsessed, theatrical, and genuinely kind underneath the clowning. He speaks like someone who has lived thousands of loops and treats everything as a game — but cares deeply when it matters. Avoid making him sound stiff or literary where the English is playful.
- **Natural Syntax:** Avoid clunky subordinate clauses starting with "который". Use natural participial phrases (причастный/деепричастный оборот) where possible.
- **Do not flatten idioms.** Find Russian equivalents that carry the same tone and weight. **Always prefer a natural Russian idiom over a calque.**
- **Preserve deliberate ambiguity.** If the original is deliberately vague, preserve it.
- **Preserve sentence rhythm.** Short punchy sentence → short punchy sentence. Long winding → long winding.
- **Use natural мат** when the English uses profanity. Match intensity: mild "damn" → «чёрт»; full "fuck" → «блядь»; "holy shit" → «ёб твою мать». Don't force it where the English is clean.

## Terminology Consistency

- **Genome / Elixir terminology** — use glossary terms exactly. The superpower system is central.
- **Power names** — transliterate or translate per glossary.
- **Faction/Organization names** — follow glossary.

## False Friends and Calque Traps

- "eventually" ≠ эвентуально → «в конце концов», «в итоге»
- "accurate" ≠ аккуратный → «точный», «меткий»
- "fabric" ≠ фабрика → «ткань»
- "actual" ≠ актуальный → «настоящий», «фактический»
- "sympathetic" ≠ симпатичный → «сочувствующий», «понимающий»

## Formality (Ты / Вы)

- Default **ты** for peers, friends, informal contexts.
- **Вы** for strangers, authority figures, formal settings.
- Ryan tends to be informal (ты) with everyone — others may address him formally.

## Dialogue Formatting

In Russian em-dash dialogue, speech/narrator boundaries can blur. **Check quote boundaries in every dialogue paragraph.**

1. If text follows a closing `"` in English, it's narrator — separate it in Russian.
2. Italic narrator thoughts between speech → separate paragraph.
3. Non-italic narrator after speech (no attribution) → separate paragraph.
4. Attribution (`— сказал он.`) between speech and narrator solves the boundary.

## Translator's Notes

- Format: `[прим. пер.: ...]`. Use sparingly.
- Only for: name meanings that matter, untranslatable wordplay, pop-culture references.

## Naturalness Checklist

Watch for:
- Calques and literal translations of English idioms
- Unnatural word order
- Stilted constructions: «в качестве», «является», «осуществлять»
- Register breaks without cause
- Unnecessary «который» chains
- Bureaucratic language where simpler Russian exists

**The core test: «Мог бы это написать русский автор, а не переводчик?»**

## Constraints

- Do NOT skip or summarize any content. Translate everything.
- Do NOT "improve" or editorialize. If the author wrote something awkward on purpose, preserve it.
- Do NOT merge or split chapters. Maintain 1:1 correspondence.
