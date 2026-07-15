# Install a skill

All packages in this repository use a portable `SKILL.md` format. The core instructions are identical across supported tools; optional `agents/openai.yaml` metadata is read by Codex and safely ignored by other tools.

Run the installer from this repository's root:

```sh
python3 scripts/install_skill.py dashboard-ux --tool <tool> --scope <scope>
```

The installer copies by default. Use `--mode symlink` to point the target at this checkout while authoring, `--dry-run` to print the destination, and `--force` only to replace an existing installed skill.

| Tool | User scope | Project scope |
| --- | --- | --- |
| Codex | `python3 scripts/install_skill.py dashboard-ux --tool codex` | Not provided by this installer; install to the configured Codex home. |
| Claude Code | `python3 scripts/install_skill.py dashboard-ux --tool claude-code --scope user` | `python3 scripts/install_skill.py dashboard-ux --tool claude-code --scope project` |
| Google Antigravity | `python3 scripts/install_skill.py dashboard-ux --tool antigravity --scope user` | `python3 scripts/install_skill.py dashboard-ux --tool antigravity --scope project` |

## Manual destinations

- Codex: `${CODEX_HOME:-$HOME/.codex}/skills/<skill-name>`
- Claude Code user: `~/.claude/skills/<skill-name>`
- Claude Code project: `.claude/skills/<skill-name>`
- Google Antigravity user: `~/.gemini/config/skills/<skill-name>`
- Google Antigravity project: `.agents/skills/<skill-name>`

Copy or symlink the complete package directory, not just `SKILL.md`, so optional metadata and future supporting resources remain available.

