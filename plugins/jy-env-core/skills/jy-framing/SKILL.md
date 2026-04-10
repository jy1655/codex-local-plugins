---
name: jy-framing
description: Use when a user is still shaping a product or feature direction and needs a sharp problem brief before implementation planning.
---

# JY Framing

## Overview

아이디어 단계의 요청을 바로 구현으로 밀지 않고, 누가 왜 이 기능을 필요로 하는지부터 좁혀서
짧고 실행 가능한 brief로 만든다. 이 skill은 외부 runtime이나 숨겨진 상태 디렉터리를 가정하지 않는다.

이 skill은 Codex의 현재 collaboration mode를 인식해서 동작해야 한다. Plan Mode가 필요한 경우에도
skill 자체가 모드를 바꾸지는 못한다.

## When to Use

- 새 제품 아이디어, 기능 방향, 범위 재정의 요청
- "이 방향이 맞나", "이걸 만들 가치가 있나", "어떻게 스코프를 잡지" 같은 대화
- 구현 전에 사용자, 문제, 성공 기준을 먼저 정리해야 할 때

사용하지 않을 때:
- 이미 구현 계획이 decision-complete한 경우
- 코드 수정만 남은 경우

## Quick Reference

| 단계 | 행동 |
|------|------|
| 0. 모드 확인 | 현재가 Default인지 Plan인지 먼저 판단 |
| 1. 문맥 읽기 | 현재 요청과 관련 repo 문서를 확인 |
| 2. 문제 고정 | 사용자, 고통, 현재 우회 수단을 구체화 |
| 3. 범위 축소 | smallest useful wedge와 non-goals 정리 |
| 4. brief 작성 | success criteria와 open questions 포함 |
| 5. handoff | `jy-plan-review` 또는 구현 착수 추천 |

## Expected Inputs

- 현재 사용자 요청
- 관련 repo 문서: `README.md`, `instructions/AGENTS.md`, 기존 계획 문서
- 사용자가 명시한 제약, 일정, 대상 사용자

## Expected Output

다음 항목이 들어간 짧은 brief:

- target user
- concrete problem
- current workaround or status quo
- smallest useful wedge
- success criteria
- non-goals
- open questions
- recommended next step

## Mode-Aware Behavior

### If current collaboration mode is Default

- 질문 왕복이 꼭 필요한지 먼저 판단한다.
- 왕복이 필요하면 이렇게 짧게 유도한다:
  - "이건 Plan Mode가 맞습니다. `Shift+Tab`으로 Plan Mode로 바꾼 뒤 `/jy-framing`를 다시 실행하세요."
- 그 자리에서 끝내지 말고, 가능하면 최소한의 compact brief 초안을 같이 준다.
- Default mode에서는 `request_user_input` 같은 Plan 전용 흐름을 전제로 쓰지 않는다.

### If current collaboration mode is Plan

- open question을 실제로 좁힌다.
- 필요할 때만 질문하고, 최종 산출물은 brief로 정리한다.
- 결과는 구현으로 바로 가지 말고 다음 단계가 `jy-plan-review`인지 구현인지 명확히 남긴다.

## Workflow

1. 현재 collaboration mode가 Default인지 Plan인지 확인한다.
2. 현재 요청과 repo 문맥을 읽고 문제 영역을 파악한다.
3. 아이디어를 사용자, 고통, 제약 기준으로 구체화한다.
4. vague wording를 measurable wording으로 바꾼다.
5. 구현으로 넘어가기 전에 합의되어야 할 핵심 결정을 brief로 정리한다.
6. 다음 단계로 `jy-plan-review` 또는 구현 착수를 추천한다.

## Boundaries

- 코드 작성 금지
- 외부 리서치 전제 금지
- 숨겨진 sidecar state 파일 전제 금지
- 산출물은 대화 응답 또는 repo-visible 계획 문서 기준으로 설명

## Common Mistakes

- Plan Mode가 필요한데 skill이 모드를 바꿀 수 있다고 가정하는 것
- Default mode인데 Plan 전용 질문 흐름을 바로 시작하는 것
- 사용자보다 해결책을 먼저 고르는 것
- 범위를 줄이지 않고 바로 큰 시스템으로 일반화하는 것
- success criteria 없이 좋은 아이디어처럼만 정리하는 것
- 다음 단계가 무엇인지 남기지 않고 끝내는 것
