# AGENTS.md

## 세컨드 브레인 (Obsidian 볼트)

이 프로젝트에는 개인 지식 볼트가 있다: `second-brain/`

작업 중 보존할 가치가 있는 지식(트러블슈팅 결과, 노하우, 수행한 업무 기록)이 나오면 아래 규칙에 따라 볼트에 기록한다.

### 적재 규칙

`second-brain/ROUTING.md`를 반드시 먼저 읽고 따를 것. 요약:

- DB 기술 지식/런북/쿼리 → `second-brain/dba/` (frontmatter `topics: [dba]`)
- 수행한 업무·성과·임팩트 기록 → `second-brain/career/` (frontmatter `topics: [career]`)
- 둘 다 해당하면 페이지를 각각 만들고 `[[wikilink]]`로 상호 연결
- 급하게 저장할 초안은 `second-brain/_raw/<ISO날짜>-<slug>.md`에 드롭 (나중에 정식 페이지로 승격됨)
- 민감정보(계정, 비밀번호, 토큰, 내부 IP, 고객 데이터)는 절대 기록하지 않는다

### git 동기화

볼트에 파일을 쓰거나 수정한 뒤에는 반드시 `bash second-brain/sync.sh`를 실행한다 (볼트 변경분만 커밋 후 push).

### 페이지 형식

frontmatter에 `title`, `topics`, `tags`, `summary`를 넣고, 대화 요약이 아닌 선언적 지식으로 작성한다. 새 페이지는 관련 페이지 최소 2개와 `[[링크]]`로 연결한다.
