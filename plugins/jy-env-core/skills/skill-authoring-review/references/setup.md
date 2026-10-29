# Tested scanner setup

Read this only when installing or troubleshooting the scanner. The skill package
does not install dependencies automatically.

The 2026-10-29 macOS arm64 trial used SkillSpector 2.12.0 at commit
`d501c0d5035c2ed6385740a384d942bb05651fda`, installed as an isolated `uv` tool:

```bash
uv tool install --python 3.13 \
  'skillspector @ git+https://github.com/NVIDIA/SkillSpector@d501c0d5035c2ed6385740a384d942bb05651fda'
skillspector --version
```

Python 3.14 failed to build `yara-python` on that machine; Python 3.13 succeeded.
Other operating systems were not tested. This pins scanner source, not its full
transitive dependency graph. Review upstream changes before updating the pin.

`--no-llm` disables model analysis, but dependency inspection can contact OSV.
There is no tested offline switch in this integration. The `codex_cli` provider
is disabled upstream at this revision; do not work around it or launch a separate
agent session merely to obtain a scanner verdict. The current authoring agent
performs semantic review directly.

Sources: [upstream repository](https://github.com/NVIDIA/SkillSpector/tree/d501c0d5035c2ed6385740a384d942bb05651fda),
[OSV lookup behavior](https://github.com/NVIDIA/SkillSpector/blob/d501c0d5035c2ed6385740a384d942bb05651fda/docs/SC4-osv-live-vulnerability-lookups.md).
