<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-COMP-SUBSYSTEMS-README",
  "document_class": "explanatory_markdown",
  "status": "active",
  "language": "en",
  "layer": "subsystem_boundaries",
  "scope": [
    "global"
  ],
  "canonical_refs": [
    "contracts/ai-navigation.contract.json",
    "contracts/subsystems/koa-spaces.subsystem.json",
    "02-system/21-koa-spaces-experience-layer.md",
    "02-system/22-koa-spaces-interface-composition.md",
    "03-profiles/14-koa-spaces-deployment.md"
  ],
  "decision_ids": [],
  "requirement_ids": [],
  "lock_ids": [
    "LOCK-SPACES-001"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-SYS-021",
    "DOC-SYS-022",
    "DOC-PROFILE-014"
  ],
  "tags": [
    "subsystems",
    "navigation",
    "koa-spaces",
    "experience-layer"
  ]
}
KOA:DOC-META:END -->

# Subsystems

This directory contains kOA integration-boundary pages. Full subsystem documentation is mounted under `subsystems/` when available.

Active boundary pages include:

- `ariane.md`;
- `konnaxion.md`;
- `orgo.md`;
- `sentient.md`;
- `semantik-architect.md`;
- `koa-spaces.md`.

`koa-spaces.md` documents the optional, replaceable experience subsystem that composes declared interface contributions into the module selector, active-module sidebar, top bar, presentation routing, and shared page surface. It does not make routes, menus, aliases, widgets, or visible actions authoritative, and it does not own business data or host privilege. UCKK remains an external platform and is not listed as a mounted subsystem.

## Koali product UI modularity

This document is interpreted with the Koali product-interface portability rule:

- each independently packaged product owns its user interface and remains independently operable when its declared standalone mode is supported;
- shared Koali shell and design-system code is reusable presentation infrastructure, not a mandatory product runtime and not a source of business authority;
- an integrated composition host discovers installed and admitted product manifests dynamically rather than hard-coding a mandatory product list;
- a surface profile is a projection of the same product routes, capabilities, commands, and contextual views, not a separately implemented frontend;
- removing one product removes only that product's admitted presentation contributions and SHALL NOT require source changes to unrelated products;
- ordinary shell behavior SHALL NOT require private UI imports from another product; cross-product journeys use explicit public routes, commands, capabilities, or integration contracts.
