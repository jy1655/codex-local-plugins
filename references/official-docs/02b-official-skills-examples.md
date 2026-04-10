# 공식 Anthropic Skills 저장소 분석

## 개요

https://github.com/anthropics/skills 저장소는 Anthropic이 유지관리하는 공식 스킬 모음. 40+개의 에이전트가 지원하는 SKILL.md 포맷의 실제 구현 사례들을 제공한다.

## 주요 스킬 분석

### 1. PDF 스킬 (pdf/)

**목적**: PDF 파일의 모든 작업 처리

**핵심 기능**:
- 텍스트/데이터 추출
- 테이블 추출
- OCR (스캔된 문서)
- PDF 병합/분할
- 페이지 회전, 워터마크, 암호 보호
- 새 PDF 생성
- 양식 채우기
- 이미지 추출
- 암호화/복호화

**권장 라이브러리**:
- `pypdf`: 병합, 분할, 회전, 암호화
- `pdfplumber`: 텍스트/테이블 추출 (레이아웃 보존)
- `reportlab`: 새 PDF 생성
- `qpdf`, `poppler-utils`: 배치 작업

**지침 구조**:
- 최상위 수준의 기능 개요
- 각 작업별 도구/라이브러리 추천
- 작업 흐름과 코드 예제
- 상세 지침은 references/FORMS.md 등으로 분리

**특징**: 광범위한 기능을 단일 스킬에서 coverage하되, 복잡한 양식 처리는 references로 분리하여 progressive disclosure 구현.

### 2. DOCX 스킬 (docx/)

**목적**: Word 문서 생성, 편집, 분석

**핵심 기능**:
- 서식 있는 Word 파일 생성
- 기존 문서 편집
- 콘텐츠 읽기/분석
- 표, 이미지, 목차 지원
- 변경 추적 (tracked changes)

**구현 세부사항**:
```
이 스킬의 지침은 극도로 구체적인 규칙을 포함:

1. 페이지 크기 명시 필수
   - US Letter: 12,240 × 15,840 DXA

2. 불릿 마크 규칙
   - 유니코드 불릿 사용 금지
   - LevelFormat.BULLET + numbering 설정 사용

3. 테이블 폭 규칙
   - columnWidths 배열과 cell width (DXA 단위) 모두 설정

4. 표 음영
   - ShadingType.CLEAR 사용
   - SOLID 절대 금지

5. 문단 구조
   - PageBreak는 Paragraph 내부에만
   - \n 사용 금지, 별도 단락으로 분리

6. 이미지
   - explicit type 필수 (png, jpg 등)

7. 변경 추적
   - <w:ins>, <w:del> 태그 사용
   - author/date 메타데이터 포함
```

**워크플로우**:
1. Unpack XML
2. 스마트 쿼트로 수정 (&amp;#x2019; 등 엔티티 사용)
3. Validation과 함께 repack

**주목점**: 에이전트가 자주 실수할 구체적 사항들을 "Critical Rules" 섹션으로 명시. 이는 best practices의 "Gotchas 섹션" 패턴을 보여주는 좋은 예제.

### 3. MCP Builder 스킬 (mcp-builder/)

**목적**: Model Context Protocol (MCP) 서버 개발 가이드

**개발 4단계**:

1. **Research & Planning**
   - 현대적 MCP 설계 원칙
   - API 커버리지 vs 워크플로우 도구 균형
   - 명확한 도구명 (agent discoverability)

2. **Implementation**
   - 핵심 인프라 (API 클라이언트, 에러 처리)
   - 개별 도구 (schema, 문서)
   - 입출력 형식

3. **Review & Testing**
   - 코드 품질 검토
   - MCP Inspector로 테스트
   - 프레임워크별 도구 활용

4. **Evaluation**
   - 10개의 복잡하고 현실적인 질문
   - 서버 효과성 검증

**권장 기술 스택**:
- TypeScript 선호 (SDK 품질, 호환성)
- Streamable HTTP (원격) 또는 stdio (로컬)

**특징**: 이 스킬은 도구/라이브러리 사용이 아닌 개념적 가이드를 제공. 실행 가능한 절차와 패턴을 제시하는 것에 중점.

## 스킬 설계 패턴 분석

### 패턴 1: 광범위 기능 + 세부 분리

PDF 스킬처럼 넓은 도메인을 커버하되:
- SKILL.md: 핵심 기능과 도구 추천
- references/FORMS.md: 복잡한 특화 작업 상세

### 패턴 2: Gotchas 우선 설계

DOCX 스킬의 "Critical Rules" 섹션처럼:
- 에이전트가 자주 실수할 항목 우선 나열
- 구체적 제약 명시
- 위반 시 결과 명확히

### 패턴 3: 계층적 지침

1. 개요 + 기능 목록
2. 권장 도구/라이브러리
3. 구체적 워크플로우
4. 예제/코드
5. 상세 레퍼런스로 분리

### 패턴 4: 구체성 레벨 표시

- DXA 단위 수치
- 정확한 라이브러리 이름과 버전
- 선택 불가능한 기본값 ("always", "must")

### 패턴 5: 실행 중심

- 코드 예제 제공
- 명령어 표시
- 워크플로우 단계별 실행

## 스킬 구조 표준

분석한 스킬들의 공통 구조:

```
skill-name/
├── SKILL.md
│   ├── 프론트매터 (name, description)
│   ├── 개요 섹션
│   ├── 핵심 기능/부분
│   ├── 도구 또는 라이브러리
│   ├── 예제/워크플로우
│   └── 제약사항 (Gotchas, Rules)
├── references/
│   ├── REFERENCE.md (기술 상세)
│   ├── FORMS.md (특화된 작업)
│   └── [도메인별 파일]
├── scripts/
│   └── [자동화 스크립트들]
└── assets/
    ├── [템플릿]
    └── [예제 파일]
```

## 프론트매터 사용 패턴

**대표 예제들의 프론트매터**:

```yaml
---
name: pdf-processing
description: PDF 추출, 양식 작성, 병합 등. PDF 작업 시 사용.
---
```

모든 분석 대상 스킬:
- 정확히 name과 description만 사용
- license, compatibility, metadata 미사용
- 간결하고 명확한 description

## 설명 필드의 품질 분석

**효과적인 description 특징**:

1. 동사 우선 ("Extract", "Process", "Create")
2. 쉼표로 구분한 기능 나열
3. 사용 시점 명시 ("When", "Use when")
4. 직접 에이전트 지시 ("Use this skill when...")

**예**:
- "Extract PDF text, fill forms, merge files. Use when handling PDFs."
- "Analyze datasets, generate charts, create summary reports."
- "Create, edit, and analyze Word documents."

## 토큰 효율성 관찰

**PDF 스킬 분석**:
- SKILL.md 본문: ~2000 토큰
- Progressive disclosure로 세부사항은 references로 분리
- 에이전트가 매번 전체 문서 로드 필요 없음

**DOCX 스킬 분석**:
- SKILL.md: ~3000 토큰 (규칙 많음)
- 하지만 구체성이 높아 에이전트의 실수 감소
- 명확한 규칙 > 모호한 지침 + 디버깅

## 스킬 활성화 시점

**분석 예시**:

PDF 스킬은:
- "I have a PDF" 명시적 언급에 활성화
- "extract tables from this document" 모호한 표현도 활성화
- Description이 광범위하게 작성되어 다양한 쿼리 커버

DOCX 스킬은:
- "Word document", ".docx" 명시적 언급
- "report writing", "memo creation" 등도 활성화

## 실제 구현 교훈

1. **너무 일반적인 설명은 피하기**
   - "Document processing" (너무 넓음)
   - 대신: "Extract text, create reports, fill forms from PDFs"

2. **구체적 예제 포함**
   - 코드 블록
   - 명령어
   - 입출력 샘플

3. **에러 케이스 명시**
   - 지원 안 하는 형식
   - 제약사항
   - 대체 방법

4. **도구/라이브러리 명시적 선택**
   - 모든 옵션 나열 대신 기본값 정함
   - "Use pdfplumber. For scanned documents, use pytesseract instead."

5. **Progressive disclosure 최대 활용**
   - SKILL.md: 핵심만
   - references: 상세
   - scripts: 재사용 가능한 로직

---

**분석 기준**: 2026년 4월 - https://github.com/anthropics/skills
**분석 스킬**: PDF, DOCX, MCP-Builder (대표성 있는 3개)
