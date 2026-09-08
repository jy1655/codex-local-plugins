# Global Codex Instructions

This machine is managed by the portable Codex environment sync repo.

## Machine-Local Instructions

- Before starting work, read `LOCAL.md` from the Codex home directory: `CODEX_HOME` when
  set, otherwise `.codex` in the current user's home directory.
- Look beside the installed global `AGENTS.md`, not beside its repository source when
  `AGENTS.md` is a symlink. Apply local instructions alongside the shared rules below.
- If `LOCAL.md` is absent, continue without it. Do not create or fetch it unless requested.
- `LOCAL.md` is user-maintained for each machine. Keep machine-specific paths, tooling,
  and workspace rules there; do not include it in this repo's sync manifest.

## Environment Rules

- Treat `~/plugins`, `~/.agents/plugins/marketplace.json`, and `~/.codex/AGENTS.md` as the source-owned install surface.
- Do not edit `~/.codex/plugins/cache` directly.
- When changing this environment repo, prefer first-party plugin bundles committed here over
  live dependencies on upstream seed sources.
- Treat `plugins/jy-env-*/skills/` as the first-party skill source of truth.
- Restart Codex after apply if plugin or instruction changes are not visible yet.

## Native Capability and Gate Policy

- Optimize for maximum task performance with minimum standing context, routing, and procedural
  weight. Treat each added harness element as overhead that must earn its place with evidence.
- Start from the simplest baseline that preserves safety, permission, and data-protection
  boundaries. Do not retain a procedure merely because an older model needed it. Reintroduce
  only the smallest rule that addresses a repeated, reproducible failure.
- Before adding agent orchestration, task registries, checkpoints, planner state, or other
  scaffolding, first use available model- or API-native session state and context compression.
  Add external state only for a concrete boundary such as a new thread, another actor, an audit
  or recovery requirement, or reproduced state loss, and keep it to the smallest justified form.
- State the objective, required context, safety boundaries, and success criteria, then let the
  model choose the solution path. Do not force an unverified procedure as the default.
- Keep always-on context to the project purpose and durable constraints. Before adding more
  instructions or examples, improve the structure of tools and source material; load transient
  logs and one-off details only when the task needs them.
- Prefer direct feedback from tests, builds, and runtime readback. For costly or hard-to-reverse
  actions, enforce least privilege, isolation, and explicit approval at the system layer rather
  than relying on prompt text alone.
- Hard gates are for permissions, explicit approvals, secrets, irreversible or consequential
  external side effects, and non-negotiable safety or security invariants. Do not make
  read-only exploration, analysis, or planning wait for a mode switch or speculative completeness.
- Keep exploration and planning moving with the best available context. When currency affects a
  decision, label evidence `CURRENT`, `STALE`, `UNKNOWN`, or `NOT-VERIFIED`; prefer current source
  and runtime evidence, and use stale material as a search lead rather than present authority.
- Retain a harness element only when representative comparison shows measurable quality, cost,
  or safety improvement over the simpler baseline. Operational procedures may evolve, but a
  change to safety, permission, or data-protection boundaries requires separate evidence and the
  harness owner's explicit approval.

## Repo Rules

- This repo only stores the customized result.
- Upstream open source skills and company-shared skills are local-only seed material.
- If a skill is worth keeping, rebuild it here as a first-party plugin asset.
- Do not rebuild the repo around vendored third-party runtimes when a Codex-native first-party skill will do.

## Response Language

- User-facing responses should default to the user's language unless the user explicitly asks otherwise.
- English-first skill authoring is an internal maintenance rule, not an output-language rule.
- If the user switches languages or explicitly asks for English, follow that request.
- Keep commands, file paths, code identifiers, and other literal tokens exact even inside localized responses.

## Pack Model

- `jy-env-core` is the compact default pack.
- `jy-env-planning`, `jy-env-delivery`, `jy-env-audit`, and `jy-env-ios` are optional marketplace installs.
- Staging a plugin under `~/plugins` makes it installable; it does not activate its skills.
- Route through skills that are actually available in the current session. Do not assume an
  optional pack is installed.

## Necessity Gate

- Before defining a new task, skill, file, audit cycle, TODO/open issue/follow-up item, or speculative cleanup that the user did not explicitly request, classify it as `user-directed`, `reproducible`, or `evidenced`.
- Reject speculative padding such as broad cleanup, manufactured follow-up sections, and extra audit loops when there is no concrete problem evidence.
- If a final response keeps a follow-up/TODO/open issue section, include a concise `[necessity-gate]` block explaining the basis and decision.
