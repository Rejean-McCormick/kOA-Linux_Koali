# Scope and Non-Goals

> **Status:** Standalone major-update specification — not yet merged into the authoritative Koali/kOA documentation.  
> **Baseline reviewed:** 2026-09-09 snapshots of Koali Spaces, Koali Control Panel, kOA Linux, LevelUpDiag, parallel design plans, and the Senior Architecture Patterns reference.  
> **Authority rule:** Until this package is explicitly adopted, existing repository documentation and contracts remain authoritative. This package defines the proposed target and the delta to close.

## In scope

This update defines the final architecture for:

- Koali Spaces as the Space experience and presentation subsystem;
- adaptive shell and global product surfaces;
- appearance modes, accents, density, and surface style;
- generic owner-app onboarding through existing contracts;
- `SpaceActivationCompiler` ownership and behavior;
- Search, Tasks, Resume, Status, and Counter projections;
- resilience controls for remote/fan-out projection boundaries;
- user-session native application launch and discovery;
- Freedesktop/XDG integration without inventing a second desktop registry;
- kOA native-app admission, security, resource, offline, and data policy;
- release/update and rollback implications for native applications;
- local endpoint versus VPS/service-node topology;
- DevPad and AI-context workflow as development tooling;
- observability, conformance, migration, and Definition of Done.

## NON-GOALS

The update does **not** introduce:

- a new Koali plugin framework;
- a new `SurfaceKind` for native applications;
- native applications as Koali modules;
- a Koali window manager or full desktop environment;
- a second MIME/application metadata registry;
- a public App Store or arbitrary user-installed application model;
- a universal SSO architecture before owner-specific need is proven;
- arbitrary executable provider loading from manifests or URLs;
- a message bus merely because multiple applications exist;
- Event Sourcing, Saga, Outbox, Pub/Sub, DLQ, Data Mesh, Service Mesh, or sharding without a concrete requirement;
- a new backup engine for native application profiles;
- a new release channel unless existing channels prove insufficient;
- a DevPad dependency in build, validation, or release;
- AI agents that write directly into source repositories;
- page-transition animation, glassmorphism, animated layout systems, or decorative theme engines.

## Scope discipline

A proposed capability belongs in this update only if it strengthens one of these outcomes:

1. clearer ownership;
2. lower marginal integration cost;
3. stronger failure isolation;
4. better daily Space UX;
5. safer endpoint/runtime behavior;
6. more reproducible development/release operations.

Anything else requires a separate decision.
