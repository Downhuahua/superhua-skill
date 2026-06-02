# SuperHUA Skill

This repository packages `superhua` as a Codex skill in the official
GitHub-installable layout:

```text
skills/superhua/
  SKILL.md
  agents/
  references/
```

`superhua` is a Codex-local adaptation of
[abadcafe/superteam](https://github.com/abadcafe/superteam). It inserts two
front-loaded gates before the upstream Superteam planning and execution flow:

1. `proposal.md` through a proposal writer and reviewer.
2. `working/high-level-design.md` through a design writer and reviewer.
3. `working/spec.md` through `spec-writer`, then the original Superteam-style
   planning and executing chain.

The upstream Superteam snapshot is bundled under
`skills/superhua/references/upstream-superteam/` and pinned to commit:

```text
8123472865985477fb49841f93ca1c8782e4781d
```

## Install

After this repository is published to GitHub, install it with the official
Codex skill installer:

```bash
python ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo <owner>/<repo> \
  --path skills/superhua
```

Or install from a GitHub URL:

```bash
python ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --url https://github.com/<owner>/<repo>/tree/main/skills/superhua
```

Restart Codex after installation so new sessions auto-discover the skill.

## Use

Example prompt:

```text
Use $superhua.

Goal:
[what you want to build]

Input:
[current project, existing files, assets, constraints]

Output:
Create proposal.md first.
Then create working/high-level-design.md.
After both are reviewed, continue automatically through working/spec.md,
task planning, TDD implementation, review, testing, and summary.

Rules:
Ask me questions for unclear requirements or design choices.
Do not guess my intent.
Do not merge proposal and high-level design into one step.
```

## Validate

Validate the packaged skill:

```bash
python ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/superhua
```

## Licensing Note

The upstream `abadcafe/superteam` repository did not include an explicit license
in the snapshot used here. This package is intended for workflow analysis and
sharing; choose an appropriate license only after confirming rights for the
bundled upstream content.
