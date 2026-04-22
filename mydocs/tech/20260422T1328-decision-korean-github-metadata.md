# 운영 결정: GitHub 메타데이터 언어

- Timestamp: 20260422T1328 KST
- Scope: 이 개인 Codex plugin 환경 repo의 GitHub issue, PR, waterfall 공개 기록
- Decision: 프로젝트-facing 운영 메타데이터는 한국어로 작성한다.

## 배경

이 repo는 개인 플러그인과 Codex 환경을 유지하기 위한 작업 공간이다. 따라서 GitHub issue와 PR은 외부 오픈소스 프로젝트의 범용 협업 문서라기보다, 나중에 내가 다시 읽고 이어서 작업하기 위한 운영 기록에 가깝다.

## 규칙

- GitHub issue 제목과 본문은 한국어로 작성한다.
- GitHub PR 제목과 본문은 한국어로 작성한다.
- `mydocs/` 아래의 공개 waterfall 기록과 운영 결정 문서는 한국어로 작성해도 된다.
- `SKILL.md`, `agents/openai.yaml`, 테스트 파일, 코드 식별자, 명령어, 경로는 기존 규칙대로 English-first 또는 literal token을 유지한다.
- 외부 공유를 전제로 하는 문서가 필요해지면 별도의 영어 요약을 추가한다.

## 적용 사례

- Issue `#7`: `jy-waterfall 스킬 개선 및 이식성 기록`
- PR `#8`: `jy-waterfall 프로젝트 기록 스킬 추가`

## 이유

작업의 주 사용자와 유지보수자가 한국어를 사용하는 개인이므로, 운영 메타데이터는 한국어가 더 빠르게 읽히고 다음 행동을 판단하기 쉽다. 반면 skill source와 테스트는 Codex skill ecosystem의 관례와 기존 repo 규칙을 따라 English-first로 유지하는 편이 이식성과 일관성에 유리하다.
