from __future__ import annotations

import json
import io
import os
from pathlib import Path
import tempfile
import unittest
from contextlib import redirect_stdout

from codex_env_sync.skill_eval import (
    ARMS,
    CodexEvalBackend,
    EvalPolicy,
    ExecObservation,
    JudgeBatch,
    JudgeScore,
    ModelRun,
    advance_state,
    build_blind_judge_request,
    build_codex_exec_command,
    build_codex_process_environment,
    build_eval_plan,
    build_parser,
    build_snapshot,
    build_task_prompt,
    discover_skill_dirs,
    evaluate_plan,
    expand_skill_names_to_pack_peers,
    load_eval_policy,
    load_model_run_artifact,
    load_scenarios,
    main,
    parse_judge_output,
    parse_exec_jsonl,
    recommend_skill,
    render_markdown_report,
    skill_dirs_for_arm,
    skill_names_for_changed_paths,
    stage_skill_dirs,
    stale_skills,
)


REPO_ROOT = Path(__file__).resolve().parents[1]


class SkillEvalDiscoveryTests(unittest.TestCase):
    def test_repository_policy_pins_current_model_and_evidence_floor(self) -> None:
        policy = load_eval_policy(REPO_ROOT)
        self.assertEqual(policy.model, "gpt-5.6-sol")
        self.assertEqual(policy.reasoning_effort, "max")
        self.assertEqual(policy.repetitions, 3)
        self.assertEqual(policy.minimum_scenarios, 2)
        self.assertEqual(policy.maximum_input_token_overhead_ratio, 0.25)
        self.assertEqual(policy.maximum_latency_overhead_ratio, 0.5)
        self.assertEqual(policy.minimum_implicit_activation_rate, 0.8)

    def test_discovers_every_first_party_skill_and_scenario_asset(self) -> None:
        skill_dirs = discover_skill_dirs(REPO_ROOT)
        self.assertGreaterEqual(len(skill_dirs), 1)
        self.assertIn("jy-change-guardrails", skill_dirs)

        scenarios = load_scenarios(REPO_ROOT, "jy-change-guardrails")
        self.assertGreaterEqual(len(scenarios), 2)
        self.assertEqual(scenarios[0].skill_name, "jy-change-guardrails")

    def test_plan_has_baseline_implicit_and_explicit_arms(self) -> None:
        plan = build_eval_plan(
            REPO_ROOT,
            model="gpt-5.6-sol",
            reasoning_effort="max",
            skill_names=["jy-change-guardrails"],
            scenario_ids=["one-off-change-pressure"],
            repetitions=2,
        )

        self.assertEqual(plan.arms, ARMS)
        self.assertEqual(len(plan.cases), 2)
        self.assertEqual(plan.task_calls, 6)
        self.assertEqual(plan.judge_calls, 1)
        self.assertEqual(plan.total_model_calls, 7)
        pack_names = {path.name for path in plan.pack_skill_dirs["jy-change-guardrails"]}
        self.assertIn("jy-change-guardrails", pack_names)
        self.assertIn("jy-debugging", pack_names)
        self.assertEqual(len(pack_names), 7)

        baseline_names = {
            path.name for path in skill_dirs_for_arm(plan, "jy-change-guardrails", "baseline")
        }
        implicit_names = {
            path.name for path in skill_dirs_for_arm(plan, "jy-change-guardrails", "implicit")
        }
        self.assertNotIn("jy-change-guardrails", baseline_names)
        self.assertIn("jy-debugging", baseline_names)
        self.assertIn("jy-change-guardrails", implicit_names)

    def test_changed_paths_select_only_affected_skills_or_all_for_harness(self) -> None:
        selected = skill_names_for_changed_paths(
            [
                "plugins/jy-env-core/skills/jy-debugging/SKILL.md",
                "skill-tests/first-party/jy-test-driven/pressure-scenarios.json",
                "README.md",
            ]
        )
        self.assertEqual(selected, {"jy-debugging", "jy-test-driven"})

        self.assertEqual(
            skill_names_for_changed_paths(["codex_env_sync/skill_eval.py"]),
            {"*"},
        )
        self.assertEqual(
            skill_names_for_changed_paths(["skill-tests/eval-policy.json"]),
            {"*"},
        )

        peers = expand_skill_names_to_pack_peers(REPO_ROOT, {"jy-debugging"})
        self.assertEqual(len(peers), 7)
        self.assertIn("jy-change-guardrails", peers)
        self.assertNotIn("ios-debugger-agent", peers)

        source_change = skill_names_for_changed_paths(
            ["plugins/jy-env-core/skills/jy-debugging/SKILL.md"],
            repo_root=REPO_ROOT,
        )
        scenario_change = skill_names_for_changed_paths(
            ["skill-tests/first-party/jy-debugging/pressure-scenarios.json"],
            repo_root=REPO_ROOT,
        )
        self.assertEqual(source_change, peers)
        self.assertEqual(scenario_change, {"jy-debugging"})


class SkillEvalEvidenceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.policy = EvalPolicy(
            model="gpt-5.6-sol",
            reasoning_effort="max",
            judge_model="gpt-5.6-luna",
            repetitions=3,
            minimum_scenarios=2,
            minimum_pairs=6,
            quality_floor=3.0,
            meaningful_gain=0.5,
            neutral_band=0.25,
        )

    def scores(
        self,
        baseline: float,
        implicit: float,
        explicit: float,
    ) -> list[JudgeScore]:
        return [
            JudgeScore(
                scenario_id=f"scenario-{index % 2}",
                repetition=index // 2,
                baseline_score=baseline,
                implicit_score=implicit,
                explicit_score=explicit,
                confidence=0.9,
                rationale="test",
            )
            for index in range(6)
        ]

    def test_keep_when_implicit_skill_materially_improves_quality(self) -> None:
        result = recommend_skill(self.scores(2.5, 3.5, 3.6), self.policy)
        self.assertEqual(result.verdict, "KEEP")

    def test_new_skill_with_material_gain_is_an_add_candidate(self) -> None:
        result = recommend_skill(
            self.scores(2.5, 3.5, 3.6),
            self.policy,
            candidate=True,
        )
        self.assertEqual(result.verdict, "ADD_CANDIDATE")

    def test_new_skill_without_gain_is_rejected_not_removed(self) -> None:
        result = recommend_skill(
            self.scores(3.5, 3.5, 3.4),
            self.policy,
            candidate=True,
        )
        self.assertEqual(result.verdict, "REJECT_CANDIDATE")

    def test_quality_gain_with_excessive_runtime_cost_requires_revision(self) -> None:
        result = recommend_skill(
            self.scores(2.5, 3.5, 3.6),
            self.policy,
            implicit_input_token_overhead_ratio=0.6,
            implicit_latency_overhead_ratio=0.1,
        )
        self.assertEqual(result.verdict, "REVISE_COST")

    def test_quality_gain_without_implicit_activation_is_a_trigger_problem(self) -> None:
        result = recommend_skill(
            self.scores(2.5, 3.5, 3.6),
            self.policy,
            implicit_activation_rate=0.0,
        )
        self.assertEqual(result.verdict, "REVISE_TRIGGER")

    def test_revise_trigger_when_only_explicit_invocation_helps(self) -> None:
        result = recommend_skill(self.scores(2.5, 2.6, 3.5), self.policy)
        self.assertEqual(result.verdict, "REVISE_TRIGGER")

    def test_remove_candidate_requires_high_baseline_and_no_skill_gain(self) -> None:
        result = recommend_skill(self.scores(3.5, 3.5, 3.4), self.policy)
        self.assertEqual(result.verdict, "REMOVE_CANDIDATE")

    def test_too_little_evidence_is_inconclusive(self) -> None:
        result = recommend_skill(self.scores(3.5, 3.5, 3.4)[:2], self.policy)
        self.assertEqual(result.verdict, "INSUFFICIENT")

    def test_exec_jsonl_parser_extracts_final_message_usage_and_tools(self) -> None:
        payload = "\n".join(
            [
                json.dumps({"type": "thread.started", "thread_id": "thread-1"}),
                json.dumps(
                    {
                        "type": "item.completed",
                        "item": {
                            "id": "item-1",
                            "type": "command_execution",
                            "command": "sed -n '1,80p' .agents/skills/demo/SKILL.md",
                            "status": "completed",
                        },
                    }
                ),
                json.dumps(
                    {
                        "type": "item.completed",
                        "item": {
                            "id": "item-2",
                            "type": "agent_message",
                            "text": "final answer",
                        },
                    }
                ),
                json.dumps(
                    {
                        "type": "turn.completed",
                        "usage": {
                            "input_tokens": 120,
                            "cached_input_tokens": 20,
                            "output_tokens": 30,
                            "reasoning_output_tokens": 10,
                        },
                    }
                ),
            ]
        )

        result = parse_exec_jsonl(payload, elapsed_seconds=1.25, skill_name="demo")
        self.assertEqual(result.final_message, "final answer")
        self.assertEqual(result.input_tokens, 120)
        self.assertEqual(result.output_tokens, 30)
        self.assertEqual(result.tool_calls, 1)
        self.assertTrue(result.skill_read_observed)

    def test_task_prompt_is_identical_for_baseline_and_implicit(self) -> None:
        scenario = load_scenarios(REPO_ROOT, "jy-change-guardrails")[0]
        baseline = build_task_prompt(scenario, "baseline")
        implicit = build_task_prompt(scenario, "implicit")
        explicit = build_task_prompt(scenario, "explicit")

        self.assertEqual(baseline, implicit)
        self.assertNotIn("jy-change-guardrails", baseline)
        self.assertIn("$jy-change-guardrails", explicit)
        self.assertIn("operating guidance, not the subject of the task", explicit)
        self.assertIn(scenario.prompt, baseline)

    def test_codex_command_explicitly_pins_reproducibility_controls(self) -> None:
        command = build_codex_exec_command(
            codex_executable="/usr/local/bin/codex",
            model="gpt-5.6-sol",
            reasoning_effort="max",
            service_tier="fast",
            workdir=Path("/tmp/eval-workspace"),
        )

        self.assertEqual(command[0], "/usr/local/bin/codex")
        self.assertIn("--json", command)
        self.assertIn("--ephemeral", command)
        self.assertIn("--ignore-user-config", command)
        self.assertIn("--ignore-rules", command)
        self.assertIn("read-only", command)
        self.assertIn("gpt-5.6-sol", command)
        self.assertIn('model_reasoning_effort="max"', command)
        self.assertIn('service_tier="fast"', command)
        self.assertIn('shell_environment_policy.inherit="none"', command)
        self.assertIn("shell_environment_policy.ignore_default_excludes=false", command)
        self.assertIn("tools.web_search=false", command)
        self.assertIn(
            f"shell_environment_policy.set.PATH={json.dumps(os.defpath)}",
            command,
        )

    def test_codex_process_environment_drops_unrelated_secrets(self) -> None:
        environment = build_codex_process_environment(
            parent_environment={
                "PATH": "/usr/bin:/bin",
                "LANG": "en_US.UTF-8",
                "CODEX_API_KEY": "codex-key",
                "AWS_SECRET_ACCESS_KEY": "aws-secret",
                "GH_TOKEN": "github-token",
                "UNRELATED": "value",
            },
            isolated_home=Path("/tmp/eval-home"),
            isolated_codex_home=Path("/tmp/eval-home/.codex"),
        )

        self.assertEqual(environment["CODEX_API_KEY"], "codex-key")
        self.assertEqual(Path(environment["HOME"]), Path("/tmp/eval-home"))
        self.assertNotIn("AWS_SECRET_ACCESS_KEY", environment)
        self.assertNotIn("GH_TOKEN", environment)
        self.assertNotIn("UNRELATED", environment)

    def test_stages_multiple_pack_skills_in_one_isolated_home(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            sources = root / "sources"
            first = sources / "first"
            second = sources / "second"
            first.mkdir(parents=True)
            second.mkdir(parents=True)
            (first / "SKILL.md").write_text("first\n", encoding="utf-8")
            (second / "SKILL.md").write_text("second\n", encoding="utf-8")
            isolated_home = root / "home"

            stage_skill_dirs((first, second), isolated_home)

            destination = isolated_home / ".agents" / "skills"
            self.assertEqual((destination / "first" / "SKILL.md").read_text(), "first\n")
            self.assertEqual((destination / "second" / "SKILL.md").read_text(), "second\n")

    def test_resume_reuses_only_matching_successful_task_artifact(self) -> None:
        plan = build_eval_plan(
            REPO_ROOT,
            model="gpt-5.6-sol",
            reasoning_effort="max",
            skill_names=["jy-change-guardrails"],
            scenario_ids=["one-off-change-pressure"],
            repetitions=1,
        )
        case = plan.cases[0]
        skill_dirs = skill_dirs_for_arm(
            plan,
            "jy-change-guardrails",
            "implicit",
        )
        prompt = build_task_prompt(case.scenario, "implicit")
        skill_context = {
            "observed_target": case.skill_name,
            "discoverable_skills": sorted(path.name for path in skill_dirs),
        }
        observation = ExecObservation(
            final_message="reused answer",
            input_tokens=100,
            cached_input_tokens=20,
            output_tokens=30,
            reasoning_output_tokens=10,
            elapsed_seconds=1.25,
            tool_calls=1,
            thread_id="thread-reused",
            skill_read_observed=True,
        )

        with tempfile.TemporaryDirectory() as temp_dir:
            run_dir = Path(temp_dir)
            artifact = (
                run_dir
                / "raw"
                / case.skill_name
                / case.scenario.id
                / "repeat-0"
                / "implicit"
            )
            artifact.mkdir(parents=True)
            (artifact / "prompt.txt").write_text(prompt, encoding="utf-8")
            (artifact / "skill-context.json").write_text(
                json.dumps(skill_context),
                encoding="utf-8",
            )
            (artifact / "execution.json").write_text(
                json.dumps({"elapsed_seconds": 1.25, "returncode": 0}),
                encoding="utf-8",
            )
            (artifact / "observation.json").write_text(
                json.dumps(observation.to_dict()),
                encoding="utf-8",
            )

            loaded = load_model_run_artifact(
                artifact,
                expected_prompt=prompt,
                expected_skill_context=skill_context,
            )
            self.assertIsNotNone(loaded)
            self.assertEqual(loaded.observation.final_message, "reused answer")
            self.assertIsNone(
                load_model_run_artifact(
                    artifact,
                    expected_prompt="different prompt",
                    expected_skill_context=skill_context,
                )
            )

            backend = object.__new__(CodexEvalBackend)
            backend.run_dir = run_dir
            backend.resume = True
            backend.executed_task_calls = 0
            backend.reused_task_calls = 0
            result = backend.run_task(case, "implicit", skill_dirs, self.policy)

        self.assertEqual(result.observation.final_message, "reused answer")
        self.assertEqual(backend.executed_task_calls, 0)
        self.assertEqual(backend.reused_task_calls, 1)

    def test_resume_reuses_only_matching_successful_judge_artifact(self) -> None:
        plan = build_eval_plan(
            REPO_ROOT,
            model="gpt-5.6-sol",
            reasoning_effort="max",
            skill_names=["jy-change-guardrails"],
            scenario_ids=["one-off-change-pressure"],
            repetitions=1,
        )
        case = plan.cases[0]
        runs = {
            case.case_id: {
                arm: ModelRun(
                    observation=ExecObservation(
                        final_message=f"{arm} answer",
                        input_tokens=100,
                        cached_input_tokens=20,
                        output_tokens=30,
                        reasoning_output_tokens=10,
                        elapsed_seconds=1.25,
                        tool_calls=0,
                        thread_id=f"thread-{arm}",
                        skill_read_observed=arm != "baseline",
                    )
                )
                for arm in ARMS
            }
        }
        prompt, mappings = build_blind_judge_request([case], runs)
        structured_output = {
            "results": [
                {
                    "case_id": case.case_id,
                    "scores": {"A": 3.0, "B": 3.5, "C": 4.0},
                    "confidence": 0.9,
                    "rationale": "reused judge result",
                }
            ]
        }
        judge_observation = ExecObservation(
            final_message=json.dumps(structured_output),
            input_tokens=100,
            cached_input_tokens=0,
            output_tokens=20,
            reasoning_output_tokens=5,
            elapsed_seconds=1.0,
            tool_calls=0,
            thread_id="thread-judge",
            skill_read_observed=False,
        )

        with tempfile.TemporaryDirectory() as temp_dir:
            run_dir = Path(temp_dir)
            artifact = run_dir / "judge" / case.skill_name
            artifact.mkdir(parents=True)
            (artifact / "prompt.txt").write_text(prompt, encoding="utf-8")
            (artifact / "skill-context.json").write_text(
                json.dumps(
                    {
                        "observed_target": "__judge__",
                        "discoverable_skills": [],
                    }
                ),
                encoding="utf-8",
            )
            (artifact / "execution.json").write_text(
                json.dumps({"elapsed_seconds": 1.0, "returncode": 0}),
                encoding="utf-8",
            )
            (artifact / "observation.json").write_text(
                json.dumps(judge_observation.to_dict()),
                encoding="utf-8",
            )
            (artifact / "label-mappings.json").write_text(
                json.dumps(mappings),
                encoding="utf-8",
            )
            (artifact / "structured-output.json").write_text(
                json.dumps(structured_output),
                encoding="utf-8",
            )

            backend = object.__new__(CodexEvalBackend)
            backend.run_dir = run_dir
            backend.resume = True
            backend.executed_judge_calls = 0
            backend.reused_judge_calls = 0
            batch = backend.run_judge(
                case.skill_name,
                [case],
                runs,
                self.policy,
            )

        self.assertEqual(len(batch.scores), 1)
        self.assertEqual(batch.scores[0].rationale, "reused judge result")
        self.assertEqual(backend.executed_judge_calls, 0)
        self.assertEqual(backend.reused_judge_calls, 1)

    def test_rejects_skill_symlinks_before_staging(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            skill_dir = root / "skill"
            skill_dir.mkdir()
            outside = root / "outside-secret"
            outside.write_text("secret\n", encoding="utf-8")
            try:
                (skill_dir / "linked-secret").symlink_to(outside)
            except OSError as exc:  # pragma: no cover - platform capability boundary
                self.skipTest(f"symlinks unavailable: {exc}")

            with self.assertRaisesRegex(ValueError, "symbolic links"):
                stage_skill_dirs((skill_dir,), root / "home")

    def test_blind_judge_output_is_unmapped_back_to_real_arms(self) -> None:
        judge_payload = {
            "results": [
                {
                    "case_id": "demo:one:0",
                    "scores": {"A": 3.5, "B": 2.0, "C": 3.0},
                    "confidence": 0.8,
                    "rationale": "A best matches the target.",
                }
            ]
        }
        mappings = {
            "demo:one:0": {
                "A": "explicit",
                "B": "baseline",
                "C": "implicit",
            }
        }

        scores = parse_judge_output(judge_payload, mappings)
        self.assertEqual(len(scores), 1)
        self.assertEqual(scores[0].baseline_score, 2.0)
        self.assertEqual(scores[0].implicit_score, 3.0)
        self.assertEqual(scores[0].explicit_score, 3.5)

    def test_evaluate_plan_aggregates_three_arm_metrics_and_verdict(self) -> None:
        plan = build_eval_plan(
            REPO_ROOT,
            model="gpt-5.6-sol",
            reasoning_effort="max",
            skill_names=["jy-codebase-explore"],
            repetitions=3,
            max_scenarios_per_skill=2,
        )

        class FakeBackend:
            codex_version = "codex-cli test"

            def __init__(self) -> None:
                self.task_calls: list[tuple[str, str, tuple[str, ...]]] = []

            def run_task(
                self,
                case: object,
                arm: str,
                skill_dir: object,
                policy: EvalPolicy,
            ) -> ModelRun:
                del policy
                case_id = getattr(case, "case_id")
                skill_names = tuple(path.name for path in skill_dir)
                self.task_calls.append((case_id, arm, skill_names))
                tokens = {"baseline": 100, "implicit": 120, "explicit": 150}[arm]
                return ModelRun(
                    observation=ExecObservation(
                        final_message=f"{arm} answer",
                        input_tokens=tokens,
                        cached_input_tokens=0,
                        output_tokens=20,
                        reasoning_output_tokens=5,
                        elapsed_seconds=1.0,
                        tool_calls=0,
                        thread_id=f"thread-{arm}",
                        skill_read_observed=arm != "baseline",
                    )
                )

            def run_judge(
                self,
                skill_name: str,
                cases: object,
                runs: object,
                policy: EvalPolicy,
            ) -> JudgeBatch:
                del skill_name, runs, policy
                scores = tuple(
                    JudgeScore(
                        scenario_id=case.scenario.id,
                        repetition=case.repetition,
                        baseline_score=3.5,
                        implicit_score=3.5,
                        explicit_score=3.4,
                        confidence=0.9,
                        rationale="No material gain.",
                    )
                    for case in cases
                )
                return JudgeBatch(scores=scores)

        backend = FakeBackend()
        outcome = evaluate_plan(plan, self.policy, backend=backend, run_id="test-run")

        self.assertEqual(len(backend.task_calls), 18)
        baseline_context = next(
            names for _, arm, names in backend.task_calls if arm == "baseline"
        )
        implicit_context = next(
            names for _, arm, names in backend.task_calls if arm == "implicit"
        )
        self.assertNotIn("jy-codebase-explore", baseline_context)
        self.assertIn("jy-debugging", baseline_context)
        self.assertIn("jy-codebase-explore", implicit_context)
        result = outcome.report["results"][0]
        self.assertEqual(result["verdict"], "REMOVE_CANDIDATE")
        self.assertEqual(result["baseline_input_tokens"], 100)
        self.assertEqual(result["implicit_input_tokens"], 120)
        self.assertEqual(result["explicit_input_tokens"], 150)
        self.assertEqual(result["activation_rate"], 1.0)
        self.assertEqual(result["implicit_activation_rate"], 1.0)
        self.assertAlmostEqual(result["implicit_input_token_overhead_ratio"], 0.2)
        self.assertAlmostEqual(result["implicit_latency_overhead_ratio"], 0.0)

    def test_blind_judge_request_hides_arm_identity_and_keeps_case_mapping(self) -> None:
        plan = build_eval_plan(
            REPO_ROOT,
            model="gpt-5.6-sol",
            reasoning_effort="max",
            skill_names=["jy-change-guardrails"],
            scenario_ids=["one-off-change-pressure"],
            repetitions=1,
        )
        case = plan.cases[0]
        runs = {
            case.case_id: {
                arm: ModelRun(
                    observation=ExecObservation(
                        final_message=f"answer-{index}",
                        input_tokens=1,
                        cached_input_tokens=0,
                        output_tokens=1,
                        reasoning_output_tokens=0,
                        elapsed_seconds=1.0,
                        tool_calls=0,
                        thread_id=None,
                        skill_read_observed=False,
                    )
                )
                for index, arm in enumerate(ARMS)
            }
        }

        prompt, mappings = build_blind_judge_request([case], runs)

        self.assertEqual(set(mappings[case.case_id].values()), set(ARMS))
        self.assertIn("answer-0", prompt)
        self.assertIn("answer-1", prompt)
        self.assertIn("answer-2", prompt)
        response_section = prompt.split("CASES_JSON:\n", 1)[1]
        self.assertNotIn('"baseline"', response_section)
        self.assertNotIn('"implicit"', response_section)
        self.assertNotIn('"explicit"', response_section)


class SkillEvalFreshnessAndReportTests(unittest.TestCase):
    def test_pack_peer_change_invalidates_every_marginal_comparison(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            for skill_name in ("demo", "peer"):
                skill_dir = root / "plugins" / "jy-env-core" / "skills" / skill_name
                scenario_dir = root / "skill-tests" / "first-party" / skill_name
                skill_dir.mkdir(parents=True)
                scenario_dir.mkdir(parents=True)
                (skill_dir / "SKILL.md").write_text(
                    f"---\nname: {skill_name}\ndescription: Use when testing.\n---\n",
                    encoding="utf-8",
                )
                (scenario_dir / "pressure-scenarios.json").write_text(
                    json.dumps(
                        {
                            "scenarios": [
                                {
                                    "id": "one",
                                    "title": "One",
                                    "prompt": "Do it",
                                    "expected_without_skill": "Misses it",
                                    "expected_with_skill": "Does it",
                                }
                            ]
                        }
                    ),
                    encoding="utf-8",
                )

            before = build_snapshot(
                root,
                model="gpt-5.6-sol",
                reasoning_effort="max",
                judge_model="gpt-5.6-luna",
                codex_version="codex-cli 0.149.0",
            )
            demo_skill = root / "plugins" / "jy-env-core" / "skills" / "demo" / "SKILL.md"
            demo_skill.write_text(
                "---\nname: demo\ndescription: Use when testing.\n---\nChanged.\n",
                encoding="utf-8",
            )
            after = build_snapshot(
                root,
                model="gpt-5.6-sol",
                reasoning_effort="max",
                judge_model="gpt-5.6-luna",
                codex_version="codex-cli 0.149.0",
            )

        self.assertEqual(stale_skills(after, before), {"demo", "peer"})

    def test_model_or_skill_hash_change_marks_expected_scope_stale(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            skill_dir = root / "plugins" / "jy-env-core" / "skills" / "demo"
            scenario_dir = root / "skill-tests" / "first-party" / "demo"
            skill_dir.mkdir(parents=True)
            scenario_dir.mkdir(parents=True)
            (skill_dir / "SKILL.md").write_text(
                "---\nname: demo\ndescription: Use when testing.\n---\nDo the thing.\n",
                encoding="utf-8",
            )
            (scenario_dir / "pressure-scenarios.json").write_text(
                json.dumps(
                    {
                        "scenarios": [
                            {
                                "id": "one",
                                "title": "One",
                                "prompt": "Do it",
                                "expected_without_skill": "Misses it",
                                "expected_with_skill": "Does it",
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )

            current = build_snapshot(
                root,
                model="gpt-5.6-sol",
                reasoning_effort="max",
                judge_model="gpt-5.6-luna",
                codex_version="codex-cli 0.149.0",
            )
            self.assertEqual(stale_skills(current, current), set())

            old_model = dict(current)
            old_model["model"] = "gpt-5.5"
            self.assertEqual(stale_skills(current, old_model), {"demo"})

            old_skill = json.loads(json.dumps(current))
            old_skill["skills"]["demo"]["skill_hash"] = "old"
            self.assertEqual(stale_skills(current, old_skill), {"demo"})

    def test_markdown_report_leads_with_model_and_verdict(self) -> None:
        report = {
            "run_id": "20260824T120000Z",
            "model": "gpt-5.6-sol",
            "reasoning_effort": "max",
            "judge_model": "gpt-5.6-luna",
            "codex_version": "codex-cli 0.149.0",
            "results": [
                {
                    "skill_name": "demo",
                    "verdict": "REMOVE_CANDIDATE",
                    "baseline_mean": 3.5,
                    "implicit_mean": 3.5,
                    "explicit_mean": 3.4,
                    "implicit_delta": 0.0,
                    "explicit_delta": -0.1,
                    "implicit_input_token_overhead_ratio": 0.4,
                    "implicit_latency_overhead_ratio": 0.2,
                    "baseline_input_tokens": 100,
                    "implicit_input_tokens": 140,
                    "explicit_input_tokens": 180,
                    "activation_rate": 0.5,
                    "implicit_activation_rate": 0.5,
                    "evidence_pairs": 6,
                }
            ],
        }

        markdown = render_markdown_report(report)
        self.assertIn("gpt-5.6-sol", markdown)
        self.assertIn("REMOVE_CANDIDATE", markdown)
        self.assertIn("demo", markdown)
        self.assertIn("baseline / implicit / explicit", markdown)

    def test_state_advances_only_for_decision_grade_results(self) -> None:
        current = build_snapshot(
            REPO_ROOT,
            model="gpt-5.6-sol",
            reasoning_effort="max",
            judge_model="gpt-5.6-luna",
            codex_version="codex-cli 0.149.0",
        )
        report = {
            "run_id": "run-1",
            "results": [
                {"skill_name": "jy-debugging", "verdict": "KEEP"},
                {"skill_name": "jy-test-driven", "verdict": "INSUFFICIENT"},
            ],
        }

        state = advance_state(current, previous_state={}, report=report)

        self.assertIn("jy-debugging", state["snapshot"]["skills"])
        self.assertNotIn("jy-test-driven", state["snapshot"]["skills"])
        self.assertEqual(
            state["evaluations"]["jy-debugging"]["last_run_id"], "run-1"
        )

    def test_plan_cli_is_cost_preview_only(self) -> None:
        stdout = io.StringIO()
        with redirect_stdout(stdout):
            exit_code = main(
                [
                    "plan",
                    "--repo-root",
                    str(REPO_ROOT),
                    "--skill",
                    "jy-change-guardrails",
                    "--scenario",
                    "one-off-change-pressure",
                    "--repetitions",
                    "1",
                ]
            )

        self.assertEqual(exit_code, 0)
        output = stdout.getvalue()
        self.assertIn("gpt-5.6-sol", output)
        self.assertIn("task_calls: 3", output)
        self.assertIn("judge_calls: 1", output)
        self.assertIn("total_model_calls: 4", output)

    def test_plan_cli_accepts_explicit_all_without_model_calls(self) -> None:
        stdout = io.StringIO()
        with redirect_stdout(stdout):
            exit_code = main(["plan", "--repo-root", str(REPO_ROOT), "--all"])

        self.assertEqual(exit_code, 0)
        output = stdout.getvalue()
        skill_count = len(discover_skill_dirs(REPO_ROOT))
        self.assertIn(f"skills: {skill_count}", output)
        self.assertIn(f"total_model_calls: {skill_count * 19}", output)
        self.assertIn("executes_models: no", output)

    def test_run_cli_accepts_explicit_resume_run_id(self) -> None:
        args = build_parser().parse_args(
            [
                "run",
                "--repo-root",
                str(REPO_ROOT),
                "--skill",
                "jy-change-guardrails",
                "--resume-run",
                "20260824T025335.545900Z-gpt-5.6-sol",
            ]
        )

        self.assertEqual(
            args.resume_run,
            "20260824T025335.545900Z-gpt-5.6-sol",
        )

    def test_status_cli_reports_all_skills_stale_without_prior_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                exit_code = main(
                    [
                        "status",
                        "--repo-root",
                        str(REPO_ROOT),
                        "--output-dir",
                        temp_dir,
                        "--codex-version",
                        "codex-cli 0.149.0",
                    ]
                )

        self.assertEqual(exit_code, 2)
        expected_count = len(discover_skill_dirs(REPO_ROOT))
        self.assertIn(f"stale_skills: {expected_count}", stdout.getvalue())

    def test_report_cli_prints_latest_human_report(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir)
            (output_dir / "latest.md").write_text(
                "# Latest\n\n- verdict: KEEP\n",
                encoding="utf-8",
            )
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                exit_code = main(
                    [
                        "report",
                        "--repo-root",
                        str(REPO_ROOT),
                        "--output-dir",
                        temp_dir,
                    ]
                )

        self.assertEqual(exit_code, 0)
        self.assertIn("verdict: KEEP", stdout.getvalue())


if __name__ == "__main__":
    unittest.main()
