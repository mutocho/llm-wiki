---
title: >-
  볼트 거버넌스 결정 — career 회사 라우팅·에이전트 규칙 단일화·브랜치 금지
category: synthesis
tags: [wiki-ops, governance, career]
sources:
  - conversation:2026-08-06
created: 2026-08-06T00:00:00Z
updated: 2026-08-06T00:00:00Z
summary: >-
  career는 회사 단위 폴더로 적재(현재 kakaogames, 불분명하면 common), 규칙은 AGENTS.md 단일 소스 + CLAUDE.md @import, 이 저장소는 브랜치 없이 main 직접 커밋.
provenance:
  extracted: 0.8
  inferred: 0.2
  ambiguous: 0.0
base_confidence: 0.75
lifecycle: draft
lifecycle_changed: 2026-08-06
---

# 볼트 거버넌스 결정 — career 회사 라우팅·에이전트 규칙 단일화·브랜치 금지

## Context

볼트를 여러 장비·여러 에이전트(Claude Code, Codex)에서 쓰고, 이직 후에도 career 기록을 이어가려면 적재 구조와 규칙 파일의 단일 소스가 필요했다.

## Decision

1. **career는 회사 단위 폴더로 적재한다** — `career/kakaogames/`(현재 회사), 회사가 불분명하거나 회사 무관한 기록은 `career/common/`. 회사명은 입력받지 않고 자동 판단하며, 이직 시 ROUTING.md의 현재 회사 문단만 갱신하고 새 폴더를 추가한다.
2. **에이전트 규칙은 AGENTS.md가 단일 소스다** — Codex는 AGENTS.md를 직접 읽고, Claude Code는 CLAUDE.md의 `@AGENTS.md` import 한 줄로 같은 내용을 로드한다. 규칙 중복을 두지 않는다.
3. **이 저장소는 브랜치를 생성하지 않는다** — 모든 커밋은 main 직접 수행. sync.sh auto-sync가 main에 커밋하므로 브랜치를 만들면 auto-sync 커밋과 갈라져 관리 비용만 생긴다. ^[inferred]

## Reasoning

- career를 회사별로 나누면 이직 시 기존 기록을 건드리지 않고 폴더만 추가하면 되고, `dba/`(회사 무관 기술 지식)와의 역할 분리가 유지된다.
- 규칙을 CLAUDE.md와 AGENTS.md 양쪽에 쓰면 드리프트가 생긴다. AGENTS.md는 다수 에이전트가 따르는 공통 표준이므로 이쪽을 원본으로 삼는다.

## Implications

- 새 career 페이지를 만들 때 `career/` 루트에 직접 두지 않는다 — 반드시 회사 폴더 하위.
- 커밋 워크플로우 스킬(/commit-push-pr 등)이 브랜치를 만들려 해도 main 직접 커밋으로 대체한다.
- `obsidian-wiki setup`은 장비의 모든 에이전트(~/.claude/skills, ~/.codex/skills)에 스킬을 심볼릭 링크로 설치하므로, 에이전트를 나중에 추가하면 setup을 재실행한다.

## Related

- [[career/_hub|커리어 관리]]
- [[references/obsidian-wiki-tooling-gotchas|obsidian-wiki 도구 동작 함정]]
