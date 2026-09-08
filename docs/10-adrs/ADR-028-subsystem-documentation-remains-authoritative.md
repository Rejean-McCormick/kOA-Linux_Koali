<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "ADR-028",
  "document_class": "adr",
  "status": "accepted",
  "language": "en",
  "layer": "decisions",
  "scope": [
    "global"
  ],
  "canonical_refs": [
    "contracts/ai-navigation.contract.json"
  ],
  "decision_ids": [],
  "requirement_ids": [],
  "lock_ids": [],
  "exception_ids": [],
  "depends_on": [],
  "tags": [
    "adr"
  ]
}
KOA:DOC-META:END -->

# ADR-028: Subsystem Documentation Remains Authoritative

## Status

Accepted.

## Decision

Ariane, Konnaxion, Orgo, SenTient, SemantiK Architect, and UCKK own their internal documentation. kOA documents operating-environment and integration boundaries.

## Consequences

Generated navigation has no independent authority. Subsystem internals are not duplicated in kOA. Stable local documentation mounts are reserved under `subsystems/`.

## Koali product UI modularity

This document is interpreted with the Koali product-interface portability rule:

- each independently packaged product owns its user interface and remains independently operable when its declared standalone mode is supported;
- shared Koali shell and design-system code is reusable presentation infrastructure, not a mandatory product runtime and not a source of business authority;
- an integrated composition host discovers installed and admitted product manifests dynamically rather than hard-coding a mandatory product list;
- a surface profile is a projection of the same product routes, capabilities, commands, and contextual views, not a separately implemented frontend;
- removing one product removes only that product's admitted presentation contributions and SHALL NOT require source changes to unrelated products;
- ordinary shell behavior SHALL NOT require private UI imports from another product; cross-product journeys use explicit public routes, commands, capabilities, or integration contracts.
