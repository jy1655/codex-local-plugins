# Making Rule Skills Hard to Rationalize Away

Rule-enforcing skills such as TDD, verification-before-completion, or plan-first workflows
must resist rationalization under pressure. Agents are capable and will look for loopholes
when speed, sunk cost, fatigue, or authority pressure pushes them there.

## 1. Ban the loopholes explicitly

Do not only state the rule. Also state the most likely escape hatches.

Bad:

```markdown
Code without writing the test first? Delete it.
```

Better:

```markdown
Code without writing the test first? Delete it. Start again.

No exceptions:
- do not keep it "as reference"
- do not adapt while writing the test
- do not keep reading it "just for context"
- deletion means deletion
```

## 2. Defend against "spirit vs. letter"

Add the principle up front:

```markdown
Violating the letter of the rule violates the spirit of the rule.
```

That blocks the whole class of "I followed the spirit" rationalizations.

## 3. Keep a rationalization table

Capture the exact excuses from baseline testing:

| Rationalization | Reality |
|-----------------|---------|
| "This is too simple to test" | Simple code still fails. The test usually costs seconds. |
| "I'll write the test later" | Later testing does not prove the current step. |
| "Writing the test afterward reaches the same goal" | Test-first asks what behavior is needed. Test-after asks what the code already does. |

## 4. Maintain a Red Flags list

Give the agent a compact self-check:

```markdown
Red Flags — stop and restart

- code before test
- "I already tested it manually"
- "writing the test after the code is equivalent"
- "the spirit matters more than the form"
- "this is different because..."

All mean the same thing: delete the code and restart with TDD.
```

## 5. Put violation signals into the description

The description should include the signals that tell Claude the rule is about to be broken.

Example:

```yaml
description: Use when implementing a feature or bug fix and stop if code already exists before the failing test.
```

## Anti-Patterns

### Narrative examples

"In the 2025-10-03 session we had an empty projectDir..."

Why it is bad: too specific and not reusable.

### Multi-language dilution

If the same rule is repeated in several languages inside the core model-facing surface,
quality usually drops and maintenance cost rises.

### Code inside a flowchart

Why it is bad: hard to scan, hard to copy, and hard to reuse.

### Generic labels

Labels should carry meaning. `step1` and `helper2` do not.

## Capture excuse patterns from testing

When you run baseline tests, record the agent's exact wording.

Do not ask "Why are you skipping the test?" up front. Instead, listen to what the agent says naturally:

- "This part is obvious"
- "I'll test later"
- "I already checked it mentally"
- "I followed the spirit"

Capture those phrases exactly. They are the evidence that the skill must counter.
