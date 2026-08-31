# Portable Codex Environment Sync

[![언어: English](https://img.shields.io/badge/Language-English-111827?style=for-the-badge)](./README.md)
[![언어: Korean](https://img.shields.io/badge/Language-Korean-0A66C2?style=for-the-badge)](./README.ko.md)

이 저장소는 이식 가능한 first-party Codex 환경을 정의합니다. 로컬 plugin bundle을
stage하고 personal marketplace와 간결한 전역 instruction을 관리하되, Codex runtime
cache를 직접 수정하지 않습니다.

## Pack model

기본 환경은 의도적으로 작게 유지합니다. `apply`는 다섯 bundle을 모두 `~/plugins`에
stage한 뒤 `INSTALLED_BY_DEFAULT` plugin을 Codex CLI로 명시적으로 설치합니다.
Marketplace policy는 기본 설치 대상을 고르며, policy 자체가 설치 작업을 수행하지는
않습니다.

| Pack | Policy | Skills |
|---|---|---|
| `jy-env-core` — core-lite | `INSTALLED_BY_DEFAULT` | `jy-change-guardrails`, `jy-debugging`, `jy-test-driven`, `jy-verification-before-completion`, `jy-codebase-explore`, `jy-library-research`, `jy-consult` |
| `jy-env-planning` | `AVAILABLE` | `jy-framing`, `jy-grill-me`, `jy-plan-review`, `jy-writing-plans` |
| `jy-env-delivery` | `AVAILABLE` | `jy-executing-plans`, `jy-worktrees`, `jy-checkpoint`, `jy-document-release`, `jy-ship`, `jy-waterfall`, `jy-env-sync-admin`, `jy-writing-skills` |
| `jy-env-audit` | `AVAILABLE` | `jy-explain-change` (명시 호출 전용), `jy-review-all`, `jy-review-work`, `jy-receiving-review`, `jy-slop-remover` |
| `jy-env-ios` | `AVAILABLE` | iOS Simulator debugging, performance, memory, App Intents, SwiftUI workflow |

Stage와 activation은 서로 다른 동작입니다.

- `~/plugins/<pack>`은 local marketplace source입니다.
- `INSTALLED_BY_DEFAULT`이면 `apply`와 bootstrap이
  `codex plugin add jy-env-core@personal-codex`를 실행합니다.
- `AVAILABLE` 선택 pack은 Plugins Directory 또는 CLI에서 설치하기 전까지
  비활성 상태입니다.
- 이 저장소는 더 이상 `~/.agents/skills/<pack>` discovery link를 별도로 만들지
  않으므로 plugin cache와 native discovery의 skill metadata 중복을 피합니다.

필요한 선택 pack만 설치합니다.

```bash
codex plugin add jy-env-planning@personal-codex
codex plugin add jy-env-delivery@personal-codex
codex plugin add jy-env-audit@personal-codex
codex plugin add jy-env-ios@personal-codex
```

설치된 pack을 바꾼 뒤에는 새 Codex thread를 시작합니다.

## 고정된 XcodeBuildMCP

`jy-env-ios`는 이 머신에서 upstream `build-ios-apps` plugin을 대체합니다.
`npx`로 `xcodebuildmcp@2.7.0`을 실행하고 `simulator`, `ui-automation`,
`debugging` workflow만 활성화합니다. 포함된 debugger skill은 현재
session-default, runtime-log, `elementRef` UI contract를 사용합니다.

`build-ios-apps@openai-curated`와 `jy-env-ios@personal-codex`를 동시에 활성화하지
마십시오. 둘 다 `xcodebuildmcp` server name을 등록합니다.

## Lazy Context7 research

Context7은 MCP server나 별도 `jy-context7` skill로 설치하지 않습니다. core-lite의
`jy-library-research`가 Context7을 선택형 read-only provider로 다룹니다.

1. 이미 `ctx7` command가 있으면 그것을 사용합니다.
2. 없다면 Node.js 18+와 `npx`가 있을 때 해당 조사 요청에서만 고정된
   `ctx7@0.5.5` package를 실행합니다.
3. CLI, network, sandbox, rate limit, index 문제 중 하나라도 발생하면 official docs,
   source, changelog, issue tracker로 즉시 fallback합니다.

대부분의 공개 문서 query는 인증 없이 동작합니다. 더 높은 rate limit이 필요하면 key를
repo 밖의 `CONTEXT7_API_KEY` 환경변수에 둡니다. Skill은 key를 command argument로
전달하지 않으며 private source나 credential을 Context7에 보내지 않습니다.

## Install surface

- plugin source: `~/plugins`
- personal marketplace: `~/.agents/plugins/marketplace.json`
- global instruction: `~/.codex/AGENTS.md`
- managed state: `~/.codex-env-sync/state.json`
- `codex plugin`으로만 변경하는 Codex 소유 cache: `~/.codex/plugins/cache`

로컬 `apply`는 macOS와 Linux에서 plugin source와 instruction을 symlink하고,
Windows에서는 copy mode를 사용합니다. Bootstrap과 `--snapshot`은 항상 안정적인
copy snapshot을 설치합니다. Stage 후에는 `codex plugin add`로 기본 plugin을
설치하거나 갱신하며, 선택 pack은 명시적으로 설치해야 합니다. Dirty checkout은
별도의 live skill discovery surface로 노출하지 않습니다.

## First run

macOS / Linux:

```bash
./scripts/bootstrap.sh <git-url>
```

Windows PowerShell:

```powershell
.\scripts\bootstrap.ps1 -GitUrl <git-url>
```

두 명령 모두 `codex` CLI가 필요하며, repo를 한 번 clone하고 안정적인 snapshot과
core-lite를 설치합니다.

## Local development

해석된 source, install mode, marketplace policy를 점검합니다.

```bash
python3 -m codex_env_sync.cli inspect --repo-root .
```

현재 checkout을 적용합니다.

```bash
python3 -m codex_env_sync.cli apply --repo-root .
```

분리된 snapshot을 설치합니다.

```bash
python3 -m codex_env_sync.cli apply --repo-root . --snapshot
```

이미 설치된 plugin을 바꾼 뒤에는 `plugin-creator`의 cachebuster/reinstall 흐름을
사용하고 새 thread를 시작합니다. `~/.codex/plugins/cache`를 직접 수정하지 않습니다.

## Layout

```text
codex-env.toml                    # 다섯 plugin source와 installation policy
codex_env_sync/                   # inspect/apply/bootstrap engine
plugins/jy-env-core/              # 기본 core-lite bundle
plugins/jy-env-planning/          # 선택 planning pack
plugins/jy-env-delivery/          # 선택 delivery pack
plugins/jy-env-audit/             # 선택 audit pack
plugins/jy-env-ios/               # 선택 pinned iOS/XcodeBuildMCP pack
instructions/AGENTS.md            # 선택 skill을 eager routing하지 않는 전역 규칙
.agents/plugins/marketplace.json  # local personal marketplace catalog
skill-tests/first-party/          # skill 실용성 pressure scenario
skill-tests/UTILITY-EVAL.md       # 3-arm skill 실용성·보고 계약
tests/                            # unit·integration test
```

First-party skill source는 `plugins/jy-env-*/skills/`에만 둡니다. Upstream 또는
company-shared skill은 seed material이며, 이 repo는 customization이 끝난 first-party
결과만 저장하고 third-party runtime을 vendor하지 않습니다.

커밋하면 안 되는 repo-local 작업 상태는 `.codex/` 아래에 둘 수 있습니다. Delivery
pack을 설치한 경우 `jy-checkpoint`는 `.codex/checkpoints/`를 사용합니다.

## Tests

전체 suite:

```bash
python3 -m unittest discover -s tests -v
```

Pressure-scenario asset 검증:

```bash
python3 -m unittest tests.test_skill_scenarios -v
```

## Skill 실용성 gate

지침이 그럴듯하다는 이유만으로 skill을 유지하지 않습니다. 실용성 evaluator는 같은
task를 같은 model·effort에서 `baseline`(skill 없음), `implicit`(발견 가능),
`explicit`(강제 호출)로 비교하되 같은 plugin의 나머지 skill은 고정합니다. 이후
응답을 blind scoring하고 품질, token,
latency, implicit 활성 gate를 적용하며 tool call과 실제 skill read 여부를 기록합니다.

먼저 model call 범위를 확인합니다.

```bash
python3 -m codex_env_sync.skill_eval plan \
  --repo-root . --skill jy-change-guardrails
```

한 skill을 실행하고 freshness 또는 최신 보고서를 확인합니다.

```bash
python3 -m codex_env_sync.skill_eval run \
  --repo-root . --skill jy-change-guardrails

python3 -m codex_env_sync.skill_eval status --repo-root .
python3 -m codex_env_sync.skill_eval report --repo-root .
```

새 source 채택 전에는 `run --candidate --skill <name>`, skill 변경에는
`run --changed-from <ref>`, 무효화된 증거에는 `run --stale`, 새 model baseline에는
`run --all --model <new-model>`을 사용합니다. 보고서와 raw JSONL은
`.codex/skill-evals/` 아래에 ignore되며 어떤 verdict도 skill을 자동 설치·삭제하지
않습니다. Threshold와 증거 경계는
[skill-tests/UTILITY-EVAL.md](skill-tests/UTILITY-EVAL.md)를 따릅니다.
