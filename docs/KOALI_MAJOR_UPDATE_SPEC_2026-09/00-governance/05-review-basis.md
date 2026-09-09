# Review Basis and Evidence Boundary

> **Status:** Standalone major-update specification — not yet merged into the authoritative Koali/kOA documentation.  
> **Baseline reviewed:** 2026-09-09 snapshots of Koali Spaces, Koali Control Panel, kOA Linux, LevelUpDiag, parallel design plans, and the Senior Architecture Patterns reference.  
> **Authority rule:** Until this package is explicitly adopted, existing repository documentation and contracts remain authoritative. This package defines the proposed target and the delta to close.

This standalone specification was derived from the reviewed 2026-09-09 material set. It intentionally distinguishes **observed baseline facts** from **proposed target decisions**.

## Reviewed Koali Spaces material

The review included the Koali Spaces source/documentation snapshot containing, among other things:

- current product/architecture/Space/shell/design-system docs;
- Surface Layer specification and ACP/runtime-registration schemas;
- Home/Search/Tasks/Health/Offline/Settings surfaces;
- `ApplicationHost`, `SurfaceRenderer`, surface resolution and runtime registry;
- `KoaliThemeProvider`, `ThemeBridge`, shell providers/components;
- Search/Task provider types/registry/execution;
- control server, validation, state store, receipts;
- current maturity report and Konnaxion adaptation map.

## Reviewed Control Panel material

The review included the development-environment reference, `spaces_pilot.py`, dev-stack/orchestration/workspace/backend structure, QEMU boundary documentation, and current Konnaxion pilot behavior.

## Reviewed kOA Linux material

The review included architecture/profile/security/operations/release documentation and indexes showing:

- immutable signed image architecture;
- profile/baseline separation;
- narrow privileged broker;
- graphical runtime/session planning;
- Resource Governor;
- LSM/security control structure;
- backup/restore verification;
- release channels and provenance;
- Koali Spaces integration adapter;
- generated AI-context/navigation mechanisms.

## Reviewed architecture-pattern reference

The Senior Architecture Patterns bundle was used only for relevant trade-off checks. The target deliberately adopts Anti-Corruption Layers, bounded BFF behavior, Ports & Adapters at real boundaries, modular-monolith discipline, Bulkheads, timeout budgets, selective circuits/retries/rate limits, graceful degradation, idempotency, health/readiness separation, structured observability, immutable infrastructure, and Strangler migration. It deliberately does not add event/message/distribution patterns without concrete need.

## Evidence boundary

This bundle does not claim that every future owner runtime (especially Orgo and other deferred systems) is currently runnable merely because contracts/adapters exist. Owner/runtime availability must be requalified from the actual owner repository/environment before final ACP acceptance.
