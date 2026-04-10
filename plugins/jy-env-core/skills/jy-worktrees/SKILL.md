---
name: jy-worktrees
description: Use when starting isolated feature work on a new branch or worktree before implementation begins.
---

# JY Worktrees

## Overview

기능 작업을 현재 workspace와 분리된 worktree에서 시작하게 만드는 skill.
핵심은 worktree를 만드는 것 자체보다, 어느 디렉터리를 쓰는지와 그 디렉터리가 안전한지 먼저 검증하는 것이다.

## When to Use

- "새 브랜치로 분리해서 시작해", "worktree 만들어", "격리된 작업 공간이 필요해"
- 구현을 시작하기 전에 branch isolation이 필요한 경우
- 현재 workspace를 건드리지 않고 병렬 작업을 시작해야 할 때

사용하지 않을 때:

- 이미 올바른 feature branch/worktree 안에 있는 경우
- 단순 읽기 작업만 필요한 경우

## Quick Reference

| 단계 | 행동 |
|------|------|
| 0. 모드 확인 | Default인지 Plan인지 먼저 판단 |
| 1. 위치 결정 | 기존 `.worktrees/` 우선, 없으면 `worktrees/`, 둘 다 없으면 `.worktrees/` |
| 2. 안전성 확인 | 선택된 디렉터리가 `gitignored`인지 확인 |
| 3. worktree 생성 | 새 branch와 path로 worktree 생성 |
| 4. baseline 확인 | 가벼운 setup/test 명령이 있으면 확인 |
| 5. 결과 보고 | full path와 baseline 결과 보고 |

## Directory Policy

- 이미 `.worktrees/`가 있으면 그 디렉터리를 사용한다
- `.worktrees/`가 없고 `worktrees/`가 있으면 그 디렉터리를 사용한다
- 둘 다 없으면 `.worktrees/`를 표준값으로 생성한다

선택된 디렉터리는 반드시 `gitignored` 상태여야 한다.

검증 예:

```bash
git check-ignore -q .worktrees
git check-ignore -q worktrees
```

선택된 디렉터리가 `gitignored`가 아니면, ignore entry를 먼저 고치고 나서 worktree를 만든다.

## Baseline Validation

- `package.json`이 있으면 테스트/검증 스크립트를 탐지한다
- `pyproject.toml` 또는 `requirements.txt`가 있으면 Python 기준 baseline 명령을 찾는다
- `Cargo.toml`, `go.mod`, `Makefile`도 같은 방식으로 본다
- obvious command가 없으면 있다고 추측하지 않는다

반드시 명시할 것:

- baseline command를 찾았는지
- 실제로 실행했는지
- 찾지 못했다면 그 사실

## Mode-Aware Behavior

### If current collaboration mode is Default

- 이 skill의 정상 실행 모드다.
- 디렉터리 정책, ignore 검증, worktree 생성, baseline 확인을 실제로 수행한다.

### If current collaboration mode is Plan

- 실제 worktree 생성은 하지 않는다.
- 이렇게 유도한다:
  - "이건 실행형 workspace workflow라 Default mode가 맞습니다. `Shift+Tab`으로 Plan Mode에서 나온 뒤 `/jy-worktrees`를 다시 실행하세요."
- 대신 compact preview는 남긴다.
  - 사용할 디렉터리
  - 필요한 `git check-ignore` 확인
  - baseline command 후보

## Workflow

1. 현재 collaboration mode가 Default인지 Plan인지 확인한다.
2. `.worktrees/`와 `worktrees/` 존재 여부를 본다.
3. 선택된 디렉터리가 `gitignored`인지 `git check-ignore`로 검증한다.
4. 필요하면 ignore entry를 먼저 고친다.
5. 새 branch 이름과 worktree path를 정한다.
6. worktree를 만든다.
7. obvious baseline command가 있으면 실행하고, 없으면 없다고 보고한다.

## Common Mistakes

- 아무 디렉터리나 잡고 worktree를 만드는 것
- `.worktrees/`와 `worktrees/` 우선순위를 무시하는 것
- 선택된 디렉터리가 `gitignored`인지 확인하지 않는 것
- `git check-ignore` 없이 안전하다고 가정하는 것
- baseline command가 없는데 테스트가 다 통과했다고 추측하는 것
- Plan Mode에서 실제 worktree를 만든 척하는 것
