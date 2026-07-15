# Useful Skills

A curated collection of portable Agent Skills for Codex, Claude Code, and Google Antigravity. Each package uses the open `SKILL.md` format: YAML frontmatter for discovery and Markdown instructions for execution.

## Install a skill

Install one skill with the portable installer:

```sh
python3 scripts/install_skill.py dashboard-ux --tool claude-code --scope user
```

Use `--tool codex`, `--tool claude-code`, or `--tool antigravity`; add `--scope project` where the tool supports project-local skills. The default copies the package; add `--mode symlink` to develop it from this checkout. See [installation instructions](docs/INSTALL.md) for every target path and manual setup.

## Repository layout

```text
skills/<skill-name>/SKILL.md       # required skill instructions
skills/<skill-name>/agents/        # optional Codex UI metadata
catalog.yaml                       # category and lifecycle registry
scripts/catalog.py                 # validation and README catalogue generator
scripts/install_skill.py           # portable installer for supported coding tools
```

## Skills

<!-- skills-catalog:start -->
### Design & UX

- [`dashboard-ux`](skills/dashboard-ux/SKILL.md) — Build or refine operational, finance, admin, and analytics dashboards that are concise, decision-first, self-explanatory, terminology-faithful, and easy to scan. Use for dashboard pages, KPI summaries, data tables, reporting views, and dashboard redesigns—especially when the UI is too wordy, card-heavy, dependent on instructional prose, inconsistent with the product vocabulary, generic, overly spacious, or visually decorative. **Stable**
<!-- skills-catalog:end -->

## Maintain the catalog

Install the development dependency, then validate the repository before committing:

```sh
python3 -m pip install -r requirements-dev.txt
python3 scripts/catalog.py --check
```

Run `python3 scripts/catalog.py --write` after adding or reclassifying a skill to regenerate the marked catalogue section above.

See [CONTRIBUTING.md](CONTRIBUTING.md) for the contribution flow.
