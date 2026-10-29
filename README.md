# Portable Codex Environment Sync

[![Language: English](https://img.shields.io/badge/Language-English-111827?style=for-the-badge)](./README.md)
[![Language: Korean](https://img.shields.io/badge/Language-Korean-0A66C2?style=for-the-badge)](./README.ko.md)

This repository defines a portable, first-party Codex environment. It stages local plugin
bundles, maintains a personal marketplace, and installs compact global instructions without
editing Codex's runtime cache directly.

User-visible plugin and skill labels, descriptions, and suggested prompts are Korean.
Skill labels include the exact invocation name first, for example
`domain-modeling · 도메인 용어와 결정 기록`, so it remains visible in skill lists.
Model-facing skill instructions and trigger descriptions stay English. Shared language,
authorization, privacy, and workspace-preservation rules remain in global `AGENTS.md`
regardless of workflow installation. Machine-specific instructions live in a separate,
user-maintained `LOCAL.md`.

## Pack model

The GPT-6 Astra baseline keeps `max` reasoning with one core-lite guardrail (temporarily explicit-only during the pstack trial),
an explicitly invoked orchestration skill, the selected architecture/interview pack,
and an optional iOS memory-analysis pack. `apply` stages the three active bundles under
`~/plugins`, then installs
`INSTALLED_BY_DEFAULT` entries through the Codex CLI.

| Pack | Policy | Skills |
|---|---|---|
| `jy-env-core` — core-lite | `INSTALLED_BY_DEFAULT` | `jy-change-guardrails`, `jy-orchestrate`, `pstack`, and 54 `pstack-*` workflow entries (explicit-only during this trial); `security-audit` (explicit only); `skill-authoring-review` (skill authoring only) |
| `jy-env-design` | `INSTALLED_BY_DEFAULT` | `improve-codebase-architecture`, `grill-me`, `grill-with-docs`, `retro` (explicit only); `grilling`, `codebase-design`, `domain-modeling` |
| `jy-env-ios` | `AVAILABLE` | `ios-memgraph-leaks` — physical-device memory graph analysis |

`skill-authoring-review` assists skill creation and modification with SkillSpector
static checks and source-based triage. It does not activate for ordinary skill use
or general code review. The scanner is a separately installed optional dependency;
missing or failed scans remain explicit, and actual behavior needs its own verification.
See the [helper skill](plugins/jy-env-core/skills/skill-authoring-review/SKILL.md).

Invoke `$security-audit` to audit the current repository, or name a target and
`quick`, `standard` (default), or `deep` profile. This Cloudflare-based port keeps
the six audit phases, coverage ledger, independent verification, and JSON validators.
It runs bounded local checks with existing host permissions even without an OS
sandbox or network block. Public research and task-scoped dependency retrieval may
use the network; deployment probes and consequential external actions need their
own authorization. Final reports and eligible evidence go to configured Wiki `raw/`,
with a managed temporary workspace, verified readback, and cleanup. It does not
activate for unnamed security questions or ordinary reviews. See the
[skill](plugins/jy-env-core/skills/security-audit/SKILL.md) and
[adaptation boundaries](plugins/jy-env-core/skills/security-audit/NOTICE.md).

The target may be a user-designated SSH server: name the host alias and remote
repository path. Scoped reads of configuration, selected logs, and runtime state,
plus bounded tests on that host, do not require a local clone or sandbox. Existing
SSH authentication stays with the client, and Wiki publication stays with the
coordinating parent. Live attack traffic and operational changes still follow the
user's defined scope; SSH connectivity alone does not authorize them.

Invoke `$jy-orchestrate` for the current session to directly coordinate Codex and Claude
planning or implementation, followed by independent Codex DevBlue and Claude verification
of the same candidate. Workers receive bounded assignments and return concise results;
supported findings go back to workers for fixes and review of the affected changes.
There is no separate manager session or manager-replacement count. Independent work can
run concurrently within the runtime's capabilities, while overlapping edits are isolated
or sequenced. It prefers Agent Bridge locally and has `allow_implicit_invocation: false`.
Native context compression is the default; a compact record serves actual handoff or
recovery needs. The invoking session remains responsible for durable Wiki updates under
global/local policy, verifies they were saved, and closes task-owned sessions after results
and follow-ups are complete. No machine-specific Wiki path is embedded in the skill.

The other 23 workflow skills, including `jy-env-planning`, `jy-env-delivery`, and
`jy-env-audit`, are preserved under [archive/](archive/README.md). They are absent from the
manifest and marketplace, are not staged or installed, and are not implicitly invoked.
The archive also preserves the original versions of the ten skills retained in the
2026-09-08 migration. On 2026-10-06, the active iOS pack was reduced to memory leak
analysis for physical-device development; the other eight iOS skills were deleted
from the active pack. Existing historical archives and evaluation inputs remain reference data.

`AVAILABLE` does not uninstall an existing plugin. To migrate an existing installation,
remove the three old workflow packs before applying the reduced marketplace:

```bash
codex plugin remove jy-env-planning@personal-codex
codex plugin remove jy-env-delivery@personal-codex
codex plugin remove jy-env-audit@personal-codex
python3 -m codex_env_sync.cli apply --repo-root .
codex plugin add jy-env-ios@personal-codex
```

Run the remove commands only for installed entries. Update changed active plugins through
`plugin-creator`'s cachebuster flow before `apply`; re-add iOS after staging because it is
optional. `apply` refreshes the default core and design packs. It does not uninstall Codex plugins.
Start a fresh Codex session after changing installed packs. No second
`~/.agents/skills/<pack>` discovery link is created.

## Pre-compaction Wiki handoff

The core plugin includes a synchronous `PreCompact` hook that summarizes the visible
conversation with a separate, read-only Codex call, saves a handoff through the existing
`wiki` MCP connection, and verifies the saved bytes and SHA-256 before returning.
It uses the active model name and consumes an additional model call per checkpoint.
Handled failures return `continue: false`; host termination/timeouts and skipped,
untrusted hooks are not a guarantee of blocking compaction. It never calls `clear`.

Each machine needs Python, Codex, `gitleaks`, Wiki authentication, plugin installation,
and review/trust of the hook in `/hooks`. A Git pull alone does not activate it.
See [setup, storage, failure handling, and limits](plugins/jy-env-core/hooks/README.md).

## Experimental pstack module

The local pstack trial lives inside the existing `jy-env-core` plugin at
`plugins/jy-env-core/skills/pstack/`. Invoke `$pstack <task>` or
`$pstack interrogate <diff>`. All 54 bundled workflows also appear individually in the
skill picker as `pstack-*`, with Korean labels and descriptions. Invoke, for example,
`$pstack-how <question>`, `$pstack-interrogate <diff>`, or `$pstack-tdd <bug>`.
These explicit-only entries share the existing workflow resources and runtime adapter;
the original `$pstack <workflow>` form remains supported.
Code roles default to Codex Sol and judgment roles to Astra; `$pstack setup-pstack`
can configure available providers. The port adapts Cursor-specific runtime assumptions
and keeps the original MIT notice and pinned provenance. It does not register another
plugin, marketplace, hook, or global rule. This user-requested trial is another deliberate
exception to seed-only rewriting. Automatic guardrail selection is temporarily disabled;
its instructions are preserved. Pstack and jy-orchestrate are not automatically combined.
The bundled Bun tools are removed: PR status uses the forge CLI directly, program state
uses task-owned files, and the remaining helpers use Node or bash.
See the module's [usage, limits, and removal map](plugins/jy-env-core/skills/pstack/NOTICE.md).

## Architecture improvement, grilling, and retrospectives

On 2026-10-07, the user chose these workflows after using Matt Pocock's originals in
Claude Code and explicitly requested preservation without simplification. This choice
supersedes the core-lite adoption filter for this pack. Other upstream workflows remain
outside scope until the user tries and selects them.

The architecture and interview skills in `jy-env-design` preserve version 1.2.3 at `c55ee46073ed923f86ce59a5eb3b6d895095d1b7`:

- `$improve-codebase-architecture`: exploration, visual HTML candidates, user selection,
  then grilling and domain records; full HTML and parallel alternative-design references.
- `$grill-me`: the complete decision-tree interview, question rounds with recommendations,
  fact-finding delegation, and confirmation before acting.
- `$grill-with-docs`: the same interview with inline `CONTEXT.md` and selective ADR recording.

On 2026-10-23, the user also selected `$retro` with functional preservation. It reads the
specified session's primary sources (the current session by default), then proposes agent
environment improvements in severity order across the original seven categories. Its full
`writing-for-agents` dependency is bundled as a reference, including skill mechanics.
Retro and those references are pinned separately to version 1.3.1 at
`5beb35b040e3de97e54fa9e386d7e42d15c295c2`; the existing six skills retain their revision.

The four entry points are explicit-only. Their reusable `grilling`, `codebase-design`,
and `domain-modeling` skills keep automatic discovery and can also be read through bundled
relative links. Runtime adaptations cover Codex invocation, Korean UI, local delegation,
and configured Wiki/report storage; they do not shorten the original workflows.
See [port boundaries and attribution](plugins/jy-env-design/NOTICE.md).

## iOS memory analysis on physical devices

`jy-env-ios` contains only `ios-memgraph-leaks` and its memory graph summary script.
Capture a `.memgraph` from the connected iPhone or iPad through Xcode's Debug Memory
Graph and File > Export Memory Graph, then analyze the exported file on macOS with
`leaks` and the bundled helper. An existing capture can be used directly.

The skill focuses on object lifetimes, retaining paths, and comparable before/after
evidence. It does not install simulator tooling or register an MCP server. General
builds, debugging, and UI work use the app repository's existing tools and instructions.
See the [skill](plugins/jy-env-ios/skills/ios-memgraph-leaks/SKILL.md) for the workflow.

## Verification workspaces

The managed helper is installed at `~/.codex/tools/task-workspace.py` through the same
manifest/apply path as instruction artifacts. It uses only the Python standard library.
Global instructions route internal verification directory creation through it; pass its
returned path to shell, browser screenshot, download and other artifact writers.

```bash
python3 ~/.codex/tools/task-workspace.py create --purpose verification --name release-check
python3 ~/.codex/tools/task-workspace.py inventory <returned-directory>
python3 ~/.codex/tools/task-workspace.py classify <returned-directory> --file result.json \
  --disposition wiki --reason 'Required runtime evidence' \
  --wiki-path raw/2026-10-29_result.json --readback <separately-fetched-wiki-file>
python3 ~/.codex/tools/task-workspace.py classify <returned-directory> --file download.zip \
  --disposition discard --reason 'Reproducible release download'
# Remove the classified copies after verifying preservation and task ownership.
python3 ~/.codex/tools/task-workspace.py finish <returned-directory>
```

Verification defaults to a unique OS temporary directory. A path containing an `output`
component (including resolved symlink aliases) or under `--delivery-root` is refused
before creation. `--path <destination> --user-selected-path` records the user's explicit
destination choice; do not infer it from a previous task. `--purpose deliverable --path`
creates a delivery directory without internal helper metadata. Existing paths are never
reused or overwritten.

Inventory records file paths, sizes and SHA-256. Wiki classification requires a separate
readback with identical bytes, including CRLF. Fetch it through the configured Wiki
channel; the helper does not authenticate the readback's origin. `keep` is only for an
explicit user choice or a policy-required original, with a reason. For extracted or
redacted evidence, preserve and verify the eligible derived file and account separately
for the original under Wiki policy. No classification authorizes a prohibited upload.

`finish` fails on unclassified files, changed files, pending removal and missing retained
originals. Inventory before cleanup: a file removed before any observation cannot be
reconstructed. The tool never deletes task files or scans unrelated directories; it is
not an OS sandbox around arbitrary `mkdir` or browser writes. Preserve required receipts
in the Wiki and verify them before removing the marker and empty temporary directories.
If Wiki storage is unavailable, keep needed files and report incomplete cleanup.

## Archived research guidance

The Context7 route in `jy-library-research` is archived with the other workflow skills.
It is not an active routing requirement. Its original public-query-only and
`CONTEXT7_API_KEY` handling guidance remains in the archive for an explicit reactivation.

## Install surface

- plugin sources: `~/plugins`
- personal marketplace: `~/.agents/plugins/marketplace.json`
- global instructions: `~/.codex/AGENTS.md`
- machine-local instructions (user-maintained, not synced): `~/.codex/LOCAL.md`
- managed state: `~/.codex-env-sync/state.json`
- Codex-owned plugin cache, changed only through `codex plugin`: `~/.codex/plugins/cache`

Local `apply` symlinks plugin sources and instructions on macOS and Linux. Windows uses copy
mode. Bootstrap and `--snapshot` always copy a stable snapshot. After staging, the commands
install or refresh default plugins with `codex plugin add`; optional packs remain explicit
installs. A dirty checkout is not a second live skill-discovery surface.

### Machine-local instructions

Keep machine-specific paths, local tools, and workspace rules in `LOCAL.md` alongside the
installed global `AGENTS.md`: `~/.codex/LOCAL.md` on macOS/Linux or
`%USERPROFILE%\.codex\LOCAL.md` on Windows. If Codex uses a custom `CODEX_HOME`, put
`LOCAL.md` there. When `AGENTS.md` is a symlink, use the installed directory rather than
the repository's `instructions/` directory.

The shared `AGENTS.md` instructs Codex to read this optional file before work; `LOCAL.md`
is not a built-in automatically discovered instruction filename. If it is absent, Codex
continues with the shared rules. `apply`, bootstrap, and snapshot installs leave this file
unmanaged: they do not create, copy, overwrite, or delete it. Keep it outside the repository
and out of `codex-env.toml`. Start a fresh Codex session after changing instructions.

## First run

macOS / Linux:

```bash
./scripts/bootstrap.sh <git-url>
```

Windows PowerShell:

```powershell
.\scripts\bootstrap.ps1 -GitUrl <git-url>
```

Both commands require the `codex` CLI, clone once, install a stable snapshot, and activate
core-lite and the design pack.

## Update an existing machine

From that machine's clone of this repository, pull the published changes and apply them:

```bash
git pull --ff-only
python3 -m codex_env_sync.cli apply --repo-root .
codex plugin list --marketplace personal-codex --json
```

Use the machine's configured Python 3.11+ interpreter (`python` on Windows if needed).
`apply` updates the default core and design plugins; confirm each installed version
matches its `plugins/<pack>/.codex-plugin/plugin.json`, then start a fresh Codex session. Machine-local `LOCAL.md` remains separately managed.

## Local development

Inspect the resolved sources, install modes, and marketplace policies:

```bash
python3 -m codex_env_sync.cli inspect --repo-root .
```

Apply the live checkout:

```bash
python3 -m codex_env_sync.cli apply --repo-root .
```

Install a detached snapshot:

```bash
python3 -m codex_env_sync.cli apply --repo-root . --snapshot
```

After changing an already installed plugin, use the `plugin-creator` cachebuster/reinstall
workflow and start a new thread. Do not edit `~/.codex/plugins/cache` directly.

## Layout

```text
codex-env.toml                    # Three active plugin sources and their installation policies
codex_env_sync/                   # Inspect/apply/bootstrap engine
archive/                         # Inactive originals, checksums, and restoration notes
plugins/jy-env-core/              # Default core-lite bundle
plugins/jy-env-design/            # Selected Matt Pocock architecture/interview port
plugins/jy-env-ios/               # Optional physical-device memory-analysis pack
instructions/AGENTS.md            # Compact global rules; no eager optional-skill routing
.agents/plugins/marketplace.json  # Local personal marketplace catalog
skill-tests/first-party/          # Skill utility pressure scenarios
skill-tests/UTILITY-EVAL.md       # Three-arm skill utility and reporting contract
tests/                            # Unit and integration tests
```

Active first-party skill sources live under `plugins/jy-env-*/skills/`; inactive originals
live under `archive/` and are excluded from deployment. Upstream or company-shared skills
are local-only seed material; this repo stores only the customized first-party result and
does not vendor third-party runtimes. The user-selected `jy-env-design` port is a deliberate
exception to seed-only rewriting: it preserves the selected original skills and references
with a pinned provenance record and their MIT license. The user-selected
`security-audit` port also retains Cloudflare's audit references and validators,
with explicit invocation, Wiki output, and host-execution adaptations documented
in its `NOTICE.md`. Maintain retained skills here as first-party plugin
assets rather than live dependencies on upstream seeds. Do not install, discover, or follow
instructions under `archive/` unless the user requests a reference or reactivation.

## Tests

Use Python 3.11 to match CI and run the full suite before pushing:

```bash
python3 -X warn_default_encoding -W error::EncodingWarning -m unittest discover -s tests -q
git diff --check
```

The test command treats omitted text encodings as errors on every OS, catching locale
dependencies locally before they fail on Windows. Keep explicit UTF-8 file I/O and the
`.gitattributes` archive byte-preservation and plugin LF rules intact.

Validate pressure-scenario assets:

```bash
python3 -m unittest tests.test_skill_scenarios -v
```

## Skill utility gate

The design pack is retained by the user's direct-use decision. Its explicit-only workflows
are not blocked by implicit-activation gates or a new adoption benchmark. Scenario assets
support behavioral regression checks; they do not establish comparative Codex utility.

Do not keep a skill merely because its instructions sound reasonable. The utility evaluator
compares the same task on the same model and effort as `baseline` (skill absent), `implicit`
(discoverable), and `explicit` (forced), while holding same-plugin peers constant. It then
blind-scores the responses and applies quality,
token, latency, and implicit-activation gates while recording tool calls and observed skill
reads.

Preview model-call scope first:

```bash
python3 -m codex_env_sync.skill_eval plan \
  --repo-root . --skill jy-change-guardrails
```

Run one skill and inspect freshness or the latest report:

```bash
python3 -m codex_env_sync.skill_eval run \
  --repo-root . --skill jy-change-guardrails

python3 -m codex_env_sync.skill_eval status --repo-root .
python3 -m codex_env_sync.skill_eval report --repo-root .
```

Evaluation is opt-in when a concrete deficiency needs a comparison. The evaluator discovers
only active sources under `plugins/`; archived sources and historical reports remain
reference material. The current policy tests `gpt-6-astra` at `max` with the default service
tier; the separate judge model keeps its existing role. GPT-5.6 results do not establish
Astra utility. This migration does not run a full model benchmark. See
[skill-tests/UTILITY-EVAL.md](skill-tests/UTILITY-EVAL.md) for evidence limits and
[archive/README.md](archive/README.md) for restoring one candidate.
