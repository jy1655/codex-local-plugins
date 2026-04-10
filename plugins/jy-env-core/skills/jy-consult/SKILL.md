---
name: jy-consult
description: Use when facing architecture decisions, repeated fix failures, or security/performance concerns that need deep strategic analysis.
---

# JY Consult

## Overview

Provide strategic technical advice for complex decisions, repeated failures, and
security or performance concerns. Analyze and recommend. Do not modify code.

## When to Use

- An architecture decision has meaningful tradeoffs across systems
- Two or more fix attempts have already failed
- There is a security or performance concern
- The code pattern is unfamiliar and the risk is high
- A large implementation needs a deeper self-review before continuing

Do not use it when:

- The task is a simple file edit
- No real attempt has been made yet
- The answer can be read directly from the code
- The question is trivial, such as naming or formatting

## Quick Reference

| Situation | Consultation Focus |
|-----------|--------------------|
| Architecture decision | Tradeoffs, long-term impact, recommended path |
| Repeated fix failure | Root cause, missed assumptions, alternative approach |
| Security/performance concern | Risk surface, mitigation, priority |
| Self-review | Design gaps, edge cases, missing considerations |

## Consultation Protocol

### 1. Gather context

Include:

- the current situation and attempted approaches
- relevant code or diff
- constraints such as stack, compatibility, or timeline
- the exact decision or question

### 2. Structure the analysis

```
Problem: what must be decided or resolved
Current state: what has been tried and what happened
Options: realistic approaches with pros and cons
Recommendation: the preferred path and why
Risks: known downsides and mitigations
Next steps: concrete follow-up actions
```

### 3. Make the advice usable

- Recommendations should be concrete and actionable
- Do not stop at "it depends"
- Also say why someone might disagree with the recommendation

## Common Mistakes

- Starting implementation instead of staying in advisory mode
- Asking for strategic consultation before making a reasonable first attempt
- Asking abstract questions without code or constraints
- Ending with "there is no right answer" and no recommendation
- Asking questions that the codebase can already answer directly
