# Orgo — Provider-Rich Hosted Conformance Application

> **Status:** Standalone major-update specification — not yet merged into the authoritative Koali/kOA documentation.  
> **Baseline reviewed:** 2026-09-09 snapshots of Koali Spaces, Koali Control Panel, kOA Linux, LevelUpDiag, parallel design plans, and the Senior Architecture Patterns reference.  
> **Authority rule:** Until this package is explicitly adopted, existing repository documentation and contracts remain authoritative. This package defines the proposed target and the delta to close.

Orgo is the permanent proof that Koali can aggregate useful global work without stealing workflow ownership.

## TARGET

- official Orgo runtime requalified before final ACP acceptance;
- owner surface onboarded generically;
- Orgo becomes a real `TaskProvider` source;
- Resume and Status are added when meaningful;
- Counter is added only when it represents a stable semantic not already cheaply derived from Tasks;
- all mutations route back to Orgo;
- no Orgo workflow/case/task engine logic enters Koali.

## Conformance gate

The Koali Tasks surface must remain usable when Orgo is degraded, and Orgo removal must not invalidate unrelated Search/Home/other modules.
