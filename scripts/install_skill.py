#!/usr/bin/env python3
"""Install a repository skill into a supported coding tool's skill directory."""

from __future__ import annotations

import argparse
import os
import shutil
import sys
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIRECTORY = REPOSITORY_ROOT / "skills"
TOOLS = ("codex", "claude-code", "antigravity")
SCOPES = ("user", "project")


def destination_root(
    tool: str,
    scope: str,
    *,
    home: Path | None = None,
    cwd: Path | None = None,
    codex_home: Path | None = None,
) -> Path:
    """Return the tool-managed directory in which skill packages live."""
    home = home or Path.home()
    cwd = cwd or Path.cwd()
    if tool == "codex":
        if scope != "user":
            raise ValueError("Codex supports only user scope in this installer")
        return (codex_home or Path(os.environ.get("CODEX_HOME", home / ".codex"))) / "skills"
    if tool == "claude-code":
        return home / ".claude" / "skills" if scope == "user" else cwd / ".claude" / "skills"
    if tool == "antigravity":
        return home / ".gemini" / "config" / "skills" if scope == "user" else cwd / ".agents" / "skills"
    raise ValueError(f"Unsupported tool: {tool}")


def install_skill(source: Path, destination: Path, mode: str, force: bool) -> None:
    """Copy or symlink one validated package, refusing replacement by default."""
    if not source.joinpath("SKILL.md").is_file():
        raise ValueError(f"Skill package is missing SKILL.md: {source}")
    if destination.exists() or destination.is_symlink():
        if not force:
            raise FileExistsError(f"Destination already exists: {destination}; use --force to replace it")
        if destination.is_symlink() or destination.is_file():
            destination.unlink()
        else:
            shutil.rmtree(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    if mode == "copy":
        shutil.copytree(source, destination)
    else:
        destination.symlink_to(source.resolve(), target_is_directory=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("skill", help="Skill folder name from skills/")
    parser.add_argument("--tool", choices=TOOLS, required=True)
    parser.add_argument("--scope", choices=SCOPES, default="user")
    parser.add_argument("--mode", choices=("copy", "symlink"), default="copy")
    parser.add_argument("--force", action="store_true", help="replace an existing destination")
    parser.add_argument("--dry-run", action="store_true", help="print the target without writing files")
    args = parser.parse_args()

    source = SKILLS_DIRECTORY / args.skill
    try:
        destination = destination_root(args.tool, args.scope) / args.skill
        if args.dry_run:
            print(f"Would {args.mode} {source} to {destination}")
            return 0
        install_skill(source, destination, args.mode, args.force)
    except (OSError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    print(f"Installed {args.skill} for {args.tool} at {destination}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

