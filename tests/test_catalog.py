import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "catalog.py"
SPEC = importlib.util.spec_from_file_location("catalog", MODULE_PATH)
catalog = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = catalog
SPEC.loader.exec_module(catalog)


class CatalogValidationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tempdir.name)
        self.original_paths = (
            catalog.ROOT,
            catalog.SKILLS_DIR,
            catalog.REGISTRY_PATH,
            catalog.README_PATH,
        )
        catalog.ROOT = self.root
        catalog.SKILLS_DIR = self.root / "skills"
        catalog.REGISTRY_PATH = self.root / "catalog.yaml"
        catalog.README_PATH = self.root / "README.md"
        self.write_repository()

    def tearDown(self) -> None:
        (
            catalog.ROOT,
            catalog.SKILLS_DIR,
            catalog.REGISTRY_PATH,
            catalog.README_PATH,
        ) = self.original_paths
        self.tempdir.cleanup()

    def write_repository(self, skill_name: str = "sample-skill", registered: bool = True) -> None:
        skill_dir = catalog.SKILLS_DIR / skill_name
        skill_dir.mkdir(parents=True, exist_ok=True)
        skill_dir.joinpath("SKILL.md").write_text(
            f"---\nname: {skill_name}\ndescription: A test skill.\n---\n\n# Test\n",
            encoding="utf-8",
        )
        skills = (
            f"skills:\n  - name: {skill_name}\n    category: test\n    status: stable\n"
            if registered
            else "skills: []\n"
        )
        catalog.REGISTRY_PATH.write_text(
            "categories:\n  - id: test\n    title: Test\n\n" + skills,
            encoding="utf-8",
        )
        catalog.README_PATH.write_text(
            "# Test\n\n" + catalog.START_MARKER + "\n" + catalog.END_MARKER + "\n",
            encoding="utf-8",
        )

    def test_accepts_a_consistent_catalog_after_rendering(self) -> None:
        skills, categories = catalog.load_skills()
        catalog.update_readme(catalog.render_catalog(skills, categories), write=True)
        catalog.update_readme(catalog.render_catalog(skills, categories), write=False)

    def test_rejects_an_unregistered_skill(self) -> None:
        self.write_repository(registered=False)
        with self.assertRaisesRegex(catalog.ValidationError, "missing from catalog"):
            catalog.load_skills()

    def test_rejects_a_stale_readme_catalog(self) -> None:
        skills, categories = catalog.load_skills()
        with self.assertRaisesRegex(catalog.ValidationError, "catalog is stale"):
            catalog.update_readme(catalog.render_catalog(skills, categories), write=False)

    def test_rejects_a_folder_name_that_differs_from_frontmatter(self) -> None:
        skill_path = catalog.SKILLS_DIR / "sample-skill" / "SKILL.md"
        skill_path.write_text(
            "---\nname: another-skill\ndescription: A test skill.\n---\n\n# Test\n",
            encoding="utf-8",
        )
        with self.assertRaisesRegex(catalog.ValidationError, "folder name must match"):
            catalog.load_skills()


if __name__ == "__main__":
    unittest.main()
