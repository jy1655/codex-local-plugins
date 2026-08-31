# GPT-5.6 Sol 스킬 실용성 20/34 실동작 평가 및 검증라인 감사

## 결론

요청한 순서의 첫 20개 스킬에서 실행을 멈췄다. 논리적으로는 360개 task 응답과
20개 blind-judge 호출이 모두 정상 종료했지만, 실행 도중 Codex CLI 설치가
`0.149.0`에서 `0.149.1`로 교체됐다. 따라서 이번 결과의 최종 증거 등급은
**PARTIAL**이며, 자동 verdict를 근거로 지금 삭제할 스킬은 **0개**다.

자동 결과는 `KEEP 3`, `REMOVE_CANDIDATE 4`, `REVISE 3`, `REVISE_COST 4`,
`REVISE_TRIGGER 3`, `INCONCLUSIVE 3`이었다. raw 응답을 검토하면 자동 삭제 후보
네 개 가운데 다음 두 종류가 섞여 있다.

- `jy-codebase-explore`, `jy-document-release`: 빈 workspace 때문에 세 arm 모두
  실제 대상 없이 안전하게 중단해 동률 만점을 받았다. 스킬 무용성이 아니라
  **fixture 공허성**이다.
- `ios-ettrace-performance`, `ios-memgraph-leaks`: 일반적인 증거 원칙은 native
  baseline도 잘 지켰지만, 스킬의 핵심인 실제 trace/memgraph 캡처·분석·스크립트
  동작은 전혀 실행하지 않았다. **설명 응답의 중복**만 관측됐다.

이 하네스는 자기완결형 decision-response 스킬의 한계효용을 거르는 1차
스크리닝에는 쓸 수 있다. repository, web, Xcode, Simulator, browser, device 또는
외부 서비스가 역할의 본체인 스킬의 추가·삭제 게이트로는 아직 부적절하다.

## 실행 범위와 완전성

- 실행 구간: 2026-08-24 11:53:35–17:14:42 KST
- run id: `20260824T025335.545900Z-gpt-5.6-sol`
- task model: `gpt-5.6-sol`, reasoning `max`, service tier `fast`
- judge model: `gpt-5.6-luna`, reasoning `medium`
- 비교: baseline / implicit / explicit, arm 순서 결정적 shuffle
- 선택 범위: 20/34 skills
- scenario asset: 선택 20개 스킬에 총 64개, 실행 40개(62.5%)
- 반복: scenario당 3회, arm 3개
- 성공 산출물: task `360/360`, judge `20/20`
- 빈 final message: `0`
- logical model calls: `380`
- physical attempts: `381` — 최초 실행의 task 한 개가 600초 timeout 후 복구
  실행에서 재시도됐다.
- evidence scope: `decision_response`
- runtime verified: `false`

원 실행은 348개 task 성공 뒤 `jy-receiving-review`의
`triage-and-verify-feedback:2/baseline`이 600초 timeout으로 종료됐다. 평가기는 당시
모든 task가 끝난 후에야 judge를 시작하는 구조였으므로 judge 결과는 0개였다.
복구 기능을 추가해 성공 artifact 348개를 재사용하고 남은 task 12개와 judge 20개만
실행했다. 재시도된 arm은 약 200초에 성공했으므로 timeout 자체는 재현되지 않았다.

## 20개 결과와 사람 검토

`B/I/E`는 blind quality 평균(0–4)이다. 아래 사람 검토는 자동 verdict를 raw 응답,
activation, fixture 가용성과 함께 해석한 결과다.

| Skill | 자동 verdict | B / I / E | Implicit read | 사람 검토 |
|---|---|---:|---:|---|
| `ios-app-intents` | INCONCLUSIVE | 1.50 / 2.50 / 3.67 | 100% | 명시 호출 효용이 크다. 제거 금지; implicit 준수 일관성을 재검증한다. |
| `ios-debugger-agent` | INCONCLUSIVE | 1.67 / 2.83 / 3.83 | 100% | 명시 호출 효용이 크다. 실제 XcodeBuildMCP fixture 전 삭제 금지. |
| `ios-ettrace-performance` | REMOVE_CANDIDATE | 3.50 / 3.33 / 3.33 | 100% | 일반 조언은 중복되지만 실제 ETTrace 역할은 미검증. 삭제 승인 안 함. |
| `ios-memgraph-leaks` | REMOVE_CANDIDATE | 3.67 / 3.83 / 3.67 | 100% | 일반 조언은 포화됐지만 캡처·ownership path 분석은 미검증. 삭제 승인 안 함. |
| `ios-simulator-browser` | REVISE | 1.67 / 2.33 / 2.33 | 100% | Simulator/browser가 없어 target behavior를 수행할 수 없었다. fixture invalid. |
| `jy-autoplan` | REVISE_COST | 3.00 / 3.67 / 4.00 | 100% | 품질 효용 확인. token +45.1%, latency +43.0%; 유지하며 비용 재검증. |
| `jy-change-guardrails` | KEEP | 2.83 / 3.50 / 4.00 | 100% | 한계효용과 비용 기준 모두 통과. 현재 20개 중 가장 직접적인 유지 증거. |
| `jy-checkpoint` | REVISE_TRIGGER | 3.00 / 3.00 / 3.50 | 100% | repo/branch/checkpoint가 없어 저장·복구를 못 했다. trigger 결론 무효. |
| `jy-codebase-explore` | REMOVE_CANDIDATE | 4.00 / 4.00 / 4.00 | 100% | 빈 repository 때문에 공허한 동률. repo-backed fixture가 필요하다. |
| `jy-consult` | REVISE_TRIGGER | 2.83 / 2.83 / 3.67 | 50% | explicit 효용은 있으나 implicit routing 약점 후보. trigger 설명 재검증. |
| `jy-debugging` | REVISE | 3.67 / 3.33 / 4.00 | 100% | baseline 포화와 한 번의 implicit 준수 분산. 실제 재현 가능한 bug fixture 전 수정·삭제 보류. |
| `jy-document-release` | REMOVE_CANDIDATE | 4.00 / 4.00 / 4.00 | 100% | diff와 docs가 없는 빈 repository에서 모두 중단했다. fixture invalid. |
| `jy-env-sync-admin` | KEEP | 2.50 / 3.50 / 3.67 | 100% | implicit +1.00, 비용 감소. decision-response 범위에서 유지 근거 확인. |
| `jy-executing-plans` | REVISE | 2.33 / 2.50 / 2.67 | 100% | plan/repository 부재로 실행 규율을 실제 행사하지 못했다. 수정 근거 부족. |
| `jy-explain-change` | INCONCLUSIVE | 3.50 / 4.00 / 3.50 | 50% | diff 부재 사례와 near-match 비활성 사례만 실행. 제거·수정 결론 없음. |
| `jy-framing` | REVISE_COST | 2.33 / 3.67 / 4.00 | 100% | 품질 효용이 강하다. token +79.1%, latency +21.3%; 유지하며 비용 기준 재검토. |
| `jy-grill-me` | REVISE_COST | 1.00 / 3.00 / 3.00 | 100% | 품질 +2.00, latency -41.1%. token +41.0%만으로 revise한 비용 taxonomy를 재검토. |
| `jy-library-research` | REVISE_TRIGGER | 2.83 / 3.00 / 3.33 | 100% | web search를 강제로 꺼 공식 source/issue 확인 역할을 막았다. verdict 무효. |
| `jy-plan-review` | REVISE_COST | 2.50 / 3.33 / 4.00 | 100% | 품질 효용 확인. input +3.9%, latency +59.4%; 유지하며 latency 재측정. |
| `jy-receiving-review` | KEEP | 2.67 / 4.00 / 4.00 | 100% | implicit/explicit +1.33, 비용 감소. decision-response 범위에서 유지 근거 확인. |

사람 검토 결과는 다음과 같다.

- 즉시 삭제: **0**
- 현재 유지 근거가 비교적 직접적인 스킬: `jy-change-guardrails`,
  `jy-env-sync-admin`, `jy-receiving-review`
- 강한 효용이 있으나 cost/routing을 다시 볼 스킬: `ios-app-intents`,
  `ios-debugger-agent`, `jy-autoplan`, `jy-consult`, `jy-framing`, `jy-grill-me`,
  `jy-plan-review`
- fixture가 역할을 행사하지 못해 판단 보류: `ios-ettrace-performance`,
  `ios-memgraph-leaks`, `ios-simulator-browser`, `jy-checkpoint`,
  `jy-codebase-explore`, `jy-document-release`, `jy-executing-plans`,
  `jy-library-research`
- 현재 시나리오에서 결론이 약한 스킬: `jy-debugging`, `jy-explain-change`

## 검증라인 자체 감사

### 적절하게 작동한 부분

1. 대상 스킬만 제거한 baseline과 같은 pack peer를 유지한 implicit/explicit을
   비교해 bundle 내부 한계효용을 측정했다.
2. baseline과 implicit task prompt는 동일하고 explicit만 명시 호출을 추가했다.
3. arm 실행 순서와 judge A/B/C mapping을 결정적으로 섞었다.
4. task의 token, latency, tool call, `SKILL.md` read, final response와 judge 근거를
   원시 artifact로 남겼다.
5. 성공 artifact의 prompt·discoverable-skill context·judge label mapping·returncode가
   모두 일치할 때만 재사용하는 복구 경로가 실제 348개 응답에서 동작했다.

### 삭제 게이트로 막는 결함

1. **Codex CLI 세대 혼합 — P0.** backend는 시작할 때 `0.149.0`만 기록했다.
   `/Users/jy/.nvm/.../@openai/codex/package.json`과 shim은 17:02경 in-place 갱신됐고,
   현재 `codex --version`은 `0.149.1`이다. 복구 task 12개는 17:04–17:09,
   judge 20개는 17:09–17:14에 생성됐다. 각 subprocess가 실제 사용한 version을
   artifact에 기록하지 않아 동일 CLI 세대는 증명되지 않는다. `status`가 즉시
   34개 전부 stale로 만든 것은 안전한 결과다.
2. **역할별 fixture 부재 — P0.** 모든 task를 빈 read-only workspace에서 실행하고
   web search도 비활성화했다. repository 탐색·수정, 계획 실행, library research,
   Simulator/browser/Xcode/profile 도구의 핵심 동작을 관측할 수 없다.
3. **fixture validity/vacuity gate 부재 — P0.** 세 arm 모두 입력 부재로 안전하게
   중단해도 고득점 동률이면 `REMOVE_CANDIDATE`가 된다. judge가 먼저
   `VALID / INVALID_FIXTURE / RUNTIME_REQUIRED`를 판정해야 한다.
4. **scenario 대표성 부족 — P1.** 20개 스킬의 64개 scenario 중 각 파일 앞 두 개만
   선택해 40개(62.5%)만 실행했다. 13개 스킬은 mode/routing/negative 사례 일부가
   순서 때문에 제외됐다.
5. **단일 judge — P1.** 스킬당 Luna batch 한 번뿐이며 judge 반복, 두 번째 judge,
   사람 calibration sample이 없다. 평균 confidence 0.92–0.99는 합의도나 정확도
   증거가 아니다.
6. **activation/compliance 혼합 — P1.** `SKILL.md`를 100% 읽었어도 implicit 품질이
   explicit보다 낮으면 `REVISE_TRIGGER`가 될 수 있다. read 실패와 읽은 규칙의
   준수 분산을 분리해야 한다.
7. **cost taxonomy의 과잉 단순화 — P1.** 6회 평균이 threshold를 조금 넘으면 품질
   이득의 크기나 task class와 무관하게 `REVISE_COST`다. 예를 들어 `jy-grill-me`는
   품질 +2.00, latency -41.1%인데 input token +41.0%만으로 비용 수정 대상이 됐다.
8. **attempt provenance 손실 — P1.** retry가 같은 artifact 경로를 덮어써 최초
   timeout record가 최종 tree에 남지 않는다. report의 executed/reused 수치도 복구
   invocation만 나타내고 전체 physical attempts를 나타내지 않는다.

OpenAI의 [latest model guidance](https://developers.openai.com/api/docs/guides/latest-model)는
대표 task로 quality·token·latency·cost를 측정하고 instruction group을 하나씩 제거해
같은 eval을 재실행하는 방식을 권한다. 현재 3-arm 구조는 그 비교 원칙에는 맞지만,
이번 task set은 여러 스킬에서 대표 runtime을 제공하지 못했고 실행 세대도 고정하지
못했다.

## 검증라인 변경

이번 timeout을 근거로 다음 최소 변경을 적용했다.

- `--resume-run <run-id>` 추가
- 성공 task artifact의 prompt와 skill context가 정확히 일치할 때만 재사용
- 성공 judge artifact의 blind prompt와 label mapping이 정확히 일치할 때만 재사용
- 실행/재사용 task·judge 수를 report에 기록
- 회귀 테스트 추가 및 CLI 사용법 문서화

이 복구 기능은 손실을 줄였지만 CLI version/model/policy/evaluator contract를 run 시작부터
고정하지 않는다. 그러므로 현재 상태는 **복구 가능성 VERIFIED, 동종 실행 보장
NOT-VERIFIED**다.

## 남은 14개

사용자 지시에 따라 다음 스킬은 실행하지 않았다.

- `jy-review-all`, `jy-review-work`, `jy-ship`, `jy-slop-remover`
- `jy-test-driven`, `jy-verification-before-completion`, `jy-waterfall`, `jy-worktrees`
- `jy-writing-plans`, `jy-writing-skills`
- `swiftui-liquid-glass`, `swiftui-performance-audit`, `swiftui-ui-patterns`,
  `swiftui-view-refactor`

현재 CLI가 `0.149.1`로 바뀌었으므로 20개뿐 아니라 전체 34개가 freshness 기준상 stale다.
남은 14개를 그대로 이어 실행하면 이번 20개와 하나의 동종 baseline으로 합칠 수 없다.

## 검증 명령과 증거 경계

- `python3 -m pytest tests/test_skill_eval.py -q`: `32 passed`
- `python3 -m pytest -q`: `110 passed, 346 subtests passed`
- `python3 -m compileall -q codex_env_sync tests`: 성공
- task `execution.json`: returncode 0인 파일 `360`
- task `observation.json`: `360`; 빈 final message `0`
- judge `execution.json`: returncode 0인 파일 `20`
- judge `structured-output.json`: `20`
- `python3 -m codex_env_sync.skill_eval status --repo-root .`: stale `34`

최종 상태:

- **VERIFIED:** 20개 범위의 360개 응답과 20개 구조화 judge 결과가 저장됐고
  산출물 수와 returncode가 완전하다.
- **VERIFIED:** 재개 시 성공 artifact 348개만 재사용하고 실패·미실행 12개만
  실행하는 경로가 동작했다.
- **PARTIAL:** decision-response에서 관측된 품질 차이와 비용·activation 신호.
- **NOT-VERIFIED:** 동일 Codex CLI 세대 재현성, runtime/tool 동작, 자동 삭제 후보의
  실제 제거 적합성, 남은 14개 스킬의 실용성.

원시 산출물은 ignored local 경로
`.codex/skill-evals/runs/20260824T025335.545900Z-gpt-5.6-sol/`에 있다.

## 다음 실행 전 필요 조건

`[necessity-gate]`

- basis: `evidenced` — CLI drift, invalid fixture, scenario 62.5% 선택, 단일 judge,
  timeout provenance 손실이 이번 실행에서 직접 관측됐다.
- decision: 남은 14개를 실행하기 전에 per-call CLI contract와 fixture-validity gate를
  먼저 고친다. 삭제/수정은 새 동종 run과 raw review 뒤 한 스킬씩 결정한다.
