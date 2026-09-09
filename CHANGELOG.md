# Changelog

This file records repository-level implementation and release history. Canonical system, component, profile, integration, artifact, and release identities remain owned by their contracts and signed release records.

## Unreleased

### Added

- Root repository entrypoint and current implementation-status summary.
- Contribution workflow aligned with canonical ownership and validation requirements.
- Security reporting and supported-release policy for the greenfield repository state.
- Git attributes and exclusions for deterministic text handling, secrets, mutable state, build outputs, and generated payloads.
- Legal notice, third-party inventory procedure, and REUSE metadata using the explicit `NOASSERTION` state where owner-approved licensing information is absent.

- Native Workspace platform support for the `user-lightweight` profile, including policy-controlled Freedesktop application admission, local user-session brokering over authenticated Unix IPC, native application projections for Koali Spaces, and permanent Firefox/VLC/LibreOffice/Thunderbird conformance fixtures.
- Native application data-policy projection into the existing backup/restore model and resource admission through the existing Resource Governor boundary.
- User-lightweight OS-image package-set composition for the native desktop substrate without introducing a new release channel.

### Changed

- Koali Spaces integration contracts are converged with the current presentation model: projection data binding is distinct from activation, appearance policy is explicit, presentation preferences remain outside Space activation authority, and legacy `status_provider` activation semantics are removed from subsystem manifests.
- Concrete Koali Spaces and Native Workspace Unix transports live under host adapters so subsystem integrations remain injectable and do not acquire platform transport authority.
- Offline verification policy now declares the normative `verify-before-use` mode explicitly.

No runtime Release Set is declared by this changelog.
