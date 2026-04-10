---
name: jy-autoplan
description: Use when the user wants the Codex planning pack to decide the next planning step automatically and return one consolidated result.
---

# JY Autoplan

## Overview

현재 요청이 brief 단계인지, plan review 단계인지 먼저 판단하고 `jy-framing`와
`jy-plan-review` 중 필요한 경로를 자동으로 선택하는 orchestrator.

중요한 제약이 하나 있다. 이 skill은 적절한 planning 경로는 고를 수 있지만, Codex의 Plan Mode를
직접 켜지는 못한다. 모드 전환이 필요하면 사용자에게 `Shift+Tab`을 안내해야 한다.

## When to Use

- "autoplan", "전체 planning 흐름 돌려줘", "계획 단계 알아서 진행해줘" 요청
- 사용자가 problem framing과 plan review를 분리해서 지시하지 않았을 때
- 하나의 consolidated planning outcome이 필요할 때

사용하지 않을 때:
- 사용자가 특정 planning skill을 직접 지정한 경우
- 코드 구현 요청이 이미 명확한 경우

## Quick Reference

| 단계 | 행동 |
|------|------|
| 0. 모드 확인 | 현재가 Default인지 Plan인지 판단 |
| 1. maturity 판정 | 아이디어 단계인지 plan 단계인지 구분 |
| 2. route 선택 | `jy-framing` 또는 `jy-plan-review` 선택 |
| 3. 결과 통합 | brief 또는 revised plan을 하나로 요약 |
| 4. next step | 사용자가 바로 다음 행동을 고를 수 있게 정리 |

## Routing Matrix

### 1. Idea-stage

신호:

- "이걸 만들 가치가 있나", "어디서부터 시작하지", "방향이 맞나"
- 사용자, 문제, 성공 기준이 아직 흐림
- 기능보다 문제 정의가 먼저 필요한 상태

경로:

- `jy-framing`

출력:

- compact brief draft 또는 Plan Mode용 office-hours handoff

### 2. Plan-stage

신호:

- 이미 plan, spec, proposal, outline, design doc, TODO 초안이 있음
- "빠진 결정 채워줘", "이대로 구현 가능해?", "구현 전에 잠그자"
- implementation 전에 decision-complete review가 필요한 상태

경로:

- `jy-plan-review`

출력:

- compact review summary 또는 Plan Mode용 plan-review handoff

### 3. Execution-ready

신호:

- "구현해", "바로 고쳐", "코드 바꿔", "테스트 돌려", "리뷰 실행해"
- 이미 구현이 끝났고 실제 review/QA/execution이 필요함
- planning보다 실행이 병목인 상태

경로:

- planning pack으로 억지 라우팅하지 않음
- 필요 시 Default mode에서 구현 또는 `jy-review-work` 같은 execution skill로 보냄

출력:

- planning pack not applicable 판단과 적절한 next step

## Routing Rules

- 사용자가 `jy-framing` 또는 `jy-plan-review`를 직접 지정했으면 autoplan이 덮어쓰지 않는다.
- idea-stage면 `jy-framing`
- plan-stage면 `jy-plan-review`
- 아이디어와 plan이 섞여 있지만 핵심 불확실성이 문제 정의 쪽이면 `jy-framing` 먼저
- execution-ready면 planning pack으로 보내지 않는다
- 요청이 "구현 전 결정 잠금"인지 "지금 실행"인지 애매하면, 사용자의 마지막 동사를 우선한다
  - "review the plan" -> plan-stage
  - "review my implementation" -> execution-ready

## Expected Output

- 현재 요청의 maturity 판정
- 그 판정 이유 한 줄
- 선택한 skill 경로 또는 planning pack not applicable 판정
- 최종 brief, revised plan, 또는 compact routing summary
- 다음 실행 단계 하나

## Mode-Aware Behavior

### If current collaboration mode is Default

- planning maturity만 판단하고 끝내지 않는다.
- 현재 요청이 idea-stage 또는 plan-stage면:
  - 어떤 skill 경로가 맞는지 먼저 판정한다.
  - 그 다음 "이건 Plan Mode가 맞습니다. `Shift+Tab`으로 Plan Mode로 바꾼 뒤 `/{skill-name}`를 다시 실행하세요."라고 유도한다.
- 그래도 사용자가 바로 얻을 수 있는 최소 결과는 남긴다.
  - idea stage면 compact brief draft
  - plan stage면 compact review summary
- 현재 요청이 execution-ready면:
  - Plan Mode를 권하지 않는다.
  - "이건 planning보다 실행이 먼저입니다. Default mode에서 바로 구현하거나 `/jy-review-work` 같은 실행형 skill로 가세요."라고 정리한다.
  - planning pack not applicable 판단을 명시한다.

### If current collaboration mode is Plan

- idea-stage면 `jy-framing` 경로로 실제 대화를 이어간다.
- plan-stage면 `jy-plan-review` 경로로 실제 대화를 이어간다.
- 결과가 plan-review 쪽이면 최종 출력은 `<proposed_plan>` 기준을 따른다.
- execution-ready면 Plan Mode에 머물지 않는다.
  - "이건 실행형 작업이라 Plan Mode보다 Default mode가 맞습니다. `Shift+Tab`으로 나온 뒤 다시 실행하세요."라고 유도한다.
- 결과를 하나의 consolidated planning outcome으로 합친다.

## Workflow

1. 현재 collaboration mode가 Default인지 Plan인지 확인한다.
2. 사용자가 특정 planning skill을 이미 직접 지정했는지 확인한다.
3. 현재 요청과 repo 문맥에서 maturity를 `idea-stage / plan-stage / execution-ready` 중 하나로 판단한다.
4. 판정 이유를 한 줄로 정리한다.
5. 필요한 skill 경로를 고르거나 planning pack not applicable로 판정한다.
6. mode에 맞는 방식으로 결과를 생성한다.
7. 결과를 하나의 요약으로 합친다.
8. 사용자가 바로 구현 또는 추가 planning을 선택할 수 있게 next step을 남긴다.

## Boundaries

- 외부 orchestration runtime 전제 금지
- third-party review pack 전제 금지
- 결과는 single-response 중심으로 정리
- execution-ready 요청을 억지로 planning workflow로 바꾸지 않는다

## Common Mistakes

- skill routing과 mode switching을 같은 일로 착각하는 것
- Plan Mode가 필요한데 그냥 skill 이름만 추천하고 끝내는 것
- Default mode에서 consolidated output 없이 "Plan Mode로 가라"만 말하는 것
- execution-ready 요청도 무조건 planning pack으로 밀어 넣는 것
- 사용자가 이미 직접 지정한 planning skill을 autoplan이 덮어쓰는 것
- routing 결정을 하지 않고 planning 조언만 섞어서 주는 것
- 아이디어 단계 요청을 바로 plan review로 보내는 것
- plan이 있는데 다시 문제 정의 단계로 되돌리는 것
- consolidated 결과 없이 단편적인 다음 행동만 남기는 것
