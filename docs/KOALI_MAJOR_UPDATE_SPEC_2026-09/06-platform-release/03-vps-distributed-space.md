# Distributed Space and VPS

> **Status:** Standalone major-update specification — not yet merged into the authoritative Koali/kOA documentation.  
> **Baseline reviewed:** 2026-09-09 snapshots of Koali Spaces, Koali Control Panel, kOA Linux, LevelUpDiag, parallel design plans, and the Senior Architecture Patterns reference.  
> **Authority rule:** Until this package is explicitly adopted, existing repository documentation and contracts remain authoritative. This package defines the proposed target and the delta to close.

The VPS is part of the final topology, not a milestone that proves product completeness.

## Remote qualification dimensions

- TLS;
- reverse proxy;
- WebSocket where used;
- cookie `SameSite`/`Secure` behavior;
- CSP `frame-src` / `frame-ancestors`;
- origins and redirects;
- authentication/SSO per owner decision;
- cache policy;
- provider deadlines/circuit states;
- observability correlation;
- backup/restore and rollback;
- partial remote outage behavior.

## Preferred browser boundary

Where an owner stack benefits from same-origin behavior, prefer a controlled registered proxy/transport over arbitrary runtime URLs and ever-broader CSP.

## Native workspace

Remote Koali/VPS instances do not implicitly launch applications on an endpoint. A future remote endpoint protocol, if ever required, is a separate security/authority decision.
