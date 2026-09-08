<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-SYS-035",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "system",
  "scope": ["global", "subsystem:koa_spaces", "user_interface"],
  "canonical_refs": [
    "02-system/21-koa-spaces-experience-layer.md",
    "02-system/22-koa-spaces-interface-composition.md",
    "contracts/subsystems/koa-spaces.subsystem.json",
    "contracts/artifact-contracts/interface-theme.schema.json",
    "contracts/artifact-contracts/interface-asset-manifest.schema.json",
    "contracts/artifact-contracts/space-definition.schema.json",
    "contracts/artifact-contracts/module-interface-manifest.schema.json"
  ],
  "decision_ids": [],
  "requirement_ids": [],
  "lock_ids": ["LOCK-SPACES-001"],
  "exception_ids": [],
  "depends_on": ["DOC-SYS-021", "DOC-SYS-022"],
  "tags": ["koa-spaces", "design-system", "interface", "visual-language", "accessibility", "offline", "konnaxion-alignment"]
}
KOA:DOC-META:END -->

# kOA Spaces Design System

## 1. Purpose

This document defines the shared Koali visual and interaction language used by kOA Spaces and by compatible standalone product interfaces. It keeps integrated and standalone Koali experiences coherent while preserving the ownership and internal interface architecture of contributing systems.

The design system is a presentation contract. It does not define business behavior, authorization, workflow logic, storage, or subsystem ownership.

## 2. Design Principles

The Koali interface favors:

- a stable shell grammar that works in standalone and integrated modes;
- predictable navigation placement;
- neutral surfaces with a restrained semantic accent;
- clear active, focus, warning, error, and success states;
- low visual noise;
- consistent density and spacing;
- outline-oriented iconography where practical;
- keyboard-first operability alongside pointer and touch;
- readable offline and degraded states;
- consistent page structure across independently owned products without requiring one product to host another.

## 3. Koali and Konnaxion Alignment

Koali intentionally aligns with Konnaxion interface conventions where the conventions are generic presentation patterns rather than Konnaxion business functions.

Suitable alignment includes:

- frontend component-library conventions;
- global spacing and density;
- typography scale;
- icon style;
- active and selected states;
- form, card, table, modal, drawer, notification, and status patterns;
- PageShell composition;
- responsive behavior;
- accessibility interaction patterns.

Alignment does not include duplicating Konnaxion domain services, pages, validation, workflows, APIs, or authoritative state inside kOA Spaces. Konnaxion can use the shared Koali shell primitives in its standalone application and expose the same presentation declarations to an integrated Koali host without depending on another product's UI implementation.

## 3.1 Shared Shell Primitives

The shared Koali UI layer can provide reusable presentation primitives such as:

- `KoaliShell`;
- product/module selector;
- surface navigation;
- context header and breadcrumbs;
- command/search surface;
- main workspace;
- optional contextual inspector;
- mobile drawer;
- PageShell;
- common status, loading, offline, degraded, and error presentation.

These primitives are a reusable library and interaction contract. They do not contain Orgo Case logic, Konnaxion domain behavior, Kristal semantics, or another product's business rules. A product can render them at its own standalone entry point. An integrated host can render them once and mount product contributions inside the resulting frame.

The shared shell MUST derive installed products from an admitted registry or manifest source rather than from product-specific hard-coded imports.

## 4. Theme Contract

A Space can reference an admitted interface theme through `appearance.theme_ref`.

The referenced theme follows `contracts/artifact-contracts/interface-theme.schema.json` and describes semantic presentation tokens such as:

- primary accent;
- semantic foreground and background roles;
- typography scale;
- spacing scale;
- radius scale;
- density defaults;
- focus presentation;
- icon policy;
- motion and reduced-motion behavior.

A theme changes presentation only. It does not change module identity, route identity, capability state, authorization, policy, or ownership.

## 5. Reference Visual Language

The reference Koali visual language uses predominantly neutral interface surfaces and a restrained primary accent. The current Koali/Konnaxion alignment family uses `#1e6864` as the reference primary accent.

The primary accent is concentrated on active or selected controls, focus-compatible emphasis, primary actions, and bounded brand cues. Semantic warning, error, and success states keep their distinct meanings rather than being recolored as brand accents.

This color value belongs to the reference theme. A profile or admitted Space can select another compatible theme without changing the global interface contract.

## 6. Layout Tokens

The design system defines reusable semantic tokens rather than page-specific pixel ownership.

Token families include:

- page gutters;
- sidebar width ranges;
- top-bar height ranges;
- control density;
- card and panel padding;
- section spacing;
- border radius;
- focus ring geometry;
- typography roles;
- compact and touch targets.

Product-specific pages can arrange their own content inside the main workspace while preserving the active shell contract and declared accessibility envelope. Reduced product surfaces can alter navigation, commands, widgets, inspector availability, and density without duplicating business pages.

## 7. Module PageShell

A reusable PageShell pattern creates consistent page framing inside the main workspace in either standalone or integrated mode.

The pattern supports:

- title;
- optional description;
- optional context or breadcrumbs;
- page-level actions;
- status or degradation messaging;
- content width and padding policy;
- the module-owned content region.

Konnaxion can keep its established page shells inside this pattern or map them directly to the same interaction language. kOA Spaces does not reinterpret the business content of those shells.

## 8. Component Patterns

Common presentation patterns include:

- navigation menu;
- dropdown selector;
- sidebar tree;
- top-bar action and status widget;
- PageShell;
- card and description panel;
- data table;
- form and validation summary;
- modal and confirmation surface;
- drawer;
- notification and alert;
- empty state;
- loading state;
- offline or degraded-state banner.

The reference implementation can map these patterns to Ant Design components. The semantic contract remains independent from Ant Design itself.

## 9. Accessibility

The global design language preserves:

- semantic landmarks;
- visible focus;
- deterministic keyboard order;
- accessible names;
- sufficient contrast;
- zoom and reflow;
- reduced-motion behavior;
- focus restoration after overlays close;
- keyboard-operable selectors, menus, dialogs, and drawers;
- status announcements for important state changes.

A product can add stronger accessibility behavior without replacing the shared navigation and shell contract.

## 10. Offline and Local Asset Behavior

Required theme, font, icon, script, style, localization, and shell resources for an offline-capable surface are installable locally.

A public CDN or arbitrary remote origin is not part of the runtime dependency path for local offline rendering. Clearing a non-authoritative presentation cache can require asset reconstruction, but it does not alter business data or authority.

## 11. Technology Mapping

The system design does not make one web framework globally authoritative.

The current reference implementation uses Next.js, React, TypeScript, Ant Design 5, `@ant-design/pro-components`, and pnpm because this family aligns closely with the existing Konnaxion interface stack and minimizes unnecessary UX divergence.

That choice is recorded in the reference frontend recipe rather than promoted to a universal architecture identity.

## 12. Validation

Design-system validation checks:

- theme schema validity;
- local asset closure for offline-capable surfaces;
- shell consistency across standalone and integrated modes;
- product-removal independence and absence of hard-coded mandatory product lists;
- responsive behavior;
- keyboard and focus behavior;
- reduced-motion handling;
- semantic state presentation;
- absence of presentation-driven authority claims;
- absence of duplicated business behavior in the experience layer.
