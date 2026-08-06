---
title: Wiki Index
---

# Wiki Index

*This index is automatically maintained. Last updated: 2026-08-06*

## 주제 허브

- [[dba/_hub|DBA 지식베이스]] — 업무 정보, 경험, 노하우, 작업용 문서
- [[career/_hub|커리어 관리]] — 성과, 작업 내역, 포트폴리오 재료

## DBA

- [[dba/mysql-operations|MySQL/Aurora MySQL 운영 지식]] — 백업 표준, Undo·락, 회수 릴리스 포함 버전 이정표
- [[dba/postgresql-operations|PostgreSQL 운영 지식]] — 계정/권한 패턴, 파라미터 베이스라인, XID 알람 기준
- [[dba/sqlserver-operations|SQL Server 운영 지식]] — VLF, Parameter Sniffing, AG vs FCI, 버전 비교
- [[dba/mysql-partition-pruning-prepared-stmt-bug|MySQL 8.0.42 파티션 pruning 회귀 (Bug #119309)]] — prepared INSERT 경계 통과 시 ERROR 1748, INSERT 이력 없으면 미노출
- [[dba/db-common-concepts|DBMS 공통 개념·3사 비교]] — 격리수준/MVCC/문법 비교표, SQL 안티패턴
- [[dba/operational-queries|운영 쿼리 모음 — 진단·권한·DDL/DML]] — 3사 대조 SQL 15개 카테고리. 1~12 읽기 전용, 13~15 변경 명령(안전 절차 포함). 실행 검증 전
- [[dba/monitoring-incident-runbook|모니터링·장애 대응 런북]] — 시간박스형 대응, 점검 주기, 알람 세트
- [[dba/dba-ops-standards|DBA 운영 표준]] — 장애 대응 5단계, 문서 생명주기
- [[dba/db-access-control|3-엔진 계정·권한 관리 표준]] — Role 분리, break-glass, 금지 권한
- [[dba/db-security-review-patterns|DB 문서 보안 검토 위험 패턴]] — 감사 체크리스트
- [[dba/aurora-dsql|AWS Aurora DSQL]] — 멀티 리전 multi-master, OCC(40001) 리트라이, 미지원 기능·공식 한도표, DPU 과금
- [[dba/cloud-platform-knowledge|클라우드·플랫폼 지식]] — Aurora 내부, Azure 백업, Docker 표준
- [[dba/dev-tooling-standards|개발 도구 운영 기준]] — Ruff·CLAUDE.md·CI 요약
- [[dba/dev-automation-detail|개발·자동화 상세]] — Ruff 설정 상세, Slack Bot scope
- [[dba/notion-llm-wiki-governance|LLM Wiki 운영 거버넌스]] — Notion 포털 3계층·상태 모델
- [[dba/notion-remediation-backlog|Notion 지식베이스 교정 백로그]] — P1~P3 교정 대상 20건

## Career

- [[career/kakaogames/notion-kb-consolidation-worklog|DBA 지식베이스 통합 정리 프로젝트 (2026-07)]] — 31개 문서, 6차 검증, 포트폴리오 재료
- [[career/kakaogames/2026|2026년 작업 내역]]

## References

- [[references/claude-code-permission-guardrails|Claude Code 권한 가드레일 동작]] — 이 머신의 훅/분류기 차단 우회 경로
- [[references/obsidian-wiki-tooling-gotchas|obsidian-wiki 도구 동작 함정]] — graph-query의 폴디드 summary 파싱 실패, index_only 오탐, wikilink 경로 접두어 함정

## Concepts

## Entities

## Skills

## Synthesis

- [[synthesis/verbal-source-verification-policy|구술·사내 출처는 공식 문서 대조 전까지 승격하지 않는다]] — 볼트 내 5건의 실제 오류 근거, 대조 우선순위는 수치·버전·한도
- [[synthesis/vault-governance-decisions|볼트 거버넌스 결정]] — career 회사 단위 라우팅(kakaogames/common), AGENTS.md 단일 소스 + CLAUDE.md @import, 브랜치 금지

## Journal
