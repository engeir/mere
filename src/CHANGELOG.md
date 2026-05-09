---
id: CHANGELOG
aliases: []
tags: []
---

# CHANGELOG

## 2026-05-09 — Lint: Laks med mangosalsa / Mangosalsa

- `Enkel servering/Mangosalsa.md`: added missing wiki-links on all ingredient lines;
  fixed typo "papper" → "pepper"; added Mango, Rødløk, Avokado, Chili, Lime to
  frontmatter `ingredients`
- `Hovedretter/Laks med mangosalsa.md`: removed redundant info callout; replaced inline
  mangosalsa ingredients/steps with `![[Mangosalsa#Ingredienser]]` /
  `![[Mangosalsa#Steg]]` transclusion

## 2026-05-09 — Planlegg

- **Ny**: `Planlegg.md` — Dataview-side som finner oppskrifter basert på prioritert
  liste. Støtter både oppskrifter (henter alle ingredienser) og enkeltingredienser
  direkte. Første element i `lyst` får høyest vekt (`n`), siste får 1.

## 2026-05-09 — Broken link audit

- **Fixed**: `[[sherry-]]` → `[[Sherryeddik]]` in `Spicy pasta med grønnkål.md` (broken
  partial link)
- **Fixed**: 23 recipe files — converted alias-based links to piped canonical form (e.g.
  `[[Isbergssalat]]` → `[[Salat|Isbergssalat]]`). Obsidian's metadata cache does not
  resolve `aliases:` frontmatter for graph edges; piped links are required. Result: 0
  unresolved links.

## 2026-05-09 — Lint audit

- **Format**: Fixed prettier violations in `CHANGELOG.md` and `Utforsk.md`
- **Moved**: `Dessert/Sjokoladefyll.md` → `Bakst/Sjokoladefyll.md` (sub-recipe belongs
  with its parent `Appelsinboller`)
- **Renamed**: `Dessert/hello-world.md` → `Dessert/Hello, World!.md` (naming convention:
  uppercase with whitespace)
- **Deleted**: `src/test.md` (Dataview experiment artifact, not a real recipe)
