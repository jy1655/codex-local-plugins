---
name: jy-ship
description: Use when the user wants to "ship", "deploy", "push to main", or create/update a PR/MR for the current branch and the work needs a verified base-branch, push, and docs-sync workflow.
---

# JY Ship

## Overview

현재 브랜치를 안전하게 밀고 PR/MR까지 닫는 repo-native ship workflow다. 핵심은
`base branch safety -> review -> fresh verification -> push -> PR/MR -> docs sync` 순서를
건너뛰지 않는 것이다.

이 skill은 gstack의 hidden runtime, telemetry, self-update, local sidecar state를 들이지 않는다.
이 repo에 실제로 있는 git surface와 first-party skills만 사용한다.

## When to Use

- "ship it", "push this branch", "PR 만들어", "merge 준비해" 요청
- 구현이 끝났고 원격 브랜치와 PR/MR 생성까지 이어서 닫아야 할 때
- handoff 전에 review, verification, docs sync까지 한 번에 마무리해야 할 때

사용하지 않을 때:

- 구현이나 디버깅이 아직 끝나지 않았을 때
- 계획만 남기고 실제 git 작업은 하지 않을 때
- 단순 문서 동기화만 필요할 때 (`jy-document-release` 사용)

## Quick Reference

| 단계 | 행동 | 중단 조건 |
|------|------|-----------|
| 0. 모드 확인 | Default면 실행, Plan이면 preview만 | Plan Mode면 `Shift+Tab` 안내 |
| 1. base branch 탐지 | remote와 CLI 메타데이터로 target branch 확인 | 현재 branch가 base branch면 중단 |
| 2. ship surface 수집 | `git status`, diff, commit log 확인 | 변경 범위를 설명할 수 없으면 중단 |
| 3. review + verify | `jy-review-work`, `jy-verification-before-completion` 기준으로 fresh gate 수행 | review FAIL, verification FAIL이면 중단 |
| 4. commit + push | 필요한 변경을 커밋하고 일반 `git push` | `Never force push` |
| 5. PR/MR | `gh`/`glab`가 있으면 create or update, 없으면 수동 next step | URL 없으면 생성 완료 주장 금지 |
| 6. docs sync | 필요 시 `jy-document-release` 흐름으로 문서 동기화 | docs drift 남기지 않기 |

## Base Branch Gate

- 먼저 현재 branch와 base branch를 찾는다.
- base branch 탐지는 다음 순서로 시도한다:
  - GitHub면 `gh pr view` 또는 `gh repo view`
  - GitLab이면 `glab mr view` 또는 project default branch 조회
  - 공통 fallback은 `origin/HEAD`
- 현재 branch가 base branch면 ship workflow를 중단한다.
- "main에서 바로 ship" 요청을 받아도 feature branch 없이 진행하지 않는다.

## Review And Verification Gate

- multi-file 구현이면 `jy-review-work` 기준으로 review gate를 먼저 닫는다.
- 완료 주장, 테스트 통과, ship readiness 평가는 `jy-verification-before-completion` 기준으로
  fresh verification evidence가 있어야 한다.
- earlier test memory, old CI run, agent success report만으로 push 또는 PR/MR 생성에 들어가지 않는다.
- review 또는 verification이 FAIL이면 ship을 멈추고 그 결과를 그대로 보고한다.

## Release File Rules

- `VERSION`, `CHANGELOG`, `TODOS.md` 같은 release bookkeeping 파일은 repo에 이미 있을 때만 다룬다.
- repo에 없는 `VERSION` 또는 `CHANGELOG`를 invent하지 않는다.
- 이 repo처럼 해당 파일이 없으면 shipping summary, verification 결과, PR/MR body로 충분하다.

## Push And PR/MR Rules

- worktree가 dirty면 현재 ship surface에 포함할 변경만 stage하고 커밋한다.
- commit message는 diff와 목표에서 안전하게 추론 가능한 범위로만 작성한다.
- 제목을 책임 있게 정할 수 없으면 임의 문구를 만들지 말고 사용자에게 commit summary를 한 번 요청한다.
- push는 일반 `git push` 또는 `git push -u origin <branch>`만 사용한다.
- `Never force push`.
- `gh` 또는 `glab`가 있으면 existing PR/MR을 update하거나 새로 만든다.
- CLI가 없으면 branch name, remote, compare URL 또는 수동 PR 생성 next step을 남긴다.
- URL이 없으면 "PR created" 같은 완료 주장을 하지 않는다.

## Documentation Sync

- shipped changes가 README, instructions, skill docs, verification assets와 연결되면
  `jy-document-release`를 follow-up으로 실행한다.
- docs sync가 새 commit을 만들었다면 같은 branch로 다시 push하고 PR/MR body도 최신 상태로 맞춘다.
- docs 변경이 필요 없으면 그 사실을 명시하고 끝낸다.

## Mode-Aware Behavior

### If current collaboration mode is Default

- 이 skill의 정상 실행 모드다.
- base branch 탐지, fresh verification, commit, push, PR/MR 생성, docs sync를 실제로 수행한다.

### If current collaboration mode is Plan

- 실제 git write, push, PR/MR 생성은 하지 않는다.
- 이렇게 유도한다:
  - "이건 실행형 ship workflow라 Default mode가 맞습니다. `Shift+Tab`으로 Plan Mode에서 나온 뒤 `/jy-ship`을 다시 실행하세요."
- 대신 compact ship checklist preview만 남긴다.
  - base branch 확인 방법
  - 필요한 review/verification 명령
  - PR/MR 생성 전까지의 중단 조건
- Plan Mode 안에서 이미 push나 PR/MR 생성을 한 것처럼 가장하지 않는다.

## Output Template

- `Base Branch:` 탐지된 target branch
- `Review Gate:` PASS/FAIL와 근거
- `Verification Gate:` 실행한 명령과 결과
- `Push:` pushed / already up to date / blocked
- `PR/MR:` created / updated / manual action required
- `Docs:` synced / no changes needed / blocked

## Common Mistakes

- base branch 확인 없이 바로 `git push`부터 하는 것
- review나 fresh verification 없이 "ship ready"라고 말하는 것
- 이 repo에 없는 `VERSION`이나 `CHANGELOG`를 자동으로 만드는 것
- force push로 문제를 덮는 것
- PR/MR URL이 없는데도 생성 완료처럼 보고하는 것
- `jy-document-release`가 필요한 변경인데 docs sync를 생략하는 것
- Plan Mode에서 실제 ship을 수행한 것처럼 말하는 것
