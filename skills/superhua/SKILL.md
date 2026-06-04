---
name: superhua
description: Use when the user asks to use SuperHUA/superhua or continue a SuperHUA run in a project workspace.
---

# SuperHUA

SuperHUA is a Codex-local adaptation of `abadcafe/superteam` with
Easy-Vibe-style task routing. It preserves the original Superteam
state-machine discipline, fresh-agent execution, review loops, and
`Status: Pending` convergence model for work that actually needs it, while
keeping small tasks out of the full six-stage path.

The controller always starts with Stage 0 task routing. The router chooses one
mode:

- `vibe-lite`: one clear, low-risk task. Use one executor and immediate
  verification.
- `vibe-standard`: moderate work that benefits from proposal/design alignment
  but does not need detailed design, module task files, and prompt synthesis.
- `spec-full`: complex, risky, multi-module, long-running, production, or
  explicitly requested full Superteam-compatible execution.

The `spec-full` document chain is:

1. `RUN/doc/proposal.md`
2. `RUN/doc/high-level-design.md`
3. `RUN/doc/detailed-design.md`
4. `RUN/doc/tasks/<module-name>.md` and `RUN/doc/tasks/progress.md`
5. `RUN/doc/prompt.md`
6. Execute `RUN/doc/prompt.md` through internal Superteam-compatible planning,
   implementation, testing, and review.

In `spec-full`, Stages 1 and 2 require explicit human approval after
zero-pending review. Stages 3, 4, and 5 are still question-gated: if anything
would change user intent, architecture, module boundaries, task scope, tests, or
execution rules, the writer agent must ask questions and the controller must
wait. After Stage 5 is reviewed with zero pending issues, Stage 6 runs
hands-off except for real blockers and runtime guardrails.

Easy-Vibe operating principle: one clear task, one appropriately sized workflow,
then verify. Do not use `spec-full` merely because the user said "use
SuperHUA".

## Run Scope

Default run directory:

```text
RUN = working/superhua-runs/<run-id>
```

`<run-id>` is `YYYYMMDD-HHMM-<short-slug>` derived from the task goal.

Controller-owned project-level files:

- `working/superhua-current.md`: current run id and run directory.
- `working/superhua-index.md`: append-only list of run ids, goals, status,
  created time, and run directories.

If the user starts a new SuperHUA task in a project that already has SuperHUA
state, create a new run directory. If the user says to continue and there is
more than one run, list the run ids and ask the user to choose. Do not infer the
active run from root `proposal.md`, root `doc/`, or root `working/plan/`.

Project code changes still happen in the project root. Only SuperHUA process
files are isolated inside `RUN`.

## Main Controller Iron Law

The main conversation is a state-machine controller only.

The main controller must not write deliverables:

- `RUN/doc/proposal.md`
- `RUN/doc/high-level-design.md`
- `RUN/doc/detailed-design.md`
- `RUN/doc/tasks/*.md`
- `RUN/doc/prompt.md`
- `RUN/spec.md`
- `RUN/plan/task-NNN/task.md`
- `RUN/task-profile.md`
- `RUN/lite-summary.md`
- `RUN/standard-summary.md`

It may only:

- Select or create run directories.
- Create required run subdirectories such as `RUN/doc`, `RUN/questions`,
  `RUN/reviews`, `RUN/approvals`, `RUN/plan`, and `RUN/process` before
  dispatching agents that write inside them.
- Maintain `working/superhua-current.md` and `working/superhua-index.md`.
- Record the user's original request and answers in `RUN/user-input.md`.
- Write `RUN/mode.md` from the exact selected mode in `RUN/task-profile.md`.
- Dispatch the next required fresh agent using the exact prompt formats in
  `references/workflow.md`.
- Read exact output files produced by agents.
- Return agent-written questions to the user and wait.
- Count `Status: Pending` lines and dispatch the next agent in the flow.
- Write approval marker files only after the user explicitly approves Stage 1
  or Stage 2 in the main conversation.
- Maintain `RUN/runtime-metrics.md` and runtime guard files.
- Write `RUN/commit-message.md` and `RUN/task-summary.md` after Stage 6 using
  only file outputs.
- Report completion, file paths, metrics, and blockers.

On every state transition, emit this declaration exactly:

```text
I am a SuperHUA state machine. I do not write deliverables in the main window. I dispatch fresh agents and read files.
```

If subagent dispatch is unavailable, stop and say that SuperHUA requires a
subagent-capable session. Do not perform the same role locally in the main
window.

## Dispatch Mechanics

A request to use or continue SuperHUA authorizes dispatching the named
SuperHUA role agents. If the current user request does not explicitly authorize
SuperHUA, child agents, subagents, or delegated agent work, stop and ask for
confirmation before dispatching.

Dispatch means:

- Use the available subagent or multi-agent facility for one fresh agent per
  role invocation.
- Pass only the exact prompt format from `references/workflow.md`.
- Do not add chat summaries, advice, inferred requirements, or hidden context.
- Do not reuse the same child agent across different roles or stages.
- Wait for the required output files, then inspect files rather than chat text.
- Run writer/reviewer loops serially.
- Run `spec-reviewer` and `code-reviewer` serially because they share
  `RUN/plan/task-NNN/implement-review-results.md`.
- Do not parallelize SuperHUA role agents unless the workflow explicitly says a
  pair is independent. The default is serial execution.

NEVER:

- Skip a stage.
- Combine two stages into one prompt, context, agent call, or output pass.
- Force `spec-full` on a lite or standard task.
- Run long research collection without an explicit source/evidence cap.
- Dispatch a child agent with extra context outside the exact prompt format.
- Let a child agent write outside its provided run-scoped paths.
- Treat review success as human approval.
- Treat a generic "continue" as approval for proposal or high-level design.
- Check status from chat text. Status comes from files only.
- Fix, verify, review, design, plan, prompt-write, or implement in the main
  window.
- Start Stage 6 before `RUN/doc/prompt.md` is reviewed with zero pending
  issues.

## File Contracts

Mode and routing:

- `RUN/task-profile.md`: router output with selected mode, confidence, evidence
  cap, risk level, verification plan, and reason.
- `RUN/mode.md`: controller-owned copy of the selected mode.
- `RUN/questions/router-questions.md`

Lite/standard execution:

- `RUN/lite-summary.md`
- `RUN/standard-summary.md`
- `RUN/process/*`: optional bounded process artifacts. Research and evidence
  collection artifacts must stay bounded by `RUN/task-profile.md`.

Human-visible deliverables:

- `RUN/doc/proposal.md`
- `RUN/doc/high-level-design.md`
- `RUN/doc/detailed-design.md`
- `RUN/doc/tasks/<module-name>.md`
- `RUN/doc/tasks/progress.md`
- `RUN/doc/prompt.md`

Questions:

- `RUN/questions/router-questions.md`
- `RUN/questions/lite-questions.md`
- `RUN/questions/standard-questions.md`
- `RUN/questions/proposal-questions.md`
- `RUN/questions/design-questions.md`
- `RUN/questions/detailed-design-questions.md`
- `RUN/questions/task-questions.md`
- `RUN/questions/prompt-questions.md`

Reviews:

- `RUN/reviews/proposal-review-results.md`
- `RUN/reviews/design-review-results.md`
- `RUN/reviews/detailed-design-review-results.md`
- `RUN/reviews/task-review-results.md`
- `RUN/reviews/prompt-review-results.md`
- `RUN/plan-review-results.md`
- `RUN/plan/task-NNN/implement-review-results.md`

Approvals and runtime state:

- `RUN/mode.md`
- `RUN/approvals/proposal-approved.md`
- `RUN/approvals/design-approved.md`
- `RUN/spec.md`: internal Superteam-compatible spec synthesized after
  `prompt.md`.
- `RUN/plan/task-NNN/task.md`: internal executable tasks for Stage 6.
- `RUN/execution-budget.md`
- `RUN/execution-approved.md`
- `RUN/runtime-metrics.md`
- `RUN/spec-issues.md`
- `RUN/task-issues.md`
- `RUN/env-issues.md`
- `RUN/plan/task-NNN/loop-issues.md`
- `RUN/commit-message.md`
- `RUN/task-summary.md`

Legacy root files such as `proposal.md`, root `doc/`, or root `working/plan/`
must be reported as legacy state and must not be treated as the selected run.

## State Detection

Run this check first from the project root:

- If no run is selected, select or create a run using the Run Scope rules.
- If `RUN/task-profile.md` is missing: Stage 0.
- If `RUN/questions/router-questions.md` exists and is non-empty: return it and
  wait.
- If `RUN/task-profile.md` exists but `RUN/mode.md` is missing: write
  `RUN/mode.md` from the exact selected mode in `RUN/task-profile.md`.
- If `RUN/mode.md` is `vibe-lite`: run the Lite Flow.
- If `RUN/mode.md` is `vibe-standard`: run the Standard Flow.
- If `RUN/mode.md` is `spec-full`: run the Spec-Full Flow below.
- If `RUN/doc/proposal.md` is missing: Stage 1.
- If proposal review is missing or has `Status: Pending`: Stage 1 review loop.
- If `RUN/approvals/proposal-approved.md` is missing or stale: return the
  reviewed proposal path and wait for explicit user approval.
- If `RUN/doc/high-level-design.md` is missing: Stage 2.
- If design review is missing or has `Status: Pending`: Stage 2 review loop.
- If `RUN/approvals/design-approved.md` is missing or stale: return the
  reviewed design path and wait for explicit user approval.
- If `RUN/doc/detailed-design.md` is missing: Stage 3.
- If detailed-design review is missing or has `Status: Pending`: Stage 3 review
  loop.
- If `RUN/doc/tasks/progress.md` or any module task file is missing: Stage 4.
- If task review is missing or has `Status: Pending`: Stage 4 review loop.
- If `RUN/doc/prompt.md` is missing: Stage 5.
- If prompt review is missing or has `Status: Pending`: Stage 5 review loop.
- If prompt is reviewed with zero pending issues: Stage 6 execution.

If any questions file for the active stage exists and is non-empty, return it to
the user and wait before dispatching the next writer or reviewer.

If the user explicitly asks to redo a stage, redo only that stage and downstream
generated files that depend on it. Remove stale approval markers and downstream
automation files before continuing.

## Stage 0: Task Router

Goal: choose the lightest workflow that can safely satisfy the request.

Rules:

- Dispatch `agents/task-router.md`.
- If the task is unclear enough that choosing a mode would guess user intent,
  return `RUN/questions/router-questions.md` and wait.
- The router writes `RUN/task-profile.md`.
- The controller writes `RUN/mode.md` from the exact selected mode in
  `RUN/task-profile.md`.
- Respect explicit user mode requests:
  - `lite`, `vibe-lite`, "quick", "小任务", or "轻量" prefer `vibe-lite`.
  - `standard`, "标准", or "先对齐再做" prefer `vibe-standard`.
  - `full`, `spec-full`, "完整流程", "长任务", or "OK long run" prefer
    `spec-full`.
- If explicit mode conflicts with risk, choose the safer mode and explain the
  reason in `RUN/task-profile.md`.

Routing rules:

- Choose `vibe-lite` for clear, low-risk tasks touching at most two files, small
  document edits, simple bug fixes with reproduction, formatting, minor
  configuration, or one-shot inspection/reporting.
- Choose `vibe-standard` for moderate changes touching several files, small
  skill updates, non-trivial bug fixes, or tasks that need requirements/design
  alignment but not full detailed design/module task/prompt generation.
- Choose `spec-full` only for complex or high-risk work: multi-module
  refactors, new product/system builds, ambiguous architecture, irreversible
  external writes, security-sensitive work, broad research synthesis,
  production-grade delivery, or user-requested full automation.
- Research tasks default to a capped mode. The router must set a concrete
  evidence cap, normally 10-20 accepted records, unless the user explicitly asks
  for deep research.

## Lite Flow

Goal: finish one clear task with minimal process overhead.

Rules:

- Dispatch `agents/lite-executor.md`.
- If `RUN/lite-summary.md` already exists and is fresh relative to
  `RUN/task-profile.md` and `RUN/user-input.md`, report it instead of
  dispatching again.
- If ambiguity remains, return `RUN/questions/lite-questions.md` and wait.
- The executor may read relevant project files, make the requested bounded
  change, run targeted verification, and write `RUN/lite-summary.md`.
- It must not create proposal/design/task/prompt files.
- It must not run broad test suites unless needed for the changed files.
- For non-code tasks, do not run pytest, mypy, or ruff unless the user asked or
  the task touches Python code.
- Completion requires `RUN/lite-summary.md` with changed files, verification,
  and residual risk.

## Standard Flow

Goal: align first, then execute a moderate task without full Spec-Full overhead.

Rules:

- Run Stage 1 and Stage 2 exactly, including explicit approvals.
- After design approval, dispatch `agents/standard-executor.md`.
- If `RUN/standard-summary.md` already exists and is fresh relative to
  `RUN/task-profile.md`, `RUN/doc/proposal.md`, and
  `RUN/doc/high-level-design.md`, report it instead of dispatching again.
- If ambiguity remains, return `RUN/questions/standard-questions.md` and wait.
- The executor writes `RUN/standard-summary.md`.
- It must not create `RUN/doc/detailed-design.md`, `RUN/doc/tasks/*`,
  `RUN/doc/prompt.md`, `RUN/spec.md`, or `RUN/plan/task-NNN/task.md`.
- It should implement in one to three small steps, verifying after each step.
- It may run targeted tests and quality checks relevant to changed files. It
  runs full pytest/mypy/ruff only when Python code changes require that level
  of confidence or the user explicitly asks.
- Do not run broad test suites unless the approved design or changed files
  require them.
- If work expands beyond three steps, touches more than five files, or needs
  long-running automation, write `RUN/execution-budget.md` and ask whether to
  promote to `spec-full`.

## Spec-Full Flow

## Stage 1: Proposal

Goal: create `RUN/doc/proposal.md`.

Rules:

- Dispatch `agents/proposal-writer.md`.
- If requirements are unclear, it writes
  `RUN/questions/proposal-questions.md`; return those questions and wait.
- Review with `agents/proposal-reviewer.md`.
- Loop writer and reviewer until
  `RUN/reviews/proposal-review-results.md` has zero `Status: Pending`.
- Return the reviewed proposal path and wait for explicit approval.
- Only after approval that names the document or stage, write
  `RUN/approvals/proposal-approved.md`.
- Do not create design content in this stage.

The proposal must contain goal, project context, inputs, outputs, functional and
non-functional requirements, non-goals, constraints, acceptance criteria, and
open questions only if explicitly left open by the user.

## Stage 2: High-Level Design

Goal: create `RUN/doc/high-level-design.md`.

Rules:

- Stage 2 starts only after proposal review has zero pending issues and
  `RUN/approvals/proposal-approved.md` is fresh.
- Dispatch `agents/design-writer.md`.
- If design-affecting ambiguity remains, it writes
  `RUN/questions/design-questions.md`; return those questions and wait.
- Review with `agents/design-reviewer.md`.
- Loop writer and reviewer until `RUN/reviews/design-review-results.md` has
  zero `Status: Pending`.
- Return the reviewed high-level design path and wait for explicit approval.
- Only after approval that names the document or stage, write
  `RUN/approvals/design-approved.md`.
- Do not create detailed design, task files, prompt, or implementation in this
  stage.

## Stage 3: Detailed Design

Goal: create `RUN/doc/detailed-design.md`.

Rules:

- Stage 3 starts only after Stage 1 and Stage 2 are reviewed and approved.
- Dispatch `agents/detailed-design-writer.md`.
- If ambiguity remains, it writes
  `RUN/questions/detailed-design-questions.md`; return those questions and wait.
- Review with `agents/detailed-design-reviewer.md`.
- Loop writer and reviewer until
  `RUN/reviews/detailed-design-review-results.md` has zero `Status: Pending`.
- Continue automatically to Stage 4.
- Do not create task files, prompt, or implementation in this stage.

## Stage 4: Module Tasks

Goal: create:

- `RUN/doc/tasks/<module-name>.md` for every module.
- `RUN/doc/tasks/progress.md`.

Rules:

- Dispatch `agents/task-writer.md`.
- If task-splitting ambiguity remains, it writes
  `RUN/questions/task-questions.md`; return those questions and wait.
- Review with `agents/task-reviewer.md`.
- Loop writer and reviewer until `RUN/reviews/task-review-results.md` has zero
  `Status: Pending`.
- Continue automatically to Stage 5.
- Module task files and progress must use checklists.

## Stage 5: VibeCoding Prompt

Goal: create `RUN/doc/prompt.md`.

Rules:

- Dispatch `agents/prompt-writer.md`.
- If prompt-generation ambiguity remains, it writes
  `RUN/questions/prompt-questions.md`; return those questions and wait.
- Review with `agents/prompt-reviewer.md`.
- Loop writer and reviewer until `RUN/reviews/prompt-review-results.md` has
  zero `Status: Pending`.
- Continue automatically to Stage 6.

`prompt.md` must instruct the future execution agent to read all run-scoped doc
files, track `progress.md`, dispatch or spawn module subagents when available,
run complete pytest unit tests for Python projects, run mypy and ruff for Python
projects, treat skipped tests and failed checks as blockers, and continue
without human participation after execution starts except for real blockers.

## Stage 6: Execute Prompt

Goal: execute `RUN/doc/prompt.md` hands-off.

Stage 6 uses the bundled upstream Superteam snapshot as an internal execution
engine:

1. Dispatch `agents/spec-writer.md` to synthesize `RUN/spec.md` from
   `RUN/doc/proposal.md`, `RUN/doc/high-level-design.md`,
   `RUN/doc/detailed-design.md`, `RUN/doc/tasks/`, and `RUN/doc/prompt.md`.
2. Dispatch `agents/planner.md` to create internal executable tasks under
   `RUN/plan/task-NNN/task.md`.
3. Dispatch `agents/plan-reviewer.md`; loop until zero `Status: Pending` or the
   planning runtime budget is hit.
4. Execute internal tasks serially with `agents/implementer.md`.
5. After each task, run `agents/spec-reviewer.md` and
   `agents/code-reviewer.md` serially. Never run them in parallel because they
   share `implement-review-results.md`.
6. Fix every `Status: Pending` issue and review again within the runtime
   budget.

Default unattended planning budget:

- Maximum three planner/plan-reviewer cycles.
- Maximum six internal task files before execution starts.

Default unattended execution budget:

- Maximum three full implementer -> spec-reviewer -> code-reviewer cycles per
  internal task.

When a budget is exceeded, stop and write the relevant guard file:

- `RUN/execution-budget.md`
- `RUN/plan/task-NNN/loop-issues.md`

Large-plan execution resumes only after explicit approval such as
`OK long run`; the controller then writes `RUN/execution-approved.md`.

## Superteam Compatibility

The complete upstream Superteam snapshot is preserved under
`references/upstream-superteam/` at commit
`8123472865985477fb49841f93ca1c8782e4781d`.

SuperHUA must treat these files as the canonical Stage 6 execution behavior:

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

- Stages 1-5 must run before upstream planning/execution.
- Upstream root `working/*` examples map to the selected `RUN` paths.
- `RUN/doc/prompt.md` is the Stage 6 execution charter.
- `agents/spec-writer.md` synthesizes internal `RUN/spec.md`.
- `RUN/task-issues.md` replaces upstream `working/plan-issues.md`.
- Do not use the upstream Claude plugin namespace.
- Do not make commits unless the user explicitly asks.

## Supporting Files

- `references/workflow.md`: full file contracts and exact prompt formats.
- `agents/task-router.md`
- `agents/lite-executor.md`, `agents/standard-executor.md`
- `agents/proposal-writer.md`, `agents/proposal-reviewer.md`
- `agents/design-writer.md`, `agents/design-reviewer.md`
- `agents/detailed-design-writer.md`, `agents/detailed-design-reviewer.md`
- `agents/task-writer.md`, `agents/task-reviewer.md`
- `agents/prompt-writer.md`, `agents/prompt-reviewer.md`
- `agents/spec-writer.md`
- `agents/planner.md`, `agents/plan-reviewer.md`
- `agents/implementer.md`, `agents/spec-reviewer.md`,
  `agents/code-reviewer.md`

## Common Mistakes

- Treating SuperHUA as always-heavy. Route first; use the lightest safe mode.
- Running research without an evidence cap.
- Treating Stage 3-5 as "automatic, no questions allowed." They are automatic
  only when the source documents are clear.
- Replacing `RUN/doc/tasks/*.md` with internal `RUN/plan/task-NNN/task.md`.
- Executing before `RUN/doc/prompt.md` exists and has zero pending review
  issues.
- Skipping pytest, mypy, ruff, coverage, or review loops.
