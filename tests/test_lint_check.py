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


def test_parse_file_dashes_in_value(tmp_path):
    f = tmp_path / "test.md"
    f.write_text('---\nid: Test\ndescription: "Text with --- dashes"\n---\n\n# Body\n')
    fm, body = checker.parse_file(f)
    assert fm["description"] == "Text with --- dashes"
    assert "Body" in body


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


VALID_RECIPE_BODY = (
    "\n## Ingredienser\n\n#ingredient\n\n"
    "- [x] 1 [[Smør|smør]]\n\n## Steg\n\n1. Gjør noe.\n"
)


def _make_ing(vault, name="Smør"):
    ing_dir = vault / "Ingredienser"
    ing_dir.mkdir(parents=True, exist_ok=True)
    (ing_dir / f"{name}.md").write_text(
        f"---\nid: {name}\npermalink: {name.lower()}\n---\n"
    )


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
        "id": "Pasta",
        "permalink": "pasta",
        "ingredients": [],
        "description": "30 min",
        "authors": ["[[someone]]"],
    }
    errors = checker.check_recipe(tmp_path / "Pasta.md", fm, VALID_RECIPE_BODY, vault)
    assert any("use 'author' not 'authors'" in e for e in errors)


def test_recipe_stale_category_field(tmp_path):
    vault = tmp_path / "src"
    fm = {
        "id": "Pasta",
        "permalink": "pasta",
        "ingredients": [],
        "description": "30 min",
        "category": "middag",
    }
    errors = checker.check_recipe(tmp_path / "Pasta.md", fm, VALID_RECIPE_BODY, vault)
    assert any("unexpected field 'category'" in e for e in errors)


def test_recipe_unknown_field(tmp_path):
    vault = tmp_path / "src"
    fm = {
        "id": "Pasta",
        "permalink": "pasta",
        "ingredients": [],
        "description": "30 min",
        "somefield": "value",
    }
    errors = checker.check_recipe(tmp_path / "Pasta.md", fm, VALID_RECIPE_BODY, vault)
    assert any("unknown field 'somefield'" in e for e in errors)


def test_recipe_ingredient_not_wikilink(tmp_path):
    vault = tmp_path / "src"
    fm = {
        "id": "Pasta",
        "permalink": "pasta",
        "ingredients": ["Smør (plain text)"],
        "description": "30 min",
    }
    errors = checker.check_recipe(tmp_path / "Pasta.md", fm, VALID_RECIPE_BODY, vault)
    assert any("is not a [[WikiLink]]" in e for e in errors)


def test_recipe_ingredient_link_missing_file(tmp_path):
    vault = tmp_path / "src"
    (vault / "Ingredienser").mkdir(parents=True)
    fm = {
        "id": "Pasta",
        "permalink": "pasta",
        "ingredients": ["[[ManglerFil]]"],
        "description": "30 min",
    }
    errors = checker.check_recipe(tmp_path / "Pasta.md", fm, VALID_RECIPE_BODY, vault)
    assert any("'[[ManglerFil]]' has no file in Ingredienser/" in e for e in errors)


def test_recipe_missing_ingredienser_section(tmp_path):
    vault = tmp_path / "src"
    body = "\n## Steg\n\n1. Gjør noe.\n"
    fm = {
        "id": "Pasta",
        "permalink": "pasta",
        "ingredients": [],
        "description": "30 min",
    }
    errors = checker.check_recipe(tmp_path / "Pasta.md", fm, body, vault)
    assert any("missing '## Ingredienser' section" in e for e in errors)


def test_recipe_missing_steg_section(tmp_path):
    vault = tmp_path / "src"
    body = "\n## Ingredienser\n\n#ingredient\n\n"
    fm = {
        "id": "Pasta",
        "permalink": "pasta",
        "ingredients": [],
        "description": "30 min",
    }
    errors = checker.check_recipe(tmp_path / "Pasta.md", fm, body, vault)
    assert any("missing '## Steg' section" in e for e in errors)


def test_recipe_missing_ingredient_tag(tmp_path):
    vault = tmp_path / "src"
    body = "\n## Ingredienser\n\n- [x] 1 [[Smør]]\n\n## Steg\n\n1. Gjør noe.\n"
    fm = {
        "id": "Pasta",
        "permalink": "pasta",
        "ingredients": [],
        "description": "30 min",
    }
    errors = checker.check_recipe(tmp_path / "Pasta.md", fm, body, vault)
    assert any("'#ingredient' tag missing" in e for e in errors)


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
        "---\nid: Pannekaker\npermalink: pannekaker\n"
        'description: 20 min | Enkel\ningredients:\n  - "[[Smør]]"\n---\n\n'
        "## Ingredienser\n\n#ingredient\n\n- [x] 1 [[Smør|smør]]\n\n## Steg\n\n1. Steg.\n"
    )
    result = run_checker("--vault-root", str(vault), str(f))
    assert result.returncode == 0
    assert result.stdout.strip() == ""


def test_cli_violations_exit_1(tmp_path):
    vault = _make_vault(tmp_path)
    f = vault / "Bakst" / "Pannekaker.md"
    f.write_text(
        "---\nid: Pannekaker\npermalink: pannekaker\n"
        "description: 20 min\ningredients: []\ncategory: bakst\n---\n\n"
        "## Ingredienser\n\n#ingredient\n\n## Steg\n\n1. Steg.\n"
    )
    result = run_checker("--vault-root", str(vault), str(f))
    assert result.returncode == 1
    assert "category" in result.stdout
    assert "[ERROR]" in result.stdout


def test_cli_error_summary_line(tmp_path):
    vault = _make_vault(tmp_path)
    f = vault / "Bakst" / "Pannekaker.md"
    f.write_text(
        "---\nid: Pannekaker\npermalink: pannekaker\n"
        "description: 20 min\ningredients: []\ncategory: bakst\n---\n\n"
        "## Ingredienser\n\n#ingredient\n\n## Steg\n\n1. Steg.\n"
    )
    result = run_checker("--vault-root", str(vault), str(f))
    assert "error" in result.stdout
    assert "1 file" in result.stdout


def test_cli_nonexistent_file_skipped(tmp_path):
    vault = _make_vault(tmp_path)
    result = run_checker("--vault-root", str(vault), str(tmp_path / "ghost.md"))
    assert result.returncode == 0
