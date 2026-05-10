---
har:
  - "[[Torsk]]"
mangler: []
---

# Planlegg

Legg til ønskede oppskrifter eller enkeltingredienser i `har`, i prioritert rekkefølge.
Første får høyest vekt, siste får 1. Oppskrifter bidrar med alle sine ingredienser;
enkeltingredienser brukes direkte.

```yaml
har:
  - "[[Middelhavsinspirert kylling]]"
  - "[[Potet]]"
  - "[[Pasta]]"
```

## Oppskrifter som passer

```dataviewjs
const page = dv.page("Planlegg")
const har = [].concat(page.har ?? []).filter(r => r?.path)
const mangler = [].concat(page.mangler ?? []).filter(r => r?.path)

const n = har.length

// Build ingredient → weight map — supports both recipes and bare ingredients
const ingredientMap = new Map()
for (let idx = 0; idx < har.length; idx++) {
  const weight = n - idx
  const linked = dv.page(har[idx].path)
  const recipeIngredients = linked ? [].concat(linked.ingredients ?? []) : []
  if (recipeIngredients.length > 0) {
    for (const ing of recipeIngredients) {
      if (!ing?.path) continue
      ingredientMap.set(ing.path, (ingredientMap.get(ing.path) ?? 0) + weight)
    }
  } else {
    ingredientMap.set(har[idx].path, (ingredientMap.get(har[idx].path) ?? 0) + weight)
  }
}

const harPaths = new Set(har.map(r => r.path))
const manglerPaths = new Set(mangler.map(r => r.path))

// Walk up: parent and ingredients: on ingredient files to collect all ancestor paths
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

function isMissing(r) {
  if (manglerPaths.size === 0) return false
  return [].concat(r.ingredients ?? [])
    .filter(i => i?.path)
    .some(i => [...getAncestorPaths(i.path)].some(p => manglerPaths.has(p)))
}

dv.table(
  ['Oppskrift', 'Score', 'Felles ingredienser'],
  dv.pages('"Hovedretter" or "Bakst" or "Dessert" or "Enkel servering"')
    .filter(r => !harPaths.has(r.file.path) && !isMissing(r) && score(r) > 0)
    .sort(r => score(r), 'desc')
    .map(r => [r.file.link, score(r), matchList(r)])
)
```
