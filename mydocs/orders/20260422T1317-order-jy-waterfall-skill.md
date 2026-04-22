# Waterfall 작업 지시

- Timestamp: 20260422T1317 KST
- Task: 이 repo에서 first-party `jy-waterfall` 스킬 작업을 위한 durable waterfall record를 수립한다.
- Record root: `mydocs/`
- Sensitivity decision: 이 개인 repo에는 공개해도 안전한 기록으로 둔다. secret, credential, private customer data, raw internal URL은 committed record에 넣지 않는다.
- GitHub linkage: Issue `#7`과 branch `feature/7-jy-waterfall-portability`가 연결되어 있다. milestone은 사용하지 않는다.
- Expected duration: 여러 세션 또는 review-heavy first-party skill 작업.
- Next skill: 구현 계획이 부족하면 `jy-writing-plans`, 완료를 주장하기 전에는 `jy-verification-before-completion`.

## 목표

`jy-waterfall` 스킬 rollout을 repo-visible project record로 남긴다. 채팅이 끝난 뒤에도 order, plan, execution note, feedback, verification, troubleshooting 흐름을 다시 읽고 이어갈 수 있어야 한다.

## 범위

- `mydocs/`를 committed waterfall record root로 사용한다.
- 현재 first-party skill 작업 대상은 `plugins/jy-env-core/skills/jy-waterfall/`이다.
- GitHub issue, milestone, branch 변경은 approval gate를 유지한다.
- 관련 없는 기존 working tree 변경을 되돌리지 않는다.

## 필요한 결정

- 이 작업에 `mydocs/plans/` 아래의 상세 implementation plan record가 필요한지 판단한다.
- 향후 아이디어, 사용 메모, 이식성 개선은 GitHub issue `#7`에 기록한다.
- 작업을 닫기 전에 어떤 verification gate를 실행할지 정한다.

## 인계

branch `feature/7-jy-waterfall-portability`에서 이어간다. 다음 단계가 상세 execution plan이면 `jy-writing-plans`를 사용하고, 구현 검증 단계에서는 `jy-verification-before-completion`을 사용한다.

연결된 issue: https://github.com/jy1655/codex-local-plugins/issues/7
