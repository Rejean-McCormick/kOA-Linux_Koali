# UserSessionAppBroker

> **Status:** Standalone major-update specification — not yet merged into the authoritative Koali/kOA documentation.  
> **Baseline reviewed:** 2026-09-09 snapshots of Koali Spaces, Koali Control Panel, kOA Linux, LevelUpDiag, parallel design plans, and the Senior Architecture Patterns reference.  
> **Authority rule:** Until this package is explicitly adopted, existing repository documentation and contracts remain authoritative. This package defines the proposed target and the delta to close.

## Decision

The native launcher is an **unprivileged user-session boundary**, distinct from kOA's existing narrow privileged broker.

## Conceptual interface

```text
launch(appId, action, validatedTarget?)
```

Possible future explicit actions may include:

- `open`;
- `open_resource`;
- `focus_existing` where application/session semantics support it;
- `ensure_running` only where idempotence is meaningful.

Do not pretend all launch operations are idempotent.

## Validation

Before delegation:

- app exists in admission policy;
- profile/capability permits it;
- action is allowed;
- target/resource is validated against action policy;
- security/resource/data policy is available;
- graphical session is ready.

## Locality/security

- local IPC preferred (for example Unix socket under user runtime directory);
- no public network listener;
- same-origin Koali API may proxy browser requests locally;
- no shell string interface;
- no arbitrary argv passthrough;
- privileged operations, if any, go through the already-defined narrow privileged boundary rather than elevating this broker.
