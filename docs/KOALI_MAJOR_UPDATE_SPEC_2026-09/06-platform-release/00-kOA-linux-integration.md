# kOA Linux Integration

> **Status:** Standalone major-update specification — not yet merged into the authoritative Koali/kOA documentation.  
> **Baseline reviewed:** 2026-09-09 snapshots of Koali Spaces, Koali Control Panel, kOA Linux, LevelUpDiag, parallel design plans, and the Senior Architecture Patterns reference.  
> **Authority rule:** Until this package is explicitly adopted, existing repository documentation and contracts remain authoritative. This package defines the proposed target and the delta to close.

kOA Linux remains the platform authority and should absorb the Native Workspace through existing profile, session, resource, security, and release mechanisms.

## Required platform additions

- explicit native-workspace capability, e.g. canonical `user.native_workspace` naming;
- profile/overlay mapping specifying where it is permitted;
- native admission policy contract;
- user-session broker/session integration;
- micro-desktop substrate contract and conformance checks;
- native application data policy contract;
- observability/security mappings;
- conformance documentation and generated AI/navigation projections.

## Reuse requirements

Reuse rather than duplicate:

- graphical runtime/session plan;
- profile and overlay system;
- narrow privileged broker;
- Resource Governor;
- LSM/security control architecture;
- backup/restore verification;
- release manifests/provenance;
- existing four release channels.

## Profile principle

Package presence never implies admission. `appliance-shell` and other restrictive profiles remain closed unless an explicit capability/policy grants native workspace behavior.
