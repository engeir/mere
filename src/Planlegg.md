---
lyst:
  - "[[Torsk]]"
  - "[[Potet]]"
  - "[[Løk]]"
---

# Planlegg

Legg til ønskede oppskrifter eller enkeltingredienser i `lyst`, i prioritert rekkefølge.
Første får høyest vekt, siste får 1. Oppskrifter bidrar med alle sine ingredienser;
enkeltingredienser brukes direkte.

```yaml
lyst:
  - "[[Middelhavsinspirert kylling]]"
  - "[[Potet]]"
  - "[[Pasta]]"
```

## Oppskrifter som passer

```dataviewjs
const page = dv.page("Planlegg")
const lyst = [].concat(page.lyst ?? []).filter(r => r?.path)

const n = lyst.length

// Build ingredient → weight map — supports both recipes and bare ingredients
const ingredientMap = new Map()
for (let idx = 0; idx < lyst.length; idx++) {
  const weight = n - idx
  const linked = dv.page(lyst[idx].path)
  const recipeIngredients = linked ? [].concat(linked.ingredients ?? []) : []
  if (recipeIngredients.length > 0) {
    for (const ing of recipeIngredients) {
      if (!ing?.path) continue
      ingredientMap.set(ing.path, (ingredientMap.get(ing.path) ?? 0) + weight)
    }
  } else {
    ingredientMap.set(lyst[idx].path, (ingredientMap.get(lyst[idx].path) ?? 0) + weight)
  }
}

const lystPaths = new Set(lyst.map(r => r.path))

// Walk up: and ingredients: on ingredient files to collect all ancestor paths
function getAncestorPaths(ingPath, visited = new Set()) {
  if (visited.has(ingPath)) return visited
  visited.add(ingPath)
  const ingPage = dv.page(ingPath)
  if (!ingPage) return visited
  for (const u of [].concat(ingPage.parent ?? []))
    if (u?.path) getAncestorPaths(u.path, visited)
  for (const i of [].concat(ingPage.ingredients ?? []))
    if (i?.path) getAncestorPaths(i.path, visited)
  return visited
}

function score(r) {
  return [].concat(r.ingredients ?? [])
    .filter(i => i?.path)
    .reduce((s, i) => {
      let maxWeight = 0
      for (const p of getAncestorPaths(i.path))
        if (ingredientMap.has(p)) maxWeight = Math.max(maxWeight, ingredientMap.get(p))
      return s + maxWeight
    }, 0)
}

function matchList(r) {
  return [].concat(r.ingredients ?? [])
    .filter(i => i?.path && [...getAncestorPaths(i.path)].some(p => ingredientMap.has(p)))
    .map(i => i.path.split('/').pop().replace('.md', ''))
    .join(', ')
}

dv.table(
  ['Oppskrift', 'Score', 'Felles ingredienser'],
  dv.pages('"Hovedretter" or "Bakst" or "Dessert" or "Enkel servering"')
    .filter(r => !lystPaths.has(r.file.path) && score(r) > 0)
    .sort(r => score(r), 'desc')
    .map(r => [r.file.link, score(r), matchList(r)])
)
```
