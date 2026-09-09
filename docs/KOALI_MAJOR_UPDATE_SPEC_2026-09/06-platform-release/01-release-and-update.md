# Release and Update Authority

> **Status:** Standalone major-update specification — not yet merged into the authoritative Koali/kOA documentation.  
> **Baseline reviewed:** 2026-09-09 snapshots of Koali Spaces, Koali Control Panel, kOA Linux, LevelUpDiag, parallel design plans, and the Senior Architecture Patterns reference.  
> **Authority rule:** Until this package is explicitly adopted, existing repository documentation and contracts remain authoritative. This package defines the proposed target and the delta to close.

## Existing channels remain the default

Use the existing kOA release authorities unless evidence proves a new one is necessary.

### OS image

Suitable for the desktop substrate and managed native application binaries such as Firefox, VLC, LibreOffice, and Thunderbird in the current target model.

### Governance policy

Suitable for admission, security, resource, and related policy.

### Service bundle

Suitable for local/remote services already belonging to that channel.

### Kristal artifacts

Unchanged.

## Security-update SLO

Browser/mail security fixes can be time-sensitive. The update documentation must define an operational maximum latency for critical native-application security updates. If the OS-image cadence cannot satisfy that SLO in practice, a future ADR may justify a dedicated signed application channel. Do not create it preemptively.

## Deployment safety

- endpoint image activation follows signed immutable-image verification/rollback semantics;
- remote service deployments may use blue-green or canary only where their operational topology benefits from it;
- no Kubernetes requirement is introduced merely to obtain deployment terminology.
