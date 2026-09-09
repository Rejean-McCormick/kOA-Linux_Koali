# Projection Cache and Staleness

> **Status:** Standalone major-update specification — not yet merged into the authoritative Koali/kOA documentation.  
> **Baseline reviewed:** 2026-09-09 snapshots of Koali Spaces, Koali Control Panel, kOA Linux, LevelUpDiag, parallel design plans, and the Senior Architecture Patterns reference.  
> **Authority rule:** Until this package is explicitly adopted, existing repository documentation and contracts remain authoritative. This package defines the proposed target and the delta to close.

Provider staleness becomes real runtime semantics rather than an unused type field.

## Cache-aside behavior

```text
provider succeeds
  → sanitize/validate
  → update allowed cache
  → return ready

provider unavailable
  → cache allowed and age <= staleAfter/maxStale policy
      → return stale
  → otherwise
      → unavailable/error
```

## Constraints

- provider/owner policy decides whether caching is permitted;
- sensitive data must not be persisted merely for convenience;
- cache does not become owner authority;
- stale state is included in operational metadata;
- `maxStale` prevents indefinite zombie data;
- user-visible labels should remain simple but not misleading.
