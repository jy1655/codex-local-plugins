---
name: security-audit
description: Use when the user explicitly invokes $security-audit or names this skill to audit a codebase, validate security findings, and preserve reports in Wiki raw. Do not select it for unnamed security questions or ordinary code review.
---

# Security Audit

Find vulnerabilities that violate a real trust boundary, then give owners the source evidence, safe reproduction, priority, and smallest effective fix. This is a defensive, source-first workflow. A candidate without a concrete affected principal, resource, or security outcome is not a confirmed finding.

## Invocation and operating modes

Use this skill only when the user explicitly invokes `$security-audit`, selects it
in the skill picker, or asks to use the named `security-audit` skill. A generic
security question, security-related code change, or ordinary review does not activate
it. `agents/openai.yaml` disables implicit invocation. Loading these files for
inspection or skill authoring is not an audit invocation.

- **Full audit mode**: An invocation to audit or pen-test a repository, request a
  report, or run this skill without a narrower question uses all six phases.
  Default to the current repository and `standard` profile unless the user gives
  another target, scope, profile, or budget. Infer these from current context;
  ask only when the missing choice materially changes the task.
- **Guidance mode**: An explicit invocation for a specific security question,
  focused finding, methodology, or triage uses only relevant references. Do not
  automatically create full-audit artifacts. Focused agents may return results
  to the current task. Preserve eligible conclusions under host Wiki policy.

In both modes read [EXECUTION.md](EXECUTION.md). For full audit also read
[WIKI-OUTPUT.md](WIKI-OUTPUT.md) during setup and before delivery.

## Platform terminology

This skill is agent-neutral:

- **Parent** is the agent that coordinates the run and owns shared state.
- **Task tool** is the platform's delegation or sub-agent mechanism.
- **`research` agent** is a delegated agent for focused source exploration and factual verification.
- **`general` agent** is a delegated agent for broad investigation and bounded local execution.
- **`subagent_type:`** in a heading names which of these two delegated agent roles runs that work.

Use native Codex subagents and map these role names to the available delegation
capabilities. Preserve prompt, ownership, and independent-verifier boundaries;
schedule work within the concurrency limit. Do not silently substitute Agent Bridge
or another provider. If native delegation is unavailable, continue source review
and report the independent-audit phases as incomplete rather than self-certifying.

## Execution policy

Follow [EXECUTION.md](EXECUTION.md) for bounded local checks using existing host
permissions. An OS sandbox and external-network blocking are optional. Their
absence alone must not prevent an explicitly requested audit or safe local test.
The execution host may be a user-designated SSH server. In this workflow,
"local" includes bounded checks on that host. Authorized read-only inspection of
its deployed configuration, logs, and runtime state follows EXECUTION.md and is
not blocked by the companion references' restrictions on live attack probes.
Preserve the evidence bar: a source hypothesis without its decisive observation
remains `needs_validation`, whether execution is sandboxed or on the normal host.
Record the actual containment and any specific limitation. Preserve target source;
the audit recommends fixes rather than applying them.

## Full audit setup

In full audit mode, resolve these values before reconnaissance:

- **Skill directory**: the absolute directory containing this `SKILL.md`.
- **Target**: the absolute repository root under review, on the named SSH host when applicable. Keep the controller and remote paths distinct; a local clone is optional.
- **Repo name**: a stable repository identifier from the directory or local Git remote.
- **Output directory**: a managed temporary verification workspace outside the target, created as described in [WIKI-OUTPUT.md](WIKI-OUTPUT.md). The durable destination is the configured Wiki `raw/`; do not use the upstream home-directory default.
- **Source ref**: the reviewed commit and whether the worktree is dirty. Do not treat unreviewed generated or modified files as another revision.

### Write isolation

The parent creates and is the only writer of shared run files:

- `run-metadata.json`
- `architecture.md`
- `coverage-ledger.json`
- `findings.json`
- `REPORT.md`
- `FINDINGS-DETAIL.md`
- `NEEDS-VALIDATION.md`

Each hunter or verifier receives a unique root under `<output-dir>/agents/<agent-id>/`,
with separate `scratch/` and parent-owned `artifacts/`. Agent IDs match
`^[a-z0-9][a-z0-9_-]{0,63}$` and exclude Windows device names. Agents write only
their scratch and return results; the parent owns shared files, retained artifacts,
and all Wiki writes. Apply the parent evidence-retention procedure in
[EXECUTION.md](EXECUTION.md). These ownership rules do not imply OS isolation.

Before delegation, write `run-metadata.json` with at least `run_id`, `repo`,
`target`, `source_ref`, `profile`, `scope_paths`, `budget` (null if unset),
`execution_policy: "host-bounded-local"`, actual containment used, selected
companion files, prior-run Wiki paths, shared-file owners, and
`run_status: "in_progress"`. Include the output and storage fields from
[WIKI-OUTPUT.md](WIKI-OUTPUT.md). Update metadata when these facts change;
candidate state belongs in the ledger and `findings.json`.
For SSH runs include `execution_transport: "ssh"`, the non-secret host alias,
remote repository path, environment role, and authorized inspection scope. Pass
this execution context to every subagent; keep connection credentials out of prompts.

## Full audit planning

The coverage, prior-run, profile, and budget requirements in this section apply only in full audit mode.

### Coverage and prior runs

No one pass is complete. Build a deterministic coverage plan before hunting and update it after every agent result. [RECONNAISSANCE.md](RECONNAISSANCE.md) defines the stable coverage units and [HUNTING.md](HUNTING.md) defines coverage-critic waves. The parent alone updates the ledger.

Search prior runs in Wiki as described in [WIKI-OUTPUT.md](WIKI-OUTPUT.md). Read every compatible `coverage-ledger.json` and `findings.json` before planning the current run:

1. Compare the relevant current source with each prior record and unit. A prior source ref alone is not evidence that a path is unchanged.
2. Carry a prior `confirmed` record into the current candidate set only when its relevant source and conditions are unchanged and its evidence still meets the current contract. Link it to a current ledger unit seeded `planned`, preserve its fingerprint, exclude only that carried root cause from hunters, and send the carried record through the current final verification path; the Phase 3 verifier that re-checks it becomes that unit's assignment owner and moves it to `candidate`.
3. When relevant source for a prior `confirmed` record changed, create a current planned revalidation unit. Do not put that record on the hunter exclusion list. It remains confirmed only if current independent validation establishes the current path and result.
4. Make prior `needs_validation`, `deferred`, `blocked`, `out_of_scope`, and any changed-source unit current work. A still-external `needs_validation` record may be carried only after the current source trace is checked and linked by fingerprint to a current `planned` unit whose verifier re-check supplies its owner and evidence; the record keeps the unresolved blocker. These prior states never suppress a current unit.
5. A prior same-source covered unit may inform priority, but it remains visible in the current ledger. A prior `rejected` record suppresses only the unchanged failed claim, not coverage of its unit; changed evidence creates current work.
6. Read the prior profile and scope. A prior `quick` or scoped ledger contributes only its recorded evidence and gaps, never an implied "rest is fine."

If no prior ledger exists, say so in the final coverage statement. Never imply that one run exhausts the target.

### Run profiles and scope

During full audit setup, pick a profile from the user's request or propose one from the target's size and stakes. Record it in `run-metadata.json` (`profile`, `scope_paths`) and state it in the report. The default is `standard`.

- **`quick`** — a bounded pass for small targets, re-runs, or a fast first look. Coarsen ledger units to surface × boundary × attack class (subsystem uses the fixed canonical `profile/quick/all-in-scope-subsystems` identifier), run exactly one hunter wave followed by exactly one final coverage-critic pass, and use one fresh verifier per candidate for both candidate validation and final record verification. Do not launch a follow-up hunter wave: record the critic's accepted discoveries and reassignments as `deferred`.
- **`standard`** — the workflow as written.
- **`deep`** — for high-stakes or large targets. Split ledger units per subsystem and lifecycle mode, run critic waves to a clean pass, keep candidate validation and final record verification as separate fresh agents, and give `prior_covered_same_source` units an independent second pass.

A **scoped run** audits a subset: named paths, one subsystem, one companion domain, or the diff between two source refs. Seed ledger units only for in-scope surfaces and record everything else as `out_of_scope` — never as `covered`. A scoped or `quick` run must present itself as partial coverage.

Profiles change breadth and redundancy, never the evidence bar. Do not scale away the candidate gate, the source/local execution boundary, `needs_validation` discipline, schema validation, or independent verification of `confirmed` records.

#### Cost budget

The ledger makes spend countable: one unit is roughly one hunter assignment, and one surviving candidate is one or two verifier assignments depending on profile. When the user sets a budget — or the parent proposes one for a large target — record `budget` in `run-metadata.json` as a maximum number of agent invocations across all phases.

Apply the strict budget gate before launching any reconnaissance agent. Reserve the four baseline reconnaissance calls, one final post-wave critic for `quick` or one post-wave plus one distinct final-clean critic for `standard`/`deep`, and at least one verifier call. Add focused reconnaissance only after repeating this gate for each extra call. If the requested budget cannot fund that minimum, launch no agent: ask for a larger budget, narrower scope, or different profile. If the request remains unchanged, set `run_status: "incomplete"` with `incomplete_reason: "budget_cannot_fund_reconnaissance_and_reserves"` and report that no audit pass ran.

Spend it in this order:

1. Count reconnaissance, every post-wave critic, and the separate final-clean critic as agent invocations.
2. **Reserve critics and validation before hunting.** For `quick`, reserve its one post-wave final critic. Before every `standard` or `deep` hunter wave, reserve one immediate post-wave critic plus one distinct final-clean critic. Also reserve verifier cost from the profile (about 1 or 2 agents per expected candidate; when in doubt reserve 30% of the balance after critic reservation). Never assign hunters into either reserve.
3. Assign hunters to units in priority order until the hunting allowance is spent. Spend the reserved post-wave critic immediately after that wave; keep the final-clean and validation reserves intact.
4. Before a later wave, reserve its new post-wave critic again. If the remaining budget cannot cover the required critic calls and validation reserve, launch no hunters from that wave, mark its planned units `deferred` with reason `budget_cannot_reserve_critics_and_validation`, and use the retained final-clean critic to record the resulting gap.

Before wave 1, update the pre-recon estimate with seeded units, implied hunter count, mandatory critic calls, validation reserve, and whether the remaining budget covers the plan. If it clearly cannot, say so and propose either a tighter scope or a coarser profile instead of silently thinning evidence. If later facts consume the required final-critic reserve, launch no hunters, mark all planned work deferred, set the run incomplete with reason `critic_budget_exhausted`, and make no complete-coverage claim.

A strict total-agent budget can still be exceeded by an unexpectedly large candidate set or by a material Phase 5 replacement that needs another independent verifier. If the remaining budget cannot validate every candidate, stop hunting, validate candidates in fingerprint order while the budget permits, and set `run_status: "incomplete"` plus `incomplete_reason: "validation_budget_exhausted"`. Keep each unvalidated fingerprint linked to a `candidate` ledger unit with that unresolved reason. Do not put an unvalidated candidate in `findings.json`, relabel it `needs_validation`, or report the run as complete. Phase 6 may produce a partial report only if its first section states that candidate validation is incomplete and lists the affected fingerprints and units. Never exceed a user-set strict budget silently.

## Core principles

### Require a boundary and result

For every candidate, name the lower-trust principal, accepted input or action, intended control, crossed boundary, affected principal or resource, and concrete observed or owner-observable result. Do not elevate a missing best practice, guessed deployment behavior, generic parser crash, or self-impact into a security finding.

### Use bounded local evidence

Static analysis establishes the source path. Bounded local tests under [EXECUTION.md](EXECUTION.md) resolve behavior: a minimal function harness, existing unit test, small parser fixture, dummy-tenant integration test, locally rendered configuration, or bounded local-loopback client. Stop at a wrong return value, unauthorized dummy record, sanitizer finding, policy difference, or other minimum effect. Do not extend the local check beyond the minimum boundary result or produce persistence, post-fault, or concealment material.

### Respect source visibility

Deployment controls, proxy behavior, provider settings, browser headers, identity policy, broker ACLs, packaging, and topology are real controls. If they are required and absent from the repository, inspect them through authorized read-only SSH access where available. Do not assume either presence or absence. If the decisive fact remains unobserved, use `needs_validation` with the exact missing fact and a safe owner-observed or host-side plan.

### Separate priority from certainty

Only `confirmed` records receive severity. Likelihood and impact must reflect the demonstrated conditions and result; overall severity cannot exceed demonstrated impact. `needs_validation` means a specific source-grounded boundary hypothesis is blocked, not a low-confidence confirmed vulnerability, and it has no severity.

Calibrate overall severity with these anchors:

- **critical** — an unauthenticated actor gains code execution, full data-store access, or takeover of arbitrary accounts.
- **high** — an actor fully defeats an explicit security control with real consequences: authentication bypass, cross-tenant read or write, stored script execution affecting other users, authenticated code execution, or an unauthenticated remote stop of a shared service.
- **medium** — a real boundary violation with limited blast radius, uncommon preconditions, or consequences confined to a narrow resource set.
- **low** — disclosure of non-secret internals, or an effect requiring sustained effort for minimal gain.
- **informational** — a confirmed but minimal-impact observation, useful mainly as a prerequisite inside a larger finding.

The high/medium discriminator: does the demonstrated result fully defeat an explicit control for an action with real consequences, or only weaken it? If you cannot state the concrete damage, the severity is lower than it feels.

### Recommend the smallest effective source fix

For each confirmed finding, identify the invariant the code must enforce and the narrowest source change that enforces it at the last trusted decision point. Prefer specific repository-relative changes and regression tests over generic hardening advice. The audit describes fixes; it does not modify target source.

## Full audit workflow

In full audit mode, follow all six phases in order:

1. **Reconnaissance** — map the source, trust boundaries, local build paths, companion selections, prior evidence, and initial deterministic coverage ledger with [RECONNAISSANCE.md](RECONNAISSANCE.md).
2. **Coverage-led hunting waves** — assign isolated hunters from the ledger and collect structured candidate results with [HUNTING.md](HUNTING.md), [ATTACK-CLASSES.md](ATTACK-CLASSES.md), and the selected domain companions.
3. **Candidate validation** — consolidate fingerprints and give every candidate to a fresh source verifier as defined in [VALIDATION-AND-REPORTING.md](VALIDATION-AND-REPORTING.md).
4. **Structured output** — write all final `confirmed`, `needs_validation`, and `rejected` records to `findings.json`; validate it with `report-schema.json` and `validate-findings.cjs`, and validate the coverage claim with `validate-coverage-ledger.cjs`.
5. **Independent record verification** — use fresh agents to verify final source claims and reconcile corrections or state changes.
6. **Target-neutral report** — derive `REPORT.md`, `FINDINGS-DETAIL.md`, and `NEEDS-VALIDATION.md` from the final records, with no live-probe instructions.

Finish the audit in one of two states: (a) all Phase 6 artifacts are written and
both validators pass, or (b) `run_status: "incomplete"` records its exact reason
and the report discloses the gap. Complete durable delivery and cleanup through
[WIKI-OUTPUT.md](WIKI-OUTPUT.md); a local report or passing validator alone is
not completed Wiki delivery. If storage is unavailable, retain the files and
report `storage_status: "incomplete"` separately. Never silently stop mid-phase.

## Anti-patterns

1. Checklist deviations presented as vulnerabilities.
2. Defense-in-depth advice with no reachable boundary violation.
3. Live or shared-environment testing where bounded local evidence is insufficient.
4. Guessing provider, proxy, browser, identity, or deployment behavior not present in source.
5. Treating intended same-principal authority or self-impact as a cross-boundary result.
6. Reporting a parser or runtime effect stronger than the observed effect.
7. Emitting prose-only hunter results that cannot be deduplicated or verified.
8. Re-reporting carried same-source prior confirmed records or using them as exemplars that anchor the hunt.
9. Assigning severity to `needs_validation` records.
10. Writing the report before independent verification or letting prose and JSON disagree.
