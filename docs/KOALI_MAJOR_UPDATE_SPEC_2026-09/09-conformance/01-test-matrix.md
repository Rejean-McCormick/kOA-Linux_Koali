# Major Update Test Matrix

> **Status:** Standalone major-update specification — not yet merged into the authoritative Koali/kOA documentation.  
> **Baseline reviewed:** 2026-09-09 snapshots of Koali Spaces, Koali Control Panel, kOA Linux, LevelUpDiag, parallel design plans, and the Senior Architecture Patterns reference.  
> **Authority rule:** Until this package is explicitly adopted, existing repository documentation and contracts remain authoritative. This package defines the proposed target and the delta to close.

## Hosted-app isolation

- two owners share identical internal route strings without collision;
- owner A down while owner B remains healthy;
- provider timeout does not block unrelated Home/Search/Tasks data;
- malicious runtime URL/origin mismatch fails closed;
- integration package/owner removal does not break the Space;
- Streamlit/WebSocket proxy case works without special renderer branch;
- cookies/storage/service-worker isolation documented/tested;
- auth/SSO unavailable does not create credential fallback.

## Projection runtime

- timeout budget exhaustion;
- per-provider and per-owner bulkhead saturation;
- load shedding/rejection behavior;
- circuit open/half-open/close for remote provider;
- bounded background retry with jitter;
- valid empty result distinguishable from provider error;
- stale cache expires at `maxStale`;
- cached data forbidden when provider policy disallows it.

## Appearance

- light/dark/system resolution;
- system theme change handling;
- accent resolution;
- density/surface-style token changes without JSX divergence;
- Space default versus user override;
- user preference change does not alter activation receipt/digest;
- module context accent cannot bypass Space policy.

## Native Workspace

- unknown app id denied;
- unauthorized profile denied;
- arbitrary argv impossible;
- invalid open-resource target denied;
- launch storm rate-limited/load-shed;
- app crash isolated;
- Firefox resource pressure leaves Koali responsive;
- MIME/open-with cross-app scenarios;
- offline native app behavior;
- binary rollback with compatible/incompatible profile;
- broker unavailable reports native workspace unavailable without breaking hosted apps.

## Development

- atomic-save interruption;
- recovery after process crash;
- external file change detection;
- UTF-8/BOM and EOL preservation;
- large paste remains responsive;
- session restoration;
- secret context exclusion;
- SmartDump/File Puller parity with standalone tools.
