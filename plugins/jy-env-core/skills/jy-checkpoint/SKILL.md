---
name: jy-checkpoint
description: Use when the user wants to save, list, or resume repo-local working-state checkpoints across sessions, context switches, or branch handoffs.
---

# JY Checkpoint

## Overview

현재 작업 상태를 repo-local checkpoint 문서로 남기고, 나중 세션이나 다른 branch에서 다시
이어붙이기 위한 skill.

핵심 원칙은 두 가지다.

- checkpoint는 hidden home-directory state가 아니라 repo 안의 `.codex/checkpoints/`에 둔다.
- checkpoint는 append-only Markdown 문서로 남기고, 기존 파일을 조용히 덮어쓰지 않는다.

## When to Use

- "이 상태 저장해둬", "나중에 이어서 하자", "checkpoint 남겨줘"
- "내가 뭘 하고 있었지?", "마지막 상태 복구해줘", "resume"
- branch를 바꾸거나 세션을 끝내기 전에 현재 결정과 남은 일을 남기고 싶을 때
- 다른 사람이 바로 이어받을 수 있는 compact handoff가 필요할 때

사용하지 않을 때:

- 단순 진행 요약만 대화에 한 번 남기면 충분한 경우
- 장기 보관용 공식 문서를 커밋해야 하는 경우

## Quick Reference

| 동작 | 해야 할 일 | 기본값 |
|------|-------------|--------|
| Save | 현재 branch, 변경 파일, 결정, 남은 일을 새 checkpoint로 저장 | 새 Markdown 파일 생성 |
| List | 현재 branch 기준 recent checkpoint를 보여줌 | 최신순 |
| Resume | 특정 checkpoint 또는 최신 checkpoint를 읽고 재개 요약 제공 | 최신 checkpoint |

## Storage Contract

- 저장 위치: `.codex/checkpoints/`
- 커밋 정책: gitignored, repo-local only
- 파일 형식: Markdown + YAML frontmatter
- 쓰기 정책: append-only
- 파일명 규칙: `YYYYMMDD-HHMMSS-title-slug.md`

필수 frontmatter:

```yaml
status: in_progress
branch: feature/foo
timestamp: 2026-04-10T16:00:00+09:00
files_modified:
  - plugins/jy-env-core/skills/jy-checkpoint/SKILL.md
```

본문 기본 섹션:

- `Summary`
- `Decisions Made`
- `Remaining Work`
- `Notes`

## Output Template

### Save

- `Checkpoint:` 생성한 파일 경로
- `Status:` 현재 상태
- `Branch:` 기록한 branch
- `Next:` resume 시 가장 먼저 할 일 한 줄

### List

- 현재 branch 기준 recent checkpoint 목록
- 각 항목의 날짜, 제목, 상태
- 필요하면 branch mismatch 항목은 별도로 구분

### Resume

- `Checkpoint:` 선택된 파일
- `What You Were Doing:` 한 단락
- `Remaining Work:` 바로 이어서 할 일
- `Warnings:` branch mismatch나 오래된 상태가 있으면 명시

## Mode-Aware Behavior

### If current collaboration mode is Default

- `Save`, `List`, `Resume` 모두 정상 동작 모드다.
- `Save`는 `.codex/checkpoints/` 아래 새 파일을 만든다.
- `List`와 `Resume`는 repo-local checkpoint를 읽고 compact summary를 제공한다.

### If current collaboration mode is Plan

- `List`와 `Resume`는 읽기 전용이므로 계속 진행할 수 있다.
- `Save`는 실제 파일 쓰기를 가장하지 않는다.
- 이렇게 유도한다:
  - "현재는 Plan Mode라 checkpoint 파일을 실제로 쓰지 않습니다. `Shift+Tab`으로 Default mode로 나온 뒤 `/jy-checkpoint save`를 다시 실행하세요."
- 대신 바로 쓸 수 있는 checkpoint 초안은 대화 안에 compact하게 남긴다.

## Workflow

1. 사용자의 의도가 `Save`, `List`, `Resume` 중 무엇인지 먼저 판정한다.
2. repo 문맥을 수집한다.
   - `git branch --show-current`
   - `git status --short`
   - 필요하면 최근 checkpoint 목록
3. `Save`면 title, status, modified files를 현재 문맥에서 추론한다.
4. `.codex/checkpoints/`에 새 append-only Markdown 파일을 만든다.
5. `List`면 현재 branch 항목을 최신순으로 먼저 보여준다.
6. `Resume`면 사용자가 지정한 항목을 찾고, 없으면 최신 checkpoint를 기본값으로 쓴다.
7. 선택된 checkpoint의 branch가 현재 branch와 다르면 경고만 하고 막지는 않는다.
8. 결과는 항상 "무엇을 하고 있었는지 / 남은 일 / 주의사항" 중심으로 compact하게 정리한다.

## Resume Matching Rules

- 명시적 지정이 있으면 그 항목을 우선한다.
  - 파일명 일부
  - 제목 일부
  - 날짜
- 명시적 지정이 없으면 현재 branch의 최신 checkpoint를 먼저 찾는다.
- 현재 branch에 checkpoint가 없으면 전체 최신 checkpoint를 사용하고 branch mismatch 경고를 붙인다.

## Boundaries

- `~/.codex/...` 또는 다른 hidden home-directory state에 의존하지 않는다.
- telemetry, update check, session analytics를 두지 않는다.
- 기존 checkpoint를 조용히 수정하거나 덮어쓰지 않는다.
- branch mismatch를 이유로 resume을 막지 않는다.
- built-in session persistence가 있다고 가정해 checkpoint 작성을 생략하지 않는다.

## Common Mistakes

- checkpoint를 대화 한 줄 요약으로만 끝내고 durable file을 남기지 않는 것
- `.codex/checkpoints/` 대신 hidden home-directory state를 도입하는 것
- 기존 checkpoint를 덮어써서 시간축을 깨는 것
- `Resume`에서 명시적 지정이 없을 때 branch를 무시하고 아무 파일이나 고르는 것
- branch mismatch를 발견하고도 경고를 안 남기는 것
- Plan Mode에서 실제 파일을 쓴 척하는 것
- 공식 문서가 필요한데도 checkpoint를 커밋 문서 대용으로 쓰는 것
