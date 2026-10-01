# Work Orchestrator Handoff

Read before the first work-orchestrator launch and before replacement. These are
coordination instructions, not runtime-enforced locks or automatic context detection.

## Minimal task record

Use one task-owned local directory reachable by the decision-maker and its children.
Prefer an existing approved scratch location; otherwise use a directory outside the
deliverable repository. Keep secrets out. Do not add tracking infrastructure or change
ignore rules just to store a handoff. For a task that forbids scratch writes too, use
retrievable structured native results and exact result IDs instead of creating files.

Keep two small records, updating current state instead of appending transcripts:

- `control.md`, written only by the final decision-maker: task ID, objective and
  acceptance criteria, current user constraints/authorizations with their source,
  instruction revision, decisions still in force, active orchestrator ID/generation,
  candidate or retiring IDs, and the handoff reference. Increment the instruction
  revision on relevant user steering and forward the changed instruction.
- `handoff.md`, written only by the active work orchestrator: revision acknowledged,
  completed and remaining work, next actions, unresolved findings and decisions,
  workspace/worktree paths and candidate identity (commit plus dirty diff or artifact
  identity), unrelated edits to preserve, and evidence references with verification
  limits. Include every task-owned session's role, ID, assignment/edit scope, current
  request ID, last consumed result ID, observed state, and owner. Track descendants
  before dispatching further work so they can be recovered if a manager disappears.

The final decision-maker retains the directory or native result locator through its own
compaction. The candidate reads these records without overwriting them. Freeze the
handoff before candidate readback; send any subsequent instruction or result delta
explicitly. Once active, the successor becomes the handoff writer. Keep supporting
evidence separately and read it on demand; do not copy the entire predecessor history.
Retain records through completion and any requested recovery period.

## Transfer one owner at a time

1. **Quiesce.** The final decision-maker tells the active orchestrator to stop new
   dispatch and prepare a handoff. Let bounded in-flight work reach a safe boundary,
   or preserve its exact request and edit ownership if it can safely continue under
   the current instructions. Account for all workers/reviewers and late results.
   Quiescing the manager does not prove its workers have stopped. If user steering
   invalidates their work, stop or pause the affected assignments before proceeding.
   Obtain an explicit relinquishment/read-only acknowledgment from the predecessor;
   a queued message or a quiet terminal is not that acknowledgment.
2. **Prepare.** The decision-maker records that there is no dispatching owner during
   handoff and launches one fresh session as a read-only successor. Supply its role,
   control/handoff locators, current instruction revision, and targeted evidence.
   It may inspect existing work and results but must not launch workers, edit the
   candidate, redirect existing sessions, or activate itself.
3. **Read back.** The successor reports the objective, constraints and revision,
   candidate identity, pending sessions/results, unresolved verification, and next
   action. It checks the recorded state against the workspace and available session
   handles. Resolve material gaps before activation. The decision-maker relays user
   changes or late results received during preparation and obtains an updated readback
   when they change the proposed next action. Never activate on an obsolete revision.
4. **Retire.** After accepting readiness, the decision-maker closes only the
   predecessor orchestrator and verifies retirement with available runtime evidence.
   Preserve transferred workers, reviewers, and their artifacts. An uncertain close
   still counts as a live slot and is not permission for a third orchestrator.
5. **Activate.** The decision-maker updates the active session/generation and sends
   explicit activation with the current instruction revision. The successor
   acknowledges ownership before dispatching or redirecting work. Collect pending
   results by exact IDs and avoid replaying work already done. Once a former session
   is retired, its late messages are evidence only, never new dispatch authority.

The final decision-maker serializes this transition. A second replacement request
during transfer updates the pending transition; it does not start another candidate.
If the user explicitly rejects the preparing successor or requests its replacement,
retire that candidate before preparing another. A generic repeated request continues the pending transition; clarify
the target only if its ambiguity materially changes which session the user will accept.
No tool return by itself grants ownership: distinguish launched, ready, retired, active,
and task complete. The same procedure applies to later replacements; two is a
simultaneous-session limit, not a lifetime limit of two generations.

## Interrupted or failed transfers

- If preparation/readback fails, keep the predecessor quiescent and inspect or close
  the candidate before retrying. The decision-maker may explicitly reactivate a
  healthy predecessor on the latest instructions if the user has not ruled that out.
  Do not let either session infer authority from silence or a failed launch.
- If the predecessor cannot hand off, stop/retire it using supported controls and
  establish that it cannot still dispatch before granting a successor authority.
  Recover from the last record plus current workspace/session evidence; mark missing
  facts as unknown. Reconcile affected workers and external actions before retrying
  them. Do not repeat a possibly completed action merely because its receipt is absent.
- If the runtime cannot interrupt a busy turn, wait for its bounded turn to finish or
  use a supported stop mechanism. Do not treat `tell` delivery as interruption. If
  retirement or worker ownership cannot be established, keep overlapping mutations
  stopped while continuing safe inspection; report the concrete limitation.
- If successor activation has an uncertain outcome, inspect that same session/request
  before retrying or replacing it. Keep both the session cap and single-owner rule.
- If child handles cannot be transferred in the chosen runtime, retrieve their results
  through the supported parent channel and settle or stop those assignments before
  retiring that parent. Supply artifacts to the successor; do not pretend it can
  control inaccessible descendants. If no fresh session can be created, report that
  replacement is unavailable; compaction alone is not a completed replacement.

## Agent Bridge mapping

Check the installed CLI's help for supported options and follow machine-local terminal
and permission preferences. Use task-owned prompt files with explicit roles and bounds.

- `ask` creates the initial orchestrator and each fresh successor; `tell` continues a
  known session only when it is ready. It does not interrupt a running turn. Do not use
  `reopen` or provider resume to claim a fresh context.
- Use `inspect` and `result --request <request-id>` to reconcile a known session and
  request. Persist request IDs from receipts. Retrieve narrowly scoped results instead
  of dumping every transcript into the decision-maker. Use `doctor --probe` when
  observed liveness is uncertain, rather than trusting stored status alone.
- `close-session <session> --explicit` closes a task-owned session. Check the outcome;
  never sweep, prune, or close sessions owned by other tasks. The decision-maker owns
  cleanup after transfer, including descendant sessions inherited from a predecessor.
