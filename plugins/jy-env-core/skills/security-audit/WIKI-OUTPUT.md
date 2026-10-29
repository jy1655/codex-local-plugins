# Wiki raw output and temporary work

Read this file during full-audit setup and again before final delivery. The
configured private Wiki's `raw/` is the durable output destination. Local files
are working copies, not an alternative completed delivery. Follow the current
global/local Wiki access, eligibility, verification, and cleanup policies.

## Setup and working files

Discover the configured Wiki through host instructions and available tools; do
not embed a machine path, server URL, account, or credential in this skill. Read
its ingest/curation policy. Use the configured verification-workspace helper to
create a task-owned directory, normally:

```sh
python3 "${CODEX_HOME:-$HOME/.codex}/tools/task-workspace.py" create \
  --purpose verification --name security-audit
```

Use its returned path as `<output-dir>` throughout the upstream workflow. Keep
the original filenames and agent subdirectories there so the bundled validators
and independent reviewers can consume them. Do not default to a persistent home
directory or create audit output in the target repository. Follow the host's
alternative workspace policy if the helper is unavailable; report the limitation.

Choose a unique run ID containing a timestamp and collision-resistant suffix;
record the repository identity and reviewed source ref separately. Use a safe
lowercase prefix such as `YYYY-MM-DD_security-audit-<repo>-<run-id>` for Wiki raw
filenames. Record `output_destination: "wiki-raw"`, `wiki_prefix`, and
`storage_status: "pending"` in `run-metadata.json`.

If Wiki access is unavailable, continue the authorized audit in the working
directory. Retain eligible evidence and report storage as incomplete. Do not
switch to another account/service or claim that a local path is Wiki delivery.

### SSH targets

Keep shared output and Wiki credentials with the coordinating parent. The remote
server need not have Wiki access, the workspace helper, or this plugin installed.
Create remote test scratch under that host's workspace policy; if no helper is
available, use a uniquely named temporary directory outside the source/deployment
tree and record its ownership and path in the parent inventory. Read-only remote
commands need no scratch unless they generate files.

Capture only needed non-secret output and explicitly named eligible files through
the existing authenticated connection. Apply EXECUTION.md's retention checks on
both ends; compare the remote and retained byte sizes and SHA-256 for file
transfers. If redaction is required, transfer an eligible text derivative and
record its provenance without saving forbidden originals. Keep controller paths,
remote paths, source refs, and observation times distinct in the manifest.

Publish from the parent through the configured Wiki tools. Inventory and account
for remote task files as well as local ones; remove only this run's disposable
remote files after verified retention. Never recursively clean a deployment or
shared temp root. Record a failed transfer or remote cleanup as a specific gap;
do not declare storage or cleanup complete from the controller inventory alone.

## Previous runs

Search the configured Wiki for this repository's audit runs before seeding the
ledger. Read compatible raw manifests, coverage ledgers, and findings; follow
the current-source revalidation rules in `SKILL.md`. If validators or reviewers
need local files, restore only named, verified records and eligible artifacts
inside the new task workspace, validating paths before writing. Previous local
paths are historical provenance and may no longer exist. Missing retained proof
is an evidence gap, not permission to carry a confirmed verdict unchanged.

## Persist final output

After the final validation pass, use the configured Wiki write tools to save:

- `REPORT.md`, `FINDINGS-DETAIL.md`, and `NEEDS-VALIDATION.md`;
- `findings.json`, `coverage-ledger.json`, `architecture.md`, and run metadata;
- eligible text evidence referenced by the final records, including archived
  ledger attempts still used as evidence, plus validation results;
- a manifest mapping each local relative path to its exact Wiki raw path,
  byte size, SHA-256, source ref, and any extracted/redacted-original provenance.

Use unique names such as `<prefix>-report.md`, `<prefix>-findings.json`, and
`<prefix>-agent-<id>-<artifact-name>`. Detect collisions instead of overwriting.
Preserve JSON bytes and local relative artifact paths; the manifest maps those
paths to Wiki locations without changing upstream schema contracts. Human-facing
reports must link to the durable raw artifacts or manifest, not depend on local
absolute paths. Write report prose in the user's language; keep identifiers exact.

Do not upload credentials, production personal data, unrestricted scratch trees,
or binary originals excluded by Wiki policy. Where eligible, preserve an extracted
text result with provenance. If the only decisive evidence cannot be retained
under policy, disclose that limit and do not imply a reproducible retained proof.

Read each saved file back through Wiki and compare byte size and SHA-256 with the
final local content. Resolve write conflicts using the current revision. Save and
verify ordinary artifacts first. Then finalize run metadata with
`storage_status: "artifacts_verified"` and save and verify it. Build the manifest
from these final bytes, including the finalized metadata. The manifest excludes
itself and the final receipt from its hash list to avoid circular hashes. Verify
the manifest separately and include its digest in the final receipt. Do not
continuously overwrite raw files as progress logs or mutate already hashed files.

## Completion and cleanup

Keep `run_status` for audit verification and `storage_status` for Wiki retention
separate. Only the final receipt declares `storage_status: "complete"`, after the
artifact and manifest readbacks succeed. Its path is named in the final response;
do not rewrite archived metadata to point back to a receipt that hashes it. If
any final write/readback fails, report storage as incomplete and preserve the
local files. Do not claim full delivery from audit status alone.

Inventory task files, classify Wiki-preserved files with independently fetched
readbacks, and classify remaining reproducible copies for disposal under the
workspace policy. Remove only those classified task-owned copies, run `finish`,
and preserve and verify its necessary receipt in Wiki before removing helper
metadata and empty directories. If storage or retention is unresolved, keep the
affected files and report the exact gap. Link the durable report and manifest in
the final response and name any summary page updated under Wiki policy.
