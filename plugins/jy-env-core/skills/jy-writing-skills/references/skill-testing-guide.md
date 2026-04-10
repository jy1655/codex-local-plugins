# Complete Guide to Skill Testing

## Table of Contents

1. Writing Pressure Scenarios
2. Types of Pressure
3. Designing Pressure Scenarios
4. Closing Loopholes Systematically
5. Common Rationalizations and Reality
6. Meta-Test: Is the Test Strong Enough?

## 1. Writing Pressure Scenarios

### Baseline scenario (RED)

Run the scenario without the skill. The goal is to see exactly what fails.

Record:

- what the agent chose to do
- the exact words used to justify it
- which pressure caused the violation

This is the equivalent of "watch the test fail first."

### Skill scenario (GREEN)

Run the same scenario again with the skill available.

Ask:

- does the agent now comply?
- if not, which part of the skill is still insufficient?

## 2. Types of Pressure

For rule skills, combine at least three meaningful pressures.

### Time pressure

"You must finish this in 30 minutes."

Effect: encourages shortcuts and test skipping.

### Sunk cost

"You already wrote 80% of the code. What if you delete it now?"

Effect: encourages reuse of invalid work.

### Authority pressure

"A senior engineer said this test is unnecessary."

Effect: encourages obedience-based rationalization.

### Fatigue

"You have already been working on this for 12 hours."

Effect: reduces careful judgment.

### Obviousness pressure

"This feature is too simple to need a test."

Effect: makes the agent underestimate risk.

## 3. Designing Pressure Scenarios

### Start with single pressure

Use one pressure first and observe how the agent justifies its choice.

### Then combine pressures

Examples:

- time + sunk cost
- time + fatigue
- sunk cost + authority

### Maximum pressure for rule skills

Combine all of the following:

- deadline pressure
- partially written code
- fatigue
- explicit authority pressure

If the agent still violates the rule, the skill still has a loophole.

## 4. Closing Loopholes Systematically

Use this cycle:

1. run the pressure scenario without the skill and record the baseline
2. write the skill section that addresses that exact violation
3. rerun the same scenario with the skill
4. look for new rationalizations
5. add explicit counters
6. retest

That is the REFACTOR phase for skill writing.

### Capture rationalizations precisely

On every test run:

- record the agent's exact words
- analyze why that justification worked
- add an explicit counter to the skill

Rationalization tables help future authors understand why the rule must be stated so explicitly.

## 5. Common Rationalizations and Reality

| Rationalization | Reality |
|-----------------|---------|
| "It is obvious, so no test is needed" | Obvious does not mean correct. Test it. |
| "Keep it as reference" | Keeping the invalid code is the same violation in slower motion. |
| "I followed the spirit" | Breaking the letter breaks the spirit too. |
| "I will test it later" | Later is not evidence. Test now. |
| "I will refactor later" | Refactor comes after passing tests, not instead of them. |
| "I verified it in my head" | Mental verification is not executable evidence. |
| "It is too simple to fail" | Simple code still fails. The test is often cheap. |
| "The senior engineer approved it" | Authority does not cancel the Iron Law. |

## 6. Meta-Test: Is the Test Strong Enough?

The test design itself must be validated.

Ask:

- does the scenario recreate real pressure?
- is the pressure strong enough to trigger shortcuts?
- if the agent complies too easily, is the scenario too weak?

If the test does not surface the likely violation, strengthen the scenario before editing the skill.
