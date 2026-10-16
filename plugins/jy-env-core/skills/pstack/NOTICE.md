# Pstack port and removal boundary

This module adapts Lauren Tan's MIT-licensed pstack 0.15.25 from
[`cursor/plugins`](https://github.com/cursor/plugins/tree/f713f14203cd6420cec13cd7c55c32d598dbab68/pstack),
revision `f713f14203cd6420cec13cd7c55c32d598dbab68`, imported on 2026-10-16.
[LICENSE](LICENSE) retains the original copyright and permission notice.
[UPSTREAM.json](UPSTREAM.json) maps retained imports and explicitly excluded files to
their original paths and SHA-256 hashes. These hashes describe the input, not the modified port.

The user requested a local trial inside the existing plugin, removable as an internal
module. This is not a new plugin or marketplace. It adds one `$pstack` entry point to
`jy-env-core`; existing guardrails and jy-orchestrate remain independent.

## Included and adapted

- All 54 upstream skills, including 24 principles, 23 poteto-mode playbooks, both
  agent prompts, and their references are included. Internal
  SKILL.md files become WORKFLOW.md resources, so they do not register independently.
- The entry point preserves poteto-mode's explicit invocation policy using
  `agents/openai.yaml`. `$pstack <workflow> <task>` selects an individual workflow.
- Cursor Grok/Opus defaults become Codex Sol/Astra roles in references/default-models.json.
  Optional pstack-only models.json replaces an always-applied Cursor rule. The original
  starting budget and task-sensitive effort adjustments are retained using separate CLI
  options. Speed defaults to standard for every role, including urgent work and verification;
  no `-fast` variants or automatic priority requests. This is a two-model OpenAI panel,
  not original cross-provider equivalence.
- A shared runtime adapter maps delegation, questions, continuation, UI/CLI verification,
  history, and skill authoring to available Codex capabilities. Runtime-sensitive
  workflow sections are adapted, including setup, help, agents, history, and PR scope.
- Host permissions, user scope, workspace preservation, language, and managed-source
  rules take precedence. A local implementation does not automatically publish a PR.
  Reflect does not silently file external backlog tickets. Missing history is not proof
  that a worktree is unused; the audit emits `verify-usage` instead of `safe`.
- The upstream feature arena, architecture triggers, characterization-first refactoring,
  fresh-agent preference, comment-editing workflow, and strict multi-phase verification
  remain. They are not simplified to fit the existing guardrail skill.
- For this trial, jy-change-guardrails has `allow_implicit_invocation: false` in its
  source agents/openai.yaml. This disables automatic selection, not explicit invocation;
  its original SKILL.md remains unchanged. Jy-orchestrate stays separate and explicit.
  Their incompatible assignment and worker-lifetime policies are documented in the
  [compatibility review](references/compatibility-review.md), not silently combined.
- On 2026-10-16 the user explicitly removed the Bun helpers. `watch-pr`, `orch`, their
  tests, and the shared dependency bootstrap/package/lock files are excluded. Babysit
  and Shipping use direct forge CLI reads; Orchestrate uses task-owned plain files.
  Autopilot and multi-phase plans inherit these adapted procedures. These are agent-run
  procedures, not equivalent replacements for the removed watcher and storage engine.
  Model roles, standard speed, fresh-agent rules, and delegation are unchanged.
- The remaining runner exposes `check-plan` (Node), `worktree-audit` (bash), and `log`
  (bash). Plan-checker tests use `node --test` with no package installation. No new
  runtime or MCP is registered, and the module has no Bun runtime or test dependency.

The Cursor manifests, marketing guide/images, and dormant `automations/benny` pack are
not installed. The make-bot-ui workflow still needs an existing authorized webhook
backend; this module does not provision Cursor services. Long-running continuation is
limited to actual host capabilities, not an emulation of Cursor's cloud scheduler.

## Usage

```text
$pstack <task>
$pstack how <question about this code>
$pstack interrogate <diff or paths>
$pstack setup-pstack
$pstack poteto-help
```

Use a new Codex session after reinstalling jy-env-core. The default needs no model
configuration. Optional configuration lives only in `${CODEX_HOME:-$HOME/.codex}/pstack/models.json`.

## Remove the experiment

1. Delete `plugins/jy-env-core/skills/pstack/`, `skill-tests/first-party/pstack/`, and
   `tests/test_pstack.py` from the source repository.
2. Remove `pstack` from `EXPECTED_PACKS["jy-env-core"]` in tests/test_packaging.py and
   the three peer sets in tests/test_skill_eval.py, and return the skill count from
   10 to 9 in tests/test_repo_bundle.py. Remove the pstack
   paragraph/table entry from both READMEs. Together with the guardrail metadata in step 3, these are the external integration points.
3. Restore automatic guardrails by removing the trial comment and `policy` stanza from
   `plugins/jy-env-core/skills/jy-change-guardrails/agents/openai.yaml` (or set
   `allow_implicit_invocation: true`). Its SKILL.md needs no restoration.
4. Give `plugins/jy-env-core/.codex-plugin/plugin.json` a fresh version and reinstall
   with `codex plugin add jy-env-core@personal-codex` after normal source staging.
   Do not uninstall jy-env-core: its other skills remain in use.
5. If model setup was used, optionally remove only the pstack models.json file.
   Work products and decision logs in user projects remain user data, not install debris.
6. Start a new Codex session. No global instructions, hooks, marketplace entries,
   separate skill symlinks, or persistent tool caches need removal.

Older trial runs may have left OS temporary directories named `pstack-tools-*` after
an interruption. Inspect ownership and running processes before removing a leftover;
the current runner does not create these directories.
