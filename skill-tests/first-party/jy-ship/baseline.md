# RED Baseline For `jy-ship`

Goal: Observe what happens when someone is asked to ship a ready branch without `jy-ship`.

Look for likely failures:

- pushes or opens a PR without checking the base branch first
- skips fresh verification because earlier tests already passed
- treats "ship it" as permission to force-push or bypass review
- invents `VERSION`, `CHANGELOG`, or other release files that the repo does not actually use
- forgets to sync docs or ignores `jy-document-release`
- in Plan Mode, pretends to ship anyway instead of routing back to Default mode
