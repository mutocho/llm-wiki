---
title: Hot Cache
updated: 2026-08-07
---

# Hot Cache

*A ~500-word semantic snapshot of recent activity. Updated after every major write operation.*

## Recent Activity

- [2026-08-07] CAPTURE — [[personal/todo]]에 2026-08-10 10:00 `DBGW 성능 개선(일괄 실행 for문)`과 `DBGWS 승인 절차` 일정을 추가.
- [2026-08-06] CAPTURE — [[career/kakaogames/dba-agent-work-plan]] 신규. 2026-08-07 수행할 DBA Agent 명칭·구조 개편, `single`/`pipe` 역할 구분, DBMS별 주간 버전·버그 점검 및 어카운트별 최근 일주일 분석 계획.

- [2026-08-06] CAPTURE — [[synthesis/vault-governance-decisions]] 신규 (decision). career를 회사 단위 폴더(`career/kakaogames/`, 불분명 시 `career/common/`)로 재구성하고 기존 2페이지 이동. 규칙은 AGENTS.md 단일 소스 + CLAUDE.md `@AGENTS.md` import, 이 저장소는 브랜치 금지·main 직접 커밋. obsidian-git askpass chmod 함정은 [[references/obsidian-wiki-tooling-gotchas]]에 병합.

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
