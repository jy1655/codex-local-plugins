---
name: jy-change-guardrails
description: Use when a non-trivial code change needs a simpler first version or risks hidden assumptions, overengineering, unnecessary runtime restrictions, unrelated edits, or repeated verification.
---

# JY Change Guardrails

Preserve the user's core goal, explicit must-haves, and required operating conditions.
Choose the smallest valid change that delivers a useful working result. Do not narrow
the required operating conditions to justify a new guard.
These are decision boundaries, not a required sequence or a reason to invoke other skills.

- Make consequential assumptions and competing interpretations explicit. Resolve routine
  details from the request and current source; ask only when the answer materially changes
  correctness, scope, authority, or a hard-to-reverse outcome. Continue independent work.
- For complex requests, prefer delivering a working smaller version first when it serves
  the core goal. Defer secondary features and briefly state the omissions, practical limits,
  and when to expand. Explicit must-haves or a request for the full version take precedence;
  do not make the user ask for them again.
- Keep the edit boundary tied to the requested outcome. Reuse project conventions and avoid
  unrequested abstractions, configuration, fallbacks, and adjacent cleanup.
- Before writing custom code or adding a dependency, check relevant existing code, standard
  library and platform features, and installed dependencies. Use a suitable existing
  capability when it meets the needed behavior; stop once the choice is clear.
- For bug fixes, trace the affected call paths and fix the evidenced cause at the appropriate
  boundary. A small diff is insufficient if another affected path remains broken.
- Prefer readable one-liners and fewer lines when behavior and clarity are comparable.
  Do not obscure control flow or remove necessary validation, error handling, accessibility,
  or safety measures to save lines.
- For a guard or failure handler you add or change, tie its blocking effect to a current
  requirement, actual security or safety boundary, or evidenced failure. Missing or delayed
  evidence alone proves neither failure nor valid authority. Use the narrowest effect that
  satisfies the requirement.
- Keep failures of auxiliary steps, such as diagnostics or logging, from cancelling valid
  input, rolling back successful work, or tearing down a healthy session unless those steps
  are established prerequisites. Do not suppress core failures while isolating auxiliary
  ones. When a guard causes the problem, reassess its necessity and dependencies before
  adding more checks, limits, or recovery layers.
- Use native session state and context handling first. Add orchestration or persistent
  state when an explicit requirement, concrete handoff boundary, or reproduced failure
  justifies it; keep ownership and lifetime clear.
- Proceed with work already authorized by the user. User instructions take precedence over
  skill guidelines; do not invent another approval or mode-switch procedure. Respect actual
  read-only restrictions, permissions, secret protection, safety invariants, and unrelated
  user work. Do not treat a threshold or mechanism as mandatory merely because it exists,
  is labeled a safeguard, or has a passing rejection test.
- For guards and failure handling you add or change, verify both required rejection and
  continued valid operation against the requested outcome. Include relevant recovery checks
  for actual authorization and stop requirements and for unsafe cached-input replay.
- Select verification proportional to the change. Use current source, relevant tests,
  builds, or runtime readback to support the claim. Reuse results for the unchanged final
  candidate; repeat or broaden checks only after new changes, failures, or unresolved
  concerns. A harmless wording edit does not require a new test or a full build.
- Finish when the delivered scope works and necessary checks are satisfied. Distinguish a
  smaller first version from completion of the full request. Report what the evidence
  establishes, including checks not run. Do not promote a partial test, another agent's
  report, or simulator evidence to proof of a broader runtime or device claim.

In planning or read-only work, provide useful analysis within that boundary and label
implementation and runtime checks as not run.
