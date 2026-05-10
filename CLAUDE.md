# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in
this repository.

For any file search or grep in the current git-indexed directory, use fff tools.

## Project Overview

This is a recipe cookbook built around **Obsidian** as the primary editing environment.
`src/` is the Obsidian vault. Recipes are written in Norwegian by default. Obsidian
Publish is a possible but non-primary publishing target. Claude maintains the wiki. The
human curates sources, asks questions, and guides the analysis.

Use the Obsidian CLI skill when working with the wiki.

## Workflow

New recipes arrive in `src/raw/` — scraped, imported, or drafted externally. Claude
reads `src/raw/` but never edits it. After reviewing a raw file, Claude places the
polished recipe in the correct wiki category under `src/`. All other files in `src/`
(except `src/raw/`) are Claude's domain to create and edit.

Prepend an entry to `src/CHANGELOG.md` with the date, source name, and what changed —
newest entry goes at the top. A single source may touch 10-15 wiki pages. That is
normal.

## Architecture

- **Vault root**: `src/` — Obsidian vault
- **Recipe categories**: `Bakst/`, `Dessert/`, `Enkel servering/`, `Hovedretter/`
- **Sub-recipes / components**: individual files (e.g. `Bakst/Bolledeig.md`,
  `Bakst/Sjokoladefyll.md`) embedded into parent recipes via `![[...]]` transclusion
- **Ingredient index**: `Ingredienser/` — one file per ingredient, linked with `[[...]]`
- **Authors**: `Forfattere/` — one file per author/source
- **Images**: `src/Attachments/[recipe-slug]/`
- **Raw inbox**: `src/raw/` — read-only for Claude; source material only
- **Templates**: `src/templates/`

## Page format

Every recipe should follow this structure, unless they are made from several. Then use
the splitting pattern described below.

```markdown
---
author:
  - "[[Navn på kokk hvis noen finnes]]"
cover:
  - Attachments/tittel-pa-filen/bilde.webp
permalink: tittel-pa-filen
ingredients:
  - "[[Lenke til ingrediens]]"
aliases:
  - alternative skrivemåter
id: Tittel på filen
tags: []
description: 120 min | Enkel
---

# Tittel på filen

![](Attachments/tittel-pa-filen/bilde.webp)

> [!info]
>
> [Denne oppskriften](lenke-til-oppskrift-hvis-noen-finnes) er originalt fra
> [[dejligbakst]].

| ⏲️ Tid  | 🍽️ Porsjoner  | 👨‍🍳 Vanskelighetsgrad |
| ------- | ------------- | -------------------- |
| 120 min | ca. 20 boller | Enkel                |

## Ingredienser

#ingredient

- [x] 1 [[Ingrediens|ingrediens med alias]]

## Steg

1. Stegene for å lage retten, hvor alle ingredienser har wiki-link referanse.
```

## Complex Recipes — Splitting Pattern

When a recipe is built from multiple sub-preparations, split it into separate files and
use Obsidian transclusion. See `Bakst/Appelsinboller.md` as the canonical example:

- `Appelsinboller.md` — main recipe; embeds sub-recipes via `![[Bolledeig#Steg]]`,
  `![[Sjokoladefyll#Ingredienser]]`, etc.
- `Bakst/Bolledeig.md` — standalone reusable dough recipe
- `Bakst/Sjokoladefyll.md` — standalone filling recipe
- `Bakst/Appelsinkrem.md` — standalone cream recipe

Apply this pattern whenever a raw recipe contains distinct sub-preparations that could
be reused independently (doughs, creams, sauces, fillings).

## Lint

When the user asks you to lint or audit the wiki, report findings as a numbered list
with suggested fixes.

`lint` covers three layers:

### 1. Format (automated)

```bash
mise run format:check   # check only
mise run format:fix     # fix in place
```

Also check that all pages follow the page format above.

### 2. Link hygiene (manual review)

- **Broken wiki links**: `[[IngredientName]]` that has no matching file in
  `Ingredienser/` — create the missing file or correct the spelling
- **Unlinked recipes**: recipe files that exist but are not reachable via any category
  index or parent recipe — add the link in the appropriate index or category overview
- **Missing ingredient links**: plain-text ingredient mentions that should be
  `[[LinkedIngredient]]`
- Identify concepts mentioned in pages that lack their own page
- Flag claims that may be outdated based on newer sources

### 3. Recipe structure (manual review)

- Identify raw or wiki recipes where multiple distinct sub-preparations are embedded
  inline and split them into separate files following the splitting pattern above
- Ensure each sub-recipe is transcluded (`![[...]]`) from the parent, not duplicated
- Check for contradictions between pages
- When finding recipes or recipe sections (for example a sauce) that look similar,
  Claude should ask if the recipes should be merged into one

## Citation rules

- Every factual claim should reference its source file
- Use the format (source: filename.pdf) after the claim
- If two sources disagree, note the contradiction explicitly
- If a claim has no source, mark it as needing verification

## Question answering

When the user asks a question:

1. Cite specific wiki pages in your response
2. If the answer is not in the wiki, say so clearly
3. If the answer is valuable, offer to save it as a new wiki page

Good answers should be filed back into the wiki so they compound over time.

## Rules

- Never modify anything in the `raw/` folder
- Always update `wiki/index.md` and `wiki/log.md` after changes
- Keep page names uppercase with whitespace (e.g. `Bakte poteter.md`)
- Write in clear, plain language
- When uncertain about how to categorize something, ask the user

## Key Configuration Files

- `.mise.toml`: task runner (format, thumbnail, scraper, migrate)
- `dprint.json`: formatter configuration
- `pyproject.toml`: Python project (rye/uv)

## Content Conventions

- YAML frontmatter: `id`, `aliases`, `tags`, `author`, `cover`, `description`,
  `ingredients` (as `[[WikiLinks]]`), `permalink`, `up`
- Ingredient links: always `[[Ingredient]]` — creates graph edges Obsidian can traverse
- Images: `Attachments/[recipe-slug]/filename.webp`
- Language: Norwegian

## Development Commands

```bash
# Format
mise run format:check
mise run format:fix

# Thumbnails
mise thumbnail

# Fix encoding issues
mise fix

# Recipe scraper (edit scraper.py URL first)
mise run recipe-scrapers:run

# Migrate raw → wiki (dry run first)
mise run migrate:dry-run
mise run migrate:execute
```

## Automated Workflows

- **Formatting**: dprint + thumbnail generation on PRs
- **Issue to PR**: converts recipe-request issues to PRs
