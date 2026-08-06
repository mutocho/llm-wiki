---
title: Hot Cache
updated: 2026-08-06
---

# Hot Cache

*A ~500-word semantic snapshot of recent activity. Updated after every major write operation.*

## Recent Activity

- [2026-08-06] CAPTURE — [[synthesis/vault-governance-decisions]] 신규 (decision). career를 회사 단위 폴더(`career/kakaogames/`, 불분명 시 `career/common/`)로 재구성하고 기존 2페이지 이동. 규칙은 AGENTS.md 단일 소스 + CLAUDE.md `@AGENTS.md` import, 이 저장소는 브랜치 금지·main 직접 커밋. obsidian-git askpass chmod 함정은 [[references/obsidian-wiki-tooling-gotchas]]에 병합.
- [2026-08-06] CAPTURE — [[synthesis/verbal-source-verification-policy]] 신규. 세미나·사내 출처의 반복 오류 5건을 근거로 한 적재 규칙. synthesis 카테고리 첫 페이지.
- [2026-08-06] UPDATE — [[dba/mysql-partition-pruning-prepared-stmt-bug]] 보강. 사내 문서의 "8.0.41 버그" 표기를 8.0.42로 정정, Reorganize는 재발 방지가 아닌 리셋임을 명시.
- [2026-08-05] CAPTURE — [[dba/mysql-partition-pruning-prepared-stmt-bug]] 신규 (dba/career 양쪽 적재). MySQL Bug #119309 공식 리포트 + 자체 재현 테스트 결과. 버그 리포트에 없는 "INSERT 이력 없으면 미노출" 조건 규명.
- [2026-08-04] CAPTURE — Aurora DSQL 세미나 노트를 [[dba/aurora-dsql]] 신규 페이지로 적재 (낙관적 락, buffer pool 없음, 앱 리트라이 필수). dba/ 13페이지를 Notion 🗃️ DBA 하위로 내보냄.
- [2026-08-04] LINT+CAPTURE — 깨진 wikilink 2건(경로 접두어 누락) 수정, career/2026 frontmatter 보강. wikilink 접두어 함정을 [[references/obsidian-wiki-tooling-gotchas]]에 병합.
- [2026-08-04] CAPTURE — forum DB 롤별 search_path 설정을 [[dba/postgresql-operations]]·[[career/2026]]에 이중 적재. career 범위를 "회사 수행 작업 전체 기록"으로 확장 (ROUTING.md).
- [2026-08-04] CAPTURE/UPDATE — [[dba/operational-queries]] 신규. 볼트의 첫 SQL 코드블록 페이지(3사 대조 15개 카테고리: 진단 1~11, 권한 감사 12, 권한 부여 13, DDL 14, DML 15). 표준 시스템 뷰 기반이라 **실행 검증 전(draft)** — 현장 쿼리로 교체 필요. `search_path` 설정 지식도 여기 흡수.
- [2026-08-04] UPDATE — [[dba/aurora-dsql]]을 AWS 공식 문서로 대조 보강(draft→verified). 세미나 노트의 "스토리지 무제한"을 정정하고 공식 한도표·미지원 기능·DPU 과금 추가.
- [2026-08-04] CAPTURE — obsidian-wiki graph-query의 폴디드 summary 파싱 함정을 [[references/obsidian-wiki-tooling-gotchas]]로 승격. psql `\dT` 메타커맨드는 [[dba/postgresql-operations]]에 섹션 추가.
- [2026-08-04] INGEST — `_raw/` 15건을 정식 페이지로 승격 (dba 13, career 1, references 1). Notion 'Muto - DBA 통합 포털' 전체 뎁스(~140페이지) 수집분 포함.
- [2026-08-04] Notion 포털 심층 감사 — 교정 백로그 20건(P1: TRUNCATE 생성기, QA 호스트명 노출, 개인 이메일 잔존 등) 도출.
- [2026-08-04] INIT — DBA/커리어 이중 허브 볼트 생성, git auto-sync 훅 구성.

## Active Threads

- Notion 원본 P1 교정 6건 대기 — [[dba/notion-remediation-backlog]]
- Notion 포털 vs 로컬 볼트 역할 분담 미결정 — [[dba/notion-llm-wiki-governance]]
- [[dba/operational-queries]] 실행 검증 대기 — 개발/QA 인스턴스에서 확인 후 현장 쿼리로 교체

## Key Takeaways

- career 새 페이지는 반드시 회사 폴더 하위(`career/kakaogames/` 또는 `career/common/`) — 루트 직접 적재 금지 — [[synthesis/vault-governance-decisions]]
- MySQL 회수 릴리스(8.0.29, 8.0.38/8.4.1)는 사용 금지 — [[dba/mysql-operations]]
- **8.0.42는 파티션 pruning 회귀** — 증상 없다고 안전한 게 아니라 INSERT 이력이 없어 미노출일 뿐 — [[dba/mysql-partition-pruning-prepared-stmt-bug]]
- 구술·사내 출처의 오류는 **수치·버전·한도**에 몰린다 — 대조 전 `verified` 승격 금지 — [[synthesis/verbal-source-verification-policy]]
- `idle_in_transaction_session_timeout` 미설정이 PG bloat 장애 1순위 원인 — [[dba/postgresql-operations]]
- AWS PI 콘솔 2026-07-31 종료 → Database Insights 전환 — [[dba/monitoring-incident-runbook]]
- graph-query의 `index_only: true`는 신뢰 금지 — 폴디드 summary를 못 읽어 오탐 — [[references/obsidian-wiki-tooling-gotchas]]
- Aurora DSQL 스토리지는 무제한이 아님 — 클러스터당 10 TiB 기본(증액 시 256 TiB) — [[dba/aurora-dsql]]
- 대량 DML 전 `sql_safe_updates=1`(MySQL) / `lock_timeout`(PG) / `SET LOCK_TIMEOUT`(MSSQL) 가드 — [[dba/operational-queries]]

## Flagged Contradictions

- KB 색인 실측 33건/검증완료 19건 vs 포털 기록 31건/17건 — 수기 집계 드리프트 확인됨.
