---
name: jy-orchestrate
description: Use when the user explicitly requests jy-orchestrate for Codex and Claude planning or implementation, with a final decision-maker, replaceable work orchestrator, and independent Codex DevBlue and Claude verification.
---

# JY Orchestrate

Keep the invoking session as the **final decision-maker**. It delegates execution
management to one **work orchestrator**, which coordinates the workers and reviewers.
Keep detailed execution context in that replaceable session so long tasks do not turn
the decision-maker into another execution log.

## Roles and authority

- **Final decision-maker:** Own the user's objective, constraints, acceptance criteria,
  consequential decisions, and final response. Launch and replace the work orchestrator;
  relay new user instructions promptly. Let it resolve routine implementation details
  within scope. Inspect targeted evidence when needed to decide or accept completion.
- **Work orchestrator:** Break down the task, coordinate Codex and Claude, manage edit
  ownership, collect evidence, integrate results, and route reviewer findings to workers.
  Maintain the handoff record and request replacement before context pressure impairs
  coordination. Do not create your own successor or another final decision-maker.
- **Workers and reviewers:** Perform bounded assignments and return results to the work
  orchestrator. Preserve the user's planning-only, read-only, authorization, and workspace
  boundaries throughout delegation and replacement.

Only the original invoking session takes the final decision-maker role. A child reading
this skill must retain the role assigned in its launch prompt; do not recursively add
management layers. Internal decisions never substitute for required user approval.

Keep **one active work orchestrator**. During replacement, allow at most **two live work
orchestrator sessions**, including launching, retiring, or uncertain sessions: the
predecessor and one read-only successor. This limit excludes the final decision-maker,
workers, and independent reviewers. Only the active owner may dispatch or redirect work.
The decision-maker may stop affected assignments to enforce user steering or recover a
failed manager; this does not make it a second routine dispatcher.

## Start and continue

Use Agent Bridge when available locally, following applicable local instructions; use
supported native delegation otherwise. Before launching, read
[orchestrator-handoff.md](references/orchestrator-handoff.md) for the small task record,
session ownership, and replacement procedure. Do not build a new scheduler or context
monitor for this skill.

The final decision-maker gives the work orchestrator its explicit role, task and current
instruction revision, constraints, acceptance criteria, record location, and result
channel. Use the invoking session's model and reasoning effort for work orchestrators
when available; pass known values explicitly and record the actual launch settings.
Do not apply the Codex worker model below to this management role. If parent settings
are unavailable, disclose the configured launch defaults instead of claiming inheritance.
For workers too, disclose actual defaults when inherited effort is unknown. If a required
worker/reviewer model or setting is unavailable, report the affected requirement to the
decision-maker and continue unaffected work. Use an alternative only within the user's
allowed choices, record any substitution, and do not claim the original requirement met.

The work orchestrator:

1. Delegates the requested planning or implementation to Codex and Claude. Use
   `gpt-5.6-sol` for Codex worker sessions and inherit the original invoking session's
   reasoning effort. With Agent Bridge, pass `--model gpt-5.6-sol` and the known
   `--effort <inherited-effort>` explicitly. Carry these settings across replacements;
   distinguish unavailable settings from verified inheritance.
2. Keeps concurrent edits separate or sequences overlapping work, preserving unrelated
   changes. Have Codex DevBlue (`gpt-daybreak-blue-latest`) and Claude independently
   verify the same identified candidate, in sessions separate from the workers.
3. Routes supported findings to workers and updates affected verification after fixes.
   A clean review does not dismiss another reviewer's supported defect. Reuse evidence
   for unchanged work; preserve what has and has not actually been verified.
4. Updates the handoff at meaningful boundaries, then returns a compact milestone,
   decision request, blocker, replacement request, or completion result. With a
   turn-based bridge, finish the turn so the parent can retrieve that result and resume
   the same session. Avoid one unbounded child turn that prevents steering or handoff.

Report upward only: status and instruction revision, material changes, evidence
references, unresolved risk or decision, and the next action. Keep transcripts, verbose
test output, full diffs, and routine worker chatter in task artifacts or native results.
Do not routinely load them into the final decision-maker. It keeps a compact current
control record and relies on native context compression for its own conversation.

## Replace and finish

Replace on a user or final decision-maker instruction, or when the work orchestrator
reports context pressure: an exposed context warning, impending compaction with work at
risk, repeated loss of constraints, or difficulty producing a reliable current summary.
Elapsed time alone is not a trigger. Do not invent token counts or require a fixed
percentage when the runtime exposes no reliable measurement. Native compaction remains
useful, but does not cancel an explicit replacement request.

Follow the handoff reference: quiesce the predecessor, prepare one fresh successor,
verify its readback, retire the predecessor, then activate the successor. Carry only
current instructions, the compact handoff, and evidence references; resuming or copying
the predecessor's full conversation defeats the replacement's purpose.

The final decision-maker accepts completion against the user's criteria and both
independent reviews, resolving material disagreements from evidence. Before the final
response, inspect the last needed results and close task-owned sessions, including
transferred descendants. Report any unverified requirements or incomplete cleanup;
never close unrelated sessions or treat dispatch/acknowledgment as completion.
