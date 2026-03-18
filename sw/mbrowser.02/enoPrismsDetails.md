# Enodia Prisms — Trusted Base + Untrusted Overlay Loader (v0.3)
# Documentation initially by CoPilot, per a refactor of code by Brygg Ullmer into a pair of YAMLs
# Initial documentation on 2026-03-18

This document explains the intent, structure, and usage of the YAML‑driven loader
**`EnoPrismsDetailsV03`** and its companion base/overlay configuration files. The aim is to keep
**powerful rendering behaviors** in a *trusted, signed* base spec while letting datasets and
collaborators contribute *untrusted, content‑only* overlays—preserving flexibility without
sacrificing safety or legibility over time.

> Implemented in **`enoPrismsDetails_v03.py`** and validated against
> **`prismsAcmTei01bb.yaml`** (trusted base) and **`prismsAcmTei01bo.yaml`** (untrusted overlay). citeturn8file10turn8search1turn8search2

---

## 1) High‑level intent

- **Separate policy from content**: rendering **capabilities** (ops, roles, geometry, colors,
  parse grids) live in a curated “base” YAML; **content** (bindings and optional template tweaks)
  live in an “overlay” YAML. The loader merges them with strict rules. citeturn8search1turn8search2
- **Security by design**: no dynamic `getattr` from config, a **sealed op registry** maps
  declarative `op` names to known functions, and label formatting is done with a **safe
  template** (flat key substitution only). citeturn8file10
- **Continuity with existing code**: the loader exposes `summonPrism(whichPrism, whichSlot)`,
  `update()`, and `draw(screen)`, and can drop into the existing `EnoPrisms` orchestration
  (which iterates domain providers and delegates those calls). citeturn1search2

---

## 2) Files & roles

- **`enoPrismsDetails.py`** — the loader that
  1) loads base and overlay YAMLs with `safe_load`,
  2) merges overlay **bindings** (and optionally `bindingText.template` when allowed),
  3) constructs `EnoActor`, `EnoPrismBars`, `EnoParseGrid`, and `EnoPrism` instances via a strict
     allowlist of ops (`addL`, `addL2`, `addL3`). citeturn8file10
- **`prismsAcmTei01bb.yaml`** (trusted **base**): colors palette, scalars, background actors,
  prism roles (`upper`/`lower`), op/ops sequences, parse grids, and label template policies. citeturn8search1
- **`prismsAcmTei01bo.yaml`** (untrusted **overlay**): per‑prism **bindings only**, referencing
  color names from the base, plus mirrored scalars as anchors for writer convenience
  (ignored for mechanics). citeturn8search2

Related context in the current codebase:
- `EnoPrisms` collects domain providers and delegates `summonPrism`, `update`, and `draw`, so the
  new loader can be appended to `domainPrisms` as a drop‑in. citeturn1search2
- The earlier hard‑coded TEI provider (`EnoPrismsTei`) motivated this refactor by showing what we
  needed to externalize (bars, bindings, parse grids, colors). citeturn1search1

---

## 3) Quick start (test & integrate)

### A. Minimal harness
```python
from enoPrismsDetails_v03 import EnoPrismsDetailsV03

# Construct the trusted+overlay provider
provider = EnoPrismsDetailsV03(
    base_yaml='prismsAcmTei01bb.yaml',
    overlay_yaml='prismsAcmTei01bo.yaml'
)

# Usual lifecycle
provider.update()  # lazy setup of background actors
p1 = provider.summonPrism('teiLandscape', 0)
p2 = provider.summonPrism('teiYearsQ4', 1)
# in draw loop: provider.draw(screen)
```

### B. Integrate into `EnoPrisms`
In your `EnoPrisms.__init__`, add the new provider to `self.domainPrisms`, keeping the rest of the
pipeline intact: `summonPrism`, `update`, `draw`, and bar interactions continue to function as
before. citeturn1search2

### C. Sanity checks
- Verify the two background actors appear and scale as defined in the base. citeturn8search1
- Confirm `teiLandscape` shows five items and `teiYearsQ4` shows six items with dual‑color roles.
  (Overlay provides those bindings.) citeturn8search2
- Confirm parse grids correspond to the base’s `rowsCols`/`xy0`/`pixDim`. citeturn8search1

---

## 4) Philosophy & specific implementation details

### 4.1 Trusted vs. untrusted YAML
- The **base** (trusted) defines *capabilities*: palette, geometry, role definitions, and
  the allowable **ops**. The **overlay** (untrusted) supplies *content*: `bindings` and (optionally)
  a restricted `bindingText.template`. This cleanly separates “what can be done” from “what is to
  be rendered.” citeturn8search1turn8search2

### 4.2 No dynamic method invocation
- The loader maintains a **sealed registry** mapping declarative `op` names to small adapters that
  call `EnoPrismBars.addBarL`, `addBarL2`, or `addBarL3(item, arg)` as needed. Config never drives
  `getattr`; only allowlisted adapters are used. citeturn8file10

### 4.3 Label templates (safe)
- Labels are produced with `bindingText.template` using a flat‑key `{name}` syntax; the loader
  validates placeholders against `allowedKeys`. Missing keys render as empty strings via a safe map.
  No evaluation or attribute traversal is permitted. citeturn8file10

### 4.4 Color resolution via names
- Bindings reference **color names** (`color: cyel` or `colors: [cgre, cgr2]`); loader resolves to
  RGBA via the base `colors` table. For dual‑role prisms, `colorStrategy` instructs which element a
  role picks (e.g., `upper → 0`, `lower → 1`). citeturn8search1turn8search2

### 4.5 ParseGrid normalization
- The loader accepts compact `rowsCols`/`xy0` as well as explicit `rows`/`cols`/`x0`/`y0` and binds
  `gridBindings` whether placed inside `parseGrid` or as its sibling, as in the base file. citeturn8search1

### 4.6 Background actors
- `background_bars` are declared in the base as a mapping (e.g., `land`, `conf`). The loader
  instantiates `EnoActor` objects and draws them every frame; overlays do not modify these. citeturn8search1

---

## 5) Schema sketch (v0.3)

### 5.1 Base (trusted)
- `meta`: `{ schemaVersion, id, version, signer }`
- `colors`: name → RGBA
- `scalars`: anchors for shared numbers (e.g., `&barNarrow1`, `&barNarrow2`)
- `background_bars`: mapping of named actors with `image`, `bottomleft`, `scale`, `name`
- `policy` (optional scaffold): lists of what overlays may/may not override
- `prisms.*`:
  - `bindingText`: `{ template, allowedKeys }`
  - `colorStrategy`: e.g., `{ mode: dual, field: colors, roleIndex: { upper: 0, lower: 1 } }`
  - `bars.roles.{role}`: `{ params, op }` **or** `{ params, ops: [{ kind, take, arg }, ...] }`
  - `parseGrid`: compact or explicit geometry; `gridBindings` either here or as a sibling

*(See `prismsAcmTei01bb.yaml` for a concrete example.)* citeturn8search1

### 5.2 Overlay (untrusted)
- `meta`: `{ baseId, baseVersion, schemaVersion }`
- `prisms.*.bars.bindings`: data dictionaries per item, using `color` or `colors` by **name** and a
  numeric `firstWidth` (scalars can be referenced via anchors for convenience). *(See
  `prismsAcmTei01bo.yaml`.)* citeturn8search2

---

## 6) Security model (practical)
- YAML loading uses `yaml.safe_load` (no Python constructors).
- Declarative ops are routed through a **read‑only registry**; no method names are invoked from
  config, preventing ambient authority issues.
- Label templates are pre‑validated against `allowedKeys`; rendering uses a safe `format_map`.
- For multi‑tenant scenarios, run the renderer in a **least‑privilege subprocess** and pre‑verify a
  detached signature on the base file. (Hook points are easy to add at loader init.) citeturn8file10

---

## 7) Testing checklist
- **Bindings round‑trip**: number of bars in each role == number of bindings; verify widths match
  `firstWidth` and colors resolve by name. citeturn8search2
- **Template enforcement**: add an unknown placeholder to the overlay and confirm the loader rejects
  it with a clear error (base `allowedKeys` in control). citeturn8search1
- **Op sequencing**: confirm `teiYearsQ4.lower` applies `addL3` to the first three, then `addL2` to
  the remainder. citeturn8search1
- **ParseGrid geometry**: verify pixel dimensions and offsets match base spec. citeturn8search1

---

## 8) Troubleshooting
- **“Color 'XYZ' not found”**: ensure the overlay uses a color **name** declared in the base.
- **“Binding missing 'firstWidth'”**: add the numeric width to the binding (anchored scalar OK).
- **No bars drawn**: check that role `op`/`ops` are defined in the base for that prism.
- **Label missing text**: confirm `bindingText.template` placeholders are in `allowedKeys`.

---

## 9) Versioning & future evolution
- Add `meta.schemaVersion` to both base and overlay. When evolving the schema, the loader can branch
  behavior by version for smooth upgrades.
- If you add new operations, extend the **op registry** (small adapter functions), not the YAML
  method names.
- If you add new label fields, include them in the prism’s `allowedKeys` and update overlays.

---

## 10) Appendix: why this fits the existing architecture
- Your `EnoPrisms` class aggregates **domain providers** and delegates `summonPrism`, `update`, and
  `draw`. The new loader is a drop‑in provider, just like the previous TEI‑specific provider, but
  entirely **data‑driven**. This allows swapping datasets by changing YAMLs without code edits.
  citeturn1search2turn1search1

---

**Maintainers’ note:** If you’re returning to this a year from now, start by reading the base YAML
(top to bottom), then the overlay YAML, then skim `EnoPrismsDetails.__init__`, the
`_apply_ops` registry, and `_render_label` to refresh the mental model. The code is intentionally
small; the behavior lives in the data.
