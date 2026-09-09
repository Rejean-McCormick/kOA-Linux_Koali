# Decision Register

> **Status:** Standalone major-update specification — not yet merged into the authoritative Koali/kOA documentation.  
> **Baseline reviewed:** 2026-09-09 snapshots of Koali Spaces, Koali Control Panel, kOA Linux, LevelUpDiag, parallel design plans, and the Senior Architecture Patterns reference.  
> **Authority rule:** Until this package is explicitly adopted, existing repository documentation and contracts remain authoritative. This package defines the proposed target and the delta to close.

| ID | Decision | Status in this standalone spec |
|---|---|---|
| D-001 | Four authority planes: Experience, Application, Platform, Development | Proposed final |
| D-002 | GlobalProjectionRuntime is internal to Koali Spaces | Proposed final |
| D-003 | Hosted integration keeps Manifest + ACP + RuntimeRegistration as authorities; package is non-authoritative | Proposed final |
| D-004 | SpaceActivationCompiler belongs to Koali, not Control Panel | Proposed final |
| D-005 | Native apps are neither SurfaceKind nor Koali modules | Proposed final |
| D-006 | Freedesktop metadata remains authoritative; kOA adds admission policy | Proposed final |
| D-007 | UserSessionAppBroker is unprivileged, endpoint-local, and not the privileged broker | Proposed final |
| D-008 | Space appearance policy and user presentation preferences are separate | Proposed final |
| D-009 | Widget projection binding is separate from click activation | Proposed final |
| D-010 | Provider fan-out requires real bulkheads/time budgets; remote calls may use circuits/backoff | Proposed final |
| D-011 | Observability correlation/structured logs/golden-signal metrics are normative | Proposed final |
| D-012 | Existing Resource Governor, backup/restore, and release channels are reused | Proposed final |
| D-013 | DevPad is optional and external AI remains clipboard/files boundary | Proposed final |
| D-014 | Native binaries remain in existing release authority unless security-update SLO proves need for new channel | Proposed final |
| D-015 | Surface selection becomes addressable in a reserved Koali navigation namespace | Proposed, exact encoding open |
| D-016 | File-manager conformance product choice | Open technical selection |
| D-017 | Exact native-workspace capability name | Open naming, authority fixed |
| D-018 | Exact local IPC implementation for UserSessionAppBroker | Open implementation, locality/security fixed |
| D-019 | Exact user-preference persistence backend | Open implementation, authority fixed |
| D-020 | Universal SSO | Explicitly open/separate; not required by this update |
