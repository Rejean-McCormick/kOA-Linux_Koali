<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-SYS-022",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "system",
  "scope": ["global"],
  "canonical_refs": [
    "contracts/artifact-contracts/module-interface-manifest.schema.json",
    "contracts/artifact-contracts/sidebar-navigation.schema.json",
    "contracts/artifact-contracts/topbar-widget.schema.json",
    "contracts/artifact-contracts/route-contribution.schema.json",
    "contracts/artifact-contracts/interface-theme.schema.json",
    "contracts/artifact-contracts/interface-asset-manifest.schema.json",
    "02-system/21-koa-spaces-experience-layer.md",
    "contracts/subsystems/koa-spaces.subsystem.json",
    "contracts/architecture-patterns.contract.json",
    "contracts/artifact-contracts/integration-resilience-policy.schema.json",
    "contracts/artifact-contracts/experience-view-adapter.schema.json",
    "contracts/artifact-contracts/cqrs-projection.schema.json",
    "contracts/artifact-contracts/cache-policy.schema.json"
  ],
  "decision_ids": ["DEC-RES-001", "DEC-BFF-001", "DEC-CQRS-001", "DEC-CACHE-001"],
  "requirement_ids": [
    "REQ-PATTERN-006", "REQ-PATTERN-007", "REQ-PATTERN-008", "REQ-PATTERN-009", "REQ-PATTERN-010", "REQ-PATTERN-011",
    "REQ-PATTERN-031", "REQ-PATTERN-032", "REQ-PATTERN-033", "REQ-PATTERN-034", "REQ-PATTERN-035", "REQ-PATTERN-036",
    "REQ-PATTERN-037", "REQ-PATTERN-038", "REQ-PATTERN-039", "REQ-PATTERN-040", "REQ-PATTERN-041", "REQ-PATTERN-042"
  ],
  "lock_ids": ["LOCK-SPACES-001", "LOCK-RES-001", "LOCK-BFF-001", "LOCK-CQRS-001", "LOCK-CACHE-001"],
  "exception_ids": [],
  "depends_on": ["DOC-SYS-021", "DOC-SYS-034"],
  "tags": ["koa-spaces", "navigation", "module-selector", "sidebar", "topbar", "routing", "responsive", "offline", "architecture-patterns"]
}
KOA:DOC-META:END -->

# kOA Spaces Interface Composition

## 1. Purpose

This document defines the visible composition contract used when kOA Spaces hosts an integrated Koali experience. It specifies the integrated frame while leaving each contributing product responsible for its pages, domain actions, standalone entry point, and internal page-level composition. The same Koali shell primitives can also be used directly by standalone product interfaces.


## 2. Standalone and Integrated Rendering Modes

The Koali UI contract supports two rendering modes:

- **standalone product mode** — one product owns the application entry point and renders the shared shell primitives around its own routes and surfaces;
- **integrated composition mode** — kOA Spaces or another admitted composition host renders the shared outer frame and mounts the active product contribution inside it.

A product does not need kOA Spaces to remain usable. Conversely, kOA Spaces does not copy the product's pages in order to compose them. The same product route, command, capability, surface, and inspector declarations SHOULD be reusable in both modes where the deployment supports both modes.

The integrated registry is dynamic. Installed and admitted product manifests determine which products appear; the frame does not contain a mandatory hard-coded list of Orgo, Konnaxion, Kristal, or other products.

## 3. Desktop Frame

```text
┌──────────────────────┬────────────────────────────────────┬──────────────────┐
│ Product selector     │ Context header                     │ Account / status │
│                      │ search • commands • alerts         │                  │
├──────────────────────┼────────────────────────────────────┼──────────────────┤
│ Active product       │                                    │ Optional context │
│ surface navigation   │ Main workspace                     │ inspector        │
│                      │                                    │                  │
│ Group                │ page • list • board • workflow     │ selected object  │
│ ├─ Item              │ document • media • report          │ actions • links  │
│ └─ Item              │                                    │                  │
└──────────────────────┴────────────────────────────────────┴──────────────────┘
```

The product selector and context header occupy the same horizontal band. Product navigation begins below the selector. The main workspace begins below the context header. An optional contextual inspector can occupy a bounded right-side panel when the active product and surface declare one.

In integrated mode, the frame is rendered once. A contributing product renders inside the main workspace and does not instantiate a second integrated global frame. In standalone mode, that same product can instantiate the shared shell primitives at its own application entry point.

## 4. Product / Module Selector

The product/module selector is placed in the upper-left corner. It lists only product contributions that are:

- installed;
- enabled by the active Space definition;
- compatible with the active deployment profile;
- permitted for the current user;
- available or meaningfully degradable in the current network state.

Selecting a product changes:

- the active surface navigation contribution;
- the active home route or retained route for that product and surface;
- product-specific header widgets and commands;
- contextual help and Ariane navigation context;
- optional public labels or visual accents allowed by the Space.

Selecting a product or surface does not change identity, authority, policy, ownership, or the owning product's business rules.

## 5. Surface Navigation

The left navigation is supplied by the active product manifest for the active surface profile and rendered by the current shell host.

Rules:

- visible hierarchy is limited to items and one child level;
- stable item and route identifiers remain unchanged when labels are localized;
- groups without any permitted child are omitted;
- deep links are checked independently of menu visibility;
- badges and counts are presentation data and cannot become authorization evidence;
- the product may define page-level tabs inside its own page surface, but those tabs do not extend the global navigation depth.

The navigation container is a shell primitive. The active product contributes only its validated navigation tree for the active surface. A reduced surface is a composition of the same product capabilities, not a separate frontend implementation.

## 6. Context Header and Commands

The shared context header has global and product-controlled slots. It keeps the active product, surface, route, and relevant operating context identifiable.

Global functions can include:

- search;
- online or offline state;
- notifications;
- pending governed operations;
- user profile;
- Ariane assistance;
- accessibility controls.

A product may contribute compact widgets or commands such as:

- resume the current course;
- create a task;
- show pending approvals;
- display transfer state;
- open an import or publication action;
- show local storage status.

Widgets and commands are ordered by slot and priority. Overflow rules keep the frame stable on narrow displays. A widget cannot embed an entire business application in the header. A command palette can expose permitted navigation and actions without replacing owner-side authorization.

## 7. Main Page Surface

The main surface renders the active route. Contributing systems own their page content and may use their established internal page shells.

For Konnaxion, product page shells such as the Ethikos, KeenKonnect, KonnectED, Kreative, or Ekoh shells remain valid inside this surface. They provide page titles, descriptions, page-level tools, and content layout. In integrated mode they do not recreate the outer product selector, context header, or navigation container.

The same rule applies to every product: the active shell host supplies frame composition; the product supplies its own business page implementation. In standalone mode, the product can host those same shared frame primitives itself.

## 8. Product PageShell Pattern

A product can use a PageShell pattern to keep page structure consistent without transferring page ownership to kOA Spaces or another shell host.

A typical PageShell exposes:

- page title;
- optional description;
- navigation context or breadcrumbs;
- primary and secondary page actions;
- status or degradation information;
- the product-owned content region.

A PageShell is an interface pattern. It does not become a shared business service and does not move validation or workflow logic into the experience layer.


## 9. Product and Surface Profiles

Product identity and surface identity are separate axes. A product identifies the owning application domain; a surface selects an intentional projection of that product for a user context.

Examples include a full control surface, personal work surface, operations surface, supervisor surface, intake surface, executive surface, administration surface, or embedded surface. The actual surface vocabulary remains product-owned.

A surface profile can select:

- its home route;
- visible navigation groups;
- available commands and quick actions;
- header widgets;
- contextual inspector behavior;
- search scopes;
- density and presentation preferences.

Surface composition never grants authority. Server-side and owner-side capability checks remain mandatory. A product SHOULD reuse the same route and feature implementations across surfaces rather than maintaining independent page copies.

## 10. Context Inspector

The shell can expose an optional contextual inspector beside the main workspace. The inspector is intended for selected-object context, quick edits, bounded actions, relations, status, and navigation to a full page.

The inspector does not replace a complete business page. Complex workflows, large forms, deep history, or configuration remain product-owned routes in the main workspace.

The inspector mechanism is generic; its content is product-owned. For example, Orgo can expose Case, Task, Signal, workflow, and action context without transferring those concepts into the shell implementation.

## 11. Removal and Product Independence

Removing one product contribution removes its routes, navigation, commands, inspectors, and widgets from the integrated registry. It does not require source changes to unrelated products and does not invalidate their standalone entry points.

Ordinary shell behavior SHALL come from the shared Koali UI contract or compatible local implementation rather than from private imports between products. Cross-product navigation or context transfer uses explicit public integration contracts.

## 12. Route and Surface Composition

Every route contribution has:

- a stable route identifier;
- a stable module identifier;
- a namespaced path;
- a stable logical page reference;
- optional local surface metadata;
- required capabilities;
- an offline state;
- a deep-link policy;
- optional aliases.

A local surface can refer to a locally admitted presentation asset bundle. A route does not gain permission to load arbitrary executable code or an arbitrary remote origin from a page reference.

The composer rejects:

- duplicate route identifiers;
- path collisions;
- routes outside the module's declared namespace unless explicitly reserved;
- a sidebar reference to an unknown route;
- a widget action targeting an unknown route;
- a default route that is unavailable in the active profile;
- circular redirects.

## 13. Interface State Vocabulary

The active shell and product surfaces use explicit presentation states:

- `loading` — required local state or assets are still resolving;
- `ready` — the declared route is available for normal interaction;
- `offline` — the local route remains usable while network-dependent functions are absent;
- `degraded` — a declared reduced local capability is active;
- `unavailable` — the requested capability is not presently available;
- `access_denied` — the owning authorization path denies access;
- `error` — the surface cannot complete its declared presentation operation;
- `empty` — the route is valid and has no content to display.

A presentation state never fabricates a business success state. In particular, `offline`, `degraded`, `loading`, or `error` cannot be interpreted as authorization or as completion of a mutation.

## 14. Public Labels and Stable Identity

A Space may adapt labels to the context:

```text
Stable module ID       Public label in one Space
uckk_learning          Learn
orgo                   Produce
koa_mediatheque        Recipes and documents
konnaxion              Share
```

Public labels do not alter identifiers, contracts, routes, logs, receipts, or authority.

## 15. Visual Alignment and Product Independence

Koali and Konnaxion can share a visual language, interaction patterns, component-library conventions, spacing, iconography, PageShell structure, and compatible design tokens when that alignment improves continuity for users.

Alignment does not imply that kOA Spaces reproduces Konnaxion functions. Konnaxion remains responsible for Konnaxion pages, commands, validation, workflows, domain services, and state.

The reference frontend recipe maps the shared Koali design language to Ant Design. The design-system contract remains independent from one frontend library so that the experience layer remains replaceable.

## 16. Responsive Behavior

On smaller displays:

- the product selector remains reachable from the context header;
- surface navigation becomes a modal or sliding drawer;
- priority widgets remain visible;
- secondary widgets move to overflow;
- the active product, surface, and page remain identifiable;
- focus returns to the invoking control when a drawer closes;
- keyboard, touch, switch, and assistive navigation remain supported.

## 17. State Restoration

kOA Spaces may remember:

- the last permitted product;
- the last permitted surface and route per product;
- sidebar expansion state;
- presentation preferences;
- locally safe widget preferences.

It does not restore a route when the capability, profile, product, surface, or offline state no longer permits it. In that case, it opens the nearest declared safe route and explains the degradation.

## 18. Local Assets and Offline Rendering

A locally available shell or product surface resolves its required JavaScript, style sheets, fonts, icons, localization data, and other presentation resources from admitted local assets.

An Internet-hosted CDN is not part of the runtime path for a surface that claims local offline availability. Network-dependent content is represented as a separate declared capability and can degrade independently from the local frame.

Browser-rendered technology does not imply public Web connectivity. Konnaxion can therefore use the same web-technology stack when installed locally in Koali and still expose its declared offline-capable functions without Internet access.

## 19. Failure and Safe Degradation

- An invalid Space definition is rejected before activation.
- An invalid product/module manifest disables only that contribution unless the Space marks it as required.
- A failed widget does not fail the page surface.
- A failed product home route falls back to the product surface's declared safe route.
- A missing optional product contribution is omitted without substitution.
- A missing required product contribution blocks activation of that Space definition.
- A missing local asset bundle makes only the dependent surface unavailable unless the active Space marks that contribution as required.

## 20. Aggregated View Composition

A route may bind an experience view adapter, a CQRS projection, and a cache policy. The route exposes staleness or partial availability, bounds fan-out, applies per-dependency circuit policy, and preserves owner authorization. Menu visibility and cached presentation never imply permission.
