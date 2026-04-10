# Codex Planning Pack Rules

This document defines the first-party rules for the Codex-native planning and review pack.

## Purpose

These skills exist to help Codex move from vague intent to decision-complete implementation
plans without importing a third-party runtime or state system.

## Collaboration Mode Contract

Codex planning skills must be mode-aware.

- A skill cannot switch the Codex collaboration mode by itself.
- If the current session is in Default mode, the skill may guide the user to enter Plan Mode,
  but it must not pretend that the mode already changed.
- If the current session is in Plan Mode, the skill can use interactive planning behavior and
  plan-only output conventions such as `<proposed_plan>`.
- If the task is still answerable in one pass while in Default mode, prefer a compact
  non-interactive brief or plan over blocking.

## Default Mode Behavior

- Detect whether the task truly needs back-and-forth planning.
- If yes, tell the user to switch to Plan Mode with `Shift+Tab`, then re-run the skill.
- If no, return a compact brief or draft plan in one response.
- Never claim that the skill can toggle Plan Mode automatically.

## Plan Mode Behavior

- Ask the missing high-impact questions.
- Drive the task toward a decision-complete plan or scoped brief.
- End with a concrete next step.
- When the output is a finalized implementation plan, use a `<proposed_plan>` block.

## Authoring Rules

- Author skills directly in `plugins/codex-env-core/skills/`.
- Do not depend on vendored upstream runtimes, custom daemons, or hidden state folders.
- Prefer repo context, committed docs, and the active conversation over sidecar metadata.
- Each skill should state:
  - when to use it
  - what inputs it expects
  - what output shape it produces
  - what the next handoff step is
- If a skill refers to files, prefer repo-visible documents such as `README.md`,
  `AGENTS.md`, plan docs, or explicit user-provided paths.

## Output Rules

- `codex-office-hours` outputs a scoped brief.
- `codex-plan-review` outputs findings plus a revised decision-complete plan.
- `codex-autoplan` orchestrates the pack and produces a single consolidated next-action result.

## Boundaries

- No self-update flow.
- No telemetry onboarding.
- No team-mode bootstrap.
- No hidden home-directory state contract that a fresh checkout cannot infer.
- No requirement for an external browser/design runtime just to use the planning pack.
- No fake mode switching. Plan Mode guidance is explicit user-facing routing, not an implicit state change.
