# Upstream and adaptation boundaries

Adapted from Cloudflare's MIT-licensed `security-audit-skill`, revision
`c1c8a8c1471069fb0e188eeaff69b8e8db6564a8` (2026-09-14).
`LICENSE` preserves the original copyright and terms. `UPSTREAM.json` records
original file paths, sizes, and SHA-256 values, not hashes of adapted files.

The user selected this port on 2026-10-29 for the existing `jy-env-core` plugin.
The six audit phases, domain hunting references, coverage ledger, profiles,
agent budgets, verdict separation, independent validation, schema, and both
validators and their tests are retained. Changes cover:

- Explicit invocation only, enforced by `policy.allow_implicit_invocation: false`,
  a matching entrypoint, and Korean UI metadata.
- Codex-native subagents under host policy, with no implicit Agent Bridge route.
- Durable reports and eligible evidence in configured Wiki `raw/`, using a
  managed temporary workspace, verified readback, manifests, and cleanup.
- Normal host execution for bounded local checks; OS sandbox, external-network
  blocking, read-only mounts, and universal OS quotas are no longer prerequisites.
  Public source research and task-scoped dependency retrieval may use the network.
  User permissions, secret protection, target-source preservation, and separate
  authorization for consequential external work remain in force.
- User-designated SSH servers are valid execution hosts. Scoped read-only runtime
  inspection and bounded remote tests do not require a local clone or remote Wiki
  credentials. Transport and host provenance remain explicit; SSH access alone
  does not authorize active production probes or operational changes.
- Portable parent-side evidence inspection in place of a required descriptor-based
  promotion implementation. Actual containment is disclosed rather than assumed.

This is a maintained adaptation, not an unchanged upstream installation or a
Cloudflare service. Installing it does not install a sandbox, scanner backend,
MCP server, daemon, or hook. Node.js runs the bundled JSON validators; the host
agent and its subagents perform the audit. Validator tests do not establish
audit effectiveness or fresh-session invocation behavior.
