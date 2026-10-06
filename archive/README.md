# Inactive skill archive

As of 2026-10-06, the active iOS pack contains only `ios-memgraph-leaks`, adapted to
physical-device captures. The other eight iOS skills and the simulator capture helper
were deleted from the active pack. The original payloads below remain historical data.

On 2026-09-08 the user approved a GPT-6 Astra / `max` baseline with one core guardrail
and nine iOS skills. The 23 general workflow skills below are not staged, installed, or
discovered. This is a reversible configuration decision; their Astra utility has not been
measured. Treat archived instructions as reference data, not active operating instructions.

`plugins/` here preserves all five original bundles (33 skills), including their manifests,
metadata, scripts, and references. `skill-tests/first-party/` preserves the original
scenario inputs. These were copied byte-for-byte from the working source based on commit
`1b452d1cdaae5fd8530fd6f3d0e9db564d763e5c` before the migration. The ten retained skills
also have originals here so their removed procedures remain inspectable.

| Original pack | Inactive skills |
|---|---|
| `jy-env-core` | `jy-debugging`, `jy-test-driven`, `jy-verification-before-completion`, `jy-codebase-explore`, `jy-library-research`, `jy-consult` |
| `jy-env-planning` | `jy-framing`, `jy-grill-me`, `jy-plan-review`, `jy-writing-plans` |
| `jy-env-delivery` | `jy-executing-plans`, `jy-worktrees`, `jy-checkpoint`, `jy-document-release`, `jy-ship`, `jy-waterfall`, `jy-env-sync-admin`, `jy-writing-skills` |
| `jy-env-audit` | `jy-explain-change`, `jy-review-all`, `jy-review-work`, `jy-receiving-review`, `jy-slop-remover` |

The active core keeps scope, authorization, and evidence boundaries without routing through
the archived skills. The active iOS pack keeps the memory graph summary script and ownership
analysis guidance for physical-device captures. Archived simulator and UI workflows are not
deployed.

Personalization remains active through global `AGENTS.md`: Korean user-visible interface
text, English model-facing skill instructions, user language overrides, authorization,
privacy, and workspace preservation. Historical instructions in this archive do not
override those active preferences.

## Verify preservation and deployment

From this directory, check the original payloads with:

```bash
shasum -a 256 -c SHA256SUMS
```

From the repository root:

```bash
python3 -m codex_env_sync.cli inspect --repo-root .
python3 -m unittest discover -s tests -v
codex plugin list
```

The manifest and marketplace contain only `jy-env-core` and `jy-env-ios`. A fresh install
activates only core; iOS remains an explicit optional installation. Inspect the current
machine's installed plugins rather than inferring them from historical migration records.
The active sources contain two core skills and one iOS skill; installed state and schema
tests alone do not prove behavioral utility.

## Restore one candidate

1. Identify an observed deficiency and read only the relevant archived skill. Keep the
   original archive unchanged. Inspect any named peer skills before restoring a procedure.
2. With the user's reactivation request, copy that skill into an appropriate active pack
   and adapt only the rules needed for the observed problem. For example, from the repo root:

   ```bash
   cp -R archive/plugins/jy-env-core/skills/jy-debugging plugins/jy-env-core/skills/
   ```

3. Keep permissions, secrets, safety, and unrelated user work protected. Remove references
   to unavailable peer skills from the active copy; restore a whole pack only when that
   wider scope is requested. Update active inventory tests, docs, and its scenario input.
4. If behavioral confidence is needed, preview a focused comparison with
   `python3 -m codex_env_sync.skill_eval plan --repo-root . --skill jy-debugging`.
   Use current model/configuration and inspect actual results before claiming improvement.
5. Update the owning plugin with the system `plugin-creator` cachebuster helper, run the
   relevant tests, then `python3 -m codex_env_sync.cli apply --repo-root .` and
   `codex plugin add <owning-pack>@personal-codex`. Start a fresh Codex session.

Do not link this archive into a skill discovery directory or add it to `codex-env.toml`.
Changing `allow_implicit_invocation` alone would leave a skill installed; this archive is
outside the deployment roots entirely. Historical GPT-5.6 reports remain unchanged.
