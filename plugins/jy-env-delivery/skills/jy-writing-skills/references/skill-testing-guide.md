# Skill Pressure and Utility Evaluation Guide

Use pressure scenarios to evaluate changes to triggers, decisions, safety rules, or workflow
behavior. Do not require them for a typo, formatting change, or metadata repair that a
targeted static check can prove.

## What the Repository Proves

`skill-tests/first-party/<skill>/pressure-scenarios.json` stores evaluation inputs. CI proves
only that each asset exists and follows the schema. A behavioral result exists only after a
scenario is run against a named model and configuration and its raw responses and scoring
report are retained.

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

## Utility Evaluation

For a behavior-changing or safety-critical skill:

1. state the behavior being changed;
2. select or add the matching scenario;
3. preview the exact scope and model-call count;
4. run the same prompt and model in three isolated arms:
   `baseline` (target absent but same-pack peers present), `implicit` (target and peers
   discoverable), and `explicit` (same treatment context with target named);
5. use the blind judge result plus raw responses, token use, latency, tool calls, and observed
   `SKILL.md` reads to distinguish instruction value from trigger value;
6. revise the skill only for an observed or strongly evidenced gap, then rerun the affected
   case;
7. require at least two representative scenarios and three repetitions before an add/remove
   recommendation. A smaller run is connection smoke only.

From this repository:

```bash
python3 -m codex_env_sync.skill_eval plan \
  --repo-root . --skill <skill-name>

python3 -m codex_env_sync.skill_eval run \
  --repo-root . --skill <skill-name>

python3 -m codex_env_sync.skill_eval status --repo-root .
```

Use `run --candidate --skill <skill-name>` for a not-yet-adopted source. Use
`run --changed-from <git-ref>` after skill edits, `run --stale` after `status` reports drift,
and `run --all --model <new-model>` for a new model baseline. The evaluator fixes model,
reasoning effort, service tier, sandbox, and task prompt across arms; randomizes arm order;
and stores raw JSONL plus Markdown/JSON summaries in `.codex/skill-evals/`.

Interpret verdicts conservatively:

- `KEEP`: implicit discovery produced a measured quality gain.
- `ADD_CANDIDATE`: a not-yet-adopted skill produced the same gain.
- `REVISE_TRIGGER`: explicit invocation helped but implicit discovery did not.
- `REVISE_COST`: the quality gain did not justify measured token or latency overhead.
- `REVISE`: the skill did not reach the quality floor or regressed behavior.
- `REMOVE_CANDIDATE`: the native baseline already passed and neither skill arm added a
  meaningful gain.
- `REJECT_CANDIDATE`: the same no-gain result for a not-yet-adopted source.
- `INCONCLUSIVE` or `INSUFFICIENT`: do not add, remove, or claim utility yet.

No verdict performs plugin installation, source deletion, or publication. Inspect raw
responses before acting. Apply at most one removal at a time and rerun the affected pack so
overlapping skills are not removed together on stale marginal evidence. Current pressure
scenarios primarily test decision responses; tool, device, and runtime claims still need
their task-specific runtime evidence.

Never backfill a result from expectation text. If the scenario was not run, report it as
not run.

## Static-Only Changes

For metadata, paths, links, formatting, or wording that does not change behavior:

- run the exact schema, link, or compliance test;
- inspect the rendered or discovered surface when relevant;
- skip manual behavioral evaluation unless new evidence shows a trigger or decision changed.
