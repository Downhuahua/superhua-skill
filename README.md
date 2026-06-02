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
[abadcafe/superteam](https://github.com/abadcafe/superteam). It turns a manual
VibeCoding preparation flow into a run-scoped automation without dropping the
human judgment gates:

1. `RUN/doc/proposal.md` through a proposal writer, reviewer, and explicit user
   approval.
2. `RUN/doc/high-level-design.md` through a design writer, reviewer, and
   explicit user approval.
3. `RUN/doc/detailed-design.md` through a question-gated writer/reviewer loop.
4. `RUN/doc/tasks/<module-name>.md` and `RUN/doc/tasks/progress.md` through a
   question-gated task writer/reviewer loop.
5. `RUN/doc/prompt.md` through a question-gated prompt writer/reviewer loop.
6. Execute `RUN/doc/prompt.md` using the bundled Superteam-style
   planning/executing/reviewing chain with runtime guards.

Each SuperHUA task gets its own run directory:

```text
working/superhua-runs/<run-id>/
```

The controller maintains `working/superhua-current.md` and
`working/superhua-index.md` so multiple SuperHUA tasks can coexist in the same
project folder without overwriting each other's proposal, designs, task files,
prompt, plan, or execution state. Legacy root files such as `proposal.md`,
root `doc/`, or `working/plan/` are reported as legacy state and are not treated
as the active run.

SuperHUA works unattended only after `RUN/doc/prompt.md` is reviewed with zero
pending issues. It still stops for questions during detailed design, task
splitting, and prompt generation when a missing answer would change intent or
execution behavior. During execution, Python projects must pass pytest, mypy,
and ruff unless the user explicitly changes that rule.

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
  --repo Downhuahua/superhua-skill \
  --path skills/superhua
```

Or install from a GitHub URL:

```bash
python ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --url https://github.com/Downhuahua/superhua-skill/tree/main/skills/superhua
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
Create a new run under working/superhua-runs/<run-id>/.
Create RUN/doc/proposal.md first.
Then create RUN/doc/high-level-design.md.
After RUN/doc/proposal.md is reviewed, stop and wait for my explicit approval
before high-level design.
After RUN/doc/high-level-design.md is reviewed, stop and wait for my explicit
approval before detailed design.
Then create RUN/doc/detailed-design.md, RUN/doc/tasks/<module-name>.md,
RUN/doc/tasks/progress.md, and RUN/doc/prompt.md.
If any of those stages is unclear, ask me questions before continuing.
After RUN/doc/prompt.md is reviewed, execute it automatically.

Rules:
Ask me questions for unclear requirements, design choices, task boundaries, or
prompt execution rules.
Do not guess my intent.
Do not merge proposal, high-level design, detailed design, tasks, or prompt into
one step.
Do not write SuperHUA process files to the project root.
Do not treat reviewer success or a generic "continue" as approval.
For Python projects, require pytest, mypy, and ruff.
If the reviewed plan is large, stop before execution and ask for OK long run.
If one task loops through three implement/review cycles, stop and report the
loop issue instead of starting a fourth cycle.
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
