# Manual Skill Pressure Scenario Guide

Use pressure scenarios to evaluate changes to triggers, decisions, safety rules, or workflow
behavior. Do not require them for a typo, formatting change, or metadata repair that a
targeted static check can prove.

## What the Repository Proves

`skill-tests/first-party/<skill>/pressure-scenarios.json` stores manual inputs. CI proves
only that each asset exists and follows the schema. A behavioral pass exists only after a
scenario is run against a named model and configuration and its result is recorded.

## Scenario Shape

Each scenario contains:

- `id`: stable identifier within the skill;
- `title`: short pressure case;
- `prompt`: realistic input;
- `expected_without_skill`: likely failure mode;
- `expected_with_skill`: observable target behavior.

Prefer observable decisions over vague language such as "handles this correctly."

## Selecting Pressure

Match pressure to the rule:

- time pressure for verification shortcuts;
- sunk cost for invalid implementation reuse;
- authority pressure for unsafe deference;
- ambiguity for routing errors;
- mode mismatch for planning/execution boundaries;
- publication pressure for git or external side effects.

One strong, realistic pressure is better than a long synthetic prompt. Combine pressures
only for high-risk safety rules with known rationalization paths.

## Manual Evaluation

For a behavior-changing or safety-critical skill:

1. state the behavior being changed;
2. select or add the matching scenario;
3. run the prompt without the revised instruction when a baseline is materially useful;
4. run it with the revised skill;
5. record model, configuration, observed decision, and deviations outside the scenario
   asset;
6. revise the skill only for an observed or strongly evidenced gap;
7. rerun the affected case.

Never backfill a result from expectation text. If the scenario was not run, report it as
not run.

## Static-Only Changes

For metadata, paths, links, formatting, or wording that does not change behavior:

- run the exact schema, link, or compliance test;
- inspect the rendered or discovered surface when relevant;
- skip manual behavioral evaluation unless new evidence shows a trigger or decision changed.
