# Static Checker Design

Date: 2026-05-13

## Overview

Python script that validates Obsidian vault files against the project's schema conventions. Runs as a pre-commit hook via hk, exits nonzero on violations.

## Files Touched

| File | Action |
|---|---|
| `.mise/tasks/lint-check` | Create — Python checker script |
| `hk.pkl` | Modify — add lint-check step to linters mapping |

## CLI

```
.mise/tasks/lint-check [files...]
```

- Positional args → check those files (hk staged/all mode)
- No args → scan full vault under `src/` (direct invocation)

## Validation Rules

### Recipe files (`src/Bakst/`, `src/Dessert/`, `src/Enkel servering/`, `src/Hovedretter/`)

**Frontmatter:**
- Required fields: `id`, `permalink`, `ingredients`, `description`
- Field `author` allowed; `authors` (plural) flagged as error (stale field name)
- No unknown/stale fields (e.g. `category`, `authors`)
- Each `ingredients` value matches `[[Link]]` or `[[Link|alias]]` pattern
- Each ingredient link resolves to a file in `src/Ingredienser/`
- `cover` path (if present) exists under `src/Attachments/`

**Body:**
- Contains `## Ingredienser` section
- Contains `## Steg` section
- `#ingredient` tag present in `## Ingredienser` section

### Ingredient files (`src/Ingredienser/`)

**Frontmatter:**
- Required fields: `id`, `permalink`
- `parent` values (if present) match `[[Link]]` pattern and resolve to `src/Ingredienser/`

### Skipped paths

- `src/raw/` — read-only inbox, never checked
- `src/Attachments/` — binary assets
- `src/templates/` — templates, not live content
- `src/_includes/` — layout partials

## Output Format

```
src/Hovedretter/Paella med byggryn og risotto.md
  [ERROR] frontmatter: unexpected field 'category'
  [ERROR] frontmatter: use 'author' not 'authors'

2 errors in 1 file
```

- Only print files that have violations
- Exit 1 if any errors; exit 0 on clean run
- Clean run prints nothing (silent success for hk)

## hk Integration

`hk.pkl` — add to `linters` mapping:

```pkl
["lint-check"] {
    glob = "src/**/*.md"
    check = "mise run lint-check -- {{ files }}"
}
```

Workflows:
- `git commit` → hk pre-commit hook → passes staged `.md` files as args
- `hk check --all` → passes all vault `.md` files as args
- `hk install` → run once to wire up git hooks
- `mise run lint-check` → no args → scans full vault directly

## Implementation Notes

- Use `pyyaml` (already a dep) for frontmatter parsing
- Split frontmatter from body on `---` delimiters
- Detect file category by parent directory name
- `[[Link]]` / `[[Link|alias]]` regex: `\[\[([^\]|]+)(?:\|[^\]]+)?\]\]`
- Resolve ingredient links: strip alias, look for `src/Ingredienser/{name}.md`
- Section detection: regex `^## SectionName` on body lines
