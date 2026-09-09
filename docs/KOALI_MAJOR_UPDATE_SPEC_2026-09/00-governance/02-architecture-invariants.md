# Architecture Invariants

> **Status:** Standalone major-update specification — not yet merged into the authoritative Koali/kOA documentation.  
> **Baseline reviewed:** 2026-09-09 snapshots of Koali Spaces, Koali Control Panel, kOA Linux, LevelUpDiag, parallel design plans, and the Senior Architecture Patterns reference.  
> **Authority rule:** Until this package is explicitly adopted, existing repository documentation and contracts remain authoritative. This package defines the proposed target and the delta to close.

The following invariants are mandatory acceptance criteria for the major update.

1. **Koali Spaces remains presentation-oriented.** It does not become business authority for owner applications.
2. **No owner introduces product-specific branching in `ApplicationHost` or `SurfaceRenderer`.**
3. **Native applications are not `SurfaceKind` values.**
4. **Native applications are not Koali modules and never become `active_module_id`.**
5. **Freedesktop `.desktop`/MIME metadata remains the desktop metadata authority; kOA adds admission and policy only.**
6. **The user-session application launcher is unprivileged and distinct from kOA's narrow privileged broker.**
7. **Native application launch is local to an endpoint unless a future explicit remote-endpoint protocol is approved.**
8. **Space activation state and user presentation preferences are separate state domains.**
9. **Widget projection binding and widget click activation are separate concepts.**
10. **Koali Control Panel does not reimplement Koali activation/conformance semantics.**
11. **DevPad is optional development UX; repositories remain independently buildable/testable/releasable.**
12. **Health/readiness never grants authorization.**
13. **Existing kOA backup/restore, Resource Governor, profile, security, and release mechanisms are reused before adding new mechanisms.**
14. **No new source of truth is introduced when an existing authority can represent the information.**
15. **An owner application can be removed without core patches and without breaking unrelated modules.**
16. **Every remote boundary has an explicit timeout budget.**
17. **Every fan-out boundary has bounded concurrency and load shedding.**
18. **Retries are bounded and only used for retryable failures.**
19. **Background retries use exponential backoff with jitter.**
20. **Repeated remote failure can open a circuit; local in-process calls do not receive ornamental circuit breakers.**
21. **Control-plane mutations are idempotent where their semantics permit.**
22. **Degradation is observable even when the user-facing UI intentionally stays quiet.**
23. **Distributed operations carry correlation context across network boundaries.**
24. **Production-critical components expose actionable latency, traffic, error, and saturation metrics.**
25. **No messaging/event architecture is introduced without an asynchronous consistency requirement.**
26. **User preference changes do not change Space activation digests, capabilities, ACP evidence, or owner manifests.**
27. **The fourth hosted integration must be materially cheaper than the second; the sixth native application must require mostly policy and qualification rather than launcher code.**
28. **No temporary compatibility path survives without an explicit deletion condition.**
