"""codex exec 실행기 + 프롬프트 템플릿. Slack 의존성 없음."""
import logging
import subprocess

log = logging.getLogger(__name__)

REPO = "/Users/kakaogames/workspace/muto"
# cmux shim이 PATH의 `codex`를 가로채므로 실제 CLI 절대 경로 사용
CODEX = "/opt/homebrew/Cellar/node/24.1.0/bin/codex"
CODEX_TIMEOUT = 600  # seconds
NEEDS_SYNC = {"capture", "ingest"}

SKILLS = "/Users/kakaogames/.claude/skills"

PROMPTS = {
    "capture": (
        "다음은 Slack 채널에 올라온 메시지다. second-brain/ROUTING.md와 AGENTS.md의 "
        "적재 규칙을 읽고, 이 내용을 second-brain 볼트에 적재하라. 보존 가치가 애매하면 "
        "second-brain/_raw/<ISO날짜>-<slug>.md 로 드롭하라. 민감정보(토큰, 비밀번호, "
        "내부 IP, 고객 데이터)는 기록하지 마라. 마지막 줄에 생성/수정한 파일 경로를 출력하라.\n\n"
        "메시지가 일정(약속, 예약, 마감일, 회의 등 날짜·시간이 있는 것)이면 추가로 "
        "google-calendar MCP 도구로 기본 캘린더에 이벤트를 등록하라 (시간대 Asia/Seoul, "
        "상대 날짜는 오늘 날짜 기준으로 절대 날짜로 변환). 등록한 이벤트의 제목과 일시를 "
        "답변에 포함하라. 일정이 아니면 캘린더 등록은 하지 마라.\n\n"
        "메시지:\n{text}"
    ),
    "query": (
        "wiki-query: second-brain/ 볼트(Obsidian 위키)에서 질문의 답을 찾아라. "
        "절차: second-brain/index.md를 읽고 후보 페이지를 고른 뒤, grep으로 좁혀 "
        "관련 페이지 최대 10개만 읽고 답하라. graph-query, QMD, 전체 스캔은 하지 마라. "
        "출처 페이지 경로를 인용하고, 볼트에 없으면 없다고 답하라. 볼트를 수정하지 마라. "
        "간결하게 답하라.\n\n질문: {text}"
    ),
    "ingest": (
        f"{SKILLS}/wiki-ingest/SKILL.md 지침 파일을 읽고 그대로 수행하라. "
        "second-brain/_raw/ 의 스테이징 페이지들을 정식 위키 페이지로 승격하라. "
        "처리한 파일 목록을 출력하라.{text}"
    ),
    "lint": (
        f"{SKILLS}/wiki-lint/SKILL.md 지침 파일을 읽고 그대로 수행하라. "
        "second-brain 볼트의 건강 상태(깨진 링크, 고아 페이지, 오래된 페이지)를 "
        "리포트만 하라. 파일을 수정하지 마라.{text}"
    ),
}


def build_prompt(kind, text):
    if kind not in PROMPTS:
        raise ValueError(f"unknown kind: {kind}")
    return PROMPTS[kind].format(text=text)


def run_codex(prompt):
    r = subprocess.run(
        [CODEX, "exec", "--sandbox", "workspace-write", "--cd", REPO, prompt],
        capture_output=True, text=True, timeout=CODEX_TIMEOUT,
    )
    if r.returncode != 0:
        raise RuntimeError(f"codex exec failed (rc={r.returncode}): {r.stderr[-500:]}")
    return r.stdout


def run_sync():
    r = subprocess.run(
        ["bash", f"{REPO}/second-brain/sync.sh"],
        capture_output=True, text=True, timeout=120,
    )
    if r.returncode != 0:
        log.warning("sync.sh failed: %s", r.stderr[-300:])
