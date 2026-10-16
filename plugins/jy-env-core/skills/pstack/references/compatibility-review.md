# Compatibility review, 2026-10-16

## Source and host evidence

Upstream: pstack 0.15.25, cursor/plugins revision
`f713f14203cd6420cec13cd7c55c32d598dbab68`. See UPSTREAM.json for every input hash.
The upstream poteto-mode Subagents section and setup-pstack role table are the source
for the model split, xhigh starting budget, task-sensitive effort, and fresh-agent rule.
This port retains all 54 workflow resources, 23 playbooks, and both agent prompts.

The local Codex model catalog (2026-10-16, CLI 0.163.0) lists gpt-6.1-sol and
gpt-6-astra with low/medium/high/xhigh/max support. It does not list the upstream
Grok/Opus Cursor slugs. Catalog presence is not proof of a completed model run.
Terminal Agent Bridge 0.4.12 --help exposes separate model and effort parameters,
ask/tell/status/result, and explicitly refuses Codex reopen. Omitted options use
provider configuration; they do not prove parent model/effort inheritance.

## Decisions

| Concern | Upstream behavior | Local trial |
|---|---|---|
| Implementation/exploration/verification | Grok role | Codex gpt-6.1-sol role |
| Judgment/prose/hardest work | Opus role | Codex gpt-6-astra role |
| Arena/architect/interrogate | Independent Opus and Grok seats | Independent Astra and Sol seats; both OpenAI |
| Reasoning budget | Default xhigh; adjust to task | Preserve ladder; separate model/effort arguments |
| Fast mode | Cursor model slug suffix | Explicit standard-speed default; no -fast variants or automatic priority requests |
| Fix round/retry/new queue item | Fresh agent with consolidated brief | Retained; reconcile uncertain delivery before retry |
| Costly private state | Existing worker may continue | Retained through supported tell/native follow-up |
| Interrupts lose directives | Upstream assertion | NOT-VERIFIED for Codex; not stated as a host defect |
| Closed worker | Host-dependent resume | Current bridge cannot reopen Codex; fresh handoff |
| Concurrency/nesting/cloud | Cursor Task/cloud assumptions | Actual host capacity and isolated local worktrees |
| PR monitoring | Bun watcher with automatic verdicts | Direct forge CLI reads interpreted by the agent |
| Program bookkeeping | Bun storage CLI | Task-owned plain files with one writer per store |

The role substitutions preserve workflow structure, not model equivalence. Same-model
fallbacks must be reported; a two-OpenAI-model panel is not original cross-provider diversity.
Defaults are bundled inside this removable module; overrides affect only pstack.

## Existing skill conflicts

An independent read-only review of the initial port identified seven findings.
Its two simulated tasks were a local defaulting bug and a feature with pstack plus
jy-orchestrate. Simulations establish instruction conflicts, not actual runtime outcomes.

- Pstack's required competing feature implementations differ from jy-orchestrate's
  complementary assignments. Its fresh fix-round workers differ from original-worker
  follow-ups; its program track managers differ from jy-orchestrate's direct topology.
  The trial keeps pstack's policy. Jy-orchestrate is not automatically activated.
- Guardrails favor proportional investigation and verification; pstack deliberately
  prescribes broader investigation, comparison, comment cleanup, and verification.
  The user chose original pstack testing, so automatic guardrail invocation is temporarily
  disabled. Arena/architect triggers and strict multi-phase checks were restored.
- The initial adapter incorrectly called Comment Sicko read-only while its workflow
  consumes edits. It is a scoped comment editor; independent verification reviewers
  remain read-only. User-requested read-only scope still wins.
- Agent paths and multi-phase templates assumed the upstream application tree. They
  now resolve installed module resources; the plan checker uses the matching marker.
- Principle/reflection evidence used SKILL.md-only recognition. It now recognizes the
  internal WORKFLOW.md resources and actual host file-read/delegation events.
- The initial Bun helpers bootstrapped dependencies in a temporary copy on every call,
  including help and status. The user subsequently requested their removal. The local
  port now excludes both helpers and their dependency files, replaces their callers with
  direct forge reads and file bookkeeping, and runs the plan-checker tests with Node.

Do not silently choose jy-orchestrate precedence if both are explicitly activated.
Resolve the conflicting protocol with the user while independent work continues.
Shared user/host permissions and workspace-preservation rules remain binding.

## Verification boundary

The repository suite checks packaging, inventory, module references, provenance coverage,
runner argument/exit propagation, and rejection of the removed tools. The retained plan
checker has five Node tests. Current provenance separates 116 retained input records
from 18 explicitly excluded Bun helper/dependency files; original hashes are retained.
Direct forge monitoring and plain-file bookkeeping are instruction-level adaptations.
The removed helpers' automatic verdicts, storage validation, locking, and inbox behavior
are no longer executable guarantees. Agent procedures retain head-SHA checks, one writer
per store, durable updates, and replay reconciliation, but require live trial evidence.
These checks do not prove the quality of every workflow or a full multi-model program.
Runtime smoke-test results are reported separately from static and helper-tool checks.

### Verification after Bun removal, 2026-10-16

The repository suite passes 121 tests with the project's Python environment on PATH;
the migrated Node plan-checker suite passes all five tests. Skill validation passes.
The model defaults, base workflow, entry point, and invocation policy match the pre-removal
files byte-for-byte. No live PR/merge or multi-session program was executed to validate
the replacement procedures.

### Historical verification before Bun removal

Observed results in the initial trial: 120 repository tests pass; 68 upstream helper tests
pass (the 5 changed plan-checker cases were rerun); TypeScript type checking passes;
help commands for orch and watch-pr run from temporary copies; removal rehearsal
passes the original 117 tests. All 134 imported input hashes match the pinned source.
A fresh Codex app-server skills/list discovers the installed pstack entry point.
These results describe the initial import and do not validate the later direct-CLI and
plain-file adaptations.

The separate local invoice-fix model smoke did not publish a completion result within
the bounded run, and its fixture remained unchanged. It was closed; this is NOT-VERIFIED,
not a passing end-to-end workflow test or proof of a model/bridge defect. The successful
independent review was a static forward simulation. Full multi-model behavior remains
for subsequent real task trials. Bridge cancel reported unsupported for Codex in 0.4.12;
the task-owned close-session completed. Do not treat hold as an interruption of a running turn.
