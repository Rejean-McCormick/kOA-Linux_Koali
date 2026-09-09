# Deployment and Locality Topology

> **Status:** Standalone major-update specification — not yet merged into the authoritative Koali/kOA documentation.  
> **Baseline reviewed:** 2026-09-09 snapshots of Koali Spaces, Koali Control Panel, kOA Linux, LevelUpDiag, parallel design plans, and the Senior Architecture Patterns reference.  
> **Authority rule:** Until this package is explicitly adopted, existing repository documentation and contracts remain authoritative. This package defines the proposed target and the delta to close.

## Endpoint

May contain:

- Koali Spaces frontend/server;
- local hosted frontends/services where admitted;
- `UserSessionAppBroker`;
- Wayland/user-session substrate;
- native applications;
- local user data and offline-capable services;
- local proxy/transport endpoints.

## Local or edge service node

May contain shared site services, media workloads, synchronization services, or other approved local infrastructure.

## VPS / remote infrastructure

May contain Konnaxion/Orgo backends, collaboration, publication, or other remote services.

## Locality rule for native launch

Native launch is endpoint-local:

```text
browser → Koali same-origin local API → local IPC → UserSessionAppBroker → user session
```

No public network listener is required for the broker. A Koali instance that is not executing on a user endpoint reports native workspace unavailable.

## Hosted transport rule

`SurfaceRuntimeRegistry` keeps the renderer topology-agnostic, but the renderer never accepts arbitrary client-provided runtime URLs. Where practical, remote services should be exposed through controlled local transport/proxy registration rather than continually widening browser origin/CSP policy.
