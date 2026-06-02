---
name: superhua
description: Use when starting or continuing SuperHUA project work with file-backed requirements, design, planning, implementation, review, and verification stages.
---

# SuperHUA

SuperHUA is a Codex-local adaptation of `abadcafe/superteam`. It keeps the
state-machine controller, file boundary, fresh-agent execution, review loop,
and `Status: Pending` convergence model from Superteam, but adds two
front-loaded document stages before planning and execution:

1. Requirements discussion and `proposal.md`.
2. High-level design and `working/high-level-design.md`.

These are two separate stages. They must never be collapsed into one prompt,
one agent call, one context, or one output pass. After each document is created
and reviewed, the main controller must stop for explicit human approval before
entering the next stage. After both documents are reviewed and human-approved,
continue automatically: normalize a spec, split tasks, execute tasks serially
with TDD, review, fix, verify, and produce a task summary.

## Main Controller Iron Law

The main conversation is a state-machine controller only.

The main controller must not write `proposal.md`, must not write
`working/high-level-design.md`, must not write `working/spec.md`, must not write
task plans, must not implement code, and must not review its own work. It may
only:

- Inspect which state files exist.
- Record the user's original request and answers in `working/user-input.md`.
- Dispatch the next required fresh agent using the prompt files in `agents/`.
- Read the exact output files produced by agents.
- Return agent-written questions to the user.
- Count `Status: Pending` lines and dispatch the next agent in the flow.
- Write approval marker files only after the user explicitly approves the
  current document in the main conversation.
- Report completion, file paths, metrics, and blockers.

On every state transition, emit this declaration exactly:

```text
I am a SuperHUA state machine. I do not write deliverables in the main window. I dispatch fresh agents and read files.
```

If subagent dispatch is unavailable, stop and say that SuperHUA requires a
subagent-capable session. Do not perform the same role locally in the main
window.

NEVER:

- Skip a state transition.
- Combine Stage 1 and Stage 2.
- Add extra context to a dispatched agent prompt.
- Interpret or summarize an agent response as proof of completion.
- Check status from chat text. Status comes from files only.
- Fix, verify, review, or implement in the main window.
- Continue when a required output file is missing.

## State Detection

Run this check first from the project root:

- Missing `proposal.md`: enter Stage 1.
- `proposal.md` exists but `working/proposal-review-results.md` is missing or
  has `Status: Pending`: run the proposal review loop first.
- Reviewed `proposal.md` exists but `working/proposal-approved.md` is missing:
  return the reviewed proposal path and wait for explicit user approval. Do not
  enter Stage 2.
- Approved `proposal.md` exists but `working/high-level-design.md` is missing:
  enter Stage 2.
- `working/high-level-design.md` exists but
  `working/design-review-results.md` is missing or has `Status: Pending`: run
  the design review loop first.
- Reviewed `working/high-level-design.md` exists but
  `working/design-approved.md` is missing: return the reviewed design path and
  wait for explicit user approval. Do not enter Stage 3.
- Both documents exist, both reviews have zero pending issues, and both
  approval marker files exist: enter Stage 3 through `agents/spec-writer.md`,
  then continue through Stage 4 automatically.

Do not dispatch `agents/spec-writer.md`, planner, or implementer while either
approval marker is missing.

If the user explicitly asks to redo a stage, redo only that stage and downstream
generated files that depend on it.

## Stage 1: Proposal

This stage is interactive but still subagent-driven. The goal is a requirements
document at `proposal.md`.

Rules:

- The main controller records the user's request and answers in
  `working/user-input.md`.
- The main controller dispatches `agents/proposal-writer.md` using the exact
  prompt format in `references/workflow.md`.
- If requirements are unclear, proposal-writer writes
  `working/proposal-questions.md` instead of `proposal.md`.
- The main controller returns those questions to the user and waits.
- After the user answers, the main controller appends the answers to
  `working/user-input.md` and re-dispatches proposal-writer.
- When `proposal.md` exists, dispatch `agents/proposal-reviewer.md` using the
  exact prompt format.
- If `working/proposal-review-results.md` contains `Status: Pending`,
  dispatch proposal-writer again. Repeat until zero pending issues remain.
- When the review has zero pending issues, return the reviewed `proposal.md`
  path plus a concise status summary to the user and wait.
- Only after the user explicitly approves the requirements document, write
  `working/proposal-approved.md` and enter Stage 2. Accept approvals that name
  the document or stage, such as `OK proposal`, `approve proposal`,
  `确认需求文档`, or `需求文档确认`. Do not treat a generic "continue" as
  approval.
- Do not guess the user's intent. Do not create a high-level design in this
  stage.

`proposal.md` must contain:

- Goal
- Current project context
- Inputs and existing assets
- Outputs
- Functional requirements
- Non-functional requirements
- Non-goals
- Constraints
- Acceptance criteria
- Open questions, only if the user explicitly leaves something open

## Stage 2: High-Level Design

This stage is interactive if design choices are unclear, but it is also
subagent-driven. The goal is a design document at
`working/high-level-design.md`.

Rules:

- Stage 2 must start only after Stage 1 is reviewed, `proposal.md` exists, and
  `working/proposal-approved.md` exists.
- The main controller dispatches `agents/design-writer.md` using the exact
  prompt format in `references/workflow.md`.
- If design-affecting ambiguity remains, design-writer writes
  `working/design-questions.md` instead of
  `working/high-level-design.md`.
- The main controller returns those questions to the user and waits.
- After the user answers, the main controller appends the answers to
  `working/user-input.md` and re-dispatches design-writer.
- When `working/high-level-design.md` exists, dispatch
  `agents/design-reviewer.md` using the exact prompt format.
- If `working/design-review-results.md` contains `Status: Pending`, dispatch
  design-writer again. Repeat until zero pending issues remain.
- When the review has zero pending issues, return the reviewed
  `working/high-level-design.md` path plus a concise status summary to the user
  and wait.
- Only after the user explicitly approves the design document, write
  `working/design-approved.md` and enter Stage 3. Accept approvals that name the
  document or stage, such as `OK design`, `approve design`, `确认概要设计`, or
  `概要设计确认`. Do not treat a generic "continue" as approval.
- Do not guess the user's intent. Do not plan implementation tasks in this
  stage.

`working/high-level-design.md` must contain:

- Overview
- Requirements traceability
- Module breakdown
- Module relationships
- Data flow and control flow
- External interfaces
- Error handling and edge cases
- Test strategy
- Risks and open decisions

## Stage 3: Planning

This stage is hands-off only after Stage 1 and Stage 2 are reviewed and
human-approved.

Dispatch `agents/spec-writer.md` to create `working/spec.md` from
`proposal.md` and `working/high-level-design.md` if it does not exist or is
stale. Then enter the original Superteam planning flow: create task files under
`working/plan/task-NNN/task.md`.

Use the planner and plan-reviewer prompts in `agents/` with the exact prompt
formats in `references/workflow.md`. Planner, plan-reviewer, implementer,
spec-reviewer, code-reviewer, black-box-testing, and hands-off issue handling
must follow the complete upstream Superteam contracts preserved under
`references/upstream-superteam/`, plus the SuperHUA overrides in
`references/workflow.md`. Iterate until `working/plan-review-results.md` has
zero `Status: Pending` issues.

Dispatch fresh agents using the prompt files. If subagent dispatch is
unavailable, stop and report that SuperHUA cannot run in this session.

## Stage 4: Execution

This stage is hands-off once the plan is reviewed.

Execute tasks serially. For each task:

1. Run the implementer role.
2. Require TDD: failing tests first, minimal implementation, passing tests.
3. Run project tests and coverage checks. Code changes must keep coverage at least 80% unless the user explicitly changes that project rule.
4. Run spec-reviewer and code-reviewer roles.
5. Fix every `Status: Pending` issue and review again.
6. Continue until no pending issues remain.

Only stop for the user after at least three distinct, actually executed attempts
fail to resolve an environment or requirement blocker. Record the blocker in the
proper issue file before stopping.

Do not create git commits unless the user explicitly asks. Produce
`working/commit-message.md` and `working/task-summary.md` instead.

## Superpowers Interop

SuperHUA borrows Superpowers discipline, especially TDD, but SuperHUA owns the
workflow after Stage 2.

When operating inside SuperHUA:

- Use `superpowers:test-driven-development` as the testing discipline when it
  applies.
- Do not switch to `superpowers:writing-plans`,
  `superpowers:executing-plans`,
  `superpowers:subagent-driven-development`,
  `superpowers:dispatching-parallel-agents`, or
  `superpowers:finishing-a-development-branch` unless the user explicitly asks.
- Do not replace SuperHUA task files with a single generic plan file.
- Keep role communication through files under `working/`.

## Upstream Compatibility Layer

The complete upstream Superteam snapshot is preserved under
`references/upstream-superteam/` at commit
`8123472865985477fb49841f93ca1c8782e4781d`.

SuperHUA must treat those files as the canonical Stage 3/4 behavior:

- `references/upstream-superteam/skills/planning/SKILL.md`
- `references/upstream-superteam/skills/executing/SKILL.md`
- `references/upstream-superteam/skills/black-box-testing/SKILL.md`
- `references/upstream-superteam/skills/hands-off-issue-handling/SKILL.md`
- `references/upstream-superteam/agents/planner.md`
- `references/upstream-superteam/agents/plan-reviewer.md`
- `references/upstream-superteam/agents/implementer.md`
- `references/upstream-superteam/agents/spec-reviewer.md`
- `references/upstream-superteam/agents/code-reviewer.md`

Only these SuperHUA overrides apply:

- Insert Stage 1 proposal and Stage 2 high-level design before upstream
  `working/spec.md`.
- Require explicit human approval marker files after proposal review and design
  review before any `working/spec.md`, planning, or execution work.
- Use `agents/spec-writer.md` to synthesize upstream-compatible
  `working/spec.md`.
- Use `working/task-issues.md`; do not use `working/plan-issues.md`.
- Do not use the upstream Claude plugin namespace. Dispatch local prompt files
  by path.
- Do not make commits unless the user explicitly asks.

## Supporting Files

- `references/workflow.md`: full file contracts and state-machine details.
- `agents/proposal-writer.md`: requirements document writer role.
- `agents/proposal-reviewer.md`: requirements document review role.
- `agents/design-writer.md`: high-level design writer role.
- `agents/design-reviewer.md`: high-level design review role.
- `agents/spec-writer.md`: normalized Superteam-compatible spec writer role.
- `agents/planner.md`: task planner role.
- `agents/plan-reviewer.md`: plan review role.
- `agents/implementer.md`: task implementation role.
- `agents/spec-reviewer.md`: task/spec compliance review role.
- `agents/code-reviewer.md`: code quality review role.

## Common Mistakes

- Skipping the proposal discussion because the prompt looks detailed.
- Writing the high-level design while requirements are still ambiguous.
- Asking the user again during Stage 3 or Stage 4 for non-blocking details.
- Treating reviewer output as advice. `Status: Pending` is a work item.
- Letting skipped tests or low coverage pass silently.
