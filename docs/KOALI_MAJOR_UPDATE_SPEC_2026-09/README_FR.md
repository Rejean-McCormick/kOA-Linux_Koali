# Koali — mise à jour majeure — guide de lecture

> **Status:** Standalone major-update specification — not yet merged into the authoritative Koali/kOA documentation.  
> **Baseline reviewed:** 2026-09-09 snapshots of Koali Spaces, Koali Control Panel, kOA Linux, LevelUpDiag, parallel design plans, and the Senior Architecture Patterns reference.  
> **Authority rule:** Until this package is explicitly adopted, existing repository documentation and contracts remain authoritative. This package defines the proposed target and the delta to close.

Ce dossier est volontairement **séparé de la documentation canonique**. Il sert à voir clairement la cible finale et tout ce qui reste à réaliser avant de fusionner les décisions dans les repos propriétaires.

Les documents normatifs sont rédigés en anglais pour faciliter une future fusion avec les documentations actives de Koali/kOA. Ce fichier est le point d'entrée français.

## Ce que le dossier fixe

- quatre plans d'autorité : Experience, Application, Platform, Development;
- Koali Spaces comme façade du Space et BFF/projection runtime de son expérience;
- maintien des trois autorités d'intégration hosted : Manifest, ACP, RuntimeRegistration;
- `SpaceActivationCompiler` dans Koali, pas dans le Control Panel;
- séparation Space policy / préférences utilisateur;
- Home final, shell adaptatif, thèmes, densité et styles de surfaces;
- Search/Tasks/Resume/Status/Counter avec résilience réelle;
- Native Workspace sous kOA Linux, sans nouveau `SurfaceKind`;
- Freedesktop comme autorité metadata + politique d'admission kOA;
- `UserSessionAppBroker` local et non privilégié;
- réutilisation Resource Governor, backup/restore, sécurité et release kOA;
- DevPad comme outil de développement facultatif;
- observabilité, conformance et qualification VPS/distribuée.

## Pour suivre ce qui reste

Ouvrir en priorité :

- [`10-work/01-remaining-work.md`](10-work/01-remaining-work.md) — registre détaillé `KMA-*`;
- [`10-work/05-baseline-gap-matrix.md`](10-work/05-baseline-gap-matrix.md) — existant vs cible;
- [`10-work/02-dependency-graph.md`](10-work/02-dependency-graph.md) — dépendances logiques sans phases;
- [`09-conformance/00-system-definition-of-done.md`](09-conformance/00-system-definition-of-done.md) — définition de « terminé ».

## Règle de lecture des statuts

- `[x]` : mécanisme déjà substantiellement présent dans le baseline;
- `[~]` : direction/primitive présente ou spécifiée ici, mais adoption/implémentation canonique incomplète;
- `[ ]` : travail restant réel.
