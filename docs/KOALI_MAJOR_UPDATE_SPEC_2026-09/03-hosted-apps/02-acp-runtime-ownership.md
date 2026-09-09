# ACP, Manifest, and Runtime Ownership

> **Status:** Standalone major-update specification — not yet merged into the authoritative Koali/kOA documentation.  
> **Baseline reviewed:** 2026-09-09 snapshots of Koali Spaces, Koali Control Panel, kOA Linux, LevelUpDiag, parallel design plans, and the Senior Architecture Patterns reference.  
> **Authority rule:** Until this package is explicitly adopted, existing repository documentation and contracts remain authoritative. This package defines the proposed target and the delta to close.

## ModuleManifest

Owner-authored. It expresses what Koali may present: identity, routes, navigation, widgets, surface profiles, and declared presentation metadata.

## ACP

A conformance artifact, not merely an owner self-assertion. It binds owner declarations to qualification evidence for:

- ownership boundary;
- runtime expectations;
- router/deep links;
- auth/SSO behavior;
- browser/frame behavior;
- storage/cookies/service worker;
- offline/degraded behavior;
- lifecycle;
- health/readiness;
- downloads/popups;
- security evidence.

## RuntimeRegistration

Runtime/control authority. It describes the current environment binding, not the owner's abstract product identity.

An owner may document runtime requirements but does not become authority for whether a specific environment target is currently available or admitted.

## Receipt

Qualification/activation receipts record what was actually validated/admitted. Receipts are evidence, not business authority.
