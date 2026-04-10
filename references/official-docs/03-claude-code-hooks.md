# Claude Code Hooks

**원본 URL:** https://code.claude.com/docs/en/hooks

---

## 개요

Claude Code Hooks는 세션 중 특정 라이프사이클 이벤트에서 실행되는 사용자 정의 자동화 포인트입니다. 도구 실행 전후로 동작을 가로채고, 검증하고, 수정하고, 반응할 수 있습니다.

### Hook의 역할

- **도구 실행 제어**: 실행 전 차단/허용
- **입력 수정**: 도구 인자 동적 변경
- **컨텍스트 추가**: Claude 대화에 정보 추가
- **작업 검증**: 커스텀 규칙으로 작업 검증
- **외부 시스템 통합**: 준수, 로깅, 승인 워크플로우
- **환경 관리**: 셋업/정리 자동화

---

## Hook 타입 (4가지)

### 1. Command Hook (`type: "command"`)
Shell 스크립트 실행. JSON을 stdin으로 받고, 종료 코드/stdout으로 동작 제어

```json
{
  "type": "command",
  "command": "/path/to/script.sh"
}
```

### 2. HTTP Hook (`type: "http"`)
JSON을 POST 요청으로 외부 엔드포인트 전송. API, 준수 시스템, 웹훅 통합 용도

```json
{
  "type": "http",
  "url": "http://localhost:8080/hooks/validate",
  "headers": {
    "Authorization": "Bearer $MY_TOKEN"
  },
  "allowedEnvVars": ["MY_TOKEN"]
}
```

### 3. Prompt Hook (`type: "prompt"`)
Claude에게 단일 회차 프롬프트 전송. 예/아니오 결정 반환 (간단한 검증용)

```json
{
  "type": "prompt",
  "prompt": "이 명령어가 안전해 보입니까?\n$ARGUMENTS"
}
```

### 4. Agent Hook (`type: "agent"`)
Subagent 생성하여 도구(Read, Grep, Glob)로 복잡한 조건 검증

```json
{
  "type": "agent",
  "prompt": "파일이 코딩 표준을 따르는지 확인하라"
}
```

---

## Hook 라이프사이클 이벤트

| 이벤트 | 타이밍 | 일반적 사용 |
|--------|--------|-----------|
| **SessionStart** | 세션 시작/재개 시 | 개발 컨텍스트 로드, 환경 셋업 |
| **UserPromptSubmit** | 사용자 입력 처리 전 | 프롬프트 필터링, 컨텍스트 추가 |
| **PreToolUse** | 도구 실행 전 | 위험한 명령어 검증/차단 |
| **PermissionRequest** | 권한 다이얼로그 표시 시 | 안전 작업 자동 승인 |
| **PostToolUse** | 도구 성공 후 | 로깅, 검증 |
| **PostToolUseFailure** | 도구 실패 후 | 에러 처리, 복구 제안 |
| **Stop** | Claude 응답 완료 시 | 정리, 후처리 |
| **SessionEnd** | 세션 종료 시 | 정리, 최종 로깅 |

추가 이벤트: 알림, Subagent, 파일 변경, 디렉토리 변경, 설정 변경, 컨텍스트 압축, MCP 도구 유도

---

## Hook 설정 구조

3단계 중첩 JSON:

```json
{
  "hooks": {
    "EventName": [
      {
        "matcher": "ToolName",
        "hooks": [
          {
            "type": "command",
            "if": "Bash(rm *)",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/validate.sh",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

### Hook 위치

| 위치 | 범위 |
|------|------|
| `~/.claude/settings.json` | 사용자 전체 Hook |
| `.claude/settings.json` | 프로젝트 Hook (공유 가능) |
| `.claude/settings.local.json` | 로컬 오버라이드 (미공유) |
| Plugin `hooks/hooks.json` | Plugin 번들 Hook |
| Skill/Agent frontmatter | 컴포넌트 범위 Hook |

---

## Hook 응답 패턴

### 종료 코드

- **Exit 0**: 성공 (Hook 허용, JSON 출력 처리)
- **Exit 2**: 차단 에러 (작업 방지, stderr 표시)
- **기타 코드**: 비차단 에러 (verbose 모드에서 표시)

### JSON 응답 구조

```json
{
  "decision": "block",
  "reason": "이 작업은 허용되지 않음"
}
```

혹은 PreToolUse의 더 상세한 제어:

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow",
    "updatedInput": {
      "command": "npm run lint"
    }
  }
}
```

---

## 실전 예제: Bash rm 명령어 검증

위험한 `rm -rf` 명령어 차단:

**`.claude/hooks/block-rm.sh`:**
```bash
#!/bin/bash
COMMAND=$(jq -r '.tool_input.command')

if echo "$COMMAND" | grep -q 'rm -rf'; then
  jq -n '{
    hookSpecificOutput: {
      hookEventName: "PreToolUse",
      permissionDecision: "deny",
      permissionDecisionReason: "파괴적 명령어 차단됨"
    }
  }'
else
  exit 0
fi
```

**`.claude/settings.json`:**
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "if": "Bash(rm *)",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/block-rm.sh"
          }
        ]
      }
    ]
  }
}
```

---

## Hook 기능

| 기능 | 설명 |
|------|------|
| **Matcher 패턴** | 도구명, 알림 타입 등에 정규표현식 필터링 |
| **조건 실행 (`if` 필드)** | 도구 파라미터로 추가 필터링 |
| **환경 변수** | `$CLAUDE_PROJECT_DIR`, `${CLAUDE_PLUGIN_ROOT}` 참조 |
| **Async Hook** | 비차단 백그라운드 작업 |
| **Deferred 실행** | 외부 승인 대기 (requires `-p` flag) |
| **Hook 메뉴** | `/hooks`로 설정된 모든 Hook 조회 |
| **전역 비활성화** | `"disableAllHooks": true` 설정 |

---

## Hook 권한 모델

Hook은 강력한 도구이며, 다음 원칙을 따릅니다:

- **Shell 실행 비활성화**: 사용자/프로젝트/Plugin Skill의 `` !`<command>` `` 실행 비활성화 가능 (`disableSkillShellExecution: true`)
- **Bundled Hook 예외**: Bundled 및 managed Hook은 비활성화 영향 없음

---

## 환경 변수와 대체

Hook 설정에서 사용 가능한 변수:

- `$CLAUDE_PROJECT_DIR`: 프로젝트 루트
- `${CLAUDE_PLUGIN_ROOT}`: Plugin 루트
- 환경 변수: `allowedEnvVars` 배열로 명시적 허용 필요 (보안)

---

## 일반적 패턴

### 파일 변경 감사 로깅

Post-tool Hook으로 모든 파일 수정 기록

### CI/CD 통합

외부 CI 시스템에 Hook 작업 동기화

### 규정 준수 확인

정책 위반 작업 자동 차단

### 승인 워크플로우

Deferred Hook으로 인간 승인 대기

---

## 문제 해결

- Hook이 실행되지 않음: Matcher 패턴, `if` 조건, 도구명 확인
- Hook이 느림: Command Hook 성능 최적화, HTTP Hook 타임아웃 조정
- Hook 로깅: Verbose 모드나 debug 로깅으로 진단

---

## 보안 고려사항

1. **민감한 정보**: 토큰, API 키는 환경 변수로만 전달
2. **Command Hook**: 신뢰할 수 있는 스크립트만 실행
3. **HTTP Hook**: HTTPS 사용, 인증 헤더 설정
4. **권한 최소화**: Skill `allowed-tools`로 도구 제한
