# Surface State and Deep Links

> **Status:** Standalone major-update specification — not yet merged into the authoritative Koali/kOA documentation.  
> **Baseline reviewed:** 2026-09-09 snapshots of Koali Spaces, Koali Control Panel, kOA Linux, LevelUpDiag, parallel design plans, and the Senior Architecture Patterns reference.  
> **Authority rule:** Until this package is explicitly adopted, existing repository documentation and contracts remain authoritative. This package defines the proposed target and the delta to close.

The current local React selection of a product surface is insufficient for a final system where refresh, browser navigation, bookmark, and restart should restore presentation intent.

## TARGET

- selected surface is encoded in Koali-owned navigation state;
- owner path remains owner-owned;
- Koali query/route metadata uses a reserved namespace;
- invalid/unavailable surface selection falls back deterministically;
- immersive/framed state restoration follows declared policy;
- state does not grant capability or bypass the runtime registry.

Conceptual example:

```text
/apps/orgo/cases/123?ks_surface=my_work
```

The concrete parameter name is a contract decision, not an implementation convenience.

## DELTA

Replace per-session-only `surfaceByModule` behavior with addressable/restorable Koali presentation state while preserving owner deep links.
