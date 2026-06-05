# Harness Adaptation for SuperHUA

SuperHUA borrows Harness's team-architecture ideas only as a routing and
orchestration decision layer. Do not import Harness's full team mode by
default; SuperHUA's main optimization is to avoid heavy process unless the task
needs it.

## Phase 0 Audit Matrix

Use this matrix during Stage 0 before selecting `vibe-lite`, `vibe-standard`,
or `spec-full`.

| Request shape | SuperHUA mode | Harness pattern | Invocation strategy |
| --- | --- | --- | --- |
| Known issue, known files, known checks | `vibe-lite` | `expert-pool` or `producer-reviewer` | `single-agent` |
| Small skill or documentation maintenance | `vibe-lite` | `expert-pool` | `single-agent` |
| One artifact needs generation plus objective review | `vibe-lite` | `producer-reviewer` | `serial-review-loop` only if the review is necessary |
| Independent inspection from several viewpoints | `vibe-lite` or `vibe-standard` | `fan-out-fan-in` | `parallel-subagents` with a bounded fan-in summary |
| Requirements, architecture, or acceptance criteria need user alignment | `vibe-standard` | `pipeline` | `serial-review-loop` |
| Multi-module implementation with dependent tasks | `spec-full` | `pipeline` or `supervisor` | `full-superteam` |
| Broad research synthesis | `spec-full` unless explicitly capped small | `fan-out-fan-in` | `parallel-subagents`, then `full-superteam` only if implementation follows |
| Dynamic large task distribution | `spec-full` | `supervisor` | `full-superteam` |

## Pattern Mapping

| Harness pattern | SuperHUA meaning |
| --- | --- |
| `pipeline` | Sequential stages where each output depends on the previous one. Use for proposal/design/spec-full flows, not simple patches. |
| `fan-out-fan-in` | Independent agents inspect different slices, then one bounded summary integrates results. Use only when parallel viewpoints add value. |
| `expert-pool` | Router selects one specialist for the current input. This is the preferred shape for small skill maintenance. |
| `producer-reviewer` | A creator and reviewer pair. Use when the artifact needs objective review; avoid it for trivial edits with direct tests. |
| `supervisor` | A coordinator assigns many runtime tasks. Use only inside `spec-full` or explicit long-running work. |
| `hierarchical` | Recursive delegation. Avoid by default; flatten to a single team or `spec-full` because nested delegation increases latency and context loss. |
| `none` | No Harness pattern is needed; direct execution is cheaper. |

## Invocation Strategies

- `single-agent`: one fresh executor performs the work and targeted checks.
  Default for `vibe-lite`.
- `parallel-subagents`: independent bounded agents run in parallel, then the
  controller reads file outputs and writes no deliverables. Use only when each
  branch has a disjoint question or file scope.
- `serial-review-loop`: writer/reviewer or producer/reviewer loop. Use only
  when objective review catches meaningful risk.
- `full-superteam`: preserved upstream Superteam-compatible planning and
  execution path. Use only for `spec-full`.

## Task Profile Fields

`RUN/task-profile.md` should include these fields under `## Task Type` or
`## Mode Bounds`:

```markdown
- Harness pattern: pipeline|fan-out-fan-in|expert-pool|producer-reviewer|supervisor|hierarchical|none
- Invocation strategy: single-agent|parallel-subagents|serial-review-loop|full-superteam
```

The selected Harness pattern must justify the selected SuperHUA mode. If the
pattern suggests more coordination than the mode allows, choose the lighter
safe alternative or ask the user before promoting.

## Anti-Overhead Rules

- Do not choose `vibe-standard` just because two agents could review each
  other. Prefer direct tests or a single executor when the task is known.
- Do not choose `fan-out-fan-in` for edits touching the same files; it creates
  merge overhead without adding useful independence.
- Do not choose `supervisor` or `hierarchical` for skill maintenance.
- Do not create extra agents or skills as outputs of SuperHUA unless the user
  explicitly asks for a new harness or team architecture.
- If the user complains about time, tokens, or says "half hour", "quick",
  "小任务", "轻量", or "别跑重流程", bias to `vibe-lite` and
  `single-agent` unless there is a concrete safety reason not to.
