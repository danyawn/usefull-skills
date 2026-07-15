# Useful Skills

A curated collection of portable Agent Skills for Codex, Claude Code, and Google Antigravity. Each package uses the open `SKILL.md` format: YAML frontmatter for discovery and Markdown instructions for execution.

## Install a skill

Install one skill with the portable installer:

```sh
python3 scripts/install_skill.py dashboard-ux --tool claude-code --scope user
```

Use `--tool codex`, `--tool claude-code`, or `--tool antigravity`; add `--scope project` where the tool supports project-local skills. The default copies the package; add `--mode symlink` to develop it from this checkout. See [installation instructions](docs/INSTALL.md) for every target path and manual setup.

## For AI agents: install on the user's behalf

An AI agent may install a skill for the user, but only after explicit approval. Follow this flow:

1. Read the generated **Skills** catalog below and present the relevant available skills with their descriptions.
2. Ask the user to choose the skill, target tool (`codex`, `claude-code`, or `antigravity`), and scope when supported (`user` or `project`).
3. State the exact destination and proposed command, then wait for an unambiguous confirmation.
4. After confirmation, verify the requested package exists in `skills/<skill-name>/SKILL.md`, then run `python3 scripts/install_skill.py <skill-name> --tool <tool> --scope <scope>`.
5. Report the installed path and any error. Do not use `--force`, overwrite an existing skill, or install a different skill unless the user explicitly approves that action.

Use `--dry-run` before the confirmation when the agent needs to show the target path without changing the user's machine.

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
