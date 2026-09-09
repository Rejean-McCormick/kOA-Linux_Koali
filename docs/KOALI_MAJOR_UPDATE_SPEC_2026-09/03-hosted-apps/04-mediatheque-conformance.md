# Médiathèque — Heterogeneous Hosted Conformance Application

> **Status:** Standalone major-update specification — not yet merged into the authoritative Koali/kOA documentation.  
> **Baseline reviewed:** 2026-09-09 snapshots of Koali Spaces, Koali Control Panel, kOA Linux, LevelUpDiag, parallel design plans, and the Senior Architecture Patterns reference.  
> **Authority rule:** Until this package is explicitly adopted, existing repository documentation and contracts remain authoritative. This package defines the proposed target and the delta to close.

Médiathèque is retained as the heterogeneous-stack proof so generic hosting is not accidentally optimized only for Next-based applications.

## TARGET qualification

Validate:

- Streamlit/runtime startup;
- WebSocket behavior;
- XSRF/CORS/frame headers;
- base-path/proxy behavior;
- cookies/storage;
- upload/download flows;
- multipage navigation;
- allowed origins and browser policies;
- offline/degraded semantics;
- Status and optional Search projection without duplicating its internal media UI.

## Architectural gate

No Médiathèque-specific branch in `ApplicationHost` or `SurfaceRenderer` is permitted. If a new generic transport capability is required, it must be expressed through the shared runtime/transport contracts and tested against other fixtures.
