---
id: Ukesmeny
aliases: []
tags: []
---

```dataviewjs
/**
 * Implement this method for your use case.
 * In this example, I'm collecting all pages
 * that appear in my sourcePage as outgoing links
 * (anything that appears like [[Veggie Burger]]).
 *
 * This function needs to return a list of pages.
 */
function gatherRecipes() {
  const sourcePage = dv.page('Ukesmeny.md')
  if (!sourcePage) return null
  const outLinks = sourcePage.file.outlinks
  return outLinks.map(link => dv.page(link)).filter(p => p)
}
/**
 * Renders the grocery list.
 */
function render() {
  const recipes = gatherRecipes()

  if (!recipes) {
    dv.paragraph('⚠️ Could not locate recipes. Please check your `gatherRecipes()` implementation.')
    return
  }
  if (!Array.isArray(recipes)) {
    dv.paragraph('⚠️ The output of `gatherRecipes()` must be Array<Page>')
  }
  if (!recipes.length) {
    dv.paragraph('⚠️ Could not locate recipes. Please check your `gatherRecipes()` implementation.')
    return
  }

  // Aggregate and deduplicate ingredients
  let ingredientMap = new Map()

  for (const recipe of recipes) {
    if (!recipe.ingredients) {
        dv.paragraph(`⚠️ ${recipe.file.link} does not have any ingredients!`)
        continue
    }
    for (const ingredient of recipe.ingredients) {
      if (!ingredientMap.has(ingredient)) {
        ingredientMap.set(ingredient, [])
      }
      ingredientMap.get(ingredient).push(recipe.file.link)
    }
  }
  // Sort ingredients alphabetically
  const sortedIngredients = Array.from(ingredientMap.entries())
  const ingredientsList = sortedIngredients.map(([ingredient, links]) => {
    const linkText = links.join(', ')
    return `${ingredient} <small>(${linkText})</small>`
  })
  dv.header(2, "Ingredienser")
  dv.paragraph(`Generert fra ${recipes.length} oppskrift${recipes.length !== 1 ? 'er' : ''}:`)
  dv.list(ingredientsList)
}
render()
```
