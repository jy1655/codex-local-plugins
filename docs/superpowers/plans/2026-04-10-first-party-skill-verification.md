# First-Party Skill Verification Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a repo-local verification package for first-party Codex skills so maintainers can run consistent baseline and pressure-scenario reviews.

**Architecture:** Keep the verification assets as repo data under a dedicated `skill-tests/first-party/` tree, one directory per first-party skill. Add unittest coverage that asserts every first-party skill has the required scenario pack, baseline case, pressure scenarios, and result template, so the verification workflow stays complete as new first-party skills are added.

**Tech Stack:** Markdown, YAML, Python `unittest`

---

### Task 1: Add Scenario Pack Tests

**Files:**
- Create: `tests/test_skill_scenarios.py`
- Test: `tests/test_skill_scenarios.py`

- [ ] **Step 1: Write the failing test**

```python
from __future__ import annotations

from pathlib import Path
import unittest
import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
FIRST_PARTY_SKILL_ROOT = REPO_ROOT / "plugins" / "codex-env-core" / "skills"
SCENARIO_ROOT = REPO_ROOT / "skill-tests" / "first-party"


class FirstPartySkillScenarioTests(unittest.TestCase):
    def test_each_first_party_skill_has_a_scenario_pack(self) -> None:
        for skill_dir in sorted(FIRST_PARTY_SKILL_ROOT.iterdir()):
            if not (skill_dir / "SKILL.md").exists():
                continue
            with self.subTest(skill=skill_dir.name):
                scenario_dir = SCENARIO_ROOT / skill_dir.name
                self.assertTrue((scenario_dir / "README.md").exists())
                self.assertTrue((scenario_dir / "baseline.md").exists())
                self.assertTrue((scenario_dir / "pressure-scenarios.yaml").exists())
                self.assertTrue((scenario_dir / "result-template.md").exists())

    def test_pressure_scenarios_define_at_least_two_cases(self) -> None:
        for scenario_file in sorted(SCENARIO_ROOT.glob("*/pressure-scenarios.yaml")):
            with self.subTest(file=scenario_file.parent.name):
                data = yaml.safe_load(scenario_file.read_text(encoding="utf-8"))
                self.assertGreaterEqual(len(data["scenarios"]), 2)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests.test_skill_scenarios -v`
Expected: FAIL because `skill-tests/first-party/...` does not exist yet

- [ ] **Step 3: Write minimal implementation**

```text
Create the scenario-pack directories and files that the tests expect.
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m unittest tests.test_skill_scenarios -v`
Expected: PASS

### Task 2: Add First-Party Scenario Packs

**Files:**
- Create: `skill-tests/first-party/env-sync-admin/README.md`
- Create: `skill-tests/first-party/env-sync-admin/baseline.md`
- Create: `skill-tests/first-party/env-sync-admin/pressure-scenarios.yaml`
- Create: `skill-tests/first-party/env-sync-admin/result-template.md`
- Create: `skill-tests/first-party/writing-skills/README.md`
- Create: `skill-tests/first-party/writing-skills/baseline.md`
- Create: `skill-tests/first-party/writing-skills/pressure-scenarios.yaml`
- Create: `skill-tests/first-party/writing-skills/result-template.md`

- [ ] **Step 1: Write the failing asset expectation via Task 1**

```text
Reuse Task 1 failures as the red state for these files.
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests.test_skill_scenarios -v`
Expected: FAIL until all scenario-pack files are present

- [ ] **Step 3: Write minimal implementation**

```text
For each first-party skill, add:
- README.md explaining what the skill pack validates
- baseline.md describing the no-skill baseline
- pressure-scenarios.yaml with at least 2 concrete cases
- result-template.md capturing observed choice, rationale, and pass/fail
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m unittest tests.test_skill_scenarios -v`
Expected: PASS

### Task 3: Verify Whole Repo

**Files:**
- Modify: `README.md`
- Test: `tests/test_skill_compliance.py`
- Test: `tests/test_skill_scenarios.py`

- [ ] **Step 1: Write the failing documentation/test expectation**

```text
Add a short README note for the new verification package and ensure all tests stay green.
```

- [ ] **Step 2: Run test to verify current state**

Run: `python3 -m unittest discover -s tests -v`
Expected: PASS after Task 1 and Task 2 are complete, with the new scenario tests included

- [ ] **Step 3: Write minimal implementation**

```markdown
Add one README paragraph pointing maintainers to `skill-tests/first-party/` and the unittest command.
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m unittest discover -s tests -v`
Expected: PASS
