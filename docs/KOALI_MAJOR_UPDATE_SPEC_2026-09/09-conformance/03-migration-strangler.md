# Migration and Strangler Rules

> **Status:** Standalone major-update specification — not yet merged into the authoritative Koali/kOA documentation.  
> **Baseline reviewed:** 2026-09-09 snapshots of Koali Spaces, Koali Control Panel, kOA Linux, LevelUpDiag, parallel design plans, and the Senior Architecture Patterns reference.  
> **Authority rule:** Until this package is explicitly adopted, existing repository documentation and contracts remain authoritative. This package defines the proposed target and the delta to close.

The update targets the final architecture directly, but existing specialized paths can be migrated safely through **temporary compatibility boundaries**.

## Konnaxion pilot migration

```text
existing KoaliSpacesPilotState / _konnaxion_manifest
            │
            ├── existing path retained temporarily
            │
            └── generic activation/compiler path introduced
                        ↓
               parity + stronger conformance
                        ↓
                default switches generic
                        ↓
                legacy path deleted
```

## Rules for temporary paths

Every compatibility path has:

- explicit owner;
- reason;
- tests proving parity;
- deletion condition;
- no new functionality added only to the legacy path.

## Schema evolution

Prefer additive compatibility for existing valid Space/theme/surface artifacts. Deprecated fields can feed defaults during migration, but once a new authority exists they must not continue to override it silently.

## No zombie migrations

A compatibility path that has met its deletion condition is considered architectural debt and must be removed before the corresponding work item is closed.
