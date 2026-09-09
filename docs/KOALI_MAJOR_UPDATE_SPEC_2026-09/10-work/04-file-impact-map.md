# Repository and File Impact Map

> **Status:** Standalone major-update specification — not yet merged into the authoritative Koali/kOA documentation.  
> **Baseline reviewed:** 2026-09-09 snapshots of Koali Spaces, Koali Control Panel, kOA Linux, LevelUpDiag, parallel design plans, and the Senior Architecture Patterns reference.  
> **Authority rule:** Until this package is explicitly adopted, existing repository documentation and contracts remain authoritative. This package defines the proposed target and the delta to close.

This map identifies likely merge targets after the standalone spec is accepted. It is not a mandate to edit every file listed.

## Koali Spaces documentation

Likely affected areas:

- `docs/00-governance/*` — authority/invariants/change control;
- `docs/01-product/*` — Space-as-front-door product definition;
- `docs/02-architecture/*` — authority/state/data flow/topology;
- `docs/03-space-model/*` — appearance authority and widget projection binding;
- `docs/04-shell/*` — adaptive sidebar/topbar/launcher/state restoration;
- `docs/05-design-system/*` — light/dark/system, accents, surface styles, density;
- `docs/06-surface-layer/*` — generic activation ownership, ACP/runtime boundary, resilience/telemetry;
- `docs/07-global-surfaces/*` — Home/Search/Tasks/provider runtime;
- `docs/08-runtime/*` — activation/compiler/control server;
- `docs/09-security/*` — provider/native projection boundary;
- `docs/10-offline/*` — stale/degraded semantics;
- `docs/11-integrations/*` — hosted conformance applications;
- `docs/12-operations/*` — observability/deployment;
- `docs/13-development/*` — generic add-app workflow;
- `docs/14-verification/*` — new gates;
- `docs/15-reference/*` — contract/index updates.

## Koali Spaces source/contracts

Likely targets:

- `src/providers/KoaliThemeProvider.tsx`;
- `src/providers/ThemeBridge.tsx`;
- `src/providers/ShellProvider.tsx`;
- `src/components/shell/GlobalShell.tsx`;
- `src/components/shell/ActiveModuleSidebar.tsx`;
- `src/components/shell/SharedTopBar.tsx`;
- `src/components/shell/ProductSurfaceSelector.tsx`;
- `src/components/global/HomeOverview.tsx`;
- `src/components/global/SettingsOverview.tsx`;
- `src/components/global/SearchSurface.tsx`;
- `src/components/global/TasksSurface.tsx`;
- `src/lib/global-providers/*`;
- `src/lib/surfaces/*` only where generic contracts require it, never owner branching;
- `server/validation.mjs`;
- `server/control-server.mjs`;
- `server/state-store.mjs` as required for new non-user activation semantics only;
- `contracts/koa/*` and `contracts/koali/*` for compatible contract evolution;
- new local native projection API/server adapter files.

## Koali Control Panel

Likely targets:

- `koali_control/spaces_pilot.py` — strangler migration then deletion/reduction;
- `koali_control/devstack.py` — generic invocation rather than Konnaxion-specific composition;
- product/workspace config only as required for canonical owner commands;
- `KOALI_DEVELOPMENT_ENVIRONMENT_REFERENCE.md`;
- new DevPad launch/IPC adapter if accepted.

## kOA Linux

Likely targets:

- architecture/security/operations/profile/release documentation;
- new ADRs for Native Workspace boundary and user-session broker;
- profile/overlay contracts and implementation settings;
- `host/sessions/koa-session-launcher.py` or adjacent user-session integration;
- a new non-privileged user-session application broker component/boundary;
- Native Application Admission Policy contracts;
- Resource Governor profile mappings;
- LSM/security policy mappings;
- backup/restore policy integration;
- release manifest/image package inputs;
- `integrations/koa-spaces/adapter/*` for new platform projections/control operations only where ownership fits;
- generated AI-context/navigation projections after canonical docs change.

## LevelUpDiag

Only add checks where LevelUpDiag's diagnostic boundary is appropriate. It should consume public repository validators/evidence rather than duplicate semantic checks already owned by Koali or kOA Linux.

## Owner repositories

- Konnaxion: canonical Koali manifest, ACP declarations/evidence, provider adapters/endpoints as needed;
- Médiathèque: ACP/runtime qualification and optional projections;
- Orgo: official runtime qualification and Task/Resume/Status adapters;
- future owners: follow the same generic contract path.
