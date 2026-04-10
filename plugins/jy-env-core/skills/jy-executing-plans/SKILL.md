---
name: jy-executing-plans
description: Use when a written implementation plan already exists and needs to be executed task by task in the current session.
---

# JY Executing Plans

## Overview

이미 작성된 implementation plan을 현재 세션에서 step-by-step으로 실행하는 skill.
핵심은 계획을 읽고 바로 코드를 쏟아내는 것이 아니라, 각 step을 현재 문맥에서 검증하면서 닫는 것이다.

이 skill은 `current session` executor다. 이 wave에서는 `does not auto-spawn subagents`.

## When to Use

- "이 계획 실행해", "plan 기준으로 진행해", "checkbox 따라 가자"
- written plan이 이미 있고 실제 작업만 남은 경우
- human이 plan은 승인했고 현재 세션에서 구현을 닫고 싶은 경우

사용하지 않을 때:

- plan이 아직 없는 경우 (`jy-writing-plans`)
- plan에 decision gap이 큰 경우 (`jy-plan-review`)
- 단순 routing이나 advisory만 필요한 경우

## Quick Reference

| 단계 | 행동 |
|------|------|
| 0. 모드 확인 | Default인지 Plan인지 먼저 판단 |
| 1. plan 읽기 | task, file path, verification step 확인 |
| 2. 현재 step 실행 | 순서를 건너뛰지 않고 현재 task만 진행 |
| 3. 구현 discipline 적용 | 코드 step은 `jy-test-driven` 기준으로 진행 |
| 4. 완료 주장 차단 | task 또는 batch 완료 전 `jy-verification-before-completion` 적용 |
| 5. milestone review | 큰 batch나 마지막 handoff 전에 `jy-review-work` 적용 |

## Input Contract

- written plan 또는 checkbox task list
- 관련 repo 규칙과 현재 branch 상태
- task별 verification command

plan이 모호하면 멈춘다:

- decision gap이 크면 `jy-plan-review`
- task breakdown이 부족하면 `jy-writing-plans`

## Execution Rules

- plan 순서를 기본값으로 따른다
- code-change step은 `jy-test-driven` 기준으로 진행한다
- task, batch, handoff 완료 주장은 `jy-verification-before-completion` 기준으로 닫는다
- 큰 milestone이나 최종 handoff 전에는 `jy-review-work`를 사용한다
- 체크박스 진행 상태와 실제 변경 상태가 다르면 plan을 과장하지 않는다

## Progress Tracking

- 현재 task 번호
- 완료한 checkbox step
- 남은 blocker
- 마지막 verification 결과

기억에 의존하지 말고, plan 문서와 실제 변경 상태를 함께 본다.

## Mode-Aware Behavior

### If current collaboration mode is Default

- 이 skill의 정상 실행 모드다.
- written plan을 읽고 현재 task부터 실제로 실행한다.
- plan이 빈약하면 그 사실을 명시하고 `jy-writing-plans` 또는 `jy-plan-review`로 되돌린다.

### If current collaboration mode is Plan

- 실제 구현, 편집, 실행은 시작하지 않는다.
- 이렇게 유도한다:
  - "이건 실행형 plan workflow라 Default mode가 맞습니다. `Shift+Tab`으로 Plan Mode에서 나온 뒤 `/jy-executing-plans`를 다시 실행하세요."
- 대신 compact execution preview는 남긴다.
  - 먼저 실행할 task
  - 필요한 verification command
  - plan gap 여부

## Workflow

1. 현재 collaboration mode가 Default인지 Plan인지 확인한다.
2. plan이 written artifact로 충분한지 본다.
3. 현재 task의 file path, verification step, completion signal을 읽는다.
4. 코드 변경이면 `jy-test-driven` 기준으로 RED부터 시작한다.
5. task가 끝났다고 느껴지면 `jy-verification-before-completion` 기준으로 fresh evidence를 만든다.
6. 큰 batch나 handoff 직전이면 `jy-review-work`를 적용한다.
7. 다음 checkbox step으로 넘어간다.

## Common Mistakes

- plan이 있는데도 순서를 무시하고 임의로 뛰어다니는 것
- `current session` executor인데 자동 swarm처럼 행동하는 것
- `does not auto-spawn subagents`인데도 이 skill이 알아서 병렬 실행을 한다고 가정하는 것
- `jy-test-driven` 없이 code step을 바로 구현하는 것
- `jy-verification-before-completion` 없이 task 완료를 주장하는 것
- plan gap을 무시하고 구현을 시작하는 것
- milestone review 없이 큰 batch를 통째로 닫는 것
