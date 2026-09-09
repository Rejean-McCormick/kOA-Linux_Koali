# Health, Readiness, and User Status

> **Status:** Standalone major-update specification — not yet merged into the authoritative Koali/kOA documentation.  
> **Baseline reviewed:** 2026-09-09 snapshots of Koali Spaces, Koali Control Panel, kOA Linux, LevelUpDiag, parallel design plans, and the Senior Architecture Patterns reference.  
> **Authority rule:** Until this package is explicitly adopted, existing repository documentation and contracts remain authoritative. This package defines the proposed target and the delta to close.

Three concepts remain separate.

## Liveness

Should the process continue running, or is it irrecoverably broken?

## Readiness

Can the component accept its declared work now?

## User status projection

What should Koali communicate to the user about availability/degradation?

A healthy process can still be unready for a specific dependency. A ready process does not imply a user is authorized. A user-facing `StatusProvider` is not a security decision.

Where services expose explicit endpoints, `/live` and `/ready` semantics should be documented independently. Existing owner health contracts can remain if their semantics are already clear; the update does not require cosmetic endpoint renaming.
