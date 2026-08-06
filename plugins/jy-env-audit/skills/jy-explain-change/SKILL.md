---
name: jy-explain-change
description: Use when the user explicitly invokes $jy-explain-change to understand a specified diff, commit, branch, or PR through system background, core intuition, a causal walkthrough, evidence boundaries, and an understanding check.
---

# JY Explain Change

## Overview

Teach a completed code change well enough for the reader to participate in the next design or
implementation decision. Build understanding rather than issuing a correctness, merge, or release
verdict.

This is an explicit-invocation-only skill. Run it only after the user invokes
`$jy-explain-change`; do not treat a similar natural-language request as activation.

This skill is advisory and read-only. Do not modify code, tests, documentation, configuration, or
Git state.

## Input Contract

Accept one of these targets:

- an uncommitted working-tree or staged diff;
- one or more commits;
- a branch comparison;
- a pull or merge request;
- another exact before-and-after source range supplied by the user.

Establish the exact comparison target before explaining it. Record the base, head, commit SHA, PR
head, staged state, or working-tree state used. When more than one target is plausible, ask one
focused question instead of silently choosing `HEAD~1`, the current branch, or an arbitrary diff.

Infer the reader's existing knowledge from the conversation when possible. Do not require a
background interview before starting; layer the explanation so familiar readers can skip basics.

## Workflow

### 1. Resolve the change boundary

- Inspect the requested comparison and list the changed files.
- Confirm whether generated files, vendored code, lockfiles, or unrelated local edits are in scope.
- Pin remote PR analysis to freshly inspected base and head identities.
- State any surface that cannot be inspected.

### 2. Reconstruct the relevant system

- Trace changed symbols to their callers, consumers, tests, configuration, and data boundaries.
- Explore only the surrounding code needed to understand the change.
- Use `jy-codebase-explore` when it is available and the path crosses multiple unclear modules.
- Separate source facts from inference, and support important claims with `file:line`, commit, or
  protocol evidence.

### 3. Teach the core intuition

- Explain the previous behavior first.
- State the change's goal in one or two plain sentences.
- Give one concrete toy example with realistic inputs, state transitions, or data.
- Explain the key invariant or tradeoff before implementation details.

### 4. Walk through the change causally

- Order the walkthrough by execution, data, ownership, or lifecycle flow rather than filename.
- For each step, explain what changed, why it is needed, and what consumes the result.
- Include only code excerpts that materially improve understanding.
- Call out unchanged boundaries when they prevent a misleading mental model.

### 5. State the evidence boundary

- Distinguish inspected source, observed tests or runtime evidence, and unresolved assumptions.
- Explain what the available evidence demonstrates and what it does not demonstrate.
- Do not convert a plausible explanation into a test, safety, performance, or merge claim.

### 6. Check understanding

- Write five medium-difficulty questions that require understanding the substance of the change.
- Test causal behavior, invariants, tradeoffs, failure modes, or ownership; avoid trivia and gotchas.
- In chat, withhold the answer key and ask the user to explicitly invoke
  `$jy-explain-change` again with their answers for grading.
- When the user explicitly requests a standalone artifact, keep answers collapsed or otherwise
  hidden until selected.

## Output Contract

Use this structure, scaling each section to the size and risk of the change:

1. **Change Scope** - the exact comparison and relevant surfaces inspected.
2. **Background** - the minimum prior-system context needed by the reader.
3. **Core Intuition** - goal, concrete example, invariant, and important tradeoff.
4. **Causal Walkthrough** - the change in an understandable behavioral order.
5. **Evidence Boundary** - verified facts, inferences, and unknowns.
6. **Understanding Check** - five questions without an exposed answer key.

Keep a tiny change compact. Do not turn a config, typo, or one-line behavior change into a generic
textbook. Use a diagram or interactive visualization only when it materially clarifies a
relationship that prose and a small example cannot.

## Boundaries

- The explanation does not establish correctness, safety, test coverage, or readiness to merge.
- Do not return PASS/FAIL, SHIP/BLOCK, or approval language from this workflow.
- If the user also requests review or QA, keep that as a separate `jy-review-work` workflow when
  available.
- If the user also requests a completion claim, require the separate
  `jy-verification-before-completion` workflow when available.
- Do not run tests, builds, or live systems merely to enrich the explanation unless the user
  explicitly adds verification to the request.
- Do not create HTML, Notion pages, documents, or repo artifacts unless the user explicitly asks
  for that output and supplies or approves the destination.
- Do not expose secrets, credentials, or private source outside the authorized workspace.
