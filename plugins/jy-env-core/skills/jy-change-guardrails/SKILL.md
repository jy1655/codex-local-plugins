---
name: jy-change-guardrails
description: Use when a non-trivial code change risks hidden assumptions, overengineering, unrelated edits, or unnecessary verification loops.
---

# JY Change Guardrails

Choose the smallest valid change that satisfies the user's request. These are decision
boundaries, not a required sequence or a reason to invoke other skills.

- Make consequential assumptions and competing interpretations explicit. Resolve routine
  details from the request and current source; ask only when the answer materially changes
  correctness, scope, authority, or a hard-to-reverse outcome. Continue independent work.
- Keep the edit boundary tied to the requested outcome. Reuse project conventions and
  avoid unrequested abstractions, configuration, fallbacks, and adjacent cleanup. When the
  user requests broader work, include it in scope and choose the simplest implementation
  that meets that request.
- Use native session state and context handling first. Add orchestration or persistent
  state when an explicit requirement, concrete handoff boundary, or reproduced failure
  justifies it; keep ownership and lifetime clear.
- Proceed with work already authorized by the user. User instructions take precedence
  over skill guidelines; do not invent an additional approval or mode-switch procedure.
  Respect actual read-only restrictions, permissions, secret protection, safety invariants,
  and unrelated user work.
- Select verification proportional to the change. Use current source, relevant tests,
  builds, or runtime readback to support the claim. Reuse results for the unchanged final
  candidate; repeat or broaden checks only after new changes, failures, or unresolved
  concerns. A harmless wording edit does not require a new test or a full build.
- Finish when the requested outcome and necessary checks are satisfied. Report what the
  evidence establishes, including checks not run. Do not promote a partial test, another
  agent's report, or simulator evidence to proof of a broader runtime or device claim.

In planning or read-only work, provide the useful analysis allowed by that boundary and
label implementation and runtime checks as not run. Effort settings govern reasoning;
these guardrails govern observable scope, actions, and completion claims.
