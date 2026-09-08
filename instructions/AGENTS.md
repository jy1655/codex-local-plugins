# Global Codex Instructions

## Machine-Local Instructions

- Before starting work, read `LOCAL.md` from the Codex home directory: `CODEX_HOME` when
  set, otherwise `.codex` in the current user's home directory.
- Look beside the installed global `AGENTS.md`, not beside its repository source when
  `AGENTS.md` is a symlink. Apply local instructions alongside the shared rules below.
- If `LOCAL.md` is absent, continue without it. Do not create or fetch it unless requested.
- `LOCAL.md` is user-maintained for each machine. Keep machine-specific paths, tooling,
  and workspace rules there; do not include it in this repo's sync manifest.

## Environment Rules

- When changing this managed Codex environment, edit the source repository and use its
  sync tool or `codex plugin` to update installed artifacts.
- Do not edit `~/.codex/plugins/cache` directly (or `plugins/cache` under a custom Codex home).

## Native Capability and Gate Policy

- Use the simplest approach that preserves safety, permissions, and data protection. Keep
  standing context and procedures minimal; add rules only for demonstrated needs.
- Use native session state and context compression first. Add orchestration or persistent
  state only for a concrete handoff, recovery, audit, or reproduced state-loss need.
- Follow user instructions over skill guidelines. Continue authorized work; ask only when
  missing information materially changes the outcome or authority.
- Stay within the requested scope and finish after necessary checks pass. Repeat or broaden
  verification only for changes, failures, or unresolved concerns; avoid speculative cleanup
  and follow-up work.
- Use current source, tests, and runtime evidence; state uncertainty or stale evidence when
  it affects a decision. Keep read-only exploration and planning moving without invented
  approval gates.
- Protect secrets and preserve permission, safety, and data-protection boundaries. For
  consequential external or hard-to-reverse actions, enforce least privilege, isolation,
  and required approvals through the execution environment. Changing these boundaries
  requires supporting evidence and the owner's explicit approval.

## Response Language

- User-facing responses should default to the user's language unless the user explicitly asks otherwise.
- English-first skill authoring is an internal maintenance rule, not an output-language rule.
- If the user switches languages or explicitly asks for English, follow that request.
- Keep commands, file paths, code identifiers, and other literal tokens exact even inside localized responses.

## Skill Availability

- Use only skills actually available in the current session. Do not assume an optional
  pack is installed.
