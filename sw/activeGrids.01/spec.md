# Specification: ActiveGrids / Enodia Tangibles
# Auto-expressed by CoPilot per request by Brygg Ullmer, Clemson University
# Begun 2026-04-08

## 1. System Overview

ActiveGrids is a modular system for exploring **grid‑based interaction spaces**
that support:

- touch and mouse interaction,
- symbolic and ethical representations,
- YAML‑defined data models,
- and optional Prolog reasoning backends.

The system is implemented primarily in Python, with Pygame Zero for interaction,
but its *semantic core is language‑agnostic*.

---

## 2. Conceptual Entities

### 2.1 Actors

An **Actor** represents an interactive or symbolic entity.

Examples:
- buttons,
- people tokens,
- themes,
- visual backdrops.

Actors may be realized as:
- graphical sprites,
- logical symbols,
- or tangible proxies.

---

### 2.2 People

A **Person** is a symbolic actor defined by:

- name,
- abbreviation,
- era,
- domains,
- themes,
- color rings,
- and narrative notes.

Canonical source:
- `yaml/peopleThemes03.yaml`

These definitions may be re‑expressed in:
- Python objects,
- Prolog facts,
- or future representational forms.

---

### 2.3 Themes

A **Theme** is a conceptual category expressing ethical,
civic, cultural, creative, or ecological dimensions.

Themes are:
- hierarchically structured,
- color‑coded,
- and intended for both visualization and reasoning.

---

## 3. Data Representation Strategy

### 3.1 YAML as Semantic Backbone

YAML files serve as **primary semantic representations**:

- `peopleThemes03.yaml`
- `mediaAssets.yaml`
- `senet03k.yaml`

They are expected to be:
- human-authored or human-reviewed,
- externally transformable,
- preserved as long-term artifacts.

---

### 3.2 Prolog as Reasoning Substrate

Selected YAML structures may be transformed into Prolog DSLs, expressing:

- relations,
- categories,
- constraints,
- and queries over ethical or conceptual structure.

Transformers live under:
- `yaml/transformers/`

Prolog is treated as a **model language**, not merely code.

---

## 4. Interaction Patterns

### 4.1 Grid-Based Interaction

Grids may be:
- uniform or non-uniform,
- warped,
- segmented via YAML-defined coordinates.

Grid segmentation is editable, inspectable, and serializable
(e.g., `EnoNUGrid`, `enoPgzGridSeg`).

---

### 4.2 Buttons and Arrays

Button arrays:
- may be toggled,
- constrained to single-selection,
- animated or static,
- driven by YAML, code, or hybrid definitions.

Button state has semantic meaning beyond UI convenience.

---

## 5. Media and Remote Content

Media assets may be:

- local,
- cached,
- remotely retrieved.

All remote retrieval must explicitly specify:
- trust policy,
- integrity expectations,
- and whether insecure transport is permitted.

---

## 6. Intended Extensions (Explicitly Non-Binding)

- Additional reasoning backends (Datalog, SQL).
- Bidirectional editing of YAML ↔ Prolog ↔ Python.
- Higher-level English-to-model projections.
- Tangible hardware integration.

---

## 7. Traceability

Every executable behavior should be traceable to:
- a YAML definition,
- a specification clause,
- or an explicit design decision.

### end ###
