# Native Workspace Boundary

> **Status:** Standalone major-update specification — not yet merged into the authoritative Koali/kOA documentation.  
> **Baseline reviewed:** 2026-09-09 snapshots of Koali Spaces, Koali Control Panel, kOA Linux, LevelUpDiag, parallel design plans, and the Senior Architecture Patterns reference.  
> **Authority rule:** Until this package is explicitly adopted, existing repository documentation and contracts remain authoritative. This package defines the proposed target and the delta to close.

Native Workspace is a **kOA Linux endpoint capability surfaced through Koali**, not an extension of the Koali Surface Layer.

## Hard rules

- no `native_application` `SurfaceKind`;
- no native app as Koali `active_module_id`;
- no browser-to-shell execution;
- no arbitrary executable/argv from frontend;
- no remote native launch by implication;
- no second desktop metadata registry.

## Experience integration

Koali may show native apps in Home's Applications region and show their availability/status. Opening a native app leaves Koali's module state intact.

## Platform integration

The actual launch path belongs to the local user session and kOA policy/profile system.

```text
Koali local API
  ↓
local authenticated IPC
  ↓
UserSessionAppBroker
  ↓
policy/admission checks
  ↓
user graphical session
```
