# .agents: agent workspace

This folder holds the standing instructions and working files for AI agents on this project. Start at [AGENTS.md](../AGENTS.md) in the repository root.

| Path | Holds | Maintained by |
|---|---|---|
| [`rules/`](rules/) | Rules every agent follows | Architect |
| [`context/`](context/) | Shared project context: what's settled, what's open, where the sources are | Architect |
| [`decisions.md`](decisions.md) | Decisions that shape how agents work, open and closed | The architect records them; the owner decides |
| [`handoffs/`](handoffs/) | One standing brief per agent role | Architect |
| [`backlog/`](backlog/) | One live work list per role | The agent in that role |
| [`skills/`](skills/) | Reusable procedures, one folder per skill | Any agent can propose one; the architect approves |

## Conventions

- **Version control.** These files aren't TT-KRC3006 controlled documents. Git is their revision history, and every change goes through a pull request.
- **Handoffs** (`handoffs/<role>.md`) cover the role's purpose, authority, scope and first assignments. They point to rules, skills and the backlog instead of repeating them.
- **Backlogs** (`backlog/<role>.md`) hold numbered items with permanent IDs, e.g. DC-NN for document control. Close an item by recording the pull request that closed it. Never renumber or delete items.
- **Skills** (`skills/<name>/SKILL.md`) follow the [Agent Skills](https://agentskills.io) format:
  - YAML frontmatter with only `name` (matching the folder name) and `description`, then the procedure.
  - Scripts go in `scripts/`. Keep them dependency-light: the Python 3 standard library, pandoc and poppler-utils.
  - Add every new skill to the skills table in AGENTS.md.
- **Rules** state the rule, then why it exists. If a rule and a handoff disagree, the rule wins and the architect fixes the handoff.
- **Public.** This repository is public. Nothing private belongs here.

## Claude Code notes

**CLAUDE.md.** The committed `CLAUDE.md` only imports `AGENTS.md`. When a `CLAUDE.md` exists, Claude Code reads it instead of `AGENTS.md`, so the import keeps everyone on the same instructions. Put new instructions in `AGENTS.md` or `.agents/`, not in `CLAUDE.md`.

**Skills.** Claude Code loads project skills from `.claude/skills/<name>/SKILL.md`. The skills here work without that, because AGENTS.md tells every agent where they are. To get native `/skill` loading as well, symlink each skill folder:

```sh
mkdir -p .claude/skills
ln -s ../../.agents/skills/doc-audit .claude/skills/doc-audit
```

Skip the symlinks if anyone works from a Windows checkout. Git checks symlinks out there as plain text files unless `core.symlinks` is enabled.
