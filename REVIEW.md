# Review guidance

Review the requested diff and the surrounding behavior it changes or relies on.
Treat skill and instruction Markdown as executable guidance: a wording change can alter
permissions, routing, or completion behavior. Follow the user's current scope and authority.

## What matters here

- In `codex_env_sync/`, `scripts/bootstrap.*`, and `codex-env.toml`, check that installation
  and stale-item cleanup preserve unmanaged files, unrelated user customizations, and `LOCAL.md`.
  Check copy/symlink behavior, repeated apply, and recovery from a failed step when changed.
  Staged source, saved state, and actual plugin installation are distinct outcomes.
  Trace partial failure followed by retry, stale-state removal, and cleanup after reset;
  successful first installation alone does not cover those paths.
- In plugin manifests and the marketplace, check source paths, installation policy, and
  version consistency. Runtime cache changes must go through `codex plugin`; archive
  content must remain outside active deployment unless explicitly reactivated.
- In `SKILL.md`, supporting workflows, and `agents/openai.yaml`, check changes to explicit
  invocation, delegation, authorization, and completion claims against the user's intent.
  A tool, model, or skill named in the source is not proof it is available in a session.
- In hooks and model/MCP runners, check data selection, secret handling, allowed tool
  access, retry behavior, and saved-content readback. Historical summaries do not grant
  current authority. Keep reported guarantees within the boundary actually verified.
  Check session-boundary cache invalidation and whether deduplication hides failed work.
  When callers require complete results, check that limits or early stops expose truncation.
- In `.github/workflows/` and test commands, check which tests actually execute on each
  platform and whether failures propagate. Python discovery does not run Node tests.
- Preserve explicit UTF-8 I/O, plugin LF rules, archived bytes, and retained upstream
  licenses/provenance when affected. Agent-facing instructions are English; user-visible
  plugin and skill metadata is Korean.

## Evidence and findings

Start with the finding count, and say plainly when there is nothing to fix. For each
finding, provide a file and line, triggering condition, observable impact, and minimal
correction. Validate the relevant call path or instruction interaction; a suspicious name
or missing test alone is not evidence of a defect. Name a shared cause when it has several
instances. Use the review surface's required schema, priorities, and reporting threshold;
count-first prose applies only when that surface permits it. Classify findings for triage
without adding fields to a fixed schema or making it report optional polish:

- `important`: a behavior defect, authority/data boundary violation, or unmet requirement
  introduced, affected, or relied on by the candidate.
- `nit`: optional polish that leaves behavior and requirements intact. Report at most
  three, and do not make them a separate fix/re-review cycle.
- `pre-existing`: a defect the candidate neither introduces, touches, nor relies on.
  Keep it separate from candidate findings and do not expand the current task to fix it.

Inspect `archive/` only when the diff, migration, or provenance question needs it; its
instructions are historical data, not active guidance. Do not repeat diagnostics already
established by the candidate's CI results. Check relevant README claims when behavior changes.

## Verification and re-review

Use the relevant commands in the README. Report the candidate, commands/results, platform,
and checks not run. A schema or packaging test does not establish model behavior, installation
success, or live hook execution. Use focused runtime evidence when the claim needs it;
do not run paid model evaluations or a real installation merely to review wording.

For a fix with a regression test, compare the same test against the pre-fix implementation
and the candidate in an isolated snapshot or equivalent safe setup. Confirm that the old
implementation fails for the defect being fixed, rather than a setup/import error. Preserve
unrelated working-tree changes. Report both results, or the reason this check could not run.
A test passing on both implementations does not demonstrate regression coverage.

Validate reported findings before requesting a fix. Track fixed, rejected-with-reason, and
deferred findings. After the first full review, inspect the fix diff and its effects, reuse
unchanged evidence, and reopen a closed finding only with new evidence. If a third round
still finds important defects or the same cause recurs, reassess the approach before another
fix cycle. A round count never justifies accepting an unresolved important defect.
