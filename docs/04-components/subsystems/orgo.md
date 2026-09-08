<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-SUB-ORGO",
  "document_class": "explanatory_markdown",
  "status": "active",
  "language": "en",
  "layer": "subsystem_boundaries",
  "scope": [
    "global"
  ],
  "canonical_refs": [
    "contracts/subsystems/orgo.subsystem.json"
  ],
  "decision_ids": [],
  "requirement_ids": [],
  "lock_ids": [],
  "exception_ids": [],
  "depends_on": [],
  "tags": [
    "subsystem",
    "orgo",
    "integration-boundary"
  ]
}
KOA:DOC-META:END -->

# Orgo Subsystem Boundary

## Purpose

This page defines the **kOA-Linux host boundary** for Orgo. Orgo remains an independently owned ecosystem system. This page does not reproduce or redefine its Task/Case/workflow documentation.

## Official documentation

The official documentation mount is `subsystems/orgo/` and remains authoritative for Orgo internals.

## Host role

Within kOA-Linux, Orgo is an **integrated subsystem**. kOA-Linux can own/mediate deployment-profile membership, process lifecycle, resource envelope, trust boundary, network/storage exposure, artifact admission, health integration, backup coordination, safe degradation, and declared cross-system interactions.

Orgo itself owns Organizations, Cases, Tasks, workflow rules/state, routing/labels, domain extensions, its APIs, and operational audit semantics.

```text
ecosystem scope: Orgo = ecosystem system
host scope:      Orgo = integrated subsystem
```

A kOA-Linux platform event or receipt does not become Orgo workflow state unless Orgo accepts it through its own contract.


## User-interface boundary

Orgo owns its own user interface and remains usable as a standalone product when an integrated Koali experience host is absent. The full Orgo Control Panel is the reference maximal Orgo surface; narrower experiences such as personal work, operations, supervision, intake, workflow administration, executive, or embedded surfaces are projections of the same Orgo routes and capabilities rather than separately owned frontends.

Orgo can implement its standalone frame with shared Koali UI primitives and can expose the same route, navigation, command, contextual-inspector, and surface declarations to kOA Spaces or another admitted Koali composition host. Shared shell code does not transfer Orgo Cases, Tasks, Signals, workflow, routing, or organization semantics into kOA-Linux or kOA Spaces.

Removing Orgo from an integrated Koali installation removes Orgo-owned interface contributions without requiring source changes to Konnaxion, kOA Spaces, or another unrelated product. Orgo SHALL NOT depend on a private Konnaxion UI implementation for ordinary shell behavior.
