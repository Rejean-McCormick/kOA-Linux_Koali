# Backup, Restore, and Rollback

> **Status:** Standalone major-update specification — not yet merged into the authoritative Koali/kOA documentation.  
> **Baseline reviewed:** 2026-09-09 snapshots of Koali Spaces, Koali Control Panel, kOA Linux, LevelUpDiag, parallel design plans, and the Senior Architecture Patterns reference.  
> **Authority rule:** Until this package is explicitly adopted, existing repository documentation and contracts remain authoritative. This package defines the proposed target and the delta to close.

Rollback is complete only when application profile compatibility is considered alongside binary rollback.

## Target flow

```text
new app version
  ↓
evaluate profile compatibility policy
  ↓
checkpoint through existing backup system if required
  ↓
launch / mark compatibility evidence
```

Rollback:

```text
binary/image rollback
  +
profile compatibility check
  ↓
compatible → continue
incompatible → restore matching checkpoint through existing restore machinery
```

## Invariants

- user documents are not treated as disposable app cache;
- cache is not restored unless policy requires it;
- credentials/secrets remain under the correct security authority;
- restore verification produces evidence;
- no native-app-specific backup engine is created unless the existing kOA restore architecture proves insufficient.
