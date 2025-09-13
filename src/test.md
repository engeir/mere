---
id: test
aliases: []
tags:
  - recipe
  - dessert
category: dessert
ingredients:
  - - watermelon
    - 80 g
  - - sugar
    - 20 g
portions: 4
recipe: Melon Salad
serving: 100 g
---

# `=this.recipe`

## Ingredients for `=this.portions` portions (`=this.serving` ea.)

```dataviewjs
var i;
for (i=0; i < dv.current().ingredients.length; i++) {
    var name = dv.current().ingredients[i][0];
    var amount = dv.current().ingredients[i][1].split(" ")[0];
    var unit = dv.current().ingredients[i][1].split(" ")[1];
    var link = '[[' + name + ']]'
    dv.paragraph("- " + amount * dv.current().portions + " " + unit + " " + link);
}
```
