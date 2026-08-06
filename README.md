# Muto 세컨드 브레인 (LLM Wiki)

DBA 업무 지식과 커리어 기록을 함께 관리하는 개인 지식 시스템입니다.
Obsidian 볼트(순수 마크다운) + Claude Code/Codex 스킬·hook + Git 자동 동기화로 구성됩니다.

## 1. 개요

```
┌─ 작업 세션 (Claude Code / Codex) ─────────────────────┐
│  발견·노하우 발생                                      │
│    ├─ 수동: /wiki-capture            → _raw/ 초안 적재 │
│    └─ 자동(Claude): Stop 훅 → /wiki-capture --quick    │
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
    ├── env.example            # .env 템플릿 (복사 후 경로 수정)
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

## 3. 새 장비 초기 설정

운영체제와 에이전트 조합에 따라 아래 네 경로 중 하나를 선택합니다. Claude Code와 Codex를 함께 사용한다면 같은 운영체제의 두 절차를 모두 적용합니다.

| 운영체제 | Claude Code | Codex |
|---|---|---|
| macOS | [3-2](#3-2-macos--claude-code) | [3-3](#3-3-macos--codex) |
| Windows | [3-4](#3-4-windows--claude-code) | [3-5](#3-5-windows--codex) |

### 3-1. 공통 준비

필수 도구는 Git, Python 3, 사용할 AI 에이전트입니다. Obsidian 앱은 선택 사항입니다.

1. 저장소를 클론합니다.
2. `obsidian-wiki`를 설치하고 `setup`을 실행합니다.
3. `second-brain/env.example`을 `second-brain/.env`로 복사한 뒤 절대 경로를 입력합니다.
4. `obsidian-wiki doctor`와 `/wiki-status`로 설치를 검증합니다.

`obsidian-wiki setup`은 설치된 에이전트를 감지하여 다음 위치에 스킬과 설정을 배치합니다.

- Claude Code: `~/.claude/skills/wiki-*`
- Codex: `~/.codex/skills/wiki-*`, `~/.codex/prompts/wiki-*`
- 공통 볼트 설정: `~/.obsidian-wiki/config`

> **Hook 호환성:** `wiki-stop-capture.sh`는 Claude Code transcript와 Stop 규약을 기준으로 작성되었습니다. Codex도 최신 버전에서 hook을 지원하지만 transcript 형식이 다르므로 이 스크립트를 Codex Stop hook에 그대로 등록하지 않습니다. Codex에서는 Git 동기화 hook과 `AGENTS.md`를 사용하고, 자동 캡처는 Codex 호환 스크립트가 제공될 때까지 `/wiki-capture --quick`을 수동 실행합니다.

### 3-2. macOS × Claude Code

```bash
git clone https://github.com/mutocho/llm-wiki.git ~/muto
cd ~/muto

python3 -m pip install obsidian-wiki
obsidian-wiki setup

cp second-brain/env.example second-brain/.env
chmod +x second-brain/sync.sh
```

`second-brain/.env`를 다음처럼 수정합니다.

```dotenv
OBSIDIAN_VAULT_PATH=/Users/<username>/muto/second-brain
OBSIDIAN_SOURCES_DIR=/Users/<username>/muto
CLAUDE_HISTORY_PATH=/Users/<username>/.claude
CODEX_HISTORY_PATH=/Users/<username>/.codex
```

#### Claude hook 설정

1. `.claude/settings.json`의 `PostToolUse` 명령을 현재 클론의 절대 경로로 바꿉니다.

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write|MultiEdit",
        "hooks": [
          {
            "type": "command",
            "command": "bash /Users/<username>/muto/second-brain/sync.sh"
          }
        ]
      }
    ]
  }
}
```

2. 세션 종료 자동 캡처용 Stop hook을 설치합니다.

```bash
mkdir -p ~/.obsidian-wiki/hooks
curl -fsSL https://raw.githubusercontent.com/Ar9av/obsidian-wiki/main/.claude/hooks/wiki-stop-capture.sh \
  -o ~/.obsidian-wiki/hooks/wiki-stop-capture.sh
chmod +x ~/.obsidian-wiki/hooks/wiki-stop-capture.sh
```

`~/.claude/settings.json`의 기존 설정을 보존하면서 다음 `Stop` 항목을 병합합니다.

```json
{
  "hooks": {
    "Stop": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "bash ~/.obsidian-wiki/hooks/wiki-stop-capture.sh"
          }
        ]
      }
    ]
  }
}
```

3. `python3 -m json.tool ~/.claude/settings.json`으로 JSON을 검사하고 Claude Code의 `/hooks`에서 등록 상태를 확인합니다. 저장소에서 `/wiki-status`를 실행한 뒤 테스트 파일을 편집해 auto-sync와 Stop 캡처를 검증합니다.

### 3-3. macOS × Codex

```bash
git clone https://github.com/mutocho/llm-wiki.git ~/muto
cd ~/muto

python3 -m pip install obsidian-wiki
obsidian-wiki setup

cp second-brain/env.example second-brain/.env
chmod +x second-brain/sync.sh
mkdir -p ~/.codex
```

`.env`는 [macOS × Claude Code](#3-2-macos--claude-code)와 동일하게 설정합니다. Codex는 프로젝트 루트의 `AGENTS.md`에서 볼트 라우팅과 동기화 규칙을 자동으로 읽습니다.

#### Codex hook 설정

`~/.codex/hooks.json`을 만들거나 기존 hook 정의에 다음 `PostToolUse` 항목을 병합합니다.

```json
{
  "description": "Sync Obsidian vault writes",
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "apply_patch|Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "bash /Users/<username>/muto/second-brain/sync.sh",
            "statusMessage": "Syncing the Obsidian vault"
          }
        ]
      }
    ]
  }
}
```

Codex를 다시 시작한 뒤 CLI의 `/hooks`에서 정의를 검토하고 신뢰해야 실행됩니다. `/wiki-status`로 볼트를 확인하고 볼트 파일을 한 번 수정해 Git 동기화를 검증합니다.

> Codex의 `Stop` hook 자체는 지원되지만, 현재 `wiki-stop-capture.sh`는 Claude transcript 구조를 분석합니다. Codex Stop에 직접 등록하면 작업량 판별이 되지 않으므로 자동 캡처에는 사용하지 않습니다. Codex에서는 세션 중 `/wiki-capture --quick`을 실행합니다.

### 3-4. Windows × Claude Code

Git for Windows, Python 3, Claude Code를 먼저 설치합니다. Claude Code가 Git Bash를 찾지 못하면 다음 환경 변수를 사용자 환경에 등록합니다.

```powershell
[Environment]::SetEnvironmentVariable(
  "CLAUDE_CODE_GIT_BASH_PATH",
  "C:\Program Files\Git\bin\bash.exe",
  "User"
)
```

PowerShell에서 공통 설치를 진행합니다.

```powershell
git clone https://github.com/mutocho/llm-wiki.git "$HOME\muto"
Set-Location "$HOME\muto"

py -m pip install obsidian-wiki
obsidian-wiki setup

Copy-Item second-brain\env.example second-brain\.env
notepad second-brain\.env
```

`second-brain/.env`에는 슬래시(`/`)를 사용한 절대 경로를 권장합니다.

```dotenv
OBSIDIAN_VAULT_PATH=C:/Users/<username>/muto/second-brain
OBSIDIAN_SOURCES_DIR=C:/Users/<username>/muto
CLAUDE_HISTORY_PATH=C:/Users/<username>/.claude
CODEX_HISTORY_PATH=C:/Users/<username>/.codex
```

#### Claude hook 설정

`.claude/settings.json`의 `PostToolUse` 명령을 다음 형식으로 바꿉니다.

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write|MultiEdit",
        "hooks": [
          {
            "type": "command",
            "command": "\"C:\\Program Files\\Git\\bin\\bash.exe\" C:/Users/<username>/muto/second-brain/sync.sh"
          }
        ]
      }
    ]
  }
}
```

Stop hook 스크립트는 설치된 패키지에서 복사합니다.

```powershell
$hookSource = py -c "import obsidian_wiki, pathlib; print(pathlib.Path(obsidian_wiki.__file__).parent / '_data' / 'hooks' / 'wiki-stop-capture.sh')"
New-Item -ItemType Directory -Force "$HOME\.obsidian-wiki\hooks" | Out-Null
Copy-Item $hookSource "$HOME\.obsidian-wiki\hooks\wiki-stop-capture.sh"
```

`$HOME\.claude\settings.json`에 다음 항목을 기존 설정과 병합합니다.

```json
{
  "hooks": {
    "Stop": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "\"C:\\Program Files\\Git\\bin\\bash.exe\" C:/Users/<username>/.obsidian-wiki/hooks/wiki-stop-capture.sh"
          }
        ]
      }
    ]
  }
}
```

`Get-Content "$HOME\.claude\settings.json" -Raw | ConvertFrom-Json | Out-Null`로 JSON을 검사하고, Claude Code를 다시 시작한 뒤 `/hooks`와 `/wiki-status`로 확인합니다.

### 3-5. Windows × Codex

Git for Windows, Python 3, Codex를 설치한 뒤 PowerShell에서 진행합니다.

```powershell
git clone https://github.com/mutocho/llm-wiki.git "$HOME\muto"
Set-Location "$HOME\muto"

py -m pip install obsidian-wiki
obsidian-wiki setup

Copy-Item second-brain\env.example second-brain\.env
notepad second-brain\.env
New-Item -ItemType Directory -Force "$HOME\.codex" | Out-Null
```

`.env`는 [Windows × Claude Code](#3-4-windows--claude-code)와 동일하게 설정합니다. Codex는 프로젝트의 `AGENTS.md`를 자동으로 읽습니다.

`$HOME\.codex\hooks.json`을 만들거나 다음 `PreToolUse`와 `PostToolUse` 항목을 기존 설정에 병합합니다. 두 훅은 셸 명령 전후에 `second-brain/git-sync-hook.sh`를 실행합니다.

```json
{
  "description": "Synchronize second-brain before and after shell tool use",
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash|shell_command",
        "hooks": [
          {
            "type": "command",
            "command": "bash C:/Users/<username>/muto/second-brain/git-sync-hook.sh",
            "commandWindows": "\"C:\\Program Files\\Git\\bin\\bash.exe\" --login -c \"bash C:/Users/<username>/muto/second-brain/git-sync-hook.sh\"",
            "statusMessage": "Syncing second-brain before tool use"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Bash|shell_command",
        "hooks": [
          {
            "type": "command",
            "command": "bash C:/Users/<username>/muto/second-brain/git-sync-hook.sh",
            "commandWindows": "\"C:\\Program Files\\Git\\bin\\bash.exe\" --login -c \"bash C:/Users/<username>/muto/second-brain/git-sync-hook.sh\"",
            "statusMessage": "Syncing second-brain after tool use"
          }
        ]
      }
    ]
  }
}
```

`git-sync-hook.sh`는 `second-brain/` 변경만 자동 커밋합니다. 저장소의 다른 경로에 로컬 변경이 있으면 동기화를 건너뛰며, pull 충돌은 원격 버전을 우선하는 `git pull --no-rebase -X theirs`로 병합한 후 push합니다. Codex의 `PreToolUse`와 `PostToolUse`는 현재 셸 명령에 대해서만 실행됩니다.

`Get-Content "$HOME\.codex\hooks.json" -Raw | ConvertFrom-Json | Out-Null`로 JSON을 검사합니다. Codex를 다시 시작한 뒤 CLI의 `/hooks`에서 hook을 검토·신뢰하고 `/wiki-status`를 실행합니다.

> Windows Codex도 `wiki-stop-capture.sh`를 직접 등록하지 않습니다. Git Bash에서 스크립트를 실행할 수는 있지만 Codex transcript 형식과 호환되지 않습니다. 자동 캡처가 필요하면 Codex 호환 Stop hook을 별도로 구현해야 하며, 현재는 `/wiki-capture --quick`을 사용합니다.

### 3-6. 공통 최종 검증

```bash
obsidian-wiki info
obsidian-wiki doctor
bash second-brain/sync.sh
git status --short --branch
```

- `obsidian-wiki doctor`에 치명적 오류가 없어야 합니다.
- `/wiki-status`가 `second-brain` 볼트를 인식해야 합니다.
- `git status`가 `main...origin/main`이고 작업 트리가 깨끗해야 합니다.
- Obsidian을 사용한다면 **Open folder as vault**로 `second-brain` 폴더를 엽니다.

공식 hook 규약은 [Claude Code Hooks reference](https://code.claude.com/docs/en/hooks)와 [Codex Advanced Configuration — Hooks](https://learn.chatgpt.com/docs/config-advanced#hooks)를 기준으로 합니다.

## 4. 일상 사용법

### 기본 흐름

1. **작업한다** — Claude Code 또는 Codex로 평소처럼 작업. Claude Code는 의미 있는 편집이 있던 턴의 Stop hook이 `/wiki-capture --quick`을 유도합니다. Codex도 hook을 지원하지만 현재 자동 캡처 스크립트와 transcript 형식이 달라 수동 캡처를 사용합니다.
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
| stdin JSON 파싱 (`[ ! -t 0 ]` 분기) | hook 호출 시 `tool_input.file_path`를 읽음. 터미널에서 직접 실행하면 건너뜀 |
| `case "$f" in "$V"/*)` | 수정된 파일이 볼트 내부일 때만 진행 — 일반 코드 작업에서는 커밋 안 생김 |
| `git add -A . && git diff --cached --quiet` | 볼트 변경분만 스테이징, 변경 없으면 종료 |
| `git commit -qm "wiki: auto-sync <일시>" && git push -q` | 타임스탬프 커밋 후 push (원격 없거나 실패해도 조용히 통과) |

수동 실행: `bash second-brain/sync.sh` (stdin 없이 실행하면 무조건 동기화).

### ~/.obsidian-wiki/hooks/wiki-stop-capture.sh — Claude 자동 캡처

Claude Code Stop 이벤트마다 실행되어, 의미 있는 작업이 있던 세션에서만 `/wiki-capture --quick`을 유도합니다. Codex에는 직접 등록하지 않습니다.

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

Codex가 이 프로젝트에서 실행되면 자동으로 읽는 지침 파일입니다. 볼트 위치, ROUTING 규칙, 민감정보 금지, 볼트 쓰기 후 `bash second-brain/sync.sh` 실행 규칙을 담습니다. Codex hook이 누락되거나 신뢰되지 않은 상황에서도 이 지침이 동기화의 안전망으로 동작합니다.

### ~/.codex/hooks.json — Codex auto-sync hook

Codex는 `SessionStart`, `PreToolUse`, `PostToolUse`, `Stop`, `SessionEnd` 등의 lifecycle hook을 지원합니다. 이 저장소에서는 Windows Codex의 `PreToolUse`와 `PostToolUse`에 `second-brain/git-sync-hook.sh`를 연결합니다. 스크립트는 볼트 변경만 커밋하고, 원격 우선 merge 후 push하며, 볼트 외부에 로컬 변경이 있으면 실행을 건너뜁니다. 현재 두 tool hook은 셸 명령에 대해서만 실행됩니다. 사용자·프로젝트 hook은 정의가 바뀔 때마다 Codex CLI의 `/hooks`에서 검토하고 신뢰해야 합니다.

현재 Claude용 `wiki-stop-capture.sh`는 Claude transcript 구조를 읽으므로 Codex Stop hook에는 연결하지 않습니다. Codex에서 남길 지식은 `/wiki-capture --quick`으로 수동 캡처합니다.

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
| 커밋이 안 생김 | `sync.sh` 경로, Git Bash, hook 등록 상태를 확인. Codex는 `/hooks`에서 신뢰 여부도 확인 |
| Claude 종료 시 캡처 안 뜸 | 편집 0건 + 읽기 전용 세션은 정상 스킵. `${TMPDIR:-/tmp}/wiki-stop-capture-*.done` 센티널 확인 |
| Codex 종료 시 자동 캡처가 안 뜸 | 현재 정상 동작. Claude용 스크립트는 Codex transcript와 호환되지 않으므로 `/wiki-capture --quick` 사용 |
| hook 등록 후 Claude Code 오류 | `~/.claude/settings.json`을 `python3 -m json.tool` 또는 PowerShell `ConvertFrom-Json`으로 검증 |
| hook 등록 후 Codex에서 실행 안 됨 | `hooks.json` 문법, `[features].codex_hooks=true` 여부, `/hooks`의 검토·신뢰 상태 확인 |
| Codex Git 동기화가 건너뛰어짐 | `second-brain/` 외부의 로컬 변경을 먼저 커밋하거나 되돌린 뒤 다시 실행 |
| `_raw/`가 계속 쌓임 | `/wiki-ingest`를 주기적으로 실행 (승격 후 `_raw/_archived/`로 이동됨) |
| push 실패가 조용히 지나감 | sync.sh는 push 실패를 무시함(오프라인 허용). `git status -sb`로 ahead 여부 확인 후 수동 push |
