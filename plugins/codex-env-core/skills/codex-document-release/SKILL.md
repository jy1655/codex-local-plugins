---
name: codex-document-release
description: Use when shipped changes in this repo need README, instructions, skill docs, or verification artifacts synced before handoff or release.
---

# Codex Document Release

## Overview

변경된 동작과 문서가 어긋나지 않게 마지막 문서 정리를 수행하는 skill.

원본 `gstack`의 `document-release`에서 가져올 핵심은 "출시 후 문서 동기화"이고, 버리는 것은
hidden runtime, telemetry, self-update, 그리고 존재하지 않는 문서 파일을 억지로 만드는 습관이다.

이 skill의 기본 자세는 targeted patch가 아니라 full consistency audit다.
이번 diff가 어디서 시작됐든, repo에 이미 존재하는 문서 전체가 현재 동작과 같은 말을 하는지 확인한다.

## When to Use

- "문서 업데이트해", "docs sync", "post-ship docs" 요청
- skill, manifest, instruction, install surface를 바꾼 뒤 설명 문서를 맞춰야 할 때
- handoff 전에 README와 verification artifact를 현재 동작과 맞춰야 할 때

사용하지 않을 때:

- 코드가 아직 불안정해서 문서보다 구현이 먼저일 때
- 단순 오탈자 수정만 필요한 경우

## Quick Reference

| 단계 | 해야 할 일 |
|------|-------------|
| 0. 모드 확인 | Default면 실제 갱신, Plan이면 preview만 |
| 1. 변경 표면 확인 | diff와 changed files에서 무엇이 바뀌었는지 파악 |
| 2. 문서 표면 매핑 | 어떤 문서가 영향 받는지 결정 |
| 3. 최소 갱신 | 실제로 바뀐 내용만 맞춤 |
| 4. 검증 | 관련 테스트와 scenario artifact까지 확인 |

## Repo-Local Doc Surface

이 repo에서 우선 검토할 문서 표면:

- `README.md`
- `instructions/AGENTS.md`
- `plugins/codex-env-core/skills/<skill>/SKILL.md`
- `skill-tests/first-party/<skill>/`
- 필요하면 `docs/` 아래의 명시적 plan 또는 design note

Do not invent 새 top-level 문서:

- `CHANGELOG`
- `VERSION`
- `ARCHITECTURE.md`
- `CONTRIBUTING.md`

위 파일이 repo에 없으면 upstream 관성만으로 새로 만들지 않는다.

## Full Consistency Audit

문서 누락은 보통 "이번 변경과 직접 연결된 파일만" 보고 지나갈 때 생긴다.
그래서 이 skill은 시작점은 좁게 잡더라도, 마무리는 항상 repo에 이미 존재하는 문서 전체 audit로 닫는다.

최소 audit 대상:

- `README.md`
- `instructions/AGENTS.md`
- `plugins/codex-env-core/skills/*/SKILL.md`
- `skill-tests/first-party/*/README.md`
- `skill-tests/first-party/*/pressure-scenarios.json`
- `docs/` 아래의 명시적 설계 또는 계획 문서

핵심 질문:

- 같은 경로, 명령, mode rule, storage location이 문서마다 같은 말로 적혀 있는가
- 한 문서에서는 있는 규칙이 다른 문서에서는 빠져 있지 않은가
- 이전에 빠뜨린 문서 drift가 이번 pass에서 회수됐는가

## Change-to-Docs Routing Matrix

### 1. Skill behavior change

필수 검토:

- `plugins/codex-env-core/skills/<skill>/SKILL.md`
- `skill-tests/first-party/<skill>/`
- 필요하면 해당 skill을 참조하는 `instructions/AGENTS.md`

기본 규칙:

- skill wording만 바뀐 것이 아니라 behavior나 trigger가 바뀌면 scenario pack도 같이 본다.
- static verification rule이 바뀌면 관련 test도 같이 본다.

### 2. Install surface or environment rule change

필수 검토:

- `README.md`
- `instructions/AGENTS.md`
- 필요하면 `plugins/codex-env-core/skills/env-sync-admin/SKILL.md`

기본 규칙:

- 경로, 명령, restart 요구사항, storage location이 바뀌면 README와 AGENTS를 둘 다 맞춘다.

### 3. Routing or skill selection rule change

필수 검토:

- `instructions/AGENTS.md`
- 해당 routing을 다루는 skill 문서
- 필요하면 관련 scenario pack

기본 규칙:

- repo-level routing 문구를 바꿨으면 skill 쪽과 전역 instruction 쪽을 따로 놀게 두지 않는다.

### 4. Docs-only cleanup

필수 검토:

- 실제로 수정하는 문서만

기본 규칙:

- docs-only 변경이면 범위를 넓히지 않는다.
- verification asset이나 test를 억지로 건드리지 않는다.

## Output Template

- `Change Surface:` 이번에 바뀐 기능, skill, install surface
- `Docs Updated:` 실제로 맞춘 문서 목록
- `Docs Skipped:` 존재하지 않거나 영향이 없어 건드리지 않은 문서
- `Verification:` 실행한 테스트나 확인 결과

## Mode-Aware Behavior

### If current collaboration mode is Default

- 이 skill의 정상 실행 모드다.
- 실제 문서와 verification artifact를 수정한다.
- 필요하면 관련 테스트까지 바로 돌린다.

### If current collaboration mode is Plan

- 실제 문서 수정은 하지 않는다.
- 이렇게 유도한다:
  - "이건 문서 갱신 실행형 workflow라 Default mode가 맞습니다. `Shift+Tab`으로 Plan Mode에서 나온 뒤 `/codex-document-release`를 다시 실행하세요."
- 대신 preview는 남긴다.
  - 어떤 문서가 바뀔지
  - 어떤 문서는 건드리면 안 되는지
  - 어떤 검증을 돌릴지

## Workflow

1. 변경 표면을 수집한다.
   - `git diff --name-only`
   - 필요하면 관련 파일 본문
2. 영향 받는 문서를 매핑한다.
   - skill 변경이면 해당 `SKILL.md`와 `skill-tests/first-party/<skill>/`
   - install surface 변경이면 `README.md`와 `instructions/AGENTS.md`
   - routing 변경이면 `instructions/AGENTS.md`와 관련 skill 문서를 같이 본다
   - 문서-only 변경이면 범위를 더 넓히지 않는다
3. 그 다음 repo에 이미 존재하는 문서 전체를 full consistency audit 대상으로 다시 훑는다.
4. 실제 동작과 어긋난 설명만 고친다.
5. 사용자-facing next step, command, storage path, routing rule이 바뀌었으면 문서에도 같은 표현으로 반영한다.
6. verification artifact도 같이 본다.
   - scenario pack
   - compliance or bundle test
7. change surface에 따라 mandatory doc pair가 빠지지 않았는지 다시 확인한다.
   - skill behavior change -> skill doc + scenario pack
   - install surface change -> README + AGENTS
   - routing change -> AGENTS + related skill doc
8. 전체 audit에서 같은 개념이 서로 다른 표현으로 drift한 곳이 없는지 마지막으로 확인한다.
9. 테스트를 돌려 문서와 정적 검증이 함께 맞는지 확인한다.

## Scope Rules

- 시작점은 change surface로 잡되, 최종 검토는 existing docs 전체 audit로 닫는다.
- 문서 톤만 손보려고 unrelated file을 넓게 건드리지 않는다.
- skill을 바꿨으면 해당 scenario pack과 정적 test를 같이 본다.
- install surface를 바꿨으면 README와 AGENTS를 둘 다 본다.
- routing을 바꿨으면 AGENTS와 관련 skill 문서를 둘 다 본다.
- repo에 없는 release artifact를 억지로 도입하지 않는다.

## Common Mistakes

- upstream 습관대로 `CHANGELOG`, `VERSION`, `ARCHITECTURE.md`, `CONTRIBUTING.md`를 자동 생성하는 것
- README만 고치고 `instructions/AGENTS.md`나 scenario pack을 놓치는 것
- install surface 변경인데 README 또는 AGENTS 하나만 고치고 끝내는 것
- routing 변경인데 AGENTS와 관련 skill 문서를 같이 안 맞추는 것
- "이번 diff와 직접 관련 없어 보인다"는 이유로 기존 drift 문서를 그대로 남기는 것
- 구현 diff를 안 보고 generic 문구로 문서를 덮어쓰는 것
- 실제 사용자나 maintainer가 보는 경로, 명령, 저장 위치를 문서에 반영하지 않는 것
- docs-only 변경인데 범위를 불필요하게 넓히는 것
- Plan Mode에서 실제 편집을 한 척하는 것
