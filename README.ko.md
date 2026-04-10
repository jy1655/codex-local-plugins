# Portable Codex Environment Sync

[![언어: English](https://img.shields.io/badge/Language-English-111827?style=for-the-badge)](./README.md)
[![언어: Korean](https://img.shields.io/badge/Language-Korean-0A66C2?style=for-the-badge)](./README.ko.md)

이 저장소는 이식 가능한 Codex 작업 환경을 정의합니다.

전체 머신을 복제하려는 목적은 아닙니다. 대신 Codex가 어디서 실행되더라도
같은 방식으로 동작하도록 만드는 표면만 동기화합니다.

- first-party 로컬 plugin bundle
- plugin marketplace entry
- 생성된 전역 instruction artifact
- 설치된 plugin bundle 안에서 직접 작성되는 first-party Codex skill

설치 표면은 의도적으로 작게 유지합니다.

- plugin은 `~/plugins`에 설치됩니다
- skill discovery link는 `~/.agents/skills/`에 설치됩니다
- marketplace는 `~/.agents/plugins/marketplace.json`에 기록됩니다
- instruction은 `~/.codex/...`에 설치됩니다
- `~/.codex/plugins/cache` 아래의 Codex runtime cache는 건드리지 않습니다

현재 manifest는 macOS와 Linux에서 symlink를 사용합니다. 그래서 같은 checkout에서
나중에 `git pull`을 하면 plugin bundle과 전역 instruction이 다시 복사되지 않아도
즉시 반영됩니다. Windows는 platform override를 통해 copy mode를 유지합니다.

커밋하면 안 되는 repo-local 작업 상태는 `.codex/` 아래에 둘 수 있습니다.
첫 번째 경로는 `.codex/checkpoints/`이며, 세션 handoff note를 저장하는
first-party `jy-checkpoint` skill이 사용합니다.

로컬 skill 개발을 지원하는 authoring reference는 `references/` 아래에 둘 수 있습니다.
이 파일들은 유지보수용으로 repo에 포함되지만, 설치되는 Codex 표면의 일부는 아닙니다.

first-party skill authoring은 `plugins/jy-env-core/skills/`에서 이뤄집니다. 이 디렉터리는
로컬 개발과 설치된 Codex skill 표면 모두의 source of truth입니다.
현재 first-party workflow pack은 planning, debugging, test-first implementation,
review, shipping, verification discipline을 다룹니다.

## First-Party Skill Catalog

실제 호출명은 `jy-*`처럼 짧게 유지하고, role 구분은 이 README에서 설명합니다.
즉 일상적인 invocation은 간결하게 두고, intended use는 문서에서 명확히 확인할 수 있게 했습니다.

### Planning

- `jy-autoplan`은 현재 요청에 맞는 planning 경로를 고르고, 사용자가 먼저 선택하지 않아도 `jy-framing` 또는 `jy-plan-review`로 라우팅합니다.
- `jy-framing`는 모호한 feature 또는 product idea를 더 선명한 problem brief, 제약 조건 목록, 다음 planning step으로 정리합니다.
- `jy-plan-review`는 이미 있는 plan 또는 outline을 받아 구현 전에 decision gap을 닫습니다.

### Execution

- `jy-debugging`은 버그를 patch하기 전에 reproduction, hypothesis test, root-cause verification을 강제합니다.
- `jy-test-driven`는 failing test first를 강제하고 구현을 red-green-refactor loop 안에 묶습니다.
- `jy-verification-before-completion`은 fresh verification command와 결과가 없으면 success claim을 막습니다.
- `jy-review-work`는 handoff 또는 merge 전에 완료된 구현을 multi-angle review 방식으로 검토합니다.
- `jy-loop`는 명시된 completion criteria가 실제로 verified될 때까지 반복 작업을 유지합니다.
- `jy-slop-remover`는 불필요하게 범위를 넓히지 않고 obvious AI-generated code smell만 정리합니다.

### Routing

- `jy-intent-gate`는 애매한 요청을 planning, execution, research 중 어떤 경로로 보낼지 분류합니다.

### Research

- `jy-codebase-explore`는 구조가 낯설거나 여러 모듈에 흩어진 repository를 multi-angle 방식으로 탐색합니다.
- `jy-library-research`는 외부 library, package, API, usage pattern에 대해 evidence-backed answer를 수집합니다.
- `jy-consult`는 architecture, reliability, performance, repeated-failure decision에 대해 advisory mode로 깊게 판단합니다.

### Maintenance

- `jy-checkpoint`는 pause, resume, branch handoff workflow를 위해 repo-local checkpoint note를 `.codex/checkpoints/` 아래에 저장합니다.
- `jy-document-release`는 shipped change 이후 README, AGENTS instruction, skill doc, verification pack을 동기화합니다.
- `jy-ship`은 base branch check, fresh verification, push, PR/MR 생성, docs sync까지 현재 branch의 마지막 ship workflow를 닫습니다.
- `jy-env-sync-admin`은 이 환경 repo를 검증하고 repo-owned install surface를 home Codex 환경에 다시 적용합니다.

### Authoring

- `jy-writing-skills`는 skill 변경을 위한 first-party authoring guide이며, TDD-style scenario validation과 deployment check를 포함합니다.

## Secret handling

MCP server definition은 커밋된 plugin bundle 안에 둘 수 있습니다.

하지만 secret value는 그렇지 않습니다.

MCP server에 API key나 account token이 필요하면, 로컬 머신 설정이나
다른 local-only secret layer에 보관해야 합니다. 이 repo에는 portable server
definition만 커밋해야 합니다.

plugin-managed MCP secret은 local-only overlay file로 다룹니다.

- `~/.codex-env-sync/local/plugins/jy-env-core.mcp.json`

이전 plugin id에서 migration 중이라면, `apply`는 새 파일이 아직 없을 때만
`~/.codex-env-sync/local/plugins/codex-env-core.mcp.json`도 읽습니다.

예시:

```json
{
  "mcpServers": {
    "korean-law": {
      "env": {
        "LAW_OC": "your-token-here"
      }
    }
  }
}
```

`apply`와 `bootstrap`은 이 파일을 설치된 plugin bundle의 `~/plugins/...` 경로에 병합합니다.
repo copy는 secret-free 상태를 유지합니다.

## First run

macOS / Linux:

```bash
./scripts/bootstrap.sh <git-url>
```

Windows PowerShell:

```powershell
.\scripts\bootstrap.ps1 -GitUrl <git-url>
```

## Local development

이 repo가 정의하는 환경을 점검하려면:

```bash
python3 -m codex_env_sync.cli inspect --repo-root .
```

현재 checkout을 홈 디렉터리에 적용하려면:

```bash
python3 -m codex_env_sync.cli apply --repo-root .
```

macOS와 Linux에서는 이 명령이 repo-managed plugin bundle, skill discovery surface,
instruction에 대한 symlink를 만듭니다. 같은 checkout에서 나중에 `git pull`을 하면
설치된 Codex 표면도 즉시 업데이트됩니다.

## Layout

```text
codex-env.toml                 # Minimal manifest: plugins + instructions + platform overrides
codex_env_sync/                # Apply engine and CLI
plugins/                       # First-party plugin bundles that get installed into ~/plugins
plugins/jy-env-core/skills/    # First-party Codex skills, authoring source and install source
instructions/                  # Generated instruction artifacts
references/                    # Local authoring references used while building first-party skills
.codex/checkpoints/            # Repo-local ignored checkpoint notes created by jy-checkpoint
.agents/plugins/               # Repo-local marketplace metadata for local plugin discovery
.agents/skills/                # Home install target for Codex native skill discovery
scripts/bootstrap.sh           # First-run shell bootstrap for macOS/Linux
scripts/bootstrap.ps1          # First-run shell bootstrap for Windows
tests/                         # Unit + integration tests
skill-tests/                   # First-party skill verification packs (baseline + pressure scenarios)
```

## Design boundaries

- upstream open source 또는 company skill은 seed material로만 사용합니다.
- raw seed source는 보통 local에만 두고 여기에는 커밋하지 않습니다.
- first-party skill을 만들 때 실제로 사용하는 curated authoring reference만 `references/` 아래에 vendor할 수 있습니다.
- first-party Codex skill은 `plugins/jy-env-core/skills/` 아래에서 직접 작성합니다.
- 이 repo는 유지보수되는 execution surface의 일부로 vendored upstream runtime을 보관하지 않습니다.
- repo-local checkpoint note는 `.codex/checkpoints/` 아래에 두고 gitignored 상태를 유지합니다.
- 여기 커밋되는 것은 customization이 끝난 first-party 결과물입니다.
- 변경이 없을 때 `apply`를 다시 실행하면 빠르고 조용하게 끝나야 합니다.

## Tests

로컬 실행:

```bash
python3 -m unittest discover -s tests -v
```

first-party skill verification asset과 static coverage를 보려면 `skill-tests/first-party/`를 참고하고,
다음 테스트를 실행하면 됩니다.

```bash
python3 -m unittest tests.test_skill_scenarios -v
```
