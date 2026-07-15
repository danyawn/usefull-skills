# Contributing skills

1. Create `skills/<kebab-case-name>/` and add its required `SKILL.md` with YAML frontmatter containing only `name` and `description`.
2. Keep the directory name identical to the skill `name`. Add `agents/openai.yaml` only when Codex UI metadata is useful.
3. Register the skill in `catalog.yaml` with one existing category and a lifecycle status of `experimental`, `stable`, or `deprecated`.
4. Install the development dependency, regenerate the catalogue with `python3 scripts/catalog.py --write`, and verify it with `python3 scripts/catalog.py --check`.
5. Submit the skill folder, registry change, and generated README update together.

Do not add a per-skill README, installation guide, or changelog. Keep reusable scripts, references, and assets inside the skill only when the skill instructions require them.

