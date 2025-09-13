---
id: Handleliste
aliases: []
tags: []
---

# Handleliste

```dataview
TASK
FROM "Varelager.md"
WHERE !completed
GROUP BY meta(section).subpath AS Heading
SORT Heading ASC
```
