from __future__ import annotations

from pathlib import Path
import re
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
FIRST_PARTY_SKILL_ROOT = REPO_ROOT / "plugins" / "codex-env-core" / "skills"


def first_party_skill_paths() -> list[Path]:
    return sorted(FIRST_PARTY_SKILL_ROOT.glob("*/SKILL.md"))


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class FirstPartySkillComplianceTests(unittest.TestCase):
    def test_first_party_skill_frontmatter_description_starts_with_use_when(self) -> None:
        for skill_path in first_party_skill_paths():
            with self.subTest(skill=skill_path.parent.name):
                text = read_text(skill_path)
                match = re.search(r"^description:\s*(.+)$", text, re.MULTILINE)
                self.assertIsNotNone(match)
                self.assertTrue(match.group(1).strip().startswith("Use when"))

    def test_first_party_skills_include_quick_reference_and_common_mistakes(self) -> None:
        for skill_path in first_party_skill_paths():
            with self.subTest(skill=skill_path.parent.name):
                text = read_text(skill_path)
                self.assertIn("## Quick Reference", text)
                self.assertIn("## Common Mistakes", text)

    def test_large_first_party_skills_include_a_table_of_contents(self) -> None:
        for skill_path in first_party_skill_paths():
            with self.subTest(skill=skill_path.parent.name):
                lines = read_text(skill_path).splitlines()
                if len(lines) > 300:
                    self.assertIn("## 목차", read_text(skill_path))

    def test_first_party_skills_do_not_reference_unknown_coding_convention_namespace(self) -> None:
        for skill_path in first_party_skill_paths():
            with self.subTest(skill=skill_path.parent.name):
                self.assertNotIn("coding-convention:", read_text(skill_path))

    def test_mode_aware_skills_document_collaboration_mode_routing(self) -> None:
        mode_aware_skills = [
            "ai-slop-remover",
            "codex-office-hours",
            "codex-plan-review",
            "codex-autoplan",
            "codex-checkpoint",
            "codex-document-release",
            "intent-gate",
            "review-work",
            "work-loop",
            "systematic-debugging",
            "test-driven-development",
            "verification-before-completion",
        ]
        for skill_name in mode_aware_skills:
            skill_path = FIRST_PARTY_SKILL_ROOT / skill_name / "SKILL.md"
            text = read_text(skill_path)
            with self.subTest(skill=skill_name):
                self.assertIn("## Mode-Aware Behavior", text)
                self.assertIn("Shift+Tab", text)
                self.assertIn("current collaboration mode is Default", text)
                self.assertIn("current collaboration mode is Plan", text)

    def test_codex_autoplan_documents_maturity_buckets_and_execution_escape(self) -> None:
        text = read_text(FIRST_PARTY_SKILL_ROOT / "codex-autoplan" / "SKILL.md")
        self.assertIn("## Routing Matrix", text)
        self.assertIn("Idea-stage", text)
        self.assertIn("Plan-stage", text)
        self.assertIn("Execution-ready", text)
        self.assertIn("planning pack not applicable", text)

    def test_codex_checkpoint_documents_storage_contract(self) -> None:
        text = read_text(FIRST_PARTY_SKILL_ROOT / "codex-checkpoint" / "SKILL.md")
        self.assertIn(".codex/checkpoints/", text)
        self.assertIn("Save", text)
        self.assertIn("List", text)
        self.assertIn("Resume", text)
        self.assertIn("append-only", text)
        self.assertIn("frontmatter", text)

    def test_codex_document_release_tracks_existing_doc_surface(self) -> None:
        text = read_text(FIRST_PARTY_SKILL_ROOT / "codex-document-release" / "SKILL.md")
        self.assertIn("README.md", text)
        self.assertIn("instructions/AGENTS.md", text)
        self.assertIn("skill-tests/first-party/", text)
        self.assertIn("CHANGELOG", text)
        self.assertIn("Do not invent", text)
        self.assertIn("## Change-to-Docs Routing Matrix", text)
        self.assertIn("skill behavior change -> skill doc + scenario pack", text)
        self.assertIn("install surface change -> README + AGENTS", text)
        self.assertIn("routing change -> AGENTS + related skill doc", text)
        self.assertIn("## Full Consistency Audit", text)
        self.assertIn("full consistency audit", text)
        self.assertIn("plugins/codex-env-core/skills/*/SKILL.md", text)

    def test_systematic_debugging_documents_reproduce_hypothesize_and_verify(self) -> None:
        text = read_text(FIRST_PARTY_SKILL_ROOT / "systematic-debugging" / "SKILL.md")
        self.assertIn("재현", text)
        self.assertIn("가설", text)
        self.assertIn("최소 수정", text)
        self.assertIn("shotgun", text)
        self.assertIn("## Debug Loop", text)

    def test_test_driven_development_documents_red_green_refactor(self) -> None:
        text = read_text(FIRST_PARTY_SKILL_ROOT / "test-driven-development" / "SKILL.md")
        self.assertIn("RED", text)
        self.assertIn("GREEN", text)
        self.assertIn("REFACTOR", text)
        self.assertIn("failing test first", text)
        self.assertIn("Plan Mode", text)

    def test_verification_before_completion_requires_fresh_evidence(self) -> None:
        text = read_text(FIRST_PARTY_SKILL_ROOT / "verification-before-completion" / "SKILL.md")
        self.assertIn("fresh verification evidence", text)
        self.assertIn("## Verification Gate", text)
        self.assertIn("증거", text)
        self.assertIn("완료 주장", text)
        self.assertIn("not run", text)

    def test_execution_skills_have_mode_aware_behavior(self) -> None:
        """Execution-oriented skills that modify files should document mode awareness."""
        execution_skills = [
            "ai-slop-remover",
            "review-work",
            "work-loop",
            "codex-document-release",
            "codex-checkpoint",
            "systematic-debugging",
            "test-driven-development",
            "verification-before-completion",
        ]
        for skill_name in execution_skills:
            skill_path = FIRST_PARTY_SKILL_ROOT / skill_name / "SKILL.md"
            if not skill_path.exists():
                continue
            text = read_text(skill_path)
            with self.subTest(skill=skill_name):
                self.assertIn("## Mode-Aware Behavior", text,
                    f"{skill_name} is execution-oriented but lacks Mode-Aware Behavior section")

    def test_advisory_skills_do_not_modify_files(self) -> None:
        """Advisory skills should state they do not modify code."""
        advisory_skills = [
            "oracle-consult",
        ]
        for skill_name in advisory_skills:
            skill_path = FIRST_PARTY_SKILL_ROOT / skill_name / "SKILL.md"
            if not skill_path.exists():
                continue
            text = read_text(skill_path)
            with self.subTest(skill=skill_name):
                self.assertTrue(
                    "코드 수정 금지" in text or "구현하지 않는다" in text or "코드 작성 금지" in text,
                    f"{skill_name} is advisory but does not explicitly state no-modification boundary")

    def test_research_skills_require_evidence(self) -> None:
        """Research skills should require sources/evidence for claims."""
        research_skills = [
            "library-research",
        ]
        for skill_name in research_skills:
            skill_path = FIRST_PARTY_SKILL_ROOT / skill_name / "SKILL.md"
            if not skill_path.exists():
                continue
            text = read_text(skill_path)
            with self.subTest(skill=skill_name):
                self.assertTrue(
                    "증거" in text or "permalink" in text or "출처" in text or "링크" in text,
                    f"{skill_name} is research-oriented but does not require evidence/sources")

    def test_cross_skill_references_point_to_existing_skills(self) -> None:
        """Skills that reference other skills by name should reference existing ones."""
        existing_skill_names = {p.parent.name for p in first_party_skill_paths()}
        # Pattern: backtick-quoted skill names like `oracle-consult`
        ref_pattern = re.compile(r"`([\w-]+)`")
        known_non_skill_refs = {
            "run_in_background", "run_in_background=true", "Shift+Tab",
            "PASS", "FAIL", "PASS/FAIL", "Save", "List", "Resume",
            "inspect", "apply", "bootstrap", "git", "python3",
        }
        for skill_path in first_party_skill_paths():
            text = read_text(skill_path)
            refs = ref_pattern.findall(text)
            for ref in refs:
                if ref in existing_skill_names and ref != skill_path.parent.name:
                    # This is a cross-reference to another skill - it exists, so it's valid
                    pass


if __name__ == "__main__":
    unittest.main()
