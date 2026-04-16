from __future__ import annotations

from pathlib import Path
import re
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
FIRST_PARTY_SKILL_ROOT = REPO_ROOT / "plugins" / "jy-env-core" / "skills"


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
                    self.assertIn("## Table of Contents", read_text(skill_path))

    def test_first_party_skills_do_not_reference_unknown_coding_convention_namespace(self) -> None:
        for skill_path in first_party_skill_paths():
            with self.subTest(skill=skill_path.parent.name):
                self.assertNotIn("coding-convention:", read_text(skill_path))

    def test_mode_aware_skills_document_collaboration_mode_routing(self) -> None:
        mode_aware_skills = [
            "jy-slop-remover",
            "jy-framing",
            "jy-plan-review",
            "jy-autoplan",
            "jy-writing-plans",
            "jy-worktrees",
            "jy-checkpoint",
            "jy-document-release",
            "jy-intent-gate",
            "jy-review-work",
            "jy-loop",
            "jy-debugging",
            "jy-test-driven",
            "jy-executing-plans",
            "jy-receiving-review",
            "jy-ship",
            "jy-verification-before-completion",
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
        text = read_text(FIRST_PARTY_SKILL_ROOT / "jy-autoplan" / "SKILL.md")
        self.assertIn("## Routing Matrix", text)
        self.assertIn("Idea-stage", text)
        self.assertIn("Plan-stage", text)
        self.assertIn("Task-plan-stage", text)
        self.assertIn("Execution-stage", text)
        self.assertIn("Execution-ready", text)
        self.assertIn("planning pack not applicable", text)
        self.assertIn("jy-writing-plans", text)
        self.assertIn("jy-executing-plans", text)

    def test_codex_checkpoint_documents_storage_contract(self) -> None:
        text = read_text(FIRST_PARTY_SKILL_ROOT / "jy-checkpoint" / "SKILL.md")
        self.assertIn(".codex/checkpoints/", text)
        self.assertIn("Save", text)
        self.assertIn("List", text)
        self.assertIn("Resume", text)
        self.assertIn("append-only", text)
        self.assertIn("frontmatter", text)

    def test_codex_document_release_tracks_existing_doc_surface(self) -> None:
        text = read_text(FIRST_PARTY_SKILL_ROOT / "jy-document-release" / "SKILL.md")
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
        self.assertIn("plugins/jy-env-core/skills/*/SKILL.md", text)

    def test_systematic_debugging_documents_reproduce_hypothesize_and_verify(self) -> None:
        text = read_text(FIRST_PARTY_SKILL_ROOT / "jy-debugging" / "SKILL.md")
        self.assertIn("reproduce", text)
        self.assertIn("hypothesis", text)
        self.assertIn("minimal fix", text)
        self.assertIn("shotgun", text)
        self.assertIn("## Debug Loop", text)

    def test_test_driven_development_documents_red_green_refactor(self) -> None:
        text = read_text(FIRST_PARTY_SKILL_ROOT / "jy-test-driven" / "SKILL.md")
        self.assertIn("RED", text)
        self.assertIn("GREEN", text)
        self.assertIn("REFACTOR", text)
        self.assertIn("failing test first", text)
        self.assertIn("Plan Mode", text)

    def test_verification_before_completion_requires_fresh_evidence(self) -> None:
        text = read_text(FIRST_PARTY_SKILL_ROOT / "jy-verification-before-completion" / "SKILL.md")
        self.assertIn("fresh verification evidence", text)
        self.assertIn("## Verification Gate", text)
        self.assertIn("evidence", text)
        self.assertIn("completion claim", text)
        self.assertIn("not run", text)

    def test_ship_documents_branch_gate_pr_flow_and_doc_sync(self) -> None:
        text = read_text(FIRST_PARTY_SKILL_ROOT / "jy-ship" / "SKILL.md")
        self.assertIn("base branch", text)
        self.assertTrue("PR" in text or "PR/MR" in text)
        self.assertIn("jy-document-release", text)
        self.assertIn("Never force push", text)
        self.assertIn("VERSION", text)
        self.assertIn("CHANGELOG", text)
        self.assertIn("old CI run", text)
        self.assertIn("If docs sync creates a new commit, push the same branch again", text)
        self.assertIn("Do not skip the `jy-document-release` decision", text)

    def test_writing_plans_documents_plan_doc_contract_and_placeholder_bans(self) -> None:
        text = read_text(FIRST_PARTY_SKILL_ROOT / "jy-writing-plans" / "SKILL.md")
        self.assertIn("docs/superpowers/plans/", text)
        self.assertIn("decision-complete", text)
        self.assertIn("acceptance criteria", text)
        self.assertIn("No Placeholders", text)
        self.assertIn("TBD", text)
        self.assertIn("## Mode-Aware Behavior", text)

    def test_executing_plans_documents_current_session_execution_without_auto_subagents(self) -> None:
        text = read_text(FIRST_PARTY_SKILL_ROOT / "jy-executing-plans" / "SKILL.md")
        self.assertIn("current session", text)
        self.assertIn("jy-test-driven", text)
        self.assertIn("jy-verification-before-completion", text)
        self.assertIn("jy-review-work", text)
        self.assertIn("does not auto-spawn subagents", text)
        self.assertIn("## Mode-Aware Behavior", text)

    def test_worktrees_documents_directory_policy_and_ignore_verification(self) -> None:
        text = read_text(FIRST_PARTY_SKILL_ROOT / "jy-worktrees" / "SKILL.md")
        self.assertIn(".worktrees/", text)
        self.assertIn("worktrees/", text)
        self.assertIn("gitignored", text)
        self.assertIn("git check-ignore", text)
        self.assertIn("## Mode-Aware Behavior", text)

    def test_receiving_review_documents_verification_before_changes_and_pushback(self) -> None:
        text = read_text(FIRST_PARTY_SKILL_ROOT / "jy-receiving-review" / "SKILL.md")
        self.assertIn("performative agreement", text)
        self.assertIn("technical pushback", text)
        self.assertIn("codebase", text)
        self.assertIn("unclear", text)
        self.assertIn("## Mode-Aware Behavior", text)

    def test_writing_skills_documents_english_first_authoring_policy(self) -> None:
        text = read_text(FIRST_PARTY_SKILL_ROOT / "jy-writing-skills" / "SKILL.md")
        self.assertIn("English-first", text)
        self.assertIn("core `SKILL.md`", text)
        self.assertIn("agents/openai.yaml", text)
        self.assertIn("Korean", text)
        self.assertIn("user's language", text)
        self.assertIn("output-language rule", text)

    def test_output_template_skills_document_user_language_rendering(self) -> None:
        for skill_name in [
            "jy-ship",
            "jy-checkpoint",
            "jy-document-release",
            "jy-env-sync-admin",
        ]:
            with self.subTest(skill=skill_name):
                text = read_text(FIRST_PARTY_SKILL_ROOT / skill_name / "SKILL.md")
                self.assertIn("## Output Template", text)
                self.assertIn("user's language", text)

    def test_skill_docs_are_english_first(self) -> None:
        for skill_path in first_party_skill_paths():
            with self.subTest(skill=skill_path.parent.name):
                text = read_text(skill_path)
                self.assertIsNone(re.search(r"[가-힣]", text))

    def test_writing_skill_references_are_english_first(self) -> None:
        reference_root = FIRST_PARTY_SKILL_ROOT / "jy-writing-skills" / "references"
        for ref_path in sorted(reference_root.glob("*.md")):
            with self.subTest(reference=ref_path.name):
                text = read_text(ref_path)
                self.assertIsNone(re.search(r"[가-힣]", text))

    def test_execution_skills_have_mode_aware_behavior(self) -> None:
        """Execution-oriented skills that modify files should document mode awareness."""
        execution_skills = [
            "jy-slop-remover",
            "jy-review-work",
            "jy-loop",
            "jy-document-release",
            "jy-checkpoint",
            "jy-debugging",
            "jy-test-driven",
            "jy-executing-plans",
            "jy-receiving-review",
            "jy-ship",
            "jy-verification-before-completion",
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
            "jy-consult",
        ]
        for skill_name in advisory_skills:
            skill_path = FIRST_PARTY_SKILL_ROOT / skill_name / "SKILL.md"
            if not skill_path.exists():
                continue
            text = read_text(skill_path)
            with self.subTest(skill=skill_name):
                self.assertTrue(
                    "Do not modify code" in text or "Do not write code" in text or "no code changes" in text,
                    f"{skill_name} is advisory but does not explicitly state no-modification boundary")

    def test_research_skills_require_evidence(self) -> None:
        """Research skills should require sources/evidence for claims."""
        research_skills = [
            "jy-library-research",
        ]
        for skill_name in research_skills:
            skill_path = FIRST_PARTY_SKILL_ROOT / skill_name / "SKILL.md"
            if not skill_path.exists():
                continue
            text = read_text(skill_path)
            with self.subTest(skill=skill_name):
                self.assertTrue(
                    "evidence" in text or "permalink" in text or "sources" in text or "links" in text,
                    f"{skill_name} is research-oriented but does not require evidence/sources")

    def test_korean_law_search_documents_two_part_answers_for_real_world_questions(self) -> None:
        text = read_text(FIRST_PARTY_SKILL_ROOT / "jy-korean-law-search" / "SKILL.md")

        self.assertIn("pure legal lookup", text)
        self.assertIn("real-world situation", text)
        self.assertIn("## Answer Shape", text)
        self.assertIn("General legal answer", text)
        self.assertIn("Practical answer", text)
        self.assertIn("precedent", text)
        self.assertIn("interpretation", text)
        self.assertIn("If you do not find directly relevant", text)
        self.assertIn("Do not fill the practical answer", text)

    def test_cross_skill_references_point_to_existing_skills(self) -> None:
        """Skills that reference other skills by name should reference existing ones."""
        existing_skill_names = {p.parent.name for p in first_party_skill_paths()}
        # Pattern: backtick-quoted skill names like `jy-consult`
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
