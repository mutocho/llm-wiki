# Muto 세컨드 브레인 (LLM Wiki)

DBA 업무 지식과 커리어 기록을 함께 관리하는 개인 지식 시스템입니다.
Obsidian 볼트(순수 마크다운) + Claude Code 스킬/훅 + git 자동 동기화로 구성되며, Codex 등 다른 AI 에이전트에서도 같은 규칙으로 사용할 수 있습니다.

## 1. 개요

```
┌─ 작업 세션 (Claude Code / Codex) ─────────────────────┐
│  발견·노하우 발생                                      │
│    ├─ 수동: /wiki-capture            → _raw/ 초안 적재 │
│    └─ 자동: Stop 훅 → /wiki-capture --quick            │
└───────────────────────────────────────────────────────┘
                     ↓ (주기적으로)
   /wiki-ingest  →  _raw/ 초안을 dba/·career/ 정식 페이지로 승격
                     ↓ (모든 볼트 쓰기 후 자동)
   sync.sh       →  git commit + push (원격 백업)
```

두 개의 주제 허브로 라우팅됩니다 (`second-brain/ROUTING.md` 참조):

| 허브 | 용도 | frontmatter |
|---|---|---|
| `second-brain/dba/` | DB 기술 지식, 트러블슈팅, 런북, 쿼리 | `topics: [dba]` |
| `second-brain/career/` | 업무 로그 → 성과 → 포트폴리오 | `topics: [career]` |

하나의 사건이 양쪽에 해당하면 페이지를 각각 만들고 `[[wikilink]]`로 상호 연결합니다 (한 페이지에 섞지 않음).

## 2. 디렉터리 구조

```
muto/
├── README.md                  # 이 문서
├── AGENTS.md                  # Codex 등 에이전트용 적재 규칙
├── .claude/
│   └── settings.json          # 프로젝트 훅: 볼트 쓰기 후 auto-sync
└── second-brain/              # Obsidian 볼트 (여기를 Obsidian에서 Open Vault)
    ├── index.md               # 전체 페이지 색인 (자동 관리)
    ├── log.md                 # 작업 로그 (INIT/INGEST/QUERY 기록)
    ├── hot.md                 # 최근 활동 스냅샷 (~500단어 캐시)
    ├── ROUTING.md             # dba/career 적재 판단 규칙
    ├── .manifest.json         # ingest 이력 (source 해시 → 생성 페이지)
    ├── sync.sh                # git 자동 동기화 스크립트
    ├── env.example            # .env 템플릿 (복사 후 rename)
    ├── dba/                   # DBA 지식 허브 (_hub.md가 입구)
    ├── career/                # 커리어 허브 (_hub.md, 2026.md 연간 뷰)
    ├── references/            # 외부 참조·환경 노트
    ├── _raw/                  # 캡처 초안 대기열 (ingest 대상)
    │   └── _archived/         # 승격 완료된 초안 원본
    ├── _staging/              # 스테이징 모드용 (기본 미사용)
    ├── _archives/             # 위키 스냅샷 보관
    ├── concepts|entities|skills|synthesis|journal|projects/  # 표준 카테고리
    └── .obsidian/             # Obsidian 설정
```

## 3. 다른 장비에서 구축하기

### 사전 조건

- AI 코딩 에이전트: Claude Code 또는 Codex CLI (둘 다 있어도 됨 — 같은 볼트를 공유)
- git, python3 (macOS/Linux 기본 포함)
- (선택) Obsidian 앱 — 그래프 뷰·편집용. 볼트는 순수 마크다운이라 없어도 동작

### 3-1. obsidian-wiki 스킬 세트 설치

위키 스킬(`/wiki-capture`, `/wiki-ingest`, `/wiki-query` 등)은 [obsidian-wiki](https://github.com/Ar9av/obsidian-wiki) 패키지가 제공합니다. 새 장비에서 먼저 설치합니다:

```bash
# 1. 패키지 설치
pip install obsidian-wiki

# 2. 스킬을 장비에 설치된 모든 AI 에이전트(Claude Code, Codex 등)에 설치 + 전역 config 생성
obsidian-wiki setup
# 프롬프트에서 볼트 경로를 물으면 <클론 경로>/second-brain 지정
# (클론 전이면 아무 경로로 진행 후 ~/.obsidian-wiki/config 에서 수정)

# 3. 설치 확인
obsidian-wiki info      # 설치 경로·버전·config 확인
obsidian-wiki doctor    # 상태 진단
ls ~/.claude/skills | grep wiki   # wiki-* 스킬 존재 확인
```

설치 결과물 (패키지 파일로의 심볼릭 링크):
- `~/.claude/skills/wiki-*`, `~/.claude/skills/llm-wiki` — Claude Code용 스킬
- `~/.codex/skills/wiki-*`, `~/.codex/prompts/wiki-*` — Codex용 스킬/프롬프트 (Codex가 설치돼 있으면 자동)
- `~/.obsidian-wiki/config` — 전역 설정 (`OBSIDIAN_VAULT_PATH` 등). 프로젝트별 `.env`가 있으면 그것이 우선

### 3-2. 저장소 클론과 기본 셋팅

```bash
# 1. 저장소 클론
git clone https://github.com/mutocho/llm-wiki.git muto
cd muto

# 2. .env 생성 (경로를 새 장비에 맞게 수정)
cp second-brain/env.example second-brain/.env
# OBSIDIAN_VAULT_PATH=<클론 경로>/second-brain
# OBSIDIAN_SOURCES_DIR=<클론 경로>
# CLAUDE_HISTORY_PATH=~/.claude

# 3. sync.sh 실행 권한
chmod +x second-brain/sync.sh

# 4. .claude/settings.json의 훅 경로 수정
#    (auto-sync 훅이 절대 경로를 쓰므로 새 장비 경로로 변경)
#    "command": "bash <클론 경로>/second-brain/sync.sh"

# 5. (선택) 세션 종료 자동 캡처 훅 설치
mkdir -p ~/.obsidian-wiki/hooks
curl -fsSL https://raw.githubusercontent.com/Ar9av/obsidian-wiki/main/.claude/hooks/wiki-stop-capture.sh \
  -o ~/.obsidian-wiki/hooks/wiki-stop-capture.sh
chmod +x ~/.obsidian-wiki/hooks/wiki-stop-capture.sh
# ~/.claude/settings.json 의 hooks 에 추가:
#   "Stop": [{"matcher": "", "hooks": [{"type": "command",
#     "command": "bash ~/.obsidian-wiki/hooks/wiki-stop-capture.sh"}]}]
# 추가 후 JSON 유효성 검증:
python3 -c "import json,os; json.load(open(os.path.expanduser('~/.claude/settings.json'))); print('OK')"

# 5-1. (선택) Stop 훅에 볼트 git 동기화 패치 추가
#    다운로드한 wiki-stop-capture.sh 의 `INPUT=$(cat)` 바로 아래에 삽입:
#
#    VAULT_SYNC="<클론 경로>/second-brain/sync.sh"
#    [[ -x "$VAULT_SYNC" ]] && bash "$VAULT_SYNC" </dev/null >/dev/null 2>&1 || true
#
#    반드시 stop_hook_active 조기 종료 검사보다 앞에 두어야 한다 —
#    캡처는 훅 알림 다음 턴에 실행되므로, 캡처 턴이 끝난 뒤의 Stop에서도
#    방금 쓴 _raw/ 파일이 커밋되게 하기 위함. 이 패치로 muto 프로젝트 밖에서
#    작업하다 볼트에 캡처한 경우에도 세션 종료 시 자동 commit+push 된다.

# 6. (선택) Obsidian에서 File → Open Vault → second-brain 선택
```

### 3-3. Codex 환경 구축 (선택)

Codex CLI를 쓰는 장비라면 추가 설정은 거의 없습니다:

- **스킬**: 3-1의 `obsidian-wiki setup`이 `~/.codex/skills/`와 `~/.codex/prompts/`에 함께 설치합니다. 이미 setup을 실행했다면 끝. Codex를 나중에 설치했다면 `obsidian-wiki setup`을 다시 실행하면 됩니다.
- **적재 규칙**: 프로젝트 루트의 `AGENTS.md`를 Codex가 자동으로 읽습니다 (볼트 위치, ROUTING 규칙, 민감정보 금지 포함). 별도 설정 불필요.
- **git 동기화**: Codex에는 Claude Code의 PostToolUse/Stop 훅이 없습니다. 대신 `AGENTS.md`가 "볼트 쓰기 후 `bash second-brain/sync.sh` 실행"을 지시하므로 지침 기반으로 동기화됩니다. 세션 종료 자동 캡처(위 5번 훅)도 없으므로, 남길 지식은 세션 중 `/wiki-capture`로 직접 캡처합니다.

검증:
- Claude Code: 이 디렉터리에서 열고 `/wiki-status` 실행 → 볼트가 인식되면 완료.
- Codex: 이 디렉터리에서 `codex` 실행 후 `/wiki-status` → 동일하게 확인.

## 4. 일상 사용법

### 기본 흐름

1. **작업한다** — Claude Code 또는 Codex로 평소처럼 작업. Claude Code는 의미 있는 편집이 있던 세션 종료 시 Stop 훅이 `/wiki-capture --quick`을 유도해 발견 사항이 `_raw/`에 자동 드롭됩니다 (Codex는 훅이 없어 수동 캡처만).
2. **수동 캡처** — 대화 중 남기고 싶은 지식이 생기면 즉시 `/wiki-capture`(정식 페이지) 또는 `/wiki-capture --quick`(초안만).
3. **주기적 승격** — `_raw/`가 쌓이면 `/wiki-ingest`로 dba/career 정식 페이지로 승격. career 페이지는 회사 단위로 자동 라우팅됩니다 (`ROUTING.md` — 현재 회사 카카오게임즈 → `career/kakaogames/`, 불분명하면 `career/common/`).
4. **검색** — 과거 지식이 필요하면 `/wiki-query <질문>`.
5. **동기화는 자동** — 볼트 쓰기마다 sync.sh가 commit+push. 수동 실행은 `bash second-brain/sync.sh`.

### 스킬 명령 요약

| 명령 | 용도 | 쓰기 범위 |
|---|---|---|
| `/wiki-capture` | 현재 대화의 지식을 분류해 정식 페이지로 저장 | 페이지 + 색인 |
| `/wiki-capture --quick` | 60초 내 초안만 `_raw/`에 드롭 (훅이 사용) | `_raw/`만 |
| `/wiki-ingest` | `_raw/` 초안을 dba/career 페이지로 승격 + 색인 갱신 | 전체 |
| `/wiki-query <질문>` | 위키에서 답 검색 (읽기 전용, log만 기록) | log.md만 |
| `/wiki-status` | 볼트 상태·미처리 초안 확인 | 없음 |
| `/wiki-history-ingest claude\|codex` | 과거 AI 세션 기록을 채굴해 위키로 | 전체 |
| `/cross-linker` | 페이지 간 누락된 링크 자동 연결 | 페이지 |
| `/wiki-dedup` | 중복 페이지 탐지·병합 | 페이지 (파괴적) |

## 5. 구성 요소 상세 (함수별 용도)

### second-brain/sync.sh — git 자동 동기화

| 블록 | 용도 |
|---|---|
| `V="$(cd "$(dirname "$0")" && pwd)"` | 스크립트 위치 기준으로 볼트 경로 자동 결정 (장비 간 이식성) |
| stdin JSON 파싱 (`[ ! -t 0 ]` 분기) | 훅 호출 시 Claude Code가 넘긴 `tool_input.file_path`를 읽음. 터미널에서 직접 실행하면 건너뜀 |
| `case "$f" in "$V"/*)` | 수정된 파일이 볼트 내부일 때만 진행 — 일반 코드 작업에서는 커밋 안 생김 |
| `git add -A . && git diff --cached --quiet` | 볼트 변경분만 스테이징, 변경 없으면 종료 |
| `git commit -qm "wiki: auto-sync <일시>" && git push -q` | 타임스탬프 커밋 후 push (원격 없거나 실패해도 조용히 통과) |

수동 실행: `bash second-brain/sync.sh` (stdin 없이 실행하면 무조건 동기화).

### ~/.obsidian-wiki/hooks/wiki-stop-capture.sh — 세션 종료 자동 캡처

Claude Code Stop 이벤트마다 실행되어, 의미 있는 작업이 있던 세션에서만 `/wiki-capture --quick`을 유도합니다.

| 함수/블록 | 용도 |
|---|---|
| 볼트 sync 패치 (`VAULT_SYNC` 블록, 로컬 추가) | 세션 종료 시 볼트 미커밋 변경분 commit+push. `stop_hook_active` 검사보다 앞이라 캡처 턴 종료 후에도 동작. 실패 무시(best-effort) |
| `stop_hook_active` 검사 | 훅이 유발한 캡처 턴에서 재실행 방지 (무한 루프 차단) |
| 센티널 `mkdir` (`/tmp/wiki-stop-capture-<session_id>.done`) | 세션당 1회만 발동. mkdir의 원자성으로 훅 중복 등록 시에도 알림 1개 보장 |
| `split_segments(cmd)` | 셸 명령을 `\|`, `&&`, `;` 기준으로 분할 — 따옴표 내부는 분할하지 않음. (원문, 비인용부, 확장가능부) 3요소 반환 |
| `segment_readonly(seg, ...)` | 명령 조각 1개가 읽기 전용인지 판정. 화이트리스트(`READONLY_CMDS`, `GIT_READONLY` 등) + 변경 플래그 검사(`sed -i`, `find -delete`, `curl -X POST`, `sort -o` 등). `$( )` 치환은 무조건 변경으로 간주(보수적) |
| `command_readonly(cmd)` | 모든 조각이 읽기 전용이어야 True |
| `PY_RISKY` / `AWK_RISKY` 정규식 | 인라인 `python -c`·awk 스크립트 안의 파일 쓰기/프로세스 실행/DML 감지 |
| MCP 도구 동사 분류 (`MCP_WRITE_VERBS`/`MCP_READ_VERBS`) | `create/update/delete…`가 이름에 있으면 변경으로, 판별 불가 도구도 변경으로 가정 |
| transcript 집계 루프 | JSONL 대화 기록에서 `Write/Edit` 수, `Bash` 수, 변경 Bash 수, 의심 도구 수를 카운트 |
| 발동 조건 | `파일 편집 ≥1` 또는 `Bash ≥4 그리고 (변경 명령 ≥1 또는 의심 도구 ≥1)` |
| `exit 2` + stderr | Stop 훅 규약: stderr 내용이 Claude에게 전달되어 `/wiki-capture --quick` 실행을 지시 |

### wiki-capture --quick의 KEEP/SKIP 게이트

훅이 발동해도 스킬 내부에서 한 번 더 거릅니다: 조사·설명만 있던 세션(SKIP) vs 수사로 찾은 수정·비자명한 동작 확인·디버깅 결론(KEEP). 훅 경유 시 SKIP 쪽으로 보수적 판단.

### AGENTS.md — Codex 연동

Codex가 이 프로젝트에서 실행되면 자동으로 읽는 지침 파일. 볼트 위치, ROUTING 규칙, 민감정보 금지, 볼트 쓰기 후 `bash second-brain/sync.sh` 실행 규칙을 담고 있습니다. Codex에는 훅이 없으므로 지침 기반으로 동작합니다.

### .claude/settings.json (프로젝트) — auto-sync 훅

```json
{"hooks": {"PostToolUse": [{"matcher": "Edit|Write|MultiEdit",
  "hooks": [{"type": "command", "command": "bash <경로>/second-brain/sync.sh"}]}]}}
```

Claude Code가 파일을 쓸 때마다 sync.sh를 호출하고, sync.sh가 볼트 내부 파일인지 스스로 필터링합니다.

## 6. 페이지 작성 규약

- frontmatter 필수: `title`, `topics`, `tags`(2~4개), `summary`(≤200자)
- 대화 요약이 아닌 **선언적 지식**으로 작성 ("X는 ~하다")
- 추론한 내용은 `^[inferred]`, 상충하는 내용은 `^[ambiguous]` 마커
- 새 페이지는 기존 페이지 최소 2개와 `[[링크]]`
- **민감정보(비밀번호·토큰·내부 IP·고객 데이터) 기록 절대 금지** — 위치 참조만 남김

## 7. 트러블슈팅

| 증상 | 원인/해결 |
|---|---|
| 커밋이 안 생김 | sync.sh 실행 권한(`chmod +x`), settings.json의 절대 경로 확인 |
| 세션 종료 시 캡처 안 뜸 | 편집 0건 + 읽기 전용 세션은 정상 스킵. `/tmp/wiki-stop-capture-*.done` 센티널은 세션당 1회 |
| 훅 등록 후 Claude Code 오류 | `~/.claude/settings.json` JSON 문법(트레일링 콤마) 검증 |
| `_raw/`가 계속 쌓임 | `/wiki-ingest`를 주기적으로 실행 (승격 후 `_raw/_archived/`로 이동됨) |
| push 실패가 조용히 지나감 | sync.sh는 push 실패를 무시함(오프라인 허용). `git status -sb`로 ahead 여부 확인 후 수동 push |
