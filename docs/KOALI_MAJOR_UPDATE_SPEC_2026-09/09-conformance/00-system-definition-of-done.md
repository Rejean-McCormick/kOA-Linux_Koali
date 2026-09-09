# System Definition of Done

> **Status:** Standalone major-update specification — not yet merged into the authoritative Koali/kOA documentation.  
> **Baseline reviewed:** 2026-09-09 snapshots of Koali Spaces, Koali Control Panel, kOA Linux, LevelUpDiag, parallel design plans, and the Senior Architecture Patterns reference.  
> **Authority rule:** Until this package is explicitly adopted, existing repository documentation and contracts remain authoritative. This package defines the proposed target and the delta to close.

The major update is complete only when all of the following are simultaneously true.

## Experience

- Koali opens into a useful Home rather than a diagnostic module list.
- appearance mode/accent/density/surface style resolve correctly and persist under user preference authority;
- empty shell regions disappear;
- hosted/native applications are presented coherently without conflating their authority models;
- Search/Tasks/Resume/Status work when owners expose them and degrade when they do not.

## Hosted integration

- a conforming new hosted app requires no patch to `ApplicationHost`, `SurfaceRenderer`, or global routes;
- Konnaxion, Médiathèque, and Orgo pass their representative conformance suites;
- owner removal is clean;
- ACP/evidence/runtime ownership is explicit;
- generic activation is Koali-owned, not Control Panel-owned.

## Native Workspace

- native apps are discovered from desktop metadata + kOA admission policy;
- launch is endpoint-local, unprivileged, policy-checked, and cannot execute arbitrary argv;
- VLC, Firefox, LibreOffice, Thunderbird, and Files conformance scenarios pass;
- native resource exhaustion cannot collapse Koali;
- offline semantics are explicit;
- profile rollback compatibility is tested through existing backup/restore machinery.

## Resilience/observability

- remote calls have timeout budgets;
- fan-out has bulkheads;
- retries/circuits/rate limits exist only where justified and are tested;
- degraded states are operationally visible;
- critical paths have structured logs, correlation, and actionable metrics.

## Development

- DevPad can disappear without affecting canonical build/release;
- Control Panel remains an orchestrator/delegator;
- development workflow can produce targeted/full AI context without silently exporting secrets.

## Marginal cost

- fourth hosted app materially cheaper than second;
- sixth compatible native app mostly policy + conformance, not new launcher code.
