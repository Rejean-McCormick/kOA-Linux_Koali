# Koali Experience Target

> **Status:** Standalone major-update specification — not yet merged into the authoritative Koali/kOA documentation.  
> **Baseline reviewed:** 2026-09-09 snapshots of Koali Spaces, Koali Control Panel, kOA Linux, LevelUpDiag, parallel design plans, and the Senior Architecture Patterns reference.  
> **Authority rule:** Until this package is explicitly adopted, existing repository documentation and contracts remain authoritative. This package defines the proposed target and the delta to close.

Koali should feel like the **front door of the Space**, not a diagnostic shell surrounding another application.

The target user flow is:

```text
boot/open Koali
  ↓
understand active Space immediately
  ↓
see what can be continued
  ↓
see what needs attention
  ↓
open hosted or native applications
  ↓
return to Koali without losing context
  ↓
use global Search/Tasks when owners expose them
  ↓
remain productive during partial failure/offline conditions
```

The product should remain visually calm and structurally minimal. Technical detail belongs in Health/diagnostics, not Home.

## BASELINE

Home currently behaves mostly like an admitted-module/system-state view. Search and Tasks have functional shells but limited value without owner providers. Settings is largely informational. Konnaxion is hosted but Koali does not yet provide a mature multi-owner composition.

## TARGET

Koali becomes useful **before entering an owner app** while avoiding ownership of owner workflows or KPI dashboards.
