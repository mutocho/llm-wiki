---
title: MySQL 8.0.42 파티션 pruning 캐시 회귀 (Bug #119309)
tags: [dba, mysql, troubleshooting, partitioning]
topics: [dba]
summary: >-
  8.0.42 회귀 — DEFAULT CURRENT_TIMESTAMP 파티션 키에 prepared INSERT를 재사용하면 경계 통과 후
  ERROR 1748. 캐시는 첫 실행 때 생기므로 INSERT 이력이 없는 테이블은 증상이 안 보인다.
project: second-brain
base_confidence: 0.85
provenance:
  extracted: 0.85
  inferred: 0.15
lifecycle_changed: 2026-08-04
sources:
  - "MySQL Bug #119309 — An insert prepared statement fails to write across partitions (https://bugs.mysql.com/bug.php?id=119309, 2026-08-04 확인)"
  - "자체 재현 테스트 (second-brain session 2026-08-04)"
category: dba
lifecycle: verified
tier: supporting
created: 2026-08-04
updated: 2026-08-04
---

# MySQL 8.0.42 파티션 pruning 캐시 회귀 (Bug #119309)

## 증상

타임스탬프 RANGE 파티션 테이블에 **prepared statement로 INSERT**할 때, 파티션 경계를 넘어간 뒤 같은 statement를 재실행하면 실패한다.

```
ERROR 1748 (HY000): Found a row not matching the given partition set
```

- **영향 버전: 8.0.42** — 8.0.41 및 그 이전에는 없던 **회귀**다. 리포터(Ivo Matsuo) 진술: *"I do not see the problem in 8.0.41 or older"*. Oracle(Roy Lyseng)이 `Verified as described`로 확인.
- Bug #119309, 상태 `Verified`, 심각도 S3.

> **사내 문서 정정** — 이 건을 "8.0.41 업스트림 버그"로 적은 자료가 있으나, **8.0.41은 정상이고 8.0.42에서 유입된 회귀**다. 버전 판단을 뒤집는 차이이므로(8.0.41 유지 = 안전, 8.0.42 업그레이드 = 노출) 인용 시 확인할 것.

## 발생 조건

세 가지가 모두 겹칠 때만 발생한다:

1. `RANGE` 파티션 + 파티션 표현식이 시각 기반 (`unix_timestamp(created_timestamp)` 등)
2. 파티션 키 컬럼이 **`DEFAULT CURRENT_TIMESTAMP`** — INSERT 문이 그 컬럼을 명시하지 않고 서버 기본값에 의존
3. **prepared statement 또는 stored procedure를 준비해 두고 재사용** — 리포트에 SP도 명시돼 있다(*"first execution of statement in procedure happens at time point"*). SP 본문의 문장도 내부적으로 준비·캐시되므로 같은 결함을 탄다.

## 원인 — 리포트의 코드 레벨 분석

파티션 프루닝이 **`Sql_cmd_insert_base::prepare_inner()`에서 테이블 락을 잡기 전에 미리 수행**되고, 그 시점의 시각을 기준으로 `partition_info::lock_partitions` 비트맵이 확정된다. **이 비트맵은 재실행 때 갱신되지 않는다.**

- `partition_info::lock_partitions` — prepare 시점에 한 번 계산되고 그대로 재사용됨 (**결함 지점**)
- `partition_info::read_partitions` — 실행마다 정상적으로 재계산됨

시간이 경계를 넘어가면 행은 새 파티션으로 가야 하는데 `lock_partitions`는 과거 파티션 집합을 고정하고 있어, 실제 행과 잠긴 파티션 집합이 어긋나고 서버가 1748로 거부한다.

> **"커넥션 연결 시점"이 아니라 "prepare / 최초 실행 시점"이 기준이다.** 커넥션을 열어만 두고 해당 statement를 아직 실행하지 않았다면 비트맵은 존재하지 않는다(아래 "핵심" 항목).

## 핵심 — 왜 어떤 테이블은 멀쩡해 보이는가

**pruning 캐시는 그 테이블에 INSERT가 실제로 실행될 때 만들어진다. INSERT 이력이 없으면 캐시 자체가 없으므로 경계를 넘어도 정상 INSERT된다.**

자체 재현 테스트로 확인한 사실이며, 버그 리포트가 명시하지 않은 부분이다. 운영에서 다음을 뜻한다:

- **증상이 안 나타난다고 해서 해당 버전이 안전한 게 아니다.** 그 테이블에 트래픽이 없었을 뿐일 수 있다.
- 반대로, **평소 쓰지 않다가 장애 시점에 처음 쓰이는 테이블**(에러 로그류)은 첫 INSERT 시점에 캐시가 생기고, 그 커넥션이 오래 살아 있으면 다음 경계에서 터진다. 조사 대상에서 빼면 안 된다.
- 영향 범위 판정은 "에러가 났는가"가 아니라 **"조건 3가지를 만족하는 테이블 + 장수 커넥션의 prepared statement 재사용 여부"**로 해야 한다.

## 재현 방법 — 경계를 기다리지 않는다

`SET TIMESTAMP`으로 세션의 현재 시각을 조작해 즉시 재현한다. **순서가 핵심이다 — 먼저 경계 이전 시각으로 INSERT해 pruning 캐시를 만들어야 한다.**

```sql
-- 1) 경계 이전 시각으로 세션 시계를 맞추고 INSERT → 이 시점에 pruning 캐시 형성
SET TIMESTAMP = UNIX_TIMESTAMP('2026-08-01 00:01:50');
-- (prepared statement 준비 후 실행)

-- 2) 경계를 넘긴 시각으로 이동
SET TIMESTAMP = UNIX_TIMESTAMP('2026-09-01 00:01:50');

-- 3) 같은 prepared statement 재실행 → ERROR 1748
```

1)을 건너뛰고 2)부터 시작하면 캐시가 없어 **정상 INSERT되고 재현에 실패한다.** 이게 위 "왜 멀쩡해 보이는가"와 같은 현상이다.

> `SET TIMESTAMP`은 `NOW()`·`CURRENT_TIMESTAMP`·`DEFAULT CURRENT_TIMESTAMP`에 적용되지만 **`SYSDATE()`에는 적용되지 않는다**(`sysdate-is-now` 옵션 미사용 시). 파티션 표현식이나 컬럼 기본값이 `SYSDATE()`를 쓰면 이 방법으로 재현되지 않는다.
> `SET TIMESTAMP`은 복제가 시각을 재현할 때 쓰는 변수다. **테스트 인스턴스에서만 쓰고 운영 세션에서는 쓰지 않는다.**

## 수정 상태

- Dmitry Lenev가 패치 기여. `DEFAULT CURRENT_TIMESTAMP`에 의존하는 표현식은 **prepare 시점 pruning을 미루고 실행 시점에 `read_partitions` 비트맵으로 매번 재계산**하도록 바꾼다 (prepared statement 파라미터를 다루는 방식과 동일한 접근).
- **8.0.45+, 8.4, 9.x 통합 예정** — 2026-08-04 확인 시점 기준 통합 전.

## 대응

1. **버전 회피가 근본 대책이다.** 8.0.42를 피하고 8.0.41 또는 수정이 반영된 릴리스를 쓴다. 8.0/8.4가 LTS 라인 — [[dba/mysql-operations]]의 버전 이정표 참조.
2. 즉시 조치가 필요하면 **prepared statement를 경계 통과 후 재준비**하거나, 해당 경로를 직접 실행(비-prepared)으로 바꾼다.
3. **파티션을 미리 넉넉히 만들어도 해결되지 않는다.** 미래 파티션이 존재하느냐가 아니라 캐시된 비트맵이 과거 파티션을 고정하고 있는 게 문제다.
4. 커넥션 풀의 **최대 수명(max lifetime)을 파티션 주기보다 짧게** 두면 노출 창이 줄어든다. 다만 캐시가 세션이 아니라 열린 TABLE 인스턴스에 붙어 있어 완전한 회피인지는 확인이 필요하다.^[inferred — 미검증]
5. 영향 조사 시 **에러 로그성 저빈도 테이블을 제외하지 않는다** (위 "핵심" 항목).

## 확인 필요

- 커넥션 재수립 / `FLUSH TABLES`로 캐시가 확실히 무효화되는지 미검증.^[inferred]
- 파티션 키가 `DEFAULT CURRENT_TIMESTAMP`가 아니라 애플리케이션이 값을 명시하는 경우의 동작은 테스트하지 않음. 리포트의 원인 설명상 발생하지 않아야 한다.^[inferred]
- Aurora MySQL 3(8.0 호환) 해당 여부 미확인 — 마이너 버전 매핑 확인 필요.

## Related

- [[dba/mysql-operations|MySQL/Aurora MySQL 운영 지식]]
- [[dba/operational-queries|운영 쿼리 모음 — 진단·권한·DDL/DML]]
- [[dba/monitoring-incident-runbook|모니터링·장애 대응 런북]]
- [[dba/_hub|DBA 지식베이스]]
