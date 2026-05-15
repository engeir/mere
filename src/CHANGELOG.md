---
id: CHANGELOG
aliases: []
tags: []
---
## 2026-05-15 — Brasiliansk seigryte + nye ingredienskategorier

- `Hovedretter/Brasiliansk seigryte.md`: ny oppskrift fra HelloFresh
- `Ingredienser/Panamat.md`: ny ingrediens (HelloFresh-krydderblanding)
- `Ingredienser/Grønnsaker.md`, `Urter.md`, `Nøtter.md`, `Olje.md`: nye kategorier
- `Ingredienser/Gulrot.md`, `Spinat.md`: `parent: [[Grønnsaker]]`
- `Ingredienser/Koriander.md`: `parent: [[Urter]]`
- `Ingredienser/Saltede peanøtter.md`, `Peanøttsmør.md`: `parent: [[Nøtter]]`
- `Ingredienser/Olivenolje.md`: `parent: [[Olje]]`
- `Ingredienser/Kokosmelk.md`: `parent: [[Kokos]]`

## 2026-05-12 — Ingredienshierarki: utvidelse

- `Ingredienser/Sei.md`: `parent: [[Hvit fisk]]`
- `Ingredienser/Bulgur.md`: `parent: [[Korn]]`
- `Ingredienser/Couscous.md`: `parent: [[Korn]]`
- `Ingredienser/Sjalottløk.md`: `parent: [[Løk]]`
- `Ingredienser/Sammalt hvete.md`: `parent: [[Mel]]`
- `Ingredienser/Tipo 00 mel.md`: `parent: [[Mel]]`
- `Ingredienser/Halloumi.md`: `parent: [[Ost]]`
- `Ingredienser/Smøreost.md`: `parent: [[Ost]]` → `[[Fersk ost]]`
- `Ingredienser/Udon nudler.md`: `parent: [[Nudler]]`, lagt til `id`
- `Ingredienser/Plommetomater.md`: `parent: [[Tomat]]`
- `Ingredienser/Hakkede tomater.md`: `parent: [[Tomat]]`
- `Ingredienser/Tomat.md`: lagt til `id: Tomat`
- `Ingredienser/Pasta.md`: lagt til `id: Pasta`
- `Ingredienser/Sitrus.md`: ny kategorinode, `parent: [[Frukt]]`
- `Ingredienser/Appelsin.md`: `parent: [[Frukt]]` → `[[Sitrus]]`
- `Ingredienser/Sitron.md`: `parent: [[Frukt]]` → `[[Sitrus]]`
- `Ingredienser/Lime.md`: `parent: [[Frukt]]` → `[[Sitrus]]`

## 2026-05-12 — Ingredienshierarki: Korn

- `Ingredienser/Korn.md`: ny kategorinode (top-level)
- `Ingredienser/Byggryn.md`: lagt til `parent: [[Korn]]`, ryddet frontmatter
- `Ingredienser/Havregryn.md`: lagt til `parent: [[Korn]]`
- `Ingredienser/Couscous.md`: standalone (semolina — passer ikke under Korn)

## 2026-05-12 — Ingredienshierarki: Ris

- `Ingredienser/Basmatiris.md`: ny ingrediensfil, `parent: [[Ris]]`
- `Ingredienser/Jasminris.md`: lagt til alias `jasminris`
- `Ingredienser/Risotto.md`: lagt til `parent: [[Ris]]`, alias `risottoris`
- `Hovedretter/Kylling teriyaki-bowl.md`: fikset `[[Ris|Jasminris]]` → `[[Jasminris]]`
- `Hovedretter/Vegetarwok med kebab og ris.md`: fikset `[[Ris|Jasminris]]` → `[[Jasminris]]`
- `Hovedretter/Kikertkarri med spinatris.md`: fikset frontmatter og ingrediens til `[[Jasminris]]`

## 2026-05-12 — Ingredienshierarki: Ost

- `Ingredienser/Hard ost.md`: ny kategorinode, `parent: [[Ost]]`
- `Ingredienser/Fersk ost.md`: ny kategorinode, `parent: [[Ost]]`
- `Ingredienser/Parmesan.md`: ny ingrediensfil, `parent: [[Hard ost]]`
- `Ingredienser/Mozzarella.md`: ny ingrediensfil, `parent: [[Fersk ost]]`
- `Ingredienser/Ricotta.md`: ny ingrediensfil, `parent: [[Fersk ost]]`
- `Ingredienser/Finrevet ost.md`: lagt til `parent: [[Hard ost]]`, aliases gulost/norvegia
- `Ingredienser/Blåmuggost.md`: lagt til `parent: [[Ost]]`, aliases gorgonzola/roquefort
- `Ingredienser/Salatost.md`: lagt til `parent: [[Ost]]`
- `Ingredienser/Fetaost.md`: lagt til `parent: [[Salatost]]`
- `Ingredienser/Smøreost.md`: lagt til `parent: [[Ost]]`, aliases smøreost/kremost
- `Ingredienser/Ost.md`: fjernet aliases som overlappet med Finrevet ost

## 2026-05-12 — Ingredienshierarki: Rød fisk

- `Ingredienser/Rød fisk.md`: ny kategorinode, `parent: [[Fisk]]`
- `Ingredienser/Laks.md`: oppdatert parent `[[Fisk]]` → `[[Rød fisk]]`
- `Ingredienser/Ørret.md`: lagt til `parent: [[Rød fisk]]`
- `Ingredienser/Røye.md`: ny ingrediensfil, `parent: [[Rød fisk]]`
- `Ingredienser/Regnbueørret.md`: ny ingrediensfil, `parent: [[Rød fisk]]`
- `Ingredienser/Fjellørret.md`: ny ingrediensfil, `parent: [[Ørret]]`
- `Ingredienser/Sjøørret.md`: ny ingrediensfil, `parent: [[Ørret]]`

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
