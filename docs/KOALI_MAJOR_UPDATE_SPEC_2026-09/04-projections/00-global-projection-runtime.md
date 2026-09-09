# GlobalProjectionRuntime

> **Status:** Standalone major-update specification — not yet merged into the authoritative Koali/kOA documentation.  
> **Baseline reviewed:** 2026-09-09 snapshots of Koali Spaces, Koali Control Panel, kOA Linux, LevelUpDiag, parallel design plans, and the Senior Architecture Patterns reference.  
> **Authority rule:** Until this package is explicitly adopted, existing repository documentation and contracts remain authoritative. This package defines the proposed target and the delta to close.

`GlobalProjectionRuntime` is an **internal Koali server capability**, not a separately deployed platform.

It behaves like a bounded Backend for Frontend for Koali's global surfaces.

## Responsibilities

- execute registered providers;
- enforce capability/offline eligibility;
- bound execution time/concurrency;
- sanitize and validate owner outputs;
- enforce owner route ownership;
- aggregate presentation models;
- expose provider freshness/failure metadata;
- optionally use bounded cache/stale fallback according to provider policy.

## Non-responsibilities

It does not:

- mutate owner state;
- authorize owner actions;
- crawl owner databases or private application profiles;
- import arbitrary provider code from manifests;
- become a universal public API for unrelated clients.

## Public Koali endpoints

Keep the API small and presentation-specific:

- `/api/global/search`;
- `/api/global/tasks`;
- `/api/global/overview` for Home/topbar summary projections.
