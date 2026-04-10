# agentskills/agentskills 레포지토리 - 도구 및 참조 라이브러리

## 개요

https://github.com/agentskills/agentskills는 Agent Skills 공식 참조 구현을 제공하는 저장소. Python 기반 `skills-ref` 라이브러리와 도구를 포함.

**특징**:
- Apache 2.0 라이선스
- 문서는 CC-BY-4.0 라이선스
- Anthropic 개발, 커뮤니티 기여 환영
- Discord 커뮤니티 활동 중

## skills-ref 라이브러리

### 목적

스킬 디렉토리 검증, 포맷 처리, 에이전트 시스템 프롬프트 XML 생성.

### 핵심 기능

#### 1. 검증 (validate)

```bash
skills-ref validate ./my-skill
```

**검사 항목**:
- SKILL.md 파일 존재 확인
- YAML frontmatter 유효성
- 필드 유효성 (name, description)
- 네이밍 컨벤션 준수
  - name은 소문자/숫자/하이픔만
  - 디렉토리 이름과 일치
  - 64자 이하
  - 하이픔으로 시작/종료 불가

**에러 처리**:
- 형식 오류 보고
- 제약사항 위반 지적
- 수정 가이드 제시

#### 2. 프로퍼티 읽기 (properties)

```bash
skills-ref properties ./my-skill --format json
```

**출력**:
```json
{
  "name": "pdf-processing",
  "description": "Extract PDF text...",
  "location": "/path/to/skill",
  "license": "Apache-2.0",
  "compatibility": "Requires Python 3.8+"
}
```

**용도**:
- 스킬 카탈로그 자동 생성
- CI/CD 파이프라인 통합
- 메타데이터 수집

#### 3. 프롬프트 생성 (prompt)

```bash
skills-ref prompt ./skills --format xml
```

**생성 내용**:
```xml
<available_skills>
  <skill>
    <name>pdf-processing</name>
    <description>Extract PDF text, fill forms, merge files...</description>
    <location>/path/to/pdf-processing/SKILL.md</location>
  </skill>
  <skill>
    <name>data-analysis</name>
    ...
  </skill>
</available_skills>
```

**특징**:
- Anthropic 모델에 최적화된 XML 포맷
- 다른 구현은 자체 포맷으로 조정 가능
- 다중 스킬 디렉토리 지원
- 재귀적 스킬 발견

### 설치 및 사용

#### pip 설치

```bash
pip install agentskills
```

#### uv 설치 (권장)

```bash
uv pip install agentskills
```

#### Python 코드에서 사용

```python
from agentskills.skills_ref import validate, properties, prompt

# 검증
result = validate("./my-skill")
if not result.valid:
    print(f"Errors: {result.errors}")

# 프로퍼티 읽기
props = properties("./my-skill")
print(f"Name: {props['name']}")

# 프롬프트 XML 생성
xml = prompt("./skills", format="xml")
print(xml)
```

### 출력 포맷 옵션

#### JSON

```bash
skills-ref prompt ./skills --format json
```

```json
{
  "available_skills": [
    {
      "name": "pdf-processing",
      "description": "...",
      "location": "/path/to/SKILL.md"
    }
  ]
}
```

#### XML (기본)

Anthropic 모델 최적화

#### YAML

```bash
skills-ref prompt ./skills --format yaml
```

## 저장소 구조

```
agentskills/
├── README.md                      # 프로젝트 개요
├── LICENSE                        # Apache 2.0
├── pyproject.toml                 # Python 프로젝트 정의
├── uv.lock                        # 의존성 락파일
├── CLAUDE.md                      # Claude 에이전트용 가이드
├── src/
│   └── agentskills/
│       └── skills_ref/            # 메인 라이브러리
│           ├── __init__.py
│           ├── cli.py             # CLI 명령어
│           ├── validator.py       # 검증 로직
│           ├── parser.py          # SKILL.md 파싱
│           └── generator.py       # 프롬프트 생성
└── tests/
    └── [단위 테스트들]
```

## 검증 상세

### 필드 검증

**name**:
```
- 1-64자
- [a-z0-9-] 만 사용 가능
- 하이피으로 시작/종료 불가
- 연속 하이픔(--) 불가
- 부모 디렉토리 이름과 일치
```

**description**:
```
- 필수 필드
- 1-1024자
- 비어있으면 안 됨
```

**license** (선택):
```
- 최대 500자
- 라이선스명 또는 파일 참조
```

**compatibility** (선택):
```
- 최대 500자
- 환경 요구사항 명시
```

**metadata** (선택):
```
- 임의 키-값 맵
- 문자열 값만 가능
```

### 디렉토리 검증

```
스킬-이름/
├── SKILL.md          # 필수, 정확히 이 이름
└── (다른 파일들)      # 자유
```

**규칙**:
- SKILL.md 파일 필수
- 정확한 파일명 (대소문자 구분)
- 디렉토리 이름 = name 필드

## 리스트 기능

스킬 디렉토리의 모든 스킬 나열:

```bash
skills-ref list ./skills
```

**출력**:
```
pdf-processing        Extract PDF text, fill forms, merge files...
data-analysis         Analyze datasets, generate charts...
code-review           Review code for quality and security...
```

**옵션**:
- `--format json`: JSON 출력
- `--format csv`: CSV 출력
- `--format yaml`: YAML 출력

## 통합 워크플로우

### 1. 스킬 개발

```bash
# 스킬 생성
mkdir my-skill
cat > my-skill/SKILL.md << 'EOF'
---
name: my-skill
description: My new skill
---

Instructions...
EOF

# 검증
skills-ref validate my-skill
```

### 2. CI/CD 통합

```bash
# GitHub Actions 예제
- name: Validate skills
  run: |
    pip install agentskills
    skills-ref validate ./skills-directory
    if [ $? -ne 0 ]; then
      echo "Skill validation failed"
      exit 1
    fi
```

### 3. 카탈로그 생성

```bash
# 모든 스킬의 카탈로그 생성
skills-ref prompt ./skills \
  --format json \
  --output catalog.json
```

### 4. 에이전트 시스템 프롬프트 주입

```python
from agentskills.skills_ref import prompt

# 스킬 카탈로그 생성
skills_xml = prompt(
    "./skills-directory",
    format="xml"
)

# 시스템 프롬프트에 주입
system_prompt = f"""
You are an AI agent.

{skills_xml}

When a task matches a skill's description, load the skill...
"""
```

## 주의사항

### 프로덕션 사용

공식 문서에서:
> "This library is intended for demonstration purposes only.
> It is not meant to be used in production."

**의미**:
- 참조 구현으로 제공
- 프로덕션 환경은 프로젝트 요구사항에 맞게 커스터마이즈
- 성능, 보안, 확장성 검토 필요
- 충분한 테스트 필수

### 성능 고려사항

- 큰 스킬 디렉토리: 스캔 속도
- 검증: YAML 파싱 오버헤드
- 프롬프트 생성: XML 직렬화

## 실전 예제

### 예제 1: 스킬 검증 자동화

```python
from pathlib import Path
from agentskills.skills_ref import validate

skills_dir = Path("./skills")
for skill_dir in skills_dir.iterdir():
    if skill_dir.is_dir():
        result = validate(str(skill_dir))
        status = "✓" if result.valid else "✗"
        print(f"{status} {skill_dir.name}")
        if not result.valid:
            for error in result.errors:
                print(f"  {error}")
```

### 예제 2: 검증을 포함한 배포

```bash
#!/bin/bash
set -e

# 모든 스킬 검증
for skill_dir in skills/*/; do
    echo "Validating $skill_dir"
    skills-ref validate "$skill_dir" || exit 1
done

# 카탈로그 생성
skills-ref prompt ./skills --format json > catalog.json

# 배포
git add catalog.json
git commit -m "Update skill catalog"
git push
```

### 예제 3: 여러 형식으로 내보내기

```bash
# XML (Anthropic 최적화)
skills-ref prompt ./skills --format xml > skills-catalog.xml

# JSON (프로그래밍 접근)
skills-ref prompt ./skills --format json > skills-catalog.json

# YAML (가독성)
skills-ref prompt ./skills --format yaml > skills-catalog.yaml
```

## 확장 포인트

### 커스텀 검증

프로젝트별 추가 규칙:

```python
from agentskills.skills_ref import validate

result = validate("./my-skill")

# 추가 검증
if result.valid:
    skill_props = properties("./my-skill")
    if "author" not in skill_props.get("metadata", {}):
        print("Warning: metadata should include author")
```

### 프로프트 커스터마이징

```python
from agentskills.skills_ref import properties
import json

skills_xml = prompt("./skills", format="json")
skills = json.loads(skills_xml)

# 커스텀 필터링 (예: 특정 버전만)
filtered = [s for s in skills.get("available_skills", [])
            if "v2" in s.get("name")]
```

## 커뮤니티 자료

- **GitHub**: https://github.com/agentskills/agentskills
- **Discord**: 공식 커뮤니티 채널
- **Issue 추적**: 버그 리포트, 기능 요청
- **Pull Requests**: 커뮤니티 기여 환영

## 요약

`skills-ref` 라이브러리는 다음 작업을 자동화:

1. **검증**: SKILL.md 형식과 필드 검사
2. **파싱**: frontmatter와 메타데이터 추출
3. **생성**: 에이전트 시스템 프롬프트 XML 생성
4. **통합**: CI/CD, 배포 파이프라인에 통합

프로덕션 사용은 요구사항에 맞게 커스터마이징 필요.

---

**작성 기준 날짜**: 2026년 4월
**소스**: https://github.com/agentskills/agentskills
