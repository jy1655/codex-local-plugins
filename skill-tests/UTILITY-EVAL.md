# Skill Utility Evaluation

This line tests whether a first-party skill changes current-model behavior enough to justify
its context, routing, latency, and maintenance cost. Scenario prose alone is not evidence.

## Comparison contract

Every case uses the same task, tested model, reasoning effort, service tier, read-only
sandbox, and isolated temporary home. The evaluator runs three arms in a deterministic
shuffled order:

- `baseline`: the target skill is absent, while its plugin-pack peers remain discoverable;
- `implicit`: the target and the same peers are discoverable and the task prompt is unchanged;
- `explicit`: the same treatment context is present and the target is explicitly named.

Holding pack peers constant measures the target's marginal value in the bundle users actually
install. It catches overlap and routing competition that a target-only comparison would miss.

Codex JSONL supplies token, latency, tool-call, and observed `SKILL.md` read data. A separate
blind judge sees responses labeled only A/B/C and scores them against the scenario contract.
The label mapping is stored only with the post-run artifacts. `KEEP` also requires implicit
activation and stays below the configured token and latency overhead ceilings; quality gain
alone is not sufficient.

The temporary `HOME` and `CODEX_HOME` contain no personal plugins or global `AGENTS.md`;
only the selected target's same-pack peers are copied as first-party controls. The Codex
process receives a small environment allowlist, while
model-spawned shells inherit no parent environment and receive only `PATH`. Saved Codex
authentication is copied into the temporary home for the invocation and is not written to
the report tree. System skills remain present in every arm.

Treat candidate skill source as executable guidance: review it before evaluation. A
read-only sandbox is not a credential vault. For untrusted third-party candidates or an
automated runner, use a dedicated restricted `CODEX_API_KEY` and an isolated account instead
of personal saved authentication. Skill-tree symbolic links are rejected before hashing or
staging so a candidate cannot pull repo-external files into its evaluation context.

## Commands

Preview cost without model calls:

```bash
python3 -m codex_env_sync.skill_eval plan \
  --repo-root . --skill jy-change-guardrails
```

Run the default decision-grade sample: two scenarios, three repetitions, three task arms,
and one batched judge call per skill.

```bash
python3 -m codex_env_sync.skill_eval run \
  --repo-root . --skill jy-change-guardrails
```

Resume an interrupted run with the exact same selection:

```bash
python3 -m codex_env_sync.skill_eval run \
  --repo-root . --skill jy-change-guardrails \
  --resume-run <run-id>
```

Resume reuses only task and judge artifacts whose prompt, discoverable-skill context, blind
label mapping, and successful execution record still match. It retries missing, failed, or
mismatched calls. The current resume path does not pin an in-place Codex CLI update or retain
failed-attempt history, so confirm the CLI version is unchanged; start a new run when the
model, policy, evaluator, or CLI changed.

Evaluate a new source before adopting or installing it:

```bash
python3 -m codex_env_sync.skill_eval run \
  --repo-root . --skill <candidate-skill> --candidate
```

Select skill changes, stale evidence, or a new model baseline:

```bash
python3 -m codex_env_sync.skill_eval run \
  --repo-root . --changed-from origin/main

python3 -m codex_env_sync.skill_eval run \
  --repo-root . --stale

python3 -m codex_env_sync.skill_eval run \
  --repo-root . --all --model <new-model>
```

Check freshness and print the latest report:

```bash
python3 -m codex_env_sync.skill_eval status --repo-root .
python3 -m codex_env_sync.skill_eval report --repo-root .
```

`status` invalidates evidence when the tested model, effort, judge, Codex CLI version,
evaluator implementation, policy, same-pack skill tree, or scenario asset changes. A
same-pack skill edit makes every skill in that pack stale. A one-scenario or one-repetition
smoke run remains stale and cannot refresh decision-grade state.

## Verdicts

- `KEEP`: implicit discovery adds a measured quality gain.
- `ADD_CANDIDATE`: a not-yet-adopted source adds the same gain.
- `REVISE_TRIGGER`: explicit use helps but implicit discovery does not.
- `REVISE_COST`: quality improves, but implicit token or latency overhead exceeds policy.
- `REVISE`: the skill misses the quality floor or regresses behavior.
- `REMOVE_CANDIDATE`: the native baseline passes and neither skill arm adds meaningful gain.
- `REJECT_CANDIDATE`: the same no-gain result for a not-yet-adopted source.
- `INCONCLUSIVE`: evidence volume is adequate, but the tradeoff is not decisive.
- `INSUFFICIENT`: coverage, repetitions, or judge confidence are below the policy floor.

The checked-in policy currently allows at most 25% implicit input-token overhead, 50%
implicit latency overhead, and requires at least 80% implicit `SKILL.md` activation. Change
these values only through `skill-tests/eval-policy.json`; the policy hash invalidates prior
evidence.

No verdict edits, installs, removes, publishes, or enables a skill. Review the raw responses
before acting. `REMOVE_CANDIDATE` is deliberately not `REMOVE`.

Removal recommendations are marginal to the current pack. Remove at most one reviewed skill
at a time and rerun the now-stale pack before considering another; two overlapping skills can
otherwise make each other look individually redundant.

## Artifacts and reporting

Ignored local artifacts live under `.codex/skill-evals/`:

```text
.codex/skill-evals/
|-- state.json
|-- latest.json
|-- latest.md
`-- runs/<run-id>/
    |-- report.json
    |-- report.md
    |-- raw/<skill>/<scenario>/<repeat>/<arm>/
    `-- judge/<skill>/
```

A scheduled or release task can use this stable contract:

1. run `status` with the intended model;
2. when stale, preview cost and run `--stale` or `--all --model <new-model>`;
3. return `report` to the maintainer;
4. make source changes only after the maintainer reviews a candidate verdict.

The repository does not install a scheduler or store credentials in CI. That external
activation needs its own cadence and authenticated runner choice.

## Evidence boundary

Current pressure scenarios primarily evaluate decisions and final responses in an empty,
read-only workspace. This can measure instruction and trigger value, but it does not prove
Simulator, device, build, external-service, or live-runtime behavior. Those skills still need
their task-specific runtime evidence before an add/remove decision.

The model slug and Codex CLI version are detectable. A silent server-side revision behind an
unchanged model slug is not; rerun periodically or when OpenAI announces a model update.
