# Constitution: ActiveGrids / Enodia Tangibles
# Auto-expressed by CoPilot per request by Brygg Ullmer, Clemson University
# Begun 2026-04-08

## Purpose

ActiveGrids is a research and pedagogical codebase concerned with:

- tangible and graphical interaction,
- ethical reflection and education,
- explicit human–machine mediation,
- and durable representations of meaning across time, media, and implementation layers.

This repository treats **specification as a first-class artifact**, and code as one of several projections of shared intent.

---

## Core Principles

### 1. Human-Legible First

All computational structures **must have a human-legible form**.
Whenever possible, this form is expressed in:

- structured English,
- YAML,
- or minimally adorned declarative DSLs.

Imperative code is a *projection*, not the origin of meaning.

---

### 2. Explicit Provenance and Trust

Remote content, derived assets, and transformations must:

- record their source,
- record integrity checks where applicable,
- record trust decisions explicitly (e.g., `trustPolicy`, `allowInsecure`).

Silent or implicit trust is a design error.

(This principle is instantiated concretely in `EnoRemoteContent`.)

---

### 3. Ethical and Civic Visibility

The system explicitly supports:

- ethical figures,
- historical actors,
- moral themes,
- cultural plurality,
- and civic reasoning.

These are not “content”; they are **structural dimensions** of the system
(e.g., `peopleThemes03.yaml`, `peopleThemes03.pl`).

---

### 4. Declarative over Procedural Bias

Where a choice exists, prefer:

- declarative descriptions,
- constraint-like formulations,
- relational mappings,

over procedural logic.

This applies across Python, YAML, Prolog, and future backends.

---

### 5. Bidirectional Evolution

Artifacts must be designed so that:

- human-authored specifications can regenerate code, and
- code revisions can be reflected back into specifications.

No layer is treated as write-only.

---

### 6. Educational Reach

The system should remain legible and meaningful to:

- secondary-school students,
- university learners,
- non-programming experts,
- and elders with lived historical experience.

Cleverness that excludes understanding is discouraged.

---

## Non-Goals

- Maximum runtime performance at the expense of legibility.
- Obscure abstractions without narrative grounding.
- Silent automation without visible rationale.

---

## Amendment Policy

This constitution is expected to evolve.

Amendments must:
- be textual,
- be diffable,
- preserve earlier versions,
- and state their motivation explicitly.

### end ###
