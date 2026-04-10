# Portable Codex Environment Sync

This repo defines a portable Codex working environment.

It is not trying to reproduce an entire machine. It only syncs the parts that make
Codex behave the same way everywhere:

- first-party local plugin bundles
- plugin marketplace entries
- generated global instruction artifacts
- first-party Codex skills authored directly inside the installed plugin bundle

The install surface is intentionally small:

- plugins are installed into `~/plugins`
- skill discovery links are installed into `~/.agents/skills/`
- marketplace is written to `~/.agents/plugins/marketplace.json`
- instructions are installed into `~/.codex/...`
- Codex runtime cache under `~/.codex/plugins/cache` is left alone

The current manifest uses symlinks on macOS and Linux so a later `git pull` updates the
installed plugin bundle and global instructions without re-copying. Windows keeps copy mode
via platform override.

Repo-local working state that should not be committed can live under `.codex/`.
The first such path is `.codex/checkpoints/`, used by the first-party `codex-checkpoint`
skill for session handoff notes.

Authoring references that support local skill development can live in `references/`.
They are part of this repo for maintenance work, not part of the installed Codex surface.

First-party skill authoring happens in `plugins/codex-env-core/skills/`. That directory is
the source of truth for both local development and the installed Codex skill surface.
The current first-party workflow pack covers planning, debugging, test-first implementation,
review, and verification disciplines.

## Secret handling

MCP server definitions can live in committed plugin bundles.

Secret values should not.

If an MCP server needs API keys or account tokens, keep those in local machine config or
another local-only secret layer. This repo should only commit the portable server
definition.

For plugin-managed MCP secrets, use a local-only overlay file:

- `~/.codex-env-sync/local/plugins/codex-env-core.mcp.json`

Example:

```json
{
  "mcpServers": {
    "korean-law": {
      "env": {
        "LAW_OC": "your-token-here"
      }
    }
  }
}
```

`apply` and `bootstrap` merge that file into the installed plugin bundle at `~/plugins/...`.
The repo copy stays secret-free.

## First run

macOS / Linux:

```bash
./scripts/bootstrap.sh <git-url>
```

Windows PowerShell:

```powershell
.\scripts\bootstrap.ps1 -GitUrl <git-url>
```

## Local development

Inspect the environment defined by this repo:

```bash
python3 -m codex_env_sync.cli inspect --repo-root .
```

Apply the local checkout into your home directory:

```bash
python3 -m codex_env_sync.cli apply --repo-root .
```

On macOS and Linux, that creates symlinks for the repo-managed plugin bundle, skill
discovery surface, and instructions. A later `git pull` in the same checkout updates the
installed Codex surface immediately.

## Layout

```text
codex-env.toml                 # Minimal manifest: plugins + instructions + platform overrides
codex_env_sync/                # Apply engine and CLI
plugins/                       # First-party plugin bundles that get installed into ~/plugins
plugins/codex-env-core/skills/ # First-party Codex skills, authoring source and install source
instructions/                  # Generated instruction artifacts
references/                    # Local authoring references used while building first-party skills
.codex/checkpoints/            # Repo-local ignored checkpoint notes created by codex-checkpoint
.agents/plugins/               # Repo-local marketplace metadata for local plugin discovery
.agents/skills/                # Home install target for Codex native skill discovery
scripts/bootstrap.sh           # First-run shell bootstrap for macOS/Linux
scripts/bootstrap.ps1          # First-run shell bootstrap for Windows
tests/                         # Unit + integration tests
skill-tests/                   # First-party skill verification packs (baseline + pressure scenarios)
```

## Design boundaries

- Upstream open source or company skills are seed material only.
- Raw seed sources normally stay local and are not committed here.
- Curated authoring references that we actively use to build first-party skills may be vendored under `references/`.
- First-party Codex skills are authored directly in `plugins/codex-env-core/skills/`.
- This repo does not keep vendored upstream runtimes as part of the maintained execution surface.
- Repo-local checkpoint notes belong under `.codex/checkpoints/` and stay gitignored.
- What gets committed here is the first-party result after customization.
- Re-running apply should be fast and mostly quiet when nothing changed.

## Tests

Run locally:

```bash
python3 -m unittest discover -s tests -v
```

For first-party skill verification assets and static coverage, see `skill-tests/first-party/`
and run:

```bash
python3 -m unittest tests.test_skill_scenarios -v
```
