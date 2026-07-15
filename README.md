# Useful Skills

A curated, installable collection of Codex skills. Each skill is a self-contained folder whose `SKILL.md` provides the instructions Codex loads when the skill applies.

## Install a skill

Copy one skill directory into your Codex skills directory, preserving its name:

```sh
cp -R skills/dashboard-ux "${CODEX_HOME:-$HOME/.codex}/skills/dashboard-ux"
```

Restart or refresh Codex after installing it. The skill can then be invoked as `$dashboard-ux`.

## Repository layout

```text
skills/<skill-name>/SKILL.md       # required skill instructions
skills/<skill-name>/agents/        # optional Codex UI metadata
catalog.yaml                       # category and lifecycle registry
scripts/catalog.py                 # validation and README catalogue generator
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

