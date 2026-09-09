# Baseline-to-Target Gap Matrix

> **Status:** Standalone major-update specification — not yet merged into the authoritative Koali/kOA documentation.  
> **Baseline reviewed:** 2026-09-09 snapshots of Koali Spaces, Koali Control Panel, kOA Linux, LevelUpDiag, parallel design plans, and the Senior Architecture Patterns reference.  
> **Authority rule:** Until this package is explicitly adopted, existing repository documentation and contracts remain authoritative. This package defines the proposed target and the delta to close.

This matrix is the compact view of **what already exists versus what the major update still has to deliver**.

| Area | BASELINE observed | TARGET | Main delta |
|---|---|---|---|
| Surface Layer | Generic host, framed/immersive, runtime registry, URL/origin policy, tests | Stable generic hosted-app foundation | Preserve; change only for proven generic contract need |
| Space activation | Control server/state/receipts exist; pilot composition is specialized | Koali-owned generic `SpaceActivationCompiler` | Generic compiler + idempotency + diagnostics; Control Panel delegates |
| Konnaxion | Development pilot navigable; Control Panel owns specialized manifest/runtime projection | Owner-owned manifest + real ACP + generic path | Migrate then delete specialized path |
| Médiathèque | Real heterogeneous app/runtime available in reviewed plan set | Generic heterogeneous hosted proof | ACP + WebSocket/XSRF/base-path/download/storage qualification |
| Orgo | Integration assets/contracts known; runtime UI not fully requalified in reviewed snapshot | Provider-rich hosted proof | Requalify runtime, ACP, Tasks/Resume/Status |
| Home | Mostly module/system-state presentation | Continue / Attention / Applications / Space state | Projection-driven Home, no hardcoded owner cards |
| Search | Surface/API/provider mechanism exists; owner registry effectively empty | Federated owner Search | Real provider adapters + resilience/freshness |
| Tasks | Surface/API/provider mechanism exists; owner registry effectively empty | Aggregated owner work queue | Orgo provider, no workflow mutation in Koali |
| Resume | Documented target, not end-to-end | Resumable owner contexts | Contract/runtime/API/UI |
| Status | Documented/topbar concept, not end-to-end | User-facing bounded status | Projection runtime + topbar/Home binding |
| Counter | Contract concept incomplete in rendering | Stable semantic counts only | Separate projection binding from activation; avoid redundant counts |
| Provider isolation | Timeouts/allSettled-style isolation | Senior-grade resilience | Bulkheads, deadlines, selective circuits/backoff/rate limits |
| Appearance | Theme infrastructure/tokens exist; light/default behavior dominates; Settings mostly read-only | System/light/dark + accent + density + surface style | Separate Space policy/user prefs, semantic token migration, controls/persistence |
| Shell | Module selector/sidebar/topbar exist | Adaptive minimal chrome | Hide empty sidebar, conditional sections, finish dynamic badges/widgets |
| Surface state | Selected surface largely local React state | Addressable/restorable | Reserved Koali URL state |
| Native apps | kOA graphical/session/security/resource foundations exist, no Koali-native workspace integration | Native Workspace under kOA | Admission policy, local broker, Koali projection, substrate qualification |
| Desktop metadata | Standard Linux mechanisms available conceptually | Freedesktop remains authority | Reference `.desktop`/MIME; do not duplicate |
| Native security/resources | kOA control frameworks exist | Per-app class/envelope/policy | Mapping + conformance/stress tests |
| Native rollback | kOA backup/restore exists | Profile-aware app rollback | Native data policy feeding existing backup/restore |
| Release | Immutable image + four channels/provenance exist | Managed native binaries under existing authority | Package inclusion + security-update SLO; no fifth channel unless proven |
| Observability | Health/readiness/telemetry pieces exist | Correlated structured observability | common fields, traces on network boundaries, golden-signal metrics |
| Control Panel | Strong dev orchestrator + Konnaxion-specific Space pilot | Generic delegating dev control | remove semantic duplication; invoke Koali compiler/owner commands |
| DevPad | Design/workflow proposal only | Optional reliable editor/context tool | Implement without becoming build/runtime authority |
| VPS/distributed | Local dev pilot strongest; network staging not final proof | Qualified distributed Space | TLS/proxy/CSP/cookies/WebSocket/circuits/rollback/partial outage |

## Architectural optimization test

A target change is suspect if it adds a new source of truth, a new general-purpose framework, a new network boundary, or a new long-lived process without eliminating a concrete failure mode or authority ambiguity.
