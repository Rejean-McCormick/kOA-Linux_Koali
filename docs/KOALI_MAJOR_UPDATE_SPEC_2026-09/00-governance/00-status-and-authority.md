# Status, Authority, and Adoption Model

> **Status:** Standalone major-update specification — not yet merged into the authoritative Koali/kOA documentation.  
> **Baseline reviewed:** 2026-09-09 snapshots of Koali Spaces, Koali Control Panel, kOA Linux, LevelUpDiag, parallel design plans, and the Senior Architecture Patterns reference.  
> **Authority rule:** Until this package is explicitly adopted, existing repository documentation and contracts remain authoritative. This package defines the proposed target and the delta to close.

## TARGET

This bundle is a **candidate major-update specification**. It is designed to be reviewable, testable, and eventually mergeable into the existing documentation hierarchy without becoming a competing long-term source of truth.

The adoption model is:

```text
standalone proposal
      ↓ review
accepted decisions
      ↓ merge by owning repository
canonical repository docs/contracts
      ↓ generated projections
indexes / AI context / receipts
      ↓
standalone proposal archived or removed
```

## Authority hierarchy during the standalone period

1. Existing repository contracts and normative documentation.
2. Existing accepted ADRs.
3. Current source/runtime behavior where documentation explicitly delegates implementation detail.
4. This major-update package as the proposed target delta.
5. Generated indexes and convenience projections.

If this package contradicts an existing accepted authority, the contradiction is **not silently resolved**. It must become an explicit adoption decision or ADR.

## Ownership of future merged documentation

- Koali Spaces owns experience, Surface Layer, global projection runtime, Space activation semantics, appearance, and hosted-app presentation contracts.
- kOA Linux owns platform profiles, user session, native-app admission, resource/security policy, release channels, backup/restore, and endpoint topology.
- Koali Control Panel owns development orchestration UX and adapters to repository-owned commands.
- Owner repositories own their `ModuleManifest`, business UI, routes, auth, data, workflows, and any provider adapter source they author.
- LevelUpDiag owns diagnostic execution/reporting semantics only where its existing boundary grants that ownership.

## BASELINE

The reviewed repositories already emphasize source-of-truth discipline, generated projections, authority boundaries, diagnostic delegation, and no unresolved active authority. This update preserves that model.

## DELTA

The main governance change is to define the **new cross-repository boundaries before implementation**, particularly native application integration, user preferences, generic activation compilation, resilience policy, and observability context.
