# SuperHUA Workflow Reference

## Origin

Source idea: `abadcafe/superteam`, cloned from
`https://github.com/abadcafe/superteam` at commit
`8123472865985477fb49841f93ca1c8782e4781d`.

Codex adaptation:

- Skill name: `superhua`.
- Claude plugin namespace references were removed.
- The user's manual VibeCoding preparation chain is preserved as
  `proposal -> high-level-design -> detailed-design -> module tasks -> prompt`.
- All process files are scoped to a SuperHUA run directory so multiple tasks can
  coexist in one project repository.
- Stage 1 and Stage 2 require explicit human approval after review.
- Stages 3-5 are question-gated but do not require approval markers.
- Stage 6 uses upstream Superteam planning/execution as the internal engine.
- Commits are not made unless the user asks.

## Run Scope

Define:

```text
RUN = working/superhua-runs/<run-id>
```

`<run-id>` is `YYYYMMDD-HHMM-<short-slug>` derived from the task goal. The slug
must be lowercase ASCII, hyphen-separated, and short enough to scan.

Controller-owned project-level files:

- `working/superhua-current.md`: current run id and run directory.
- `working/superhua-index.md`: append-only index of run ids, goals, status,
  created time, and run directories.

Run selection rules:

- If the user starts a new SuperHUA task, create a new `RUN`.
- If the user continues a task and `working/superhua-current.md` points to one
  existing run, use that run.
- If the user continues a task and multiple runs exist without a clear current
  run, list run ids from `working/superhua-index.md` and ask the user to choose.
- If legacy root files such as `proposal.md`, root `doc/`, or root
  `working/plan/` exist outside `working/superhua-runs/`, report them as legacy
  state. Do not treat them as the selected run and do not overwrite them.
- Project code changes still happen in the project root. Only SuperHUA process
  files live under `RUN`.

## File Contracts

Human-visible deliverables:

- `RUN/doc/proposal.md`: requirements document.
- `RUN/doc/high-level-design.md`: module-level design.
- `RUN/doc/detailed-design.md`: detailed design.
- `RUN/doc/tasks/<module-name>.md`: one module task checklist per module.
- `RUN/doc/tasks/progress.md`: module progress checklist.
- `RUN/doc/prompt.md`: VibeCoding execution prompt.

Questions:

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

- `RUN/approvals/proposal-approved.md`
- `RUN/approvals/design-approved.md`
- `RUN/runtime-metrics.md`
- `RUN/spec.md`
- `RUN/plan/task-NNN/task.md`
- `RUN/plan/task-NNN/test-results.md`
- `RUN/plan/task-NNN/changes.md`
- `RUN/spec-issues.md`
- `RUN/task-issues.md`
- `RUN/env-issues.md`
- `RUN/execution-budget.md`
- `RUN/execution-approved.md`
- `RUN/plan/task-NNN/loop-issues.md`
- `RUN/commit-message.md`
- `RUN/task-summary.md`

SuperHUA standardizes on `RUN/task-issues.md` for task-document problems. Some
upstream Superteam text used `working/plan-issues.md`; agents must not create
or read `working/plan-issues.md` in SuperHUA.

## Agent Prompt Formats

Dispatch prompts must contain only the relevant prompt-file path and file-path
metadata. Do not include summaries, advice, copied requirements, or chat
history. The fresh agent must read files from disk. In the templates below,
replace `RUN` with the concrete selected run directory, for example
`working/superhua-runs/20260602-1430-3-2-refactor`.

### proposal-writer

```text
- Prompt file: C:/Users/HUA/.codex/skills/superhua/agents/proposal-writer.md
- Run id: <run-id>
- Run directory: RUN
- User input path: RUN/user-input.md
- Proposal path: RUN/doc/proposal.md
- Questions path: RUN/questions/proposal-questions.md
- Review results path: RUN/reviews/proposal-review-results.md
```

### proposal-reviewer

```text
- Prompt file: C:/Users/HUA/.codex/skills/superhua/agents/proposal-reviewer.md
- Run id: <run-id>
- Run directory: RUN
- User input path: RUN/user-input.md
- Proposal path: RUN/doc/proposal.md
- Review results path: RUN/reviews/proposal-review-results.md
```

### design-writer

```text
- Prompt file: C:/Users/HUA/.codex/skills/superhua/agents/design-writer.md
- Run id: <run-id>
- Run directory: RUN
- User input path: RUN/user-input.md
- Proposal path: RUN/doc/proposal.md
- Design path: RUN/doc/high-level-design.md
- Questions path: RUN/questions/design-questions.md
- Review results path: RUN/reviews/design-review-results.md
```

### design-reviewer

```text
- Prompt file: C:/Users/HUA/.codex/skills/superhua/agents/design-reviewer.md
- Run id: <run-id>
- Run directory: RUN
- Proposal path: RUN/doc/proposal.md
- Design path: RUN/doc/high-level-design.md
- Review results path: RUN/reviews/design-review-results.md
```

### detailed-design-writer

```text
- Prompt file: C:/Users/HUA/.codex/skills/superhua/agents/detailed-design-writer.md
- Run id: <run-id>
- Run directory: RUN
- User input path: RUN/user-input.md
- Proposal path: RUN/doc/proposal.md
- High-level design path: RUN/doc/high-level-design.md
- Detailed design path: RUN/doc/detailed-design.md
- Questions path: RUN/questions/detailed-design-questions.md
- Review results path: RUN/reviews/detailed-design-review-results.md
```

### detailed-design-reviewer

```text
- Prompt file: C:/Users/HUA/.codex/skills/superhua/agents/detailed-design-reviewer.md
- Run id: <run-id>
- Run directory: RUN
- Proposal path: RUN/doc/proposal.md
- High-level design path: RUN/doc/high-level-design.md
- Detailed design path: RUN/doc/detailed-design.md
- Review results path: RUN/reviews/detailed-design-review-results.md
```

### task-writer

```text
- Prompt file: C:/Users/HUA/.codex/skills/superhua/agents/task-writer.md
- Run id: <run-id>
- Run directory: RUN
- User input path: RUN/user-input.md
- Proposal path: RUN/doc/proposal.md
- High-level design path: RUN/doc/high-level-design.md
- Detailed design path: RUN/doc/detailed-design.md
- Task directory: RUN/doc/tasks/
- Progress path: RUN/doc/tasks/progress.md
- Questions path: RUN/questions/task-questions.md
- Review results path: RUN/reviews/task-review-results.md
```

### task-reviewer

```text
- Prompt file: C:/Users/HUA/.codex/skills/superhua/agents/task-reviewer.md
- Run id: <run-id>
- Run directory: RUN
- Proposal path: RUN/doc/proposal.md
- High-level design path: RUN/doc/high-level-design.md
- Detailed design path: RUN/doc/detailed-design.md
- Task directory: RUN/doc/tasks/
- Progress path: RUN/doc/tasks/progress.md
- Review results path: RUN/reviews/task-review-results.md
```

### prompt-writer

```text
- Prompt file: C:/Users/HUA/.codex/skills/superhua/agents/prompt-writer.md
- Run id: <run-id>
- Run directory: RUN
- User input path: RUN/user-input.md
- Proposal path: RUN/doc/proposal.md
- High-level design path: RUN/doc/high-level-design.md
- Detailed design path: RUN/doc/detailed-design.md
- Task directory: RUN/doc/tasks/
- Progress path: RUN/doc/tasks/progress.md
- Prompt path: RUN/doc/prompt.md
- Questions path: RUN/questions/prompt-questions.md
- Review results path: RUN/reviews/prompt-review-results.md
```

### prompt-reviewer

```text
- Prompt file: C:/Users/HUA/.codex/skills/superhua/agents/prompt-reviewer.md
- Run id: <run-id>
- Run directory: RUN
- Proposal path: RUN/doc/proposal.md
- High-level design path: RUN/doc/high-level-design.md
- Detailed design path: RUN/doc/detailed-design.md
- Task directory: RUN/doc/tasks/
- Progress path: RUN/doc/tasks/progress.md
- Prompt path: RUN/doc/prompt.md
- Review results path: RUN/reviews/prompt-review-results.md
```

### spec-writer

```text
- Prompt file: C:/Users/HUA/.codex/skills/superhua/agents/spec-writer.md
- Run id: <run-id>
- Run directory: RUN
- Proposal path: RUN/doc/proposal.md
- Design path: RUN/doc/high-level-design.md
- Detailed design path: RUN/doc/detailed-design.md
- Task directory: RUN/doc/tasks/
- Progress path: RUN/doc/tasks/progress.md
- Prompt path: RUN/doc/prompt.md
- Spec path: RUN/spec.md
- Spec issues path: RUN/spec-issues.md
```

### planner

```text
- Prompt file: C:/Users/HUA/.codex/skills/superhua/agents/planner.md
- Upstream contract path: C:/Users/HUA/.codex/skills/superhua/references/upstream-superteam/agents/planner.md
- Upstream planning skill path: C:/Users/HUA/.codex/skills/superhua/references/upstream-superteam/skills/planning/SKILL.md
- Upstream black-box testing path: C:/Users/HUA/.codex/skills/superhua/references/upstream-superteam/skills/black-box-testing/SKILL.md
- Upstream issue handling path: C:/Users/HUA/.codex/skills/superhua/references/upstream-superteam/skills/hands-off-issue-handling/SKILL.md
- Run id: <run-id>
- Run directory: RUN
- Proposal path: RUN/doc/proposal.md
- Design path: RUN/doc/high-level-design.md
- Detailed design path: RUN/doc/detailed-design.md
- Task directory: RUN/doc/tasks/
- Progress path: RUN/doc/tasks/progress.md
- Prompt path: RUN/doc/prompt.md
- Spec path: RUN/spec.md
- Plan directory: RUN/plan/
- Review results path: RUN/plan-review-results.md
- Task issues path: RUN/task-issues.md
- Spec issues path: RUN/spec-issues.md
```

### plan-reviewer

```text
- Prompt file: C:/Users/HUA/.codex/skills/superhua/agents/plan-reviewer.md
- Upstream contract path: C:/Users/HUA/.codex/skills/superhua/references/upstream-superteam/agents/plan-reviewer.md
- Upstream planning skill path: C:/Users/HUA/.codex/skills/superhua/references/upstream-superteam/skills/planning/SKILL.md
- Upstream black-box testing path: C:/Users/HUA/.codex/skills/superhua/references/upstream-superteam/skills/black-box-testing/SKILL.md
- Run id: <run-id>
- Run directory: RUN
- Proposal path: RUN/doc/proposal.md
- Design path: RUN/doc/high-level-design.md
- Detailed design path: RUN/doc/detailed-design.md
- Task directory: RUN/doc/tasks/
- Progress path: RUN/doc/tasks/progress.md
- Prompt path: RUN/doc/prompt.md
- Spec path: RUN/spec.md
- Plan directory: RUN/plan/
- Review results path: RUN/plan-review-results.md
- Task issues path: RUN/task-issues.md
```

### implementer

```text
- Prompt file: C:/Users/HUA/.codex/skills/superhua/agents/implementer.md
- Upstream contract path: C:/Users/HUA/.codex/skills/superhua/references/upstream-superteam/agents/implementer.md
- Upstream executing skill path: C:/Users/HUA/.codex/skills/superhua/references/upstream-superteam/skills/executing/SKILL.md
- Upstream black-box testing path: C:/Users/HUA/.codex/skills/superhua/references/upstream-superteam/skills/black-box-testing/SKILL.md
- Upstream issue handling path: C:/Users/HUA/.codex/skills/superhua/references/upstream-superteam/skills/hands-off-issue-handling/SKILL.md
- Run id: <run-id>
- Run directory: RUN
- Task number: NNN
- Task directory: RUN/plan/task-NNN/
- Task file: RUN/plan/task-NNN/task.md
- Task issues path: RUN/task-issues.md
- Environment issues path: RUN/env-issues.md
```

### spec-reviewer

```text
- Prompt file: C:/Users/HUA/.codex/skills/superhua/agents/spec-reviewer.md
- Upstream contract path: C:/Users/HUA/.codex/skills/superhua/references/upstream-superteam/agents/spec-reviewer.md
- Upstream executing skill path: C:/Users/HUA/.codex/skills/superhua/references/upstream-superteam/skills/executing/SKILL.md
- Upstream black-box testing path: C:/Users/HUA/.codex/skills/superhua/references/upstream-superteam/skills/black-box-testing/SKILL.md
- Run id: <run-id>
- Run directory: RUN
- Task number: NNN
- Task directory: RUN/plan/task-NNN/
- Task file: RUN/plan/task-NNN/task.md
- Proposal path: RUN/doc/proposal.md
- Design path: RUN/doc/high-level-design.md
- Detailed design path: RUN/doc/detailed-design.md
- Prompt path: RUN/doc/prompt.md
- Spec path: RUN/spec.md
- Task issues path: RUN/task-issues.md
```

### code-reviewer

```text
- Prompt file: C:/Users/HUA/.codex/skills/superhua/agents/code-reviewer.md
- Upstream contract path: C:/Users/HUA/.codex/skills/superhua/references/upstream-superteam/agents/code-reviewer.md
- Upstream executing skill path: C:/Users/HUA/.codex/skills/superhua/references/upstream-superteam/skills/executing/SKILL.md
- Upstream black-box testing path: C:/Users/HUA/.codex/skills/superhua/references/upstream-superteam/skills/black-box-testing/SKILL.md
- Run id: <run-id>
- Run directory: RUN
- Task number: NNN
- Task directory: RUN/plan/task-NNN/
- Task file: RUN/plan/task-NNN/task.md
- Proposal path: RUN/doc/proposal.md
- Design path: RUN/doc/high-level-design.md
- Detailed design path: RUN/doc/detailed-design.md
- Prompt path: RUN/doc/prompt.md
- Spec path: RUN/spec.md
- Task issues path: RUN/task-issues.md
```

## State Machine Rules

On every state transition, the controller emits:

```text
I am a SuperHUA state machine. I do not write deliverables in the main window. I dispatch fresh agents and read files.
```

The controller checks files with file probes only. Chat output from an agent is
not a state signal.

NEVER:

- Skip, combine, or reorder stages.
- Fix, verify, review, plan, design, prompt-write, or implement in the main
  window.
- Add extra content to agent prompts beyond the exact prompt formats above.
- Treat agent review success as human approval.
- Treat a generic "continue" as approval for proposal or high-level design.
- Treat stale approval markers as valid after the document or review file has
  changed.
- Dispatch spec-reviewer and code-reviewer in parallel; they share one output
  file and must run serially.
- Start a fourth full implementation review cycle for the same task without
  explicit user approval.

## Stage Checks

### Stage 1: Proposal

1. Select or create `RUN`; maintain `working/superhua-current.md` and
   `working/superhua-index.md`.
2. If `RUN/user-input.md` is missing, create it from the user's exact request.
3. Dispatch proposal-writer.
4. If `RUN/questions/proposal-questions.md` exists and is non-empty, return it
   and wait.
5. Dispatch proposal-reviewer when `RUN/doc/proposal.md` exists.
6. Count `Status: Pending` in `RUN/reviews/proposal-review-results.md`.
7. Repeat writer/reviewer until zero pending issues.
8. If `RUN/approvals/proposal-approved.md` is missing or stale relative to the
   proposal or review file, return the reviewed proposal path and wait.
9. Only explicit approval naming the proposal/stage writes
   `RUN/approvals/proposal-approved.md`.

### Stage 2: High-Level Design

1. Require fresh proposal approval and zero pending proposal review issues.
2. Dispatch design-writer.
3. If `RUN/questions/design-questions.md` exists and is non-empty, return it and
   wait.
4. Dispatch design-reviewer when `RUN/doc/high-level-design.md` exists.
5. Count `Status: Pending` in `RUN/reviews/design-review-results.md`.
6. Repeat writer/reviewer until zero pending issues.
7. If `RUN/approvals/design-approved.md` is missing or stale relative to the
   design or review file, return the reviewed high-level design path and wait.
8. Only explicit approval naming the design/stage writes
   `RUN/approvals/design-approved.md`.

### Stage 3: Detailed Design

1. Require fresh proposal and design approvals and zero pending proposal/design
   review issues.
2. Dispatch detailed-design-writer.
3. If `RUN/questions/detailed-design-questions.md` exists and is non-empty,
   return it and wait.
4. Dispatch detailed-design-reviewer when `RUN/doc/detailed-design.md` exists.
5. Count `Status: Pending` in
   `RUN/reviews/detailed-design-review-results.md`.
6. Repeat writer/reviewer until zero pending issues, then continue to Stage 4.

### Stage 4: Module Tasks

1. Require `RUN/doc/detailed-design.md` and zero pending detailed-design review
   issues.
2. Dispatch task-writer.
3. If `RUN/questions/task-questions.md` exists and is non-empty, return it and
   wait.
4. Dispatch task-reviewer when `RUN/doc/tasks/progress.md` exists and module
   task files exist.
5. Count `Status: Pending` in `RUN/reviews/task-review-results.md`.
6. Repeat writer/reviewer until zero pending issues, then continue to Stage 5.

### Stage 5: Prompt

1. Require zero pending task review issues.
2. Dispatch prompt-writer.
3. If `RUN/questions/prompt-questions.md` exists and is non-empty, return it and
   wait.
4. Dispatch prompt-reviewer when `RUN/doc/prompt.md` exists.
5. Count `Status: Pending` in `RUN/reviews/prompt-review-results.md`.
6. Repeat writer/reviewer until zero pending issues, then continue to Stage 6.

### Stage 6: Execute Prompt

1. Require `RUN/doc/prompt.md` and zero pending prompt review issues.
2. Dispatch spec-writer if `RUN/spec.md` is missing or stale relative to any
   Stage 1-5 deliverable.
3. Dispatch planner.
4. Dispatch plan-reviewer.
5. Count `Status: Pending` in `RUN/plan-review-results.md`.
6. Repeat planner/plan-reviewer until zero pending issues or three cycles.
7. If pending issues remain after three cycles, write
   `RUN/execution-budget.md` and stop.
8. Count internal tasks matching `RUN/plan/task-NNN/task.md`.
9. If the task count is greater than six, write `RUN/execution-budget.md` and
   wait for explicit `OK long run`; then write `RUN/execution-approved.md`.
10. Execute each internal task in numeric order with implementer.
11. Require `RUN/plan/task-NNN/test-results.md` and
    `RUN/plan/task-NNN/changes.md`.
12. If test status is not `EXPECTED`, retry implementer within the three-cycle
    task budget or write `RUN/plan/task-NNN/loop-issues.md`.
13. Dispatch spec-reviewer, then code-reviewer, serially.
14. Count `Status: Pending` in
    `RUN/plan/task-NNN/implement-review-results.md`.
15. Retry implementer/reviewers until zero pending issues or the three-cycle
    task budget is exceeded.
16. After the last task, write `RUN/commit-message.md` and
    `RUN/task-summary.md` through the controller using only file outputs.

## Prompt Contracts

Question responses must quote the relevant questions file contents and then
wait. The main controller never invents questions.

Approval responses:

```text
RUN/doc/proposal.md is reviewed with zero pending issues.
Please approve the requirements document before I enter Stage 2.
Accepted approvals: OK proposal, approve proposal, 确认需求文档.
```

```text
RUN/doc/high-level-design.md is reviewed with zero pending issues.
Please approve the high-level design before I enter Stage 3.
Accepted approvals: OK design, approve design, 确认概要设计.
```

Runtime guard files:

```text
RUN/execution-budget.md
RUN/plan/task-NNN/loop-issues.md
```

Repeated-review loops do not auto-resume. The user must inspect the loop issue
and explicitly direct the next action.
