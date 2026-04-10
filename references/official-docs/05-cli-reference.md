# Claude Code CLI Reference

**원본 URL:** https://code.claude.com/docs/en/cli-reference

---

## CLI 명령어

기본 명령어들로 세션 시작, 파이프 처리, 대화 재개, 업데이트 관리:

| 명령어 | 설명 | 예시 |
|--------|------|------|
| `claude` | 대화형 세션 시작 | `claude` |
| `claude "query"` | 초기 프롬프트로 세션 시작 | `claude "이 프로젝트 설명해줘"` |
| `claude -p "query"` | SDK로 쿼리 후 종료 | `claude -p "이 함수 설명해줘"` |
| `cat file \| claude -p "query"` | 파이프 콘텐츠 처리 | `cat logs.txt \| claude -p "분석해줘"` |
| `claude -c` | 현재 디렉토리의 최근 대화 계속 | `claude -c` |
| `claude -c -p "query"` | SDK로 계속 진행 | `claude -c -p "타입 에러 확인"` |
| `claude -r "<session>" "query"` | 세션 ID/이름으로 재개 | `claude -r "auth-refactor" "PR 완료해줘"` |
| `claude update` | 최신 버전으로 업데이트 | `claude update` |
| `claude auth login` | Anthropic 계정으로 로그인 | `claude auth login --email user@example.com` |
| `claude auth logout` | 로그아웃 | `claude auth logout` |
| `claude auth status` | 인증 상태 (JSON) | `claude auth status --text` (인간 읽기 형식) |
| `claude agents` | 모든 설정된 Subagent 목록 | `claude agents` |
| `claude auto-mode defaults` | 기본 auto mode 분류자 규칙 출력 | `claude auto-mode defaults > rules.json` |
| `claude mcp` | MCP 서버 설정 | [MCP 문서](/en/mcp) 참조 |
| `claude plugin` | Plugin 관리 | `claude plugin install code-review@claude-plugins-official` |
| `claude remote-control` | Remote Control 서버 시작 | `claude remote-control --name "My Project"` |

---

## CLI 플래그

세션 동작을 커스터마이즈하는 플래그들. `claude --help`가 모든 플래그를 나열하지 않으므로, 플래그가 없어도 사용 가능할 수 있습니다.

### 기본 플래그

| 플래그 | 설명 | 예시 |
|--------|------|------|
| `--help` | 도움말 표시 | `claude --help` |
| `--version`, `-v` | 버전 번호 출력 | `claude -v` |
| `--verbose` | Verbose 로깅 활성화 | `claude --verbose` |
| `--debug [categories]` | 디버그 모드 (선택적 카테고리) | `claude --debug "api,mcp"` |
| `--debug-file <path>` | 디버그 로그를 파일에 쓰기 | `claude --debug-file /tmp/debug.log` |
| `--init` | 초기화 Hook 실행 후 시작 | `claude --init` |
| `--init-only` | 초기화 Hook만 실행 | `claude --init-only` |
| `--maintenance` | 유지보수 Hook 실행 후 시작 | `claude --maintenance` |

### 파일/디렉토리 플래그

| 플래그 | 설명 | 예시 |
|--------|------|------|
| `--add-dir` | 추가 작업 디렉토리 접근 허용 | `claude --add-dir ../apps ../lib` |
| `--strict-mcp-config` | 지정된 MCP 설정만 사용 | `claude --strict-mcp-config --mcp-config ./mcp.json` |
| `--plugin-dir` | Plugin 로드 경로 (반복 가능) | `claude --plugin-dir ./my-plugins` |
| `--mcp-config` | MCP 서버 JSON 설정 (공백 구분) | `claude --mcp-config ./mcp.json` |

### 세션/모델 플래그

| 플래그 | 설명 | 예시 |
|--------|------|------|
| `--continue`, `-c` | 최근 대화 계속 | `claude -c` |
| `--resume`, `-r` | 특정 세션 재개 (ID/이름) | `claude -r "auth-refactor"` |
| `--name`, `-n` | 세션 디스플레이 이름 설정 | `claude -n "my-feature"` |
| `--session-id` | 특정 세션 ID 사용 (UUID) | `claude --session-id "550e8400..."` |
| `--fork-session` | 재개 시 새 세션 ID 생성 | `claude --resume abc123 --fork-session` |
| `--model` | 모델 선택 (별칭: sonnet, opus) | `claude --model claude-opus-4-6` |
| `--effort` | 노력 수준 (low, medium, high, max) | `claude --effort high` |
| `--agent` | 특정 Agent 지정 (세션 스코프) | `claude --agent my-agent` |
| `--agents` | 동적 Subagent JSON 정의 | `claude --agents '{"reviewer":{...}}'` |

### 권한/보안 플래그

| 플래그 | 설명 | 예시 |
|--------|------|------|
| `--permission-mode` | 권한 모드 (default, acceptEdits, plan, auto, dontAsk, bypassPermissions) | `claude --permission-mode plan` |
| `--dangerously-skip-permissions` | 모든 권한 프롬프트 스킵 | `claude --dangerously-skip-permissions` |
| `--allow-dangerously-skip-permissions` | bypassPermissions 모드 활성화 | `claude --permission-mode plan --allow-dangerously-skip-permissions` |
| `--tools` | 사용 가능한 도구 제한 | `claude --tools "Bash,Edit,Read"` |
| `--allowedTools` | 권한 없이 사용 가능한 도구 | `"Bash(git log *)" "Read"` |
| `--disallowedTools` | 사용 불가능한 도구 | `"Bash(git log *)" "Edit"` |

### 시스템 프롬프트 플래그

| 플래그 | 설명 | 예시 |
|--------|------|------|
| `--system-prompt` | 전체 시스템 프롬프트 교체 | `claude --system-prompt "넌 Python 전문가다"` |
| `--system-prompt-file` | 파일에서 전체 프롬프트 교체 | `claude --system-prompt-file ./prompts/review.txt` |
| `--append-system-prompt` | 기본 프롬프트에 텍스트 추가 | `claude --append-system-prompt "항상 TypeScript 사용"` |
| `--append-system-prompt-file` | 파일 내용 추가 | `claude --append-system-prompt-file ./style-rules.txt` |

### 출력/포맷 플래그

| 플래그 | 설명 | 예시 |
|--------|------|------|
| `--print`, `-p` | 대화형 모드 없이 응답 출력 | `claude -p "query"` |
| `--output-format` | 출력 포맷 (text, json, stream-json) | `claude -p "query" --output-format json` |
| `--input-format` | 입력 포맷 (text, stream-json) | `claude -p --input-format stream-json` |
| `--json-schema` | 검증된 JSON 스키마 요청 | `claude -p --json-schema '{"type":"object",...}'` |
| `--max-turns` | 최대 Agent 턴 수 제한 | `claude -p --max-turns 3` |
| `--max-budget-usd` | 최대 비용 한계 (달러) | `claude -p --max-budget-usd 5.00` |
| `--include-hook-events` | Hook 라이프사이클 이벤트 포함 | `claude -p --output-format stream-json --include-hook-events` |
| `--include-partial-messages` | 스트리밍 이벤트 포함 | `claude -p --output-format stream-json --include-partial-messages` |
| `--replay-user-messages` | 사용자 메시지를 stdout으로 재출력 | `claude -p --input-format stream-json --replay-user-messages` |

### 기술 플래그

| 플래그 | 설명 | 예시 |
|--------|------|------|
| `--bare` | 최소 모드 (Hook, Skill, Plugin 스킵) | `claude --bare -p "query"` |
| `--betas` | 베타 헤더 포함 (API 키 사용자) | `claude --betas interleaved-thinking` |
| `--chrome` | Chrome 브라우저 통합 활성화 | `claude --chrome` |
| `--no-chrome` | Chrome 통합 비활성화 | `claude --no-chrome` |
| `--ide` | IDE 자동 연결 (정확히 1개) | `claude --ide` |
| `--tmux` | Tmux 세션 생성 (with --worktree) | `claude -w feature-auth --tmux` |
| `--worktree`, `-w` | Git worktree에서 시작 | `claude -w feature-auth` |
| `--teammate-mode` | Agent team 표시 모드 (auto, in-process, tmux) | `claude --teammate-mode in-process` |
| `--no-session-persistence` | 세션 지속성 비활성화 (print 모드) | `claude -p --no-session-persistence "query"` |
| `--setting-sources` | 설정 소스 로드 (user, project, local) | `claude --setting-sources user,project` |
| `--settings` | JSON 파일 또는 문자열에서 설정 로드 | `claude --settings ./settings.json` |
| `--disable-slash-commands` | 모든 Skill과 명령어 비활성화 | `claude --disable-slash-commands` |
| `--fallback-model` | 모델 과부하 시 폴백 모델 (print 모드) | `claude -p --fallback-model sonnet "query"` |

### 원격/웹 플래그

| 플래그 | 설명 | 예시 |
|--------|------|------|
| `--remote` | claude.ai에 웹 세션 생성 | `claude --remote "로그인 버그 수정"` |
| `--teleport` | 웹 세션을 로컬 터미널에서 재개 | `claude --teleport` |
| `--remote-control`, `--rc` | Remote Control 활성화 | `claude --remote-control "My Project"` |
| `--remote-control-session-name-prefix` | RC 세션 이름 접두사 | `claude remote-control --remote-control-session-name-prefix dev-box` |
| `--channels` | MCP 서버 Channel 리스닝 | `claude --channels plugin:my-notifier@my-marketplace` |
| `--dangerously-load-development-channels` | 승인되지 않은 Channel 개발 로드 | `claude --dangerously-load-development-channels server:webhook` |
| `--from-pr` | GitHub PR에 연결된 세션 재개 | `claude --from-pr 123` |

### Auth 플래그

| 플래그 | 설명 | 예시 |
|--------|------|------|
| `--email` | 로그인 이메일 미리 채우기 | `claude auth login --email user@example.com` |
| `--sso` | SSO 강제 | `claude auth login --sso` |
| `--console` | Console API 사용 (API 청구) | `claude auth login --console` |

---

## 시스템 프롬프트 플래그 (상세)

4가지 방법으로 시스템 프롬프트 커스터마이즈:

| 플래그 | 동작 | 예시 |
|--------|------|------|
| `--system-prompt` | 전체 기본 프롬프트 교체 | `claude --system-prompt "넌 Python 전문가"` |
| `--system-prompt-file` | 파일로 전체 교체 | `claude --system-prompt-file ./prompts/review.txt` |
| `--append-system-prompt` | 기본 프롬프트에 추가 | `claude --append-system-prompt "항상 TypeScript"` |
| `--append-system-prompt-file` | 파일 내용 추가 | `claude --append-system-prompt-file ./style-rules.txt` |

`--system-prompt`와 `--system-prompt-file` 상호 배타적. Append 플래그는 어느 대체 플래그와도 결합 가능.

**권장**: 대부분의 경우 Append 플래그 사용. Replacement 플래그는 시스템 프롬프트를 완전히 제어할 필요한 경우에만 사용.

---

## 환경 변수

기본 설정 보완:

- `CLAUDE_CODE_DISABLE_CRON=1`: Cron 스케줄러 비활성화
- `CLAUDE_CODE_SIMPLE=1`: 최소 모드
- `CLAUDE_REMOTE_CONTROL_SESSION_NAME_PREFIX`: RC 이름 접두사

더 많은 환경 변수는 [Environment Variables 문서](/en/env-vars) 참조

---

## 관련 자료

- **Chrome 확장**: 웹 자동화 및 테스트
- **대화형 모드**: 단축키, 입력 모드
- **빠른 시작**: Claude Code 시작하기
- **일반적 워크플로우**: 고급 패턴
- **설정**: 설정 옵션
- **Agent SDK 문서**: 프로그래밍 방식 사용 및 통합
