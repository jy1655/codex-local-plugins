# Codex runtime adapter

Apply this contract before any bundled workflow, including prompts sent to children.
It replaces Cursor runtime assumptions while retaining the workflow phases, evidence
requirements, templates, and engineering principles. Do not execute upstream names as
if they were available tools. Follow the user's language and requested output format.

## Scope and permission

Pstack is a workflow, not permission to publish, message others, merge, deploy, delete
data, modify unrelated skills, or change global instructions. Continue already authorized
work without adding approvals. Where an answer or approval is actually required, elapsed
time is not approval. Keep unrelated edits, existing workspaces, and sessions intact.

An implementation request can finish locally. An upstream `Opening a PR` step applies
only when publication is in scope. Never reset or force-remove work to make a playbook
fit. Untracked and ignored files may contain user work. Cleanup requires the actual
authorized target set and evidence that no active work uses it; a script's bucket alone
is insufficient. Do not introduce simulator use where project rules require a device.

Skill edits go to their managed source and through its normal install mechanism. Never
write to installed plugin caches, including dependency installation. A problem in an
unrelated skill goes in the report unless repairing it is part of the authorized task.

## Trial isolation and existing core skills

The user requested an upstream-faithful trial. Jy-change-guardrails is temporarily
excluded from implicit invocation by its source agents/openai.yaml; do not apply its
proportionality rules to simplify this trial. Its source instructions remain intact.
Jy-orchestrate remains explicit-only and is not activated by installing pstack or by
asking whether the skills conflict. Pstack owns its selected workflow, model roles,
competing implementation candidates, and fresh-agent default during this trial.

The two orchestration workflows have real differences: pstack permits competing
implementations and nested track managers and prefers fresh fix-round workers;
jy-orchestrate uses complementary assignments, direct coordination, and useful
original-worker follow-ups. Do not silently combine them or claim both protocols ran.
If the user explicitly invokes both, explain the conflicting requirements and resolve
which protocol owns those decisions before the conflicting delegation. Continue
independent work. User and host permissions remain binding in either workflow.

## Tools and delegation

- `Task`, `subagent_type`, `readonly`, `run_in_background`, `environment`, and
  `cloud_base_branch` in retained prompts are upstream notation, not Codex API fields.
  Use only the actual tool schema. A `poteto-agent` means the bundled agent prompt;
  `generalPurpose` means a normal scoped worker; `comment-sicko` means the scoped
  [comment editor](agents/comment-sicko.md). Pass prompt paths explicitly.
- Use the authorized host mechanism. Where machine-local policy chooses Terminal Agent
  Bridge, inspect `tabcli --help` and use task-owned prompt files and sessions, the required
  terminal, and that policy's permission mode. Otherwise use available native subagents.
  Do not create a new orchestration layer or require an uninstalled delegation skill.
- Preserve the named roles and independent passes. Parallelize within the actual host
  capacity. Use local worktrees for concurrent writers; a cloud flag does not create an
  isolated VM. Never assume nesting depth, MCP inheritance, or provider availability.
- Give independent verification reviewers read-only scope. Comment Sicko is an
  editing role: it may edit scoped comments when the no-comments workflow is authorized;
  a read-only user request still forbids those edits. Read-only does not imply that MCP
  is unavailable. Do not enable writes merely to get MCP.
- Collect actual completion results, inspect their artifacts, and close only task-owned
  sessions after their last needed result and follow-up. Do not resume an agent to poll it.
- `AskQuestion` means the host's question tool when available, otherwise a concise chat
  question. Observe mode restrictions. A todolist means native plan state when available,
  otherwise a small task checklist; it does not require an invented tool call.

## Model roles

Read [default-models.json](default-models.json), then merge any role overrides from
`${CODEX_HOME:-$HOME/.codex}/pstack/models.json`. Configuration applies only to pstack;
no setup or global config change is required. The local trial replaces the upstream
Grok code role with Codex `gpt-6.1-sol` and the Opus judgment role with Codex
`gpt-6-astra`. This is a role mapping, not a capability-equivalence claim. Both were
listed by the local Codex catalog on 2026-10-16; validate availability at invocation.
Arena, architect, and interrogate default to one independent seat of each model.
These are two OpenAI models, not the original cross-provider Grok/Anthropic panel.

Each role is one seat object or a list with `provider`, `model`, and optional `effort`.
A missing override keeps its bundled role. Panel list length sets the number of runs;
`arena cross-judge pool` is a pool from which to select ONE judge, preferring a model
different from the parent. Preserve explicit user-requested counts and providers.
When a seat override changes provider/model, merge those fields with the role and
validate effort against the resulting model. An explicit inheritance alias inherits both
parent model and parent effort unless its override supplies effort; bundled effort must
not accidentally force xhigh onto an inheritance alias.
`provider: native` uses available native delegation; a CLI provider must be supported
and authorized locally. Never silently switch providers to make a name work.

Keep the upstream starting budget: large=xhigh. Optional `budget` accepts
small=medium, medium=high, large=xhigh, unlimited=max and changes starting effort;
Effort precedence is override seat effort, then override budget, then bundled seat
effort. A bundled xhigh value does not prevent a requested budget change. Before a spawn, keep the selected model and move
up one supported level (capped at max) for the hardest work, down one for judgment,
or down at least two for routine work. Verification uses the swarm role's starting
effort. The ladder is low, medium, high, xhigh, max; do not introduce ultra's automatic
delegation into this explicit worker protocol. If role and task descriptions overlap,
use the more demanding justified level and state the actual choice in the brief.

The bundled `speed: "standard"` is the pstack default for every role, including urgent
work and verification. Do not select `-fast` variants, enable fast mode, or request a
priority service tier. Change speed only when the user explicitly requests it; changing
models or reasoning budget alone does not opt into fast mode. Reasoning effort and speed
are separate choices. This speed field is pstack policy, not a Codex CLI argument.

Cursor `-fast` and effort suffixes are not Codex model IDs. With tabcli, pass model and
effort separately, for example `--model gpt-6.1-sol --effort xhigh`; omission uses the
child CLI's configuration, not guaranteed parent inheritance. The audited bridge exposes
no speed flag: check the effective launch configuration rather than inventing one. If
it enables fast mode, use a supported session-scoped standard setting or report the
mismatch; never silently count it as standard or edit global settings to implement this
skill preference. Native APIs use only their actual schema. Where an override requires
a new fork rather than inherited history, include the full scoped brief and resource
paths explicitly.

`inherit-parent` and `auto` are optional aliases, not provider IDs. Use native inheritance
or explicitly pass the known parent model and effort to a CLI; when unknown, report use
of the CLI's configured default. Validate all explicit choices and reasoning levels from
current host metadata. An unavailable model is a coverage gap: do not invent a slug,
retry guessed variants, or silently downgrade a requested panel. Continue independent
work; use a fallback only when authorized. Same-model independent passes remain useful
but must not be reported as model diversity. See the compatibility review for evidence.

## Fresh agents and follow-ups

Retain pstack's fresh-agent default for new assignments, independent reviewers,
fix rounds, and retries. Every fresh brief includes the original objective, all
subsequent directives, the precise candidate/worktree, prior findings, and open checks.
Reuse is still allowed for costly live state, as poteto-mode specifies. Fresh sessions
isolate context; they do not isolate filesystem writes. Use separate worktrees where needed.

For Terminal Agent Bridge, `ask` creates a session and `tell` delivers a turn to an
existing session. These are supported choices, not evidence that one drops directives.
Use `result`/`status` to collect an existing turn, never a follow-up just to poll it.
A timeout or missing receipt is not permission to resend uncertain work. Reconcile the
same request first. Stop/hold is a control action, not a new assignment. At the audited
version (0.4.12), `cancel` and `reopen` do not support Codex, and `hold` does not
interrupt an already running turn; inspect supported control/close behavior. A closed
worker cannot be resumed through this bridge: a closed Codex worker needs a fresh
session and explicit handoff. Close only task-owned sessions after their last needed use.
Native delegation uses its actual follow-up/interrupt APIs and host limits instead.

## Continuation, history, and state

- `/loop` and cloud wakeups become ordinary continuation in the active Codex task, with
  available process/session status and bounded waits. Continue until the done predicate,
  user stop, or a genuine external blocker. Do not claim an overnight scheduler or a
  surviving background agent unless the host actually provides and verifies one.
- Use known conversation IDs, host-provided transcript paths, explicit handoffs, or
  workspace-filtered history tools. Check session/workspace metadata before reading a
  transcript. Do not scan all of `~/.codex/sessions` or infer paths from Cursor slugs.
  Codex JSONL has metadata, messages, and tool events; inspect the actual record schema.
  If history is unavailable, use current context and mark the evidence gap.
- Use native context and task state first. The orchestration store is only for an actual
  multi-session program. Keep it in a task-owned ignored directory, or a temporary work
  directory, and include its absolute path in the relevant briefs. Update its plain files
  with the host's file tools under the playbook's single-writer rule. On restart, inspect actual
  worker status; do not assume workers survived or died.

## External capabilities

- `create-skill` maps to the available `skill-creator`. Create project skills in the
  host-supported project directory; for this repository edit `plugins/<pack>/skills/`
  and reinstall. User skills follow the configured Codex home.
- `deslop` is not bundled. Use an installed equivalent when available, otherwise inspect
  the diff for unnecessary code, comments, duplication, and scope drift using the
  bundled principles. Report the substitution instead of installing cursor-team-kit.
- `control-ui` maps to available computer/browser control, such as cua_repl, and
  `control-cli` to a terminal/PTY or the project's actual harness. Report inaccessible
  surfaces; compilation is not UI or device verification.
- Discover actual MCP/connector tools. Unavailable services are coverage gaps, not a
  reason to read credentials or invent tool names. Use `gh` when GitHub CLI access
  is available. Secrets and external actions follow host and user policy.
- `make-bot-ui` needs an existing authorized bot backend and webhook. The upstream
  Cursor automation endpoint is only an example for users who actually supply that
  service. This port does not provision Cursor automations or the dormant Benny pack.

## Bundled executables

Resolve `PSTACK_ROOT` to the directory containing the invoked SKILL.md. Run tools through:

```text
python3 <PSTACK_ROOT>/scripts/run_tool.py check-plan <plan-path>
python3 <PSTACK_ROOT>/scripts/run_tool.py worktree-audit -b <base-ref> <repo-path>
python3 <PSTACK_ROOT>/scripts/run_tool.py log <logfile> <phase> <decision> <why> <evidence> <result>
```

The user removed the bundled Bun helpers. PR monitoring uses the active forge CLI
directly; program bookkeeping uses the task-owned plain files described in Orchestrate.
Do not install or recreate the removed helpers as an implicit prerequisite. The remaining
tools require no package installation. Node, bash, git, jq, and gh are used only where
needed; do not install missing software without an authorized need. The worktree audit's
`PSTACK_TRANSCRIPTS_DIR`, when supplied, must contain already workspace-scoped exports.
No history source means usage is unknown, not that a worktree is unused.
