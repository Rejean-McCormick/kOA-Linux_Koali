# Hosted Application Integration Model

> **Status:** Standalone major-update specification — not yet merged into the authoritative Koali/kOA documentation.  
> **Baseline reviewed:** 2026-09-09 snapshots of Koali Spaces, Koali Control Panel, kOA Linux, LevelUpDiag, parallel design plans, and the Senior Architecture Patterns reference.  
> **Authority rule:** Until this package is explicitly adopted, existing repository documentation and contracts remain authoritative. This package defines the proposed target and the delta to close.

Hosted onboarding composes existing authorities rather than inventing a plugin framework.

## Three normative integration authorities

1. `ModuleManifest` — presentation contribution owned by the application owner.
2. `ApplicationConformanceProfile` — admission/conformance artifact with evidence.
3. `RuntimeRegistration` / `SurfaceRuntimeRegistry` — current environment/runtime binding owned by runtime/control authority.

`SpaceDefinition` selects/composes admitted contributions. An optional Integration Package may group artifacts but is not a fourth source of truth.

## Generic onboarding goal

A conforming hosted app must be addable without modifying:

- `ApplicationHost`;
- `SurfaceRenderer`;
- global Koali routes;
- product-specific functions in Control Panel.

## Owner boundary

The owner retains:

- router;
- internal navigation;
- business pages;
- API/auth logic;
- workflows;
- data models;
- domain validation.

Koali receives only presentation contracts and explicit projections.
