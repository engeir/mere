---
id: CHANGELOG
aliases: []
tags: []
---
## 2026-05-11 — Ny oppskrift: Ostegratinert kyllingfilet (HelloFresh)

- `Hovedretter/Ostegratinert kyllingfilet.md`: ny oppskrift fra HelloFresh — ovnsbakt ostegratinert kyllingfilet med sesampoteter, brokkoli og balsamicosalat
- `Ingredienser/Aioli.md`: ny ingrediensfil opprettet
- `Attachments/ostegratinert-kyllingfilet/`: mappe opprettet for bilder



# CHANGELOG

## 2026-05-10 — Ingredient hierarchy, field renames, body wikification (Category B)

- `Planlegg.md`: dataview updated — `score()` now traverses `parent:` and `ingredients:` on ingredient files recursively; searching `[[Pasta]]` finds recipes using `[[Tagliatelle]]`, `[[Rigatoni]]`, `[[Spagetti]]`, `[[Tortelloni]]` etc.
- All `Ingredienser/` files: renamed `up:` → `parent:` (taxonomic hierarchy)
- All recipe / other files: renamed `up:` → `category:` (navigation breadcrumb)
- `Ingredienser/Sukker.md`: added aliases `Brunt sukker` / `brunt sukker`; deleted `Ingredienser/Brunt sukker.md`
- `Ingredienser/Torsk.md`: added alias `Torskefilet`; deleted `Ingredienser/Torskefilet.md`
- `Ingredienser/Sopptortelloni.md`: set `ingredients: ["[[Tortelloni]]"]` (product hierarchy, not subtype)
- `Ingredienser/Tortelloni.md`: added `parent: ["[[Pasta]]"]`
- `Ingredienser/Spagetti.md`: fixed `[[pasta]]` → `[[Pasta]]` (case)
- `Dessert/Hello, World!.md`: fixed `category: Hoofdretter` → `category: Dessert`
- `Dessert/Oreokake.md`: fixed `category: Hoofdretter` → `category: Dessert`
- `Enkel servering/Rødvinsglogg.md`: fixed nested wikilink bug → `[[Sukker|brunt sukker]]`
- `Enkel servering/Maisstuing.md`: added `[[Fløte|kremfløte]]` wikilink (compound word)
- `Hoofdretter/Spicy pasta med grønnkål.md`: `[[Brunt sukker]]` → `[[Sukker|Brunt sukker]]`
- 21 recipe files (Bakst, Dessert, Enkel servering, Hoofdretter): auto-wikified plain-text ingredient lines

## 2026-05-10 — Audit: fix FM ingredients gaps (Category A)

- `Bakst/Bananpannekaker.md`: populated empty `ingredients` FM (Havregryn, Banan, Egg, Melk)
- `Bakst/Appelsinboller.md`: added missing `Vann`
- `Dessert/Sjokoladekake med kaffeglasur.md`: populated empty `ingredients` FM (Egg, Hvetemel)
- `Kremet basilikumkylling.md`: added missing Kruspersille, Rosmarin, Timian
- `Kylling teriyaki-bowl.md`: added missing `Vann`
- `Vegetar-lasagne.md`: populated empty `ingredients` FM (Pepper, Hvetemel)
- `Paella med byggryn og risotto.md`: updated links to `[[Torsk|Torskefilet]]`; added Hvitløk, Løk, Gulrot, Hakkede tomater, Chili, Sitron, Vann, Grønnsaksbuljong, Kruspersille; deleted `Ingredienser/Torskefilet.md` (merged as alias on `Torsk.md`)
- `Kikertkarri med spinatris.md`: replaced `[[Jasminris]]` → `[[Ris]]` (body links `[[Ris|jasminris]]`)

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
