# Static Checker Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Python script at `.mise/tasks/lint-check` that validates Obsidian vault `.md` files against schema conventions and runs as an hk pre-commit hook.

**Architecture:** Single executable Python script. Accepts file list as positional args (hk staged mode) or scans full `src/` vault when called with no args. All validation logic is in plain functions. hk.pkl routes staged `.md` files to the checker via `mise run lint-check -- {{ files }}`.

**Tech Stack:** Python 3.12+, pyyaml (already in deps), pytest (dev dep to add), hk, mise

---

### Task 1: Test infrastructure + checker stub

**Files:**
- Modify: `pyproject.toml`
- Create: `tests/__init__.py`
- Create: `tests/test_lint_check.py`
- Create: `.mise/tasks/lint-check`

- [ ] **Step 1: Add pytest as dev dependency**

```bash
rye add --dev pytest
rye sync
```

Expected: `pyproject.toml` `[tool.rye] dev-dependencies` gains `pytest`, `.venv` updated.

- [ ] **Step 2: Create test file with shared helpers**

Create `tests/__init__.py` — empty file.

Create `tests/test_lint_check.py`:
```python
import importlib.util
import subprocess
from importlib.machinery import SourceFileLoader
from pathlib import Path

CHECKER = Path(__file__).parent.parent / ".mise" / "tasks" / "lint-check"
PYTHON = Path(__file__).parent.parent / ".venv" / "bin" / "python"


def _load_checker():
    loader = SourceFileLoader("lint_check", str(CHECKER))
    spec = importlib.util.spec_from_file_location("lint_check", CHECKER, loader=loader)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


checker = _load_checker()


def run_checker(*args):
    result = subprocess.run(
        [str(PYTHON), str(CHECKER), *args],
        capture_output=True,
        text=True,
    )
    return result
```

- [ ] **Step 3: Create checker stub**

Create `.mise/tasks/lint-check`:
```python
#!/usr/bin/env python3
import re
import sys
from pathlib import Path

import yaml

DEFAULT_VAULT_ROOT = Path(__file__).parent.parent.parent / "src"

RECIPE_DIRS = {"Bakst", "Dessert", "Enkel servering", "Hovedretter"}
INGREDIENT_DIR = "Ingredienser"
SKIP_DIRS = {"raw", "Attachments", "templates", "_includes"}

RECIPE_REQUIRED_FIELDS = {"id", "permalink", "ingredients", "description"}
RECIPE_KNOWN_FIELDS = {
    "id", "permalink", "ingredients", "description",
    "author", "cover", "aliases", "tags", "up",
}
INGREDIENT_REQUIRED_FIELDS = {"id", "permalink"}
INGREDIENT_KNOWN_FIELDS = {"id", "permalink", "aliases", "tags", "parent"}

WIKILINK_RE = re.compile(r'\[\[([^\]|]+)(?:\|[^\]]+)?\]\]')


def main():
    pass


if __name__ == "__main__":
    main()
```

```bash
chmod +x .mise/tasks/lint-check
```

- [ ] **Step 4: Verify test setup**

```bash
.venv/bin/pytest tests/ -v
```

Expected: 0 tests collected, no import errors.

---

### Task 2: Frontmatter parser

**Files:**
- Modify: `.mise/tasks/lint-check`
- Modify: `tests/test_lint_check.py`

- [ ] **Step 1: Write failing tests**

Append to `tests/test_lint_check.py`:
```python
def test_parse_file_with_frontmatter(tmp_path):
    f = tmp_path / "test.md"
    f.write_text("---\nid: Test\npermalink: test\n---\n\n# Test\n\nBody content.\n")
    fm, body = checker.parse_file(f)
    assert fm == {"id": "Test", "permalink": "test"}
    assert "Body content." in body


def test_parse_file_without_frontmatter(tmp_path):
    f = tmp_path / "test.md"
    f.write_text("# Test\n\nNo frontmatter.\n")
    fm, body = checker.parse_file(f)
    assert fm == {}
    assert "No frontmatter." in body


def test_parse_file_with_list_field(tmp_path):
    f = tmp_path / "test.md"
    f.write_text('---\nid: Test\ningredients:\n  - "[[Smør]]"\n---\n\n# Test\n')
    fm, body = checker.parse_file(f)
    assert fm["ingredients"] == ["[[Smør]]"]
```

- [ ] **Step 2: Run to confirm failure**

```bash
.venv/bin/pytest tests/test_lint_check.py -k "parse_file" -v
```

Expected: FAIL — `AttributeError: module 'lint_check' has no attribute 'parse_file'`

- [ ] **Step 3: Implement parse_file**

Add to `.mise/tasks/lint-check` before `main()`:
```python
def parse_file(path: Path) -> tuple[dict, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {}, text
    end = text.index("---", 3)
    fm = yaml.safe_load(text[3:end])
    body = text[end + 3:]
    return fm or {}, body
```

- [ ] **Step 4: Run tests to confirm pass**

```bash
.venv/bin/pytest tests/test_lint_check.py -k "parse_file" -v
```

Expected: 3 PASSED.

---

### Task 3: File categorizer

**Files:**
- Modify: `.mise/tasks/lint-check`
- Modify: `tests/test_lint_check.py`

- [ ] **Step 1: Write failing tests**

Append to `tests/test_lint_check.py`:
```python
def test_categorize_recipe(tmp_path):
    vault = tmp_path / "src"
    f = vault / "Hovedretter" / "Pasta.md"
    assert checker.categorize(f, vault) == "recipe"


def test_categorize_bakst(tmp_path):
    vault = tmp_path / "src"
    f = vault / "Bakst" / "Bolle.md"
    assert checker.categorize(f, vault) == "recipe"


def test_categorize_ingredient(tmp_path):
    vault = tmp_path / "src"
    f = vault / "Ingredienser" / "Smør.md"
    assert checker.categorize(f, vault) == "ingredient"


def test_categorize_skip_raw(tmp_path):
    vault = tmp_path / "src"
    f = vault / "raw" / "draft.md"
    assert checker.categorize(f, vault) == "skip"


def test_categorize_skip_other(tmp_path):
    vault = tmp_path / "src"
    f = vault / "Blog" / "post.md"
    assert checker.categorize(f, vault) == "skip"
```

- [ ] **Step 2: Run to confirm failure**

```bash
.venv/bin/pytest tests/test_lint_check.py -k "categorize" -v
```

Expected: FAIL — `AttributeError: module 'lint_check' has no attribute 'categorize'`

- [ ] **Step 3: Implement categorize**

Add to `.mise/tasks/lint-check` after `parse_file`, before `main()`:
```python
def categorize(path: Path, vault_root: Path) -> str:
    try:
        parts = path.relative_to(vault_root).parts
    except ValueError:
        return "skip"
    if not parts:
        return "skip"
    top = parts[0]
    if top in SKIP_DIRS:
        return "skip"
    if top in RECIPE_DIRS:
        return "recipe"
    if top == INGREDIENT_DIR:
        return "ingredient"
    return "skip"
```

- [ ] **Step 4: Run tests to confirm pass**

```bash
.venv/bin/pytest tests/test_lint_check.py -k "categorize" -v
```

Expected: 5 PASSED.

---

### Task 4: Recipe checks (frontmatter + links + body)

**Files:**
- Modify: `.mise/tasks/lint-check`
- Modify: `tests/test_lint_check.py`

- [ ] **Step 1: Write failing tests**

Append to `tests/test_lint_check.py`:
```python
VALID_RECIPE_BODY = (
    "\n## Ingredienser\n\n#ingredient\n\n"
    "- [x] 1 [[Smør|smør]]\n\n## Steg\n\n1. Gjør noe.\n"
)


def _make_ing(vault, name="Smør"):
    ing_dir = vault / "Ingredienser"
    ing_dir.mkdir(parents=True, exist_ok=True)
    (ing_dir / f"{name}.md").write_text(f"---\nid: {name}\npermalink: {name.lower()}\n---\n")


def test_recipe_valid(tmp_path):
    vault = tmp_path / "src"
    _make_ing(vault)
    fm = {
        "id": "Pasta",
        "permalink": "pasta",
        "ingredients": ["[[Smør]]"],
        "description": "30 min | Enkel",
    }
    errors = checker.check_recipe(tmp_path / "Pasta.md", fm, VALID_RECIPE_BODY, vault)
    assert errors == []


def test_recipe_missing_required_field(tmp_path):
    vault = tmp_path / "src"
    fm = {"id": "Pasta", "permalink": "pasta", "ingredients": []}
    errors = checker.check_recipe(tmp_path / "Pasta.md", fm, VALID_RECIPE_BODY, vault)
    assert any("missing required field 'description'" in e for e in errors)


def test_recipe_stale_authors_field(tmp_path):
    vault = tmp_path / "src"
    fm = {
        "id": "Pasta", "permalink": "pasta",
        "ingredients": [], "description": "30 min",
        "authors": ["[[someone]]"],
    }
    errors = checker.check_recipe(tmp_path / "Pasta.md", fm, VALID_RECIPE_BODY, vault)
    assert any("use 'author' not 'authors'" in e for e in errors)


def test_recipe_stale_category_field(tmp_path):
    vault = tmp_path / "src"
    fm = {
        "id": "Pasta", "permalink": "pasta",
        "ingredients": [], "description": "30 min",
        "category": "middag",
    }
    errors = checker.check_recipe(tmp_path / "Pasta.md", fm, VALID_RECIPE_BODY, vault)
    assert any("unexpected field 'category'" in e for e in errors)


def test_recipe_unknown_field(tmp_path):
    vault = tmp_path / "src"
    fm = {
        "id": "Pasta", "permalink": "pasta",
        "ingredients": [], "description": "30 min",
        "somefield": "value",
    }
    errors = checker.check_recipe(tmp_path / "Pasta.md", fm, VALID_RECIPE_BODY, vault)
    assert any("unknown field 'somefield'" in e for e in errors)


def test_recipe_ingredient_not_wikilink(tmp_path):
    vault = tmp_path / "src"
    fm = {
        "id": "Pasta", "permalink": "pasta",
        "ingredients": ["Smør (plain text)"], "description": "30 min",
    }
    errors = checker.check_recipe(tmp_path / "Pasta.md", fm, VALID_RECIPE_BODY, vault)
    assert any("is not a [[WikiLink]]" in e for e in errors)


def test_recipe_ingredient_link_missing_file(tmp_path):
    vault = tmp_path / "src"
    (vault / "Ingredienser").mkdir(parents=True)
    fm = {
        "id": "Pasta", "permalink": "pasta",
        "ingredients": ["[[ManglerFil]]"], "description": "30 min",
    }
    errors = checker.check_recipe(tmp_path / "Pasta.md", fm, VALID_RECIPE_BODY, vault)
    assert any("'[[ManglerFil]]' has no file in Ingredienser/" in e for e in errors)


def test_recipe_missing_ingredienser_section(tmp_path):
    vault = tmp_path / "src"
    body = "\n## Steg\n\n1. Gjør noe.\n"
    fm = {"id": "Pasta", "permalink": "pasta", "ingredients": [], "description": "30 min"}
    errors = checker.check_recipe(tmp_path / "Pasta.md", fm, body, vault)
    assert any("missing '## Ingredienser' section" in e for e in errors)


def test_recipe_missing_steg_section(tmp_path):
    vault = tmp_path / "src"
    body = "\n## Ingredienser\n\n#ingredient\n\n"
    fm = {"id": "Pasta", "permalink": "pasta", "ingredients": [], "description": "30 min"}
    errors = checker.check_recipe(tmp_path / "Pasta.md", fm, body, vault)
    assert any("missing '## Steg' section" in e for e in errors)


def test_recipe_missing_ingredient_tag(tmp_path):
    vault = tmp_path / "src"
    body = "\n## Ingredienser\n\n- [x] 1 [[Smør]]\n\n## Steg\n\n1. Gjør noe.\n"
    fm = {"id": "Pasta", "permalink": "pasta", "ingredients": [], "description": "30 min"}
    errors = checker.check_recipe(tmp_path / "Pasta.md", fm, body, vault)
    assert any("'#ingredient' tag missing" in e for e in errors)
```

- [ ] **Step 2: Run to confirm failure**

```bash
.venv/bin/pytest tests/test_lint_check.py -k "recipe" -v
```

Expected: FAIL — `AttributeError: module 'lint_check' has no attribute 'check_recipe'`

- [ ] **Step 3: Implement _extract_wikilinks and check_recipe**

Add to `.mise/tasks/lint-check` after `categorize`, before `main()`:
```python
def _extract_wikilinks(value) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [m for v in value for m in WIKILINK_RE.findall(str(v))]
    return WIKILINK_RE.findall(str(value))


def check_recipe(path: Path, fm: dict, body: str, vault_root: Path) -> list[str]:
    errors = []

    for field in RECIPE_REQUIRED_FIELDS:
        if field not in fm:
            errors.append(f"frontmatter: missing required field '{field}'")

    if "authors" in fm:
        errors.append("frontmatter: use 'author' not 'authors'")
    if "category" in fm:
        errors.append("frontmatter: unexpected field 'category'")
    for key in fm:
        if key not in RECIPE_KNOWN_FIELDS and key not in ("authors", "category"):
            errors.append(f"frontmatter: unknown field '{key}'")

    ingredients = fm.get("ingredients") or []
    if not isinstance(ingredients, list):
        errors.append("frontmatter: 'ingredients' must be a list")
    else:
        for item in ingredients:
            links = WIKILINK_RE.findall(str(item))
            if not links:
                errors.append(f"frontmatter: ingredient '{item}' is not a [[WikiLink]]")
            else:
                for link in links:
                    target = vault_root / "Ingredienser" / f"{link}.md"
                    if not target.exists():
                        errors.append(
                            f"link: ingredient '[[{link}]]' has no file in Ingredienser/"
                        )

    cover = fm.get("cover")
    if cover:
        if isinstance(cover, list):
            cover = cover[0] if cover else None
        if cover:
            if not (vault_root / cover).exists():
                errors.append(f"cover: path '{cover}' does not exist")

    if "## Ingredienser" not in body:
        errors.append("body: missing '## Ingredienser' section")
    if "## Steg" not in body:
        errors.append("body: missing '## Steg' section")

    ing_match = re.search(r"## Ingredienser\s*\n(.*?)(?=\n##|\Z)", body, re.DOTALL)
    if ing_match and "#ingredient" not in ing_match.group(1):
        errors.append("body: '#ingredient' tag missing from '## Ingredienser' section")

    return errors
```

- [ ] **Step 4: Run tests to confirm pass**

```bash
.venv/bin/pytest tests/test_lint_check.py -k "recipe" -v
```

Expected: all recipe tests PASSED.

---

### Task 5: Ingredient file checks

**Files:**
- Modify: `.mise/tasks/lint-check`
- Modify: `tests/test_lint_check.py`

- [ ] **Step 1: Write failing tests**

Append to `tests/test_lint_check.py`:
```python
def test_ingredient_valid(tmp_path):
    vault = tmp_path / "src"
    (vault / "Ingredienser").mkdir(parents=True)
    fm = {"id": "Smør", "permalink": "smor"}
    errors = checker.check_ingredient(tmp_path / "Smør.md", fm, "", vault)
    assert errors == []


def test_ingredient_missing_id(tmp_path):
    vault = tmp_path / "src"
    fm = {"permalink": "smor"}
    errors = checker.check_ingredient(tmp_path / "Smør.md", fm, "", vault)
    assert any("missing required field 'id'" in e for e in errors)


def test_ingredient_missing_permalink(tmp_path):
    vault = tmp_path / "src"
    fm = {"id": "Smør"}
    errors = checker.check_ingredient(tmp_path / "Smør.md", fm, "", vault)
    assert any("missing required field 'permalink'" in e for e in errors)


def test_ingredient_parent_resolves(tmp_path):
    vault = tmp_path / "src"
    ing_dir = vault / "Ingredienser"
    ing_dir.mkdir(parents=True)
    (ing_dir / "Fisk.md").write_text("---\nid: Fisk\npermalink: fisk\n---\n")
    fm = {"id": "Laks", "permalink": "laks", "parent": ["[[Fisk]]"]}
    errors = checker.check_ingredient(tmp_path / "Laks.md", fm, "", vault)
    assert errors == []


def test_ingredient_parent_missing(tmp_path):
    vault = tmp_path / "src"
    (vault / "Ingredienser").mkdir(parents=True)
    fm = {"id": "Laks", "permalink": "laks", "parent": ["[[Fisk]]"]}
    errors = checker.check_ingredient(tmp_path / "Laks.md", fm, "", vault)
    assert any("'[[Fisk]]' has no file in Ingredienser/" in e for e in errors)
```

- [ ] **Step 2: Run to confirm failure**

```bash
.venv/bin/pytest tests/test_lint_check.py -k "ingredient" -v
```

Expected: FAIL — `AttributeError: module 'lint_check' has no attribute 'check_ingredient'`

- [ ] **Step 3: Implement check_ingredient**

Add to `.mise/tasks/lint-check` after `check_recipe`, before `main()`:
```python
def check_ingredient(path: Path, fm: dict, body: str, vault_root: Path) -> list[str]:
    errors = []
    for field in INGREDIENT_REQUIRED_FIELDS:
        if field not in fm:
            errors.append(f"frontmatter: missing required field '{field}'")
    parent = fm.get("parent")
    if parent:
        for link in _extract_wikilinks(parent):
            target = vault_root / "Ingredienser" / f"{link}.md"
            if not target.exists():
                errors.append(f"link: parent '[[{link}]]' has no file in Ingredienser/")
    return errors
```

- [ ] **Step 4: Run tests to confirm pass**

```bash
.venv/bin/pytest tests/test_lint_check.py -k "ingredient" -v
```

Expected: all ingredient tests PASSED.

---

### Task 6: Wire CLI + output formatting

**Files:**
- Modify: `.mise/tasks/lint-check`
- Modify: `tests/test_lint_check.py`

- [ ] **Step 1: Write failing CLI tests**

Append to `tests/test_lint_check.py`:
```python
def _make_vault(tmp_path):
    vault = tmp_path / "src"
    ing_dir = vault / "Ingredienser"
    ing_dir.mkdir(parents=True)
    (ing_dir / "Smør.md").write_text("---\nid: Smør\npermalink: smor\n---\n\n# Smør\n")
    (vault / "Bakst").mkdir()
    return vault


def test_cli_clean_file_exits_0(tmp_path):
    vault = _make_vault(tmp_path)
    f = vault / "Bakst" / "Pannekaker.md"
    f.write_text(
        '---\nid: Pannekaker\npermalink: pannekaker\n'
        'description: 20 min | Enkel\ningredients:\n  - "[[Smør]]"\n---\n\n'
        '## Ingredienser\n\n#ingredient\n\n- [x] 1 [[Smør|smør]]\n\n## Steg\n\n1. Steg.\n'
    )
    result = run_checker("--vault-root", str(vault), str(f))
    assert result.returncode == 0
    assert result.stdout.strip() == ""


def test_cli_violations_exit_1(tmp_path):
    vault = _make_vault(tmp_path)
    f = vault / "Bakst" / "Pannekaker.md"
    f.write_text(
        '---\nid: Pannekaker\npermalink: pannekaker\n'
        'description: 20 min\ningredients: []\ncategory: bakst\n---\n\n'
        '## Ingredienser\n\n#ingredient\n\n## Steg\n\n1. Steg.\n'
    )
    result = run_checker("--vault-root", str(vault), str(f))
    assert result.returncode == 1
    assert "category" in result.stdout
    assert "[ERROR]" in result.stdout


def test_cli_error_summary_line(tmp_path):
    vault = _make_vault(tmp_path)
    f = vault / "Bakst" / "Pannekaker.md"
    f.write_text(
        '---\nid: Pannekaker\npermalink: pannekaker\n'
        'description: 20 min\ningredients: []\ncategory: bakst\n---\n\n'
        '## Ingredienser\n\n#ingredient\n\n## Steg\n\n1. Steg.\n'
    )
    result = run_checker("--vault-root", str(vault), str(f))
    assert "error" in result.stdout
    assert "1 file" in result.stdout


def test_cli_nonexistent_file_skipped(tmp_path):
    vault = _make_vault(tmp_path)
    result = run_checker("--vault-root", str(vault), str(tmp_path / "ghost.md"))
    assert result.returncode == 0
```

- [ ] **Step 2: Run to confirm failure**

```bash
.venv/bin/pytest tests/test_lint_check.py -k "cli" -v
```

Expected: `test_cli_clean_file_exits_0` and `test_cli_violations_exit_1` FAIL (main() is a no-op).

- [ ] **Step 3: Implement check_file and main()**

Replace the `main()` stub in `.mise/tasks/lint-check` with:
```python
def check_file(path: Path, vault_root: Path) -> list[str]:
    category = categorize(path, vault_root)
    if category == "skip":
        return []
    fm, body = parse_file(path)
    if category == "recipe":
        return check_recipe(path, fm, body, vault_root)
    if category == "ingredient":
        return check_ingredient(path, fm, body, vault_root)
    return []


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Vault static checker")
    parser.add_argument("files", nargs="*", help="Files to check")
    parser.add_argument(
        "--vault-root",
        type=Path,
        default=DEFAULT_VAULT_ROOT,
        help="Path to vault src/ directory (default: repo src/)",
    )
    args = parser.parse_args()

    vault_root: Path = args.vault_root.resolve()

    paths: list[Path] = (
        [Path(f).resolve() for f in args.files if f.endswith(".md")]
        if args.files
        else sorted(vault_root.rglob("*.md"))
    )

    total_errors = 0
    files_with_errors = 0

    for path in paths:
        if not path.exists():
            continue
        errors = check_file(path, vault_root)
        if errors:
            files_with_errors += 1
            total_errors += len(errors)
            print(path)
            for e in errors:
                print(f"  [ERROR] {e}")
            print()

    if total_errors:
        noun = "error" if total_errors == 1 else "errors"
        foun = "file" if files_with_errors == 1 else "files"
        print(f"{total_errors} {noun} in {files_with_errors} {foun}")
        sys.exit(1)
```

- [ ] **Step 4: Run all tests**

```bash
.venv/bin/pytest tests/ -v
```

Expected: all tests PASSED.

- [ ] **Step 5: Smoke test on real vault**

```bash
mise run lint-check
```

Expected: output listing known violations — at minimum Paella's `category` and `authors` fields.

---

### Task 7: Wire up hk.pkl + install hooks

**Files:**
- Modify: `hk.pkl`

- [ ] **Step 1: Add lint-check step to hk.pkl**

Edit `hk.pkl`. Replace the empty `linters` mapping with:
```pkl
local linters = new Mapping<String, Step> {
    ["lint-check"] {
        glob = List("src/**/*.md")
        check = "mise run lint-check -- {{ files }}"
    }
}
```

- [ ] **Step 2: Validate config**

```bash
mise exec -- hk validate
```

Expected: exits 0, no errors printed.

- [ ] **Step 3: Install git hooks**

```bash
mise exec -- hk install
```

Expected: output like `Installing pre-commit hook...` or similar, exits 0.

- [ ] **Step 4: Smoke test via hk**

```bash
mise exec -- hk check --all
```

Expected: same violations as `mise run lint-check` in Task 6 Step 5.

- [ ] **Step 5: Test staged-files mode**

Stage one known-bad file and run hk pre-commit manually:

```bash
git add "src/Hovedretter/Paella med byggryn og risotto.md"
mise exec -- hk run pre-commit --check
git restore --staged "src/Hovedretter/Paella med byggryn og risotto.md"
```

Expected: exits 1, shows Paella violations.
