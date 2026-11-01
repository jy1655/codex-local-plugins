---
name: jy-orchestrate
description: Use when the user explicitly requests jy-orchestrate for directly coordinated Codex and Claude planning or implementation with independent Codex DevBlue and Claude verification.
---

# JY Orchestrate

The invoking session directly coordinates Codex and Claude workers and reviewers. It owns
the user's objective, current constraints, task assignment, integration, and final
acceptance. Do not insert a separate work-orchestrator session or a manager-replacement
workflow. A child reading this skill keeps its assigned role and returns scoped results.

## Assign bounded work

Prefer Codex's built-in subagents for Codex work. Use Agent Bridge for Codex-to-Codex
delegation only when the user explicitly requests that route; invoking this skill alone
does not select it. If native delegation is unavailable, continue locally where possible
and report any unmet independent-review requirement rather than silently switching routes.
Cross-provider work with Claude may use Agent Bridge within the authorized task scope;
apply machine-local launch options only after selecting that route.

Preserve planning-only, read-only, authorization, and
workspace boundaries in every assignment. Relay changed user instructions promptly and
stop or revise affected assignments before accepting results produced under old instructions.
A queued instruction is not proof that a busy worker stopped. Use supported interruption
controls and verify its state; report an unconfirmed halt when those controls are unavailable.

Split work by dependencies and edit ownership. Batch small changes of the same kind.
Run independent assignments concurrently when their edits and shared resources do not
conflict; isolate or sequence overlapping work. Preserve unrelated changes. Choose useful
assignments for Codex and Claude rather than duplicating the same implementation.

Give each worker the objective, allowed edit scope, necessary interfaces and dependencies,
acceptance criteria, relevant verification, and expected result. Supply only the context
needed for that assignment, using artifact references for lengthy material.

Use `gpt-5.6-sol` for Codex workers and inherit the invoking session's reasoning effort.
With Agent Bridge, pass `--model gpt-5.6-sol` and the known `--effort <inherited-effort>`
explicitly. Disclose actual defaults when effort is unknown. If a required model or
setting is unavailable, report the affected requirement and continue unaffected work;
substitute only within the user's allowed choices and identify the substitution.

## Collect results

Keep task-owned session IDs, assignments, request IDs, and consumed result IDs retrievable
through native state or an existing task record. Include any descendants in that ownership
record. A dispatch receipt is not completion. Inspect the actual result before follow-ups
or acceptance; after a timeout or interruption, reconcile the same request before retrying.

Ask workers to return a concise status (`DONE`, `DONE_WITH_CONCERNS`, `NEEDS_CONTEXT`, or
`BLOCKED`), changed candidate or artifact, verification evidence, unresolved concerns, and
evidence locations. Resolve correctness concerns before acceptance. Supply missing context,
split an oversized task, or change the approach when blocked; do not repeat an unchanged
failed assignment. Keep full transcripts, diffs, and test logs outside routine summaries.

## Review and revise

Integrate the work and identify the candidate: a commit plus relevant uncommitted changes,
or the exact planning artifact. Have Codex DevBlue (`gpt-daybreak-blue-latest`) and Claude
independently verify that same candidate in sessions separate from the workers and the
invoking session. The invoking session dispatches these reviews; worker self-review is
useful but does not replace them.

Give both reviewers the requirements, current constraints, candidate, scoped changes,
applicable global and repository review guidance, and verification evidence. Each checks
requirement coverage and implementation or plan quality.
Reviews are read-only; inspect surrounding code or run focused checks when a concrete concern
requires it. Reuse valid evidence instead of routinely rerunning unchanged checks.

For code changes, ask reviewers to trace relevant release/reset/failure, retry, state-boundary,
mode, compatibility, and incomplete-result paths beyond the proposed scenario. Before reviewing
a fix with a regression test, obtain its result on both the pre-fix implementation and candidate,
or the reason comparison could not run. Use isolated snapshots or an equivalent safe comparison;
preserve unrelated working-tree changes. A failure must demonstrate the intended defect, not a
setup error; a test passing before the fix does not establish regression coverage.

Ask each reviewer to open with the finding count, saying plainly when nothing needs fixing,
and to give every finding its location (file and line, or plan section), triggering
condition, minimal fix, and one tag when the review surface permits this format. Preserve
required schemas, priorities, and reporting thresholds; otherwise classify findings during
triage without requiring extra fields or optional-polish findings:

- `important`: a defect or unmet requirement in what the candidate changes or relies on.
- `nit`: style or polish that leaves behavior and requirements intact.
- `pre-existing`: a defect the candidate neither introduces, touches, nor relies on.

Reviewers name the bug class when one cause has several instances, and name what they could
not verify.

Verify each finding against the candidate, then close it as fixed, rejected with a reason,
or deferred. Route `important` findings back to the original worker when practical, asking
for every instance of a named class. Fold `nit` findings into the next routed fix or list
them in the final report. Report `pre-existing` findings to the user as follow-up work
outside this candidate. After the first full review, re-review the fix diff and its effects,
giving reviewers the earlier findings and their dispositions so a closed finding returns
only with new evidence. Refresh affected evidence for the final candidate. Resolve reviewer
disagreements from evidence: one clean review does not dismiss another's supported defect.

A review round is one pass by both reviewers over one candidate; the first full review is
round one. When fixes stop making progress, or round three still reports `important`
findings, revisit the approach, cause, context, or task split before routing more fixes.
Continue the same approach when the evidence shows `important` findings being resolved
rather than recurring in the same class; newly exposed boundary cases can hold the count
flat or raise it, so state the reason for continuing. Ask the user when the approach itself
is in doubt. The round count triggers that check; it never makes an unresolved defect
acceptable. Report material decisions and verification gaps.

Accept completion against the user's criteria and both independent reviews. Additional
intermediate review is justified by a concrete integration risk, not every small task.

## Context, Wiki, and completion

Use native session state and context compression first. For an actual cross-session handoff
or recovery need, keep one compact current record: objective and current instructions,
completed and remaining work, candidate and workspace, pending session/request/result IDs,
edit ownership, unresolved findings, and evidence references. Follow local storage policy
for its canonical location; keep large evidence separately. Recover against current workspace
and session evidence before resuming, preserving newer edits and avoiding duplicate actions.

The invoking session also owns durable Wiki recording under the global and local instructions.
When a local Wiki is configured, read its `AGENTS.md` and follow that policy for qualifying
decisions, corrections, outcomes, lessons, and verification limits. Compact task records do
not replace these Wiki updates. Before the final response, verify the required updates were
saved and report their location. If access or authorization prevents recording, disclose the
gap and continue unaffected authorized work. Keep machine-specific paths in local instructions.

After inspecting the last needed results and completing follow-ups, close task-owned sessions,
including descendants, through supported controls. Preserve unrelated sessions and existing
records. Report incomplete cleanup or unverified requirements rather than claiming completion.
