#!/usr/bin/env python3
"""Validate skill packages and render the README skill catalogue."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / "skills"
REGISTRY_PATH = ROOT / "catalog.yaml"
README_PATH = ROOT / "README.md"
START_MARKER = "<!-- skills-catalog:start -->"
END_MARKER = "<!-- skills-catalog:end -->"
VALID_STATUSES = {"experimental", "stable", "deprecated"}
SKILL_NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


class ValidationError(Exception):
    """Raised when repository metadata is invalid."""


@dataclass(frozen=True)
class Skill:
    name: str
    description: str
    path: Path
    category: str
    status: str


def load_yaml(path: Path) -> Any:
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as error:
        raise ValidationError(f"{path.relative_to(ROOT)}: invalid YAML: {error}") from error


def load_frontmatter(path: Path) -> dict[str, Any]:
    content = path.read_text(encoding="utf-8")
    if not content.startswith("---\n"):
        raise ValidationError(f"{path.relative_to(ROOT)}: must start with YAML frontmatter")
    try:
        _, raw_frontmatter, _ = content.split("---\n", 2)
    except ValueError as error:
        raise ValidationError(f"{path.relative_to(ROOT)}: frontmatter is not closed") from error
    try:
        metadata = yaml.safe_load(raw_frontmatter)
    except yaml.YAMLError as error:
        raise ValidationError(f"{path.relative_to(ROOT)}: invalid frontmatter YAML: {error}") from error
    if not isinstance(metadata, dict):
        raise ValidationError(f"{path.relative_to(ROOT)}: frontmatter must be a mapping")
    if set(metadata) != {"name", "description"}:
        raise ValidationError(
            f"{path.relative_to(ROOT)}: frontmatter must contain only name and description"
        )
    if not all(isinstance(metadata[key], str) and metadata[key].strip() for key in metadata):
        raise ValidationError(f"{path.relative_to(ROOT)}: name and description must be non-empty strings")
    return metadata


def validate_agent_metadata(skill: Skill) -> None:
    agent_path = skill.path / "agents" / "openai.yaml"
    if not agent_path.exists():
        return
    data = load_yaml(agent_path)
    interface = data.get("interface") if isinstance(data, dict) else None
    if not isinstance(interface, dict):
        raise ValidationError(f"{agent_path.relative_to(ROOT)}: interface mapping is required")
    for key in ("display_name", "short_description", "default_prompt"):
        value = interface.get(key)
        if not isinstance(value, str) or not value.strip():
            raise ValidationError(f"{agent_path.relative_to(ROOT)}: interface.{key} must be a non-empty string")
    if f"${skill.name}" not in interface["default_prompt"]:
        raise ValidationError(
            f"{agent_path.relative_to(ROOT)}: default_prompt must mention ${skill.name}"
        )


def load_skills() -> tuple[list[Skill], list[dict[str, str]]]:
    registry = load_yaml(REGISTRY_PATH)
    if not isinstance(registry, dict):
        raise ValidationError("catalog.yaml: must be a mapping")
    categories = registry.get("categories")
    entries = registry.get("skills")
    if not isinstance(categories, list) or not isinstance(entries, list):
        raise ValidationError("catalog.yaml: categories and skills must be lists")

    category_titles: dict[str, str] = {}
    for category in categories:
        if not isinstance(category, dict) or set(category) != {"id", "title"}:
            raise ValidationError("catalog.yaml: each category requires only id and title")
        category_id, title = category["id"], category["title"]
        if not isinstance(category_id, str) or not isinstance(title, str) or not category_id or not title:
            raise ValidationError("catalog.yaml: category id and title must be non-empty strings")
        if category_id in category_titles:
            raise ValidationError(f"catalog.yaml: duplicate category id {category_id}")
        category_titles[category_id] = title

    registry_by_name: dict[str, dict[str, str]] = {}
    for entry in entries:
        if not isinstance(entry, dict) or set(entry) != {"name", "path", "category", "status"}:
            raise ValidationError("catalog.yaml: each skill requires only name, path, category, and status")
        name, path, category, status = entry["name"], entry["path"], entry["category"], entry["status"]
        if not all(isinstance(value, str) and value for value in (name, path, category, status)):
            raise ValidationError("catalog.yaml: skill fields must be non-empty strings")
        if not SKILL_NAME_PATTERN.fullmatch(name):
            raise ValidationError(f"catalog.yaml: skill name must be kebab-case: {name}")
        if path != f"skills/{name}":
            raise ValidationError(f"catalog.yaml: path must be skills/{name} for {name}")
        if name in registry_by_name:
            raise ValidationError(f"catalog.yaml: duplicate skill name {name}")
        if category not in category_titles:
            raise ValidationError(f"catalog.yaml: unknown category {category} for {name}")
        if status not in VALID_STATUSES:
            raise ValidationError(f"catalog.yaml: invalid status {status} for {name}")
        registry_by_name[name] = entry

    skill_paths = sorted(SKILLS_DIR.glob("*/SKILL.md"))
    if not skill_paths:
        raise ValidationError("skills: at least one skill is required")
    discovered_names: set[str] = set()
    skills: list[Skill] = []
    for path in skill_paths:
        metadata = load_frontmatter(path)
        name = metadata["name"]
        if not SKILL_NAME_PATTERN.fullmatch(name):
            raise ValidationError(f"{path.relative_to(ROOT)}: skill name must be kebab-case")
        if path.parent.name != name:
            raise ValidationError(f"{path.relative_to(ROOT)}: folder name must match skill name {name}")
        if name in discovered_names:
            raise ValidationError(f"skills: duplicate skill name {name}")
        if name not in registry_by_name:
            raise ValidationError(f"{path.relative_to(ROOT)}: skill is missing from catalog.yaml")
        discovered_names.add(name)
        entry = registry_by_name[name]
        if entry["path"] != path.parent.relative_to(ROOT).as_posix():
            raise ValidationError(f"catalog.yaml: path does not match package location for {name}")
        skill = Skill(name, metadata["description"], path.parent, entry["category"], entry["status"])
        validate_agent_metadata(skill)
        skills.append(skill)

    untracked = set(registry_by_name) - discovered_names
    if untracked:
        raise ValidationError(f"catalog.yaml: registered skills missing on disk: {', '.join(sorted(untracked))}")
    return skills, [{"id": key, "title": value} for key, value in category_titles.items()]


def render_catalog(skills: list[Skill], categories: list[dict[str, str]]) -> str:
    sections: list[str] = []
    for category in categories:
        grouped = sorted((skill for skill in skills if skill.category == category["id"]), key=lambda skill: skill.name)
        if not grouped:
            continue
        lines = [f"### {category['title']}", ""]
        for skill in grouped:
            lines.append(
                f"- [`{skill.name}`](skills/{skill.name}/SKILL.md) — {skill.description} **{skill.status.title()}**"
            )
        sections.append("\n".join(lines))
    return "\n\n".join(sections)


def update_readme(catalog: str, write: bool) -> None:
    readme = README_PATH.read_text(encoding="utf-8")
    if readme.count(START_MARKER) != 1 or readme.count(END_MARKER) != 1:
        raise ValidationError("README.md: must contain one pair of skills catalog markers")
    end = readme.index(END_MARKER)
    rendered = f"{START_MARKER}\n{catalog}\n{END_MARKER}"
    current = readme[readme.index(START_MARKER):end + len(END_MARKER)]
    if current == rendered:
        return
    if write:
        README_PATH.write_text(readme[:readme.index(START_MARKER)] + rendered + readme[end + len(END_MARKER):], encoding="utf-8")
        print("Updated README.md")
        return
    raise ValidationError("README.md: generated skills catalog is stale; run python3 scripts/catalog.py --write")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true", help="validate and require an up-to-date README")
    mode.add_argument("--write", action="store_true", help="validate and update the README catalog")
    args = parser.parse_args()
    try:
        skills, categories = load_skills()
        update_readme(render_catalog(skills, categories), write=args.write)
    except (OSError, ValidationError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    print(f"Validated {len(skills)} skill(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
