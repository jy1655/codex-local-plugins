# `jy-change-guardrails` GPT-5.6 Sol 실동작 평가 보고서

## 결론

`jy-change-guardrails`는 **즉시 제거 대상이 아니다.** 과잉 일반화를 유도한
시나리오에서 native baseline보다 반복 3회 중 2회 더 나은 결정을 만들었고,
명시 호출은 3회 모두 개선됐다. 다만 implicit 평균 향상은 `+0.33`으로 정책의
의미 있는 향상 기준 `+0.50`에 못 미쳤으므로 `KEEP`도 아직 확정할 수 없다.

자동 판정은 `REVISE_TRIGGER`다. 그러나 raw log에서 implicit arm은 6/6 모두
대상 `SKILL.md`를 읽었다. 실제 약점은 발견 실패보다 **읽은 지침을 한 반복에서
일관되게 지키지 못한 것**이다. 따라서 사람 검토 결론은 다음과 같다.

- 스킬: 현 상태로 보존하되 문구를 즉시 늘리지 않는다.
- 평가기: `REVISE_TRIGGER`와 `REVISE_COMPLIANCE`를 분리할 필요가 있다.
- 시나리오: native baseline이 전부 만점인 포화 시나리오는 더 변별력 있는
  repo-backed 시나리오로 교체하거나 보강한다.
- 범위: 이번 결과를 나머지 33개 스킬로 일반화하지 않는다.

## 실행 계약

- 실행 시각: 2026-08-24 11:28–11:42 KST
- 실행 명령: `python3 -m codex_env_sync.skill_eval run --repo-root . --skill jy-change-guardrails`
- run id: `20260824T022831.194424Z-gpt-5.6-sol`
- tested model: `gpt-5.6-sol`, reasoning effort `max`, service tier `fast`
- blind judge: `gpt-5.6-luna`, reasoning effort `medium`
- Codex: `codex-cli 0.149.0`
- repository commit: `61589aa8c3325598c8976311cfa2c8a033d6e80d`
- repository state: dirty working tree. evaluator 구현 중 변경과 기존 사용자 변경이
  함께 있었으므로 commit만으로 실행 입력 전체를 재구성할 수 없다. report의
  snapshot hash가 실제 skill·pack·scenario·policy·evaluator 입력을 고정한다.
- evidence scope: `decision_response`; runtime verified: `false`

두 시나리오를 각각 3회 반복하고, 매 반복에서 같은 작업을 세 arm으로 실행했다.

1. `baseline`: 대상 스킬만 제외하고 같은 `jy-env-core` pack peer 6개를 노출
2. `implicit`: 대상 스킬과 peer 6개를 노출하되 작업 prompt는 그대로 유지
3. `explicit`: 같은 7개를 노출하고 `$jy-change-guardrails`를 명시

총 task call은 18회, blind batched judge call은 1회다. 세 arm은 빈 read-only
workspace와 격리된 임시 home에서 실행했고 judge에는 arm 이름을 숨겼다. 이
방식은 한 번에 한 instruction/tool 집합만 바꾸고 같은 대표 작업으로 다시
평가하라는 [OpenAI GPT-5.6 model guidance](https://developers.openai.com/api/docs/guides/latest-model)의
원칙과도 일치한다.

## 측정 결과

| 지표 | Baseline | Implicit | Explicit |
|---|---:|---:|---:|
| blind quality 평균 (0–4) | 3.50 | 3.83 | 4.00 |
| baseline 대비 향상 | — | +0.33 | +0.50 |
| `SKILL.md` read 관측 | 대상 없음 | 6/6 (100%) | 5/6 (83.3%) |
| 평균 input tokens | 70,369 | 78,636 | 78,809 |
| 평균 output tokens | 1,843 | 1,964 | 2,181 |
| 평균 elapsed | 44.05초 | 41.84초 | 47.61초 |

Implicit input-token overhead는 `+11.75%`로 정책 상한 `+25%` 이내다. latency는
baseline보다 `-5.04%`였으며 상한 `+50%`를 넘지 않았다. 따라서 이번 판정의
병목은 비용이 아니라 품질 향상 기준이다.

정책 기준은 quality floor `3.0`, meaningful gain `0.50`, 최소 implicit activation
`80%`, 최소 2개 시나리오·6개 evidence pair다. 모든 evidence volume과 confidence
조건은 충족했고 judge confidence 평균은 `0.957`이었다.

## 시나리오별 결과

| 시나리오 | 반복별 Baseline | 반복별 Implicit | 반복별 Explicit | 해석 |
|---|---:|---:|---:|---|
| `ambiguous-feature-scope` | 4 / 4 / 4 | 4 / 4 / 4 | 4 / 4 / 4 | native model도 이미 assumptions·범위를 잘 처리했다. 이 사례는 현재 모델에서 포화되어 변별력이 낮다. |
| `one-off-change-pressure` | 3 / 3 / 3 | 4 / 4 / 3 | 4 / 4 / 4 | 스킬의 한계효용이 관측됐지만 implicit 준수는 한 번 흔들렸다. |

`one-off-change-pressure`의 baseline은 세 번 모두 코드베이스 확인 전에 interface나
registry를 제안했다. implicit은 첫 두 번 이를 거부했지만 세 번째에는
`rule interface plus registration`을 가장 작은 확장점으로 미리 제안해 3점을
받았다. 그 실행은 대상 `SKILL.md`를 실제로 읽었으므로 발견 문제가 아니라
행동 준수의 분산이다.

반대로 explicit 세 번째 실행은 `SKILL.md` read가 관측되지 않았지만 “기존 설계가
정당화할 때만 interface/registry를 도입한다”는 답으로 4점을 받았다. 이는 skill
read activation과 최종 행동 품질이 별도 축이며, 둘을 하나의 verdict 이름으로
합치면 원인을 오진할 수 있음을 보여준다.

## 판정 해석과 조치

기계 판정 `REVISE_TRIGGER`는 재현 가능한 정책 결과로 그대로 보존한다. 다만
implicit activation이 100%이므로 “trigger 설명이 약하다”가 이번 raw evidence의
주원인은 아니다. 다음 판정 분리가 더 정확하다.

- `REVISE_TRIGGER`: implicit read 자체가 기준 미달이고 explicit arm만 개선됨
- `REVISE_COMPLIANCE`: implicit read는 기준을 충족하지만 행동 향상이 기준 미달이고
  explicit arm은 개선됨

현재 `SKILL.md`에는 이미 “기존 project pattern을 먼저 재사용”, “future-proofing과
configurability는 요청되지 않으면 범위 밖”이라는 규칙이 있다. 한 번의 분산을
근거로 같은 문장을 더 반복하면 오히려 context 병목을 키울 수 있으므로, 이번에는
skill source를 수정하지 않는다. 먼저 verdict taxonomy와 변별 시나리오를 개선한 뒤
같은 모델·조건으로 재실행해야 한다.

## 후속 검증

- `python3 -m pytest tests/test_skill_eval.py -q`: `29 passed`
- `python3 -m codex_env_sync.skill_eval report --repo-root .`: 저장된 run과 동일한
  `REVISE_TRIGGER`, quality·cost·activation 수치를 재출력
- 18개 task execution과 1개 judge execution: 모두 return code `0`, final message
  누락 `0`
- `status`: `jy-change-guardrails`는 fresh, 미실행 33개는 stale

## 증거 경계

- **VERIFIED:** 18개 task call과 1개 judge call이 정상 종료했고, token·latency·read
  observation·blind score가 report에 저장됐다.
- **VERIFIED:** `jy-change-guardrails`는 현재 snapshot에서 fresh이며 나머지 33개
  스킬은 아직 stale다.
- **PARTIAL:** 빈 workspace의 의사결정 응답만 검증했다. 실제 repository edit,
  build, test, device, external service 동작은 검증하지 않았다.
- **NOT-VERIFIED:** 7개 core 전체와 27개 optional 전체의 실용성, 다른 reasoning
  effort·service tier·server-side snapshot에서의 재현성.

원시 산출물은 local ignored 경로
`.codex/skill-evals/runs/20260824T022831.194424Z-gpt-5.6-sol/`에 보존된다.
