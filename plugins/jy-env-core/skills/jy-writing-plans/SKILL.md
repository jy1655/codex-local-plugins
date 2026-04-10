---
name: jy-writing-plans
description: Use when approved requirements or a reviewed plan need to become a detailed implementation plan another engineer can execute directly.
---

# JY Writing Plans

## Overview

승인된 brief, reviewed plan, 또는 안정된 요구사항을 implementer가 그대로 집어 실행할 수 있는
`decision-complete` implementation plan으로 바꾸는 skill.

이 wave의 문서 정책은 단순하다. repo-visible 산출물은 spec이 아니라 plan만 남긴다.
즉 `docs/superpowers/plans/` 아래의 구현 계획 문서만 작성하고, 별도 spec 문서는 강제하지 않는다.

## When to Use

- "구현 계획 써줘", "task list로 풀어줘", "implementer가 바로 집을 수 있게 해줘"
- approved brief는 있는데 task-level breakdown이 아직 없을 때
- reviewed plan을 file path, verification command, acceptance criteria 수준까지 잠가야 할 때

사용하지 않을 때:

- 아직 문제 정의가 흔들리는 경우 (`jy-framing`)
- 계획의 결정 공백이 큰 경우 (`jy-plan-review`)
- written plan이 이미 있고 실제 실행만 남은 경우 (`jy-executing-plans`)

## Quick Reference

| 단계 | 행동 |
|------|------|
| 0. 모드 확인 | Default인지 Plan인지 먼저 판단 |
| 1. 입력 잠금 | brief, reviewed plan, repo 규칙, 제약 수집 |
| 2. 구조 결정 | 변경 파일, 책임 경계, 검증 흐름 고정 |
| 3. task 분해 | implementer가 그대로 따를 수 있는 step으로 분해 |
| 4. plan 문서화 | `docs/superpowers/plans/` 아래에 저장 |
| 5. handoff | `jy-worktrees` 또는 `jy-executing-plans`로 연결 |

## Plan Document Contract

- 저장 위치: `docs/superpowers/plans/YYYY-MM-DD-<topic>.md`
- 산출물은 implementer가 추가 결정을 하지 않아도 되는 `decision-complete` plan이어야 한다
- 각 task에는 정확한 file path, 실행 명령, 기대 결과, `acceptance criteria`가 있어야 한다
- checkbox step 기준으로 추적 가능해야 한다
- 이 wave에서는 repo-visible spec 문서를 새로 만들지 않는다

## Required Content

최소 포함 항목:

- Goal
- Architecture summary
- Files to create or modify
- Ordered tasks with checkbox steps
- Verification commands and expected result
- `acceptance criteria`
- Next handoff (`jy-worktrees` 또는 `jy-executing-plans`)

좋은 plan의 기준:

- 변경 파일과 책임 경계가 먼저 잠긴다
- task는 실행 순서가 명확하다
- 검증 명령이 추상적이지 않다
- 구현자에게 남는 해석 여지가 적다

## No Placeholders

다음 표현은 plan 실패다:

- `TBD`
- `TODO`
- "implement later"
- "write tests"
- "add appropriate error handling"
- "handle edge cases"
- "similar to previous task"

이런 문구가 보이면 plan을 닫지 않는다. 실제 file path, step, command, expected output으로 바꾼다.

## Mode-Aware Behavior

### If current collaboration mode is Default

- 입력이 이미 안정적이고 한 번 답변으로 끝낼 수 있을 때만 실제 plan 문서를 작성한다.
- 입력이 아직 흔들리면 이렇게 유도한다:
  - "이건 Plan Mode로 잠그는 게 맞습니다. `Shift+Tab`으로 Plan Mode로 바꾼 뒤 `/jy-writing-plans`를 다시 실행하세요."
- 그래도 빈손으로 끝내지 않는다.
  - compact file map
  - task skeleton
  - 필요한 open question

### If current collaboration mode is Plan

- missing decision을 질문으로 잠근다.
- 결과를 `<proposed_plan>` 블록 수준의 implementation plan으로 정리한다.
- Plan Mode에서는 실제 파일이 이미 저장된 것처럼 가장하지 않는다.

## Workflow

1. 현재 collaboration mode가 Default인지 Plan인지 확인한다.
2. 입력이 충분히 잠겼는지 판단한다.
3. 관련 repo 구조와 기존 패턴을 읽는다.
4. 변경 파일과 책임 경계를 먼저 고정한다.
5. task를 checkbox step으로 분해한다.
6. verification command와 expected result를 각 task에 붙인다.
7. `acceptance criteria`를 plan 끝에 명시한다.
8. 다음 단계로 `jy-worktrees` 또는 `jy-executing-plans`를 남긴다.

## Common Mistakes

- brief가 아직 흔들리는데 task plan부터 쓰는 것
- `decision-complete`하지 않은 outline을 구현 계획이라고 부르는 것
- `docs/superpowers/plans/` 대신 임의 경로에 저장하는 것
- `acceptance criteria` 없이 task checklist만 적고 끝내는 것
- `TBD` 같은 placeholder를 남기는 것
- verification command 없이 "테스트 추가"처럼 뭉뚱그리는 것
- spec 문서까지 자동으로 만들려는 것
