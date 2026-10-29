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
- Install or update the Agent Bridge plugin (`agent-bridge@agent-bridge`) only with
  `scripts/update-agent-bridge-plugins.sh` (`.ps1` on Windows) in the claude-local-plugins clone
  that `~/.claude/CLAUDE.md` points to; it installs the verified latest tabcli release archive
  for Claude Code and Codex. Run it right after installing a new `tabcli` binary. Without that
  clone, follow "Release archives" in tabcli's `docs/integrations.md`. Never add a tabcli source
  checkout as the marketplace; a checkout catalog carries unreleased skill text.

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

## Verification Artifacts

- Create internal verification directories through `python3 ~/.codex/tools/task-workspace.py
  create --purpose verification --name <task>` (use the installed Codex home and available
  Python interpreter). Pass the returned path to shell, browser and download tools. The
  default is an OS temporary directory; `output/` is for deliverables. Use `--path <path>
  --user-selected-path` only when the user explicitly selected that destination.
- Before cleanup, run the helper's `inventory`, classify each file, and preserve eligible
  evidence in the configured Wiki under its policy. `classify --disposition wiki` requires
  a separately fetched Wiki `--readback` whose byte size and SHA-256 match, plus `--wiki-path`.
  Use `discard` only for task-owned reproducible or unnecessary files, and `keep` only for
  a user-requested or policy-required retained original, with its reason. Do not copy
  credentials, prohibited content or binary originals excluded by Wiki policy.
- Completion includes verified evidence storage and disposition of remaining task files,
  not just a summary or passing tests. Remove only classified task-owned disposable or
  already-preserved copies, then run `finish`; it lists unclassified, changed and pending
  files and never deletes them. Save the necessary receipt in the Wiki, verify it, and
  remove the temporary helper metadata and empty directory. Unavailable Wiki storage or
  unresolved retention leaves cleanup incomplete: retain the files and report the gap.

## Response Language

- User-facing responses should default to the user's language unless the user explicitly asks otherwise.
- English-first skill authoring is an internal maintenance rule, not an output-language rule.
- Write model-facing `SKILL.md` instructions, trigger descriptions, and technical references
  in English. Keep user-visible plugin and skill names, descriptions, and suggested prompts
  in Korean, including `interface` fields in plugin manifests and `agents/openai.yaml`.
- Personal language, authorization, privacy, and workspace-preservation preferences apply
  independently of whether a workflow skill is installed.
- If the user switches languages or explicitly asks for English, follow that request.
- Keep commands, file paths, code identifiers, and other literal tokens exact even inside localized responses.

## Skill Availability

- Use only skills actually available in the current session. Do not assume an optional
  pack is installed.
