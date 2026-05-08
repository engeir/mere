---
har:
  - "[[Bacon]]"
  - "[[Tomat]]"
  - "[[Brokkoli|10]]"
---

# Utforsk

Legg til ingredienser i `har`. Valgfri vekt etter `|` — høyere = mer urgent (standard: 1).

```yaml
har:
  - "[[Melk|10]]"
  - "[[Fisk|3]]"
  - "[[Bacon]]"
```

## Beste oppskrifter nå

```dataviewjs
const fridge = dv.page("Utforsk")
const har = [].concat(fridge.har ?? [])

const fridgeMap = new Map(
  har.filter(l => l?.path).map(l => [l.path, parseInt(l.display ?? '1') || 1])
)

function score(r) {
  return [].concat(r.ingredients ?? [])
    .filter(i => i?.path && fridgeMap.has(i.path))
    .reduce((s, i) => s + fridgeMap.get(i.path), 0)
}

function matchList(r) {
  return [].concat(r.ingredients ?? [])
    .filter(i => i?.path && fridgeMap.has(i.path))
    .map(i => i.path.split('/').pop().replace('.md', ''))
    .join(', ')
}

dv.table(
  ['Oppskrift', 'Score', 'Har ingredienser'],
  dv.pages('"Hovedretter" or "Bakst" or "Dessert" or "Enkel servering"')
    .filter(r => score(r) > 0)
    .sort(r => score(r), 'desc')
    .map(r => [r.file.link, score(r), matchList(r)])
)
```
