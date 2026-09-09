# Terminology

> **Status:** Standalone major-update specification — not yet merged into the authoritative Koali/kOA documentation.  
> **Baseline reviewed:** 2026-09-09 snapshots of Koali Spaces, Koali Control Panel, kOA Linux, LevelUpDiag, parallel design plans, and the Senior Architecture Patterns reference.  
> **Authority rule:** Until this package is explicitly adopted, existing repository documentation and contracts remain authoritative. This package defines the proposed target and the delta to close.

- **Space** — the active Koali composition and capability projection selected by `SpaceDefinition` and activation state.
- **Module** — a Koali-presented owner contribution with a `ModuleManifest`; not synonymous with a native desktop application.
- **Hosted application** — an owner application presented through Koali's existing surface hosting model.
- **Native application** — a user-session desktop application launched by kOA platform facilities; not a Koali surface.
- **Owner** — subsystem/application retaining its business data, routes, auth, workflows, and authoritative decisions.
- **Projection** — bounded, non-authoritative data shaped for Koali presentation.
- **GlobalProjectionRuntime** — internal Koali server runtime executing Search/Task/Resume/Status/Counter providers.
- **ACP** — `ApplicationConformanceProfile`, the admission/conformance artifact combining owner declarations with qualification evidence.
- **RuntimeRegistration** — environment/control-owned description of current runtime location/transport/health binding.
- **SpaceActivationCompiler** — Koali-owned validation/composition logic that turns selected valid inputs into an activation-ready Space payload/receipt.
- **Integration package** — optional packaging convention that groups references/artifacts; never a fourth normative contract.
- **Native Application Admission Policy** — kOA policy referring to existing desktop metadata and adding capability/resource/security/data constraints.
- **UserSessionAppBroker** — unprivileged, endpoint-local service or boundary that validates allowed application actions and delegates launch into the active user graphical session.
- **SpaceAppearancePolicy** — Space-owned defaults/allowed presentation choices.
- **UserPresentationPreferences** — user/local presentation selections independent from activation authority.
- **EffectiveAppearance** — resolved result of base theme, Space policy, user preferences, and optional owner context accent.
- **Conformance application** — representative real application kept as a permanent proof of a generic integration class.
