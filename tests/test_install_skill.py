import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "install_skill.py"
SPEC = importlib.util.spec_from_file_location("install_skill", MODULE_PATH)
installer = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = installer
SPEC.loader.exec_module(installer)


class InstallSkillTests(unittest.TestCase):
    def test_returns_supported_user_and_project_destinations(self) -> None:
        home = Path("/home/tester")
        cwd = Path("/work/project")
        self.assertEqual(installer.destination_root("codex", "user", home=home), home / ".codex" / "skills")
        self.assertEqual(installer.destination_root("claude-code", "project", home=home, cwd=cwd), cwd / ".claude" / "skills")
        self.assertEqual(installer.destination_root("antigravity", "user", home=home, cwd=cwd), home / ".gemini" / "config" / "skills")

    def test_rejects_unsupported_codex_project_scope(self) -> None:
        with self.assertRaisesRegex(ValueError, "only user scope"):
            installer.destination_root("codex", "project")

    def test_rejects_skill_names_that_could_escape_the_package_directory(self) -> None:
        for name in ("../dashboard-ux", "nested/dashboard-ux", "/tmp/dashboard-ux", "Dashboard_UX"):
            with self.subTest(name=name):
                with self.assertRaisesRegex(ValueError, "kebab-case"):
                    installer.skill_source(name)

    def test_rejects_a_missing_repository_skill(self) -> None:
        with self.assertRaisesRegex(ValueError, "direct repository child"):
            installer.skill_source("missing-skill")

    def test_copies_a_complete_skill_package(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source"
            source.mkdir()
            source.joinpath("SKILL.md").write_text("# Test\n", encoding="utf-8")
            source.joinpath("agents").mkdir()
            source.joinpath("agents", "openai.yaml").write_text("interface: {}\n", encoding="utf-8")
            destination = root / "installed" / "test-skill"
            installer.install_skill(source, destination, "copy", force=False)
            self.assertEqual(destination.joinpath("SKILL.md").read_text(encoding="utf-8"), "# Test\n")
            self.assertTrue(destination.joinpath("agents", "openai.yaml").is_file())
            with self.assertRaises(FileExistsError):
                installer.install_skill(source, destination, "copy", force=False)
            self.assertEqual(destination.joinpath("SKILL.md").read_text(encoding="utf-8"), "# Test\n")

    def test_creates_a_symlink_to_the_source_package(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source"
            source.mkdir()
            source.joinpath("SKILL.md").write_text("# Test\n", encoding="utf-8")
            destination = root / "installed" / "test-skill"
            installer.install_skill(source, destination, "symlink", force=False)
            self.assertTrue(destination.is_symlink())
            self.assertEqual(destination.resolve(), source.resolve())

    def test_force_replaces_an_existing_directory_file_or_symlink(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source"
            source.mkdir()
            source.joinpath("SKILL.md").write_text("# Test\n", encoding="utf-8")
            for kind in ("directory", "file", "symlink"):
                with self.subTest(kind=kind):
                    destination = root / "installed" / kind
                    destination.parent.mkdir(parents=True, exist_ok=True)
                    if kind == "directory":
                        destination.mkdir()
                    elif kind == "file":
                        destination.write_text("old", encoding="utf-8")
                    else:
                        destination.symlink_to(source, target_is_directory=True)
                    installer.install_skill(source, destination, "copy", force=True)
                    self.assertTrue(destination.is_dir())
                    self.assertFalse(destination.is_symlink())
                    self.assertTrue(destination.joinpath("SKILL.md").is_file())


if __name__ == "__main__":
    unittest.main()
