# Four Authority Planes

> **Status:** Standalone major-update specification — not yet merged into the authoritative Koali/kOA documentation.  
> **Baseline reviewed:** 2026-09-09 snapshots of Koali Spaces, Koali Control Panel, kOA Linux, LevelUpDiag, parallel design plans, and the Senior Architecture Patterns reference.  
> **Authority rule:** Until this package is explicitly adopted, existing repository documentation and contracts remain authoritative. This package defines the proposed target and the delta to close.

## 1. Experience Plane — Koali Spaces

Owns:

- global shell and routes;
- Home/Search/Tasks/Health/Offline/Settings presentation;
- hosted surface resolution/presentation;
- GlobalProjectionRuntime;
- appearance policy resolution and user presentation preferences;
- local native-application projection API/view model;
- Space activation compilation and presentation receipts.

Does not own:

- owner business authorization;
- owner workflow mutation;
- arbitrary OS execution;
- native app profile contents;
- release image assembly.

## 2. Application Plane

### Hosted owners

Own their UI, routes, APIs, authentication, data, workflows, domain validation, and manifest contribution.

### Native applications

Own their own desktop behavior and profile formats. kOA controls whether/how they are admitted and launched on an endpoint.

## 3. Platform Plane — kOA Linux

Owns:

- profile/capability admission;
- graphical session and local execution substrate;
- resource governance;
- filesystem/network/security policy;
- secrets substrate policy;
- package/image/release channels;
- backup/restore and rollback verification;
- endpoint/service-node topology policy.

## 4. Development Plane

Owns developer convenience and orchestration only:

- Control Panel workflow;
- DevPad editor/context UX;
- SmartDump and File Puller adapters;
- LevelUpDiag delegation/presentation.

The Development Plane does not manufacture production authority.
