
# enoPrismsDetails.py — trusted base + untrusted overlay loader
# Brygg Ullmer & collaborators — refactor scaffold by Copilot (2026-03-16)
# - Loads a **trusted** base YAML (policy + machinery) and an **untrusted** overlay YAML (content)
# - Validates and merges them with a minimal, sealed op registry (no getattr on user-provided names)
# - Renders prisms with safe label templating and color resolution

from ataBase import *
from enoActor import *
from enoPrism import *
from enoPrismBars import *
from enoParseGrid import *

from dataclasses import dataclass, field
from typing import Any, Dict, List, Tuple, Callable, Optional
from types import MappingProxyType
import re

try:
  import yaml
except Exception as e:
  raise RuntimeError("PyYAML is required to use enoPrismsDetails") from e

# ------------------------- Utilities -------------------------

def _to_tuple(v):
  if isinstance(v, list):
    return tuple(_to_tuple(x) for x in v)
  return v

class _SafeMap(dict):
  """Formatting map that returns empty string for missing keys.
  Prevents KeyError and avoids leaking object attributes.
  """
  def __missing__(self, key):
    return ""

_placeholder_re = re.compile(r"\{([a-zA-Z0-9_]+)\}")

def _validate_template_keys(template: str, allowed: List[str]):
  ph = set(_placeholder_re.findall(template or ""))
  bad = ph - set(allowed or [])
  if bad:
    raise ValueError(f"Template references disallowed keys: {sorted(bad)}")

# Shallow dict merge with allowlist keys

def _merge_overlay_into_base(base: Dict[str, Any], overlay: Dict[str, Any]) -> Dict[str, Any]:
  """Merge overlay into base respecting the intended policy:
  - Only allow overlay to provide prism->bars->bindings
  - Optionally allow bindingText.template override if base has allowedKeys
  (Additional policy hooks can be added later.)
  """
  result = {**base}
  prisms_b = dict(base.get('prisms', {}))
  prisms_o = dict((overlay or {}).get('prisms', {}))

  for pkey, pval_b in prisms_b.items():
    pval = dict(pval_b)
    o = prisms_o.get(pkey)
    if o:
      # bindings override
      bars_b = dict(pval.get('bars', {}))
      bars_o = dict((o.get('bars') or {}))
      if 'bindings' in bars_o:
        # allow direct replacement of bindings
        bars_b['bindings'] = list(bars_o['bindings'])
      pval['bars'] = bars_b

      # optional safe bindingText.template override if allowedKeys present
      bt_b = pval.get('bindingText')
      bt_o = o.get('bindingText')
      if bt_b and bt_o and 'template' in bt_o:
        allowed = bt_b.get('allowedKeys', [])
        _validate_template_keys(bt_o['template'], allowed)
        pval['bindingText'] = dict(bt_b)
        pval['bindingText']['template'] = bt_o['template']
    prisms_b[pkey] = pval

  result['prisms'] = prisms_b
  return result


##################### Bar operations ##################### 

# ------------------------- Op Registry -------------------------

# We do not expose getattr on user strings. Instead, we map declarative ops to small adapters.

@dataclass(frozen=True)
class BarOp:
  name: str
  fn: Callable[..., Any]
  accepts_arg: bool = False

# Adapter to coerce binding dicts into the tuple that EnoPrismBars.add* expect: (label, color, width)

def _binding_to_tuple(binding: Dict[str, Any], *,
            label: str,
            color_rgba: Tuple[int, int, int, int],
            width: float) -> Tuple[str, Tuple[int,int,int,int], float]:
  return (label, color_rgba, width)

# Registry is exposed as an immutable mapping

def build_op_registry():
  def addL( epb: EnoPrismBars, item: Tuple[str, Tuple[int,int,int,int], float]):           epb.addBarL(item)
  def addL2(epb: EnoPrismBars, item: Tuple[str, Tuple[int,int,int,int], float]):           epb.addBarL2(item)
  def addL3(epb: EnoPrismBars, item: Tuple[str, Tuple[int,int,int,int], float], arg: Any): epb.addBarL3(item, arg)
  ops = {
    'addL':  BarOp('addL',  addL,  accepts_arg=False),
    'addL2': BarOp('addL2', addL2, accepts_arg=False),
    'addL3': BarOp('addL3', addL3, accepts_arg=True),
  }
  from types import MappingProxyType
  return MappingProxyType(ops)

BAR_OPS = build_op_registry()

##################### Role Specification ##################### 

@dataclass(frozen=True)
class RoleSpec:
  params: Dict[str, Any] = field(default_factory=dict)
  op: Optional[str] = None
  # ops: sequence steps like [{kind: addL3, take: 3, arg: 65}, {kind: addL2}]
  ops: Optional[List[Dict[str, Any]]] = None
  set_attrs: Dict[str, Any] = field(default_factory=dict)

##################### Enodia Prisms Details ##################### 

class EnoPrismsDetails(AtaBase):
  """
  Construct with:
    EnoPrismsDetails(base_yaml='prismsAcmTei01bb.yaml', overlay_yaml='prismsAcmTei01bo.yaml')
  The instance exposes summonPrism(whichPrism, whichSlot), update(), draw(screen)
  and serves as a drop-in domain provider for EnoPrisms.
  """

  def __init__(self, base_yaml: str, overlay_yaml: Optional[str] = None, **kwargs):
    self.__dict__.update(kwargs)
    self.base_yaml = base_yaml
    self.overlay_yaml = overlay_yaml

    with open(base_yaml, 'r', encoding='utf-8') as f:
      base_cfg = yaml.safe_load(f)
    overlay_cfg = None
    if overlay_yaml:
      with open(overlay_yaml, 'r', encoding='utf-8') as f:
        overlay_cfg = yaml.safe_load(f)

    self.cfg = _merge_overlay_into_base(base_cfg, overlay_cfg or {})

    # State
    self.activePrisms: List[Any] = []
    self.bars: List[Any] = []
    self.initialized = False

    # Pull shared tables
    self.colors  = dict(self.cfg.get('colors', {}))
    self.scalars = dict(self.cfg.get('scalars', {}))

    # Summon bindings from base if present
    self._summon_map = {}
    for sb in (self.cfg.get('summon_bindings') or []):
      self._summon_map[(str(sb['prism']), int(sb['slot']))] = str(sb.get('use', sb['prism']))

    # Background actors from base
    self.background = self.cfg.get('background_bars', {})

  # ---------------- helpers ----------------
  def _norm_params(self, params: Dict[str, Any]) -> Dict[str, Any]:
    if not params: return {}
    p = dict(params)
    # Normalize pathMaxDxy → pathMaxDx + pathMaxDy
    if 'pathMaxDxy' in p and (('pathMaxDx' not in p) and ('pathMaxDy' not in p)):
      dx, dy = p.pop('pathMaxDxy')
      p['pathMaxDx'] = dx
      p['pathMaxDy'] = dy
    # Convert lists to tuples where appropriate
    for key in ('textOffset2', 'basePos'):
      if key in p: p[key] = _to_tuple(p[key])
    return p

  def _build_bars_for_prism(self, prism_key: str, prism_cfg: Dict[str, Any]):
    roles_cfg = ((prism_cfg.get('bars') or {}).get('roles') or {})
    result = {}
    for role_name, role_dict in roles_cfg.items():
      rs = RoleSpec(
        params = self._norm_params(role_dict.get('params')),
        op   = role_dict.get('op'),
        ops  = role_dict.get('ops'),
        set_attrs = role_dict.get('set_attrs') or {}
      )
      epb = EnoPrismBars(**rs.params)
      for ak, av in rs.set_attrs.items(): setattr(epb, ak, av)
      result[role_name] = (rs, epb)
    return result

  def _build_parse_grid(self, prism_cfg: Dict[str, Any]):
    pg = prism_cfg.get('parseGrid') or {}
    # Normalize rowsCols and xy0
    rows, cols = pg.get('rows', None), pg.get('cols', None)
    if rows is None or cols is None:
      rc = pg.get('rowsCols')
      if rc and len(rc) == 2:
        rows, cols = int(rc[0]), int(rc[1])
    x0, y0 = pg.get('x0', None), pg.get('y0', None)
    if x0 is None or y0 is None:
      xy0 = pg.get('xy0')
      if xy0 and len(xy0) == 2:
        x0, y0 = int(xy0[0]), int(xy0[1])
    pixDim = pg.get('pixDim')
    verbose = bool(pg.get('verbose', False))

    epg = EnoParseGrid(rows=rows, cols=cols, x0=x0, y0=y0, pixDim=_to_tuple(pixDim), verbose=verbose)
    gb = prism_cfg.get('gridBindings') or pg.get('gridBindings')
    if gb: epg.setGridBindings(list(gb))
    return epg

  def _render_label(self, prism_cfg: Dict[str, Any], binding: Dict[str, Any]) -> str:
    bt = prism_cfg.get('bindingText') or {}
    template = bt.get('template', '{label}')
    allowed  = bt.get('allowedKeys', list(binding.keys()))
    _validate_template_keys(template, allowed)
    return template.format_map(_SafeMap(binding))

  def _resolve_color(self, name: str) -> Tuple[int,int,int,int]:
    val = self.colors.get(name)
    if not val:
      raise KeyError(f"Color '{name}' not found in base colors table")
    if isinstance(val, list): val = tuple(val)
    return val

  def _choose_color_for_role(self, prism_cfg: Dict[str, Any], role: str, binding: Dict[str, Any]) -> Tuple[int,int,int,int]:
    cs = prism_cfg.get('colorStrategy') or {}
    mode = cs.get('mode', 'single')
    if mode == 'dual':
      field = cs.get('field', 'colors')
      roleIdx = cs.get('roleIndex', { 'upper': 0, 'lower': 1 })
      idx = int(roleIdx.get(role, 0))
      name = (binding.get(field) or [None, None])[idx]
      return self._resolve_color(name)
    else:
      name = binding.get('color')
      return self._resolve_color(name)

  def _binding_width(self, binding: Dict[str, Any]) -> float:
    # We standardize on 'firstWidth' key in bindings
    w = binding.get('firstWidth')
    if w is None:
      raise ValueError("Binding missing 'firstWidth'")
    return float(w)

  def _apply_ops(self, epb: EnoPrismBars, role_spec: RoleSpec, items: List[Tuple[str, Tuple[int,int,int,int], float]]):
    # Single op case
    if role_spec.op:
      op = BAR_OPS.get(role_spec.op)
      if not op:
        raise ValueError(f"op '{role_spec.op}' is not permitted")
      for it in items:
        if op.accepts_arg:
          # No arg given in single-op mode; treat as missing arg
          raise ValueError(f"op '{op.name}' requires an argument; use ops sequence")
        op.fn(epb, it)
      return
    # Sequence case
    if role_spec.ops:
      idx = 0
      n = len(items)
      for step in role_spec.ops:
        kind = step['kind']
        op = BAR_OPS.get(kind)
        if not op:
          raise ValueError(f"ops.kind '{kind}' is not permitted")
        take = int(step.get('take', n - idx))
        arg = step.get('arg', None)
        for _ in range(max(0, min(take, n - idx))):
          it = items[idx]
          if op.accepts_arg:
            op.fn(epb, it, arg)
          else:
            op.fn(epb, it)
          idx += 1
      # If any items remain, ignore or append with last op? For safety, ignore silently.
      return
    # If neither provided, nothing to add.

  # ---------------- API expected by EnoPrisms ----------------
  def summonPrism(self, whichPrism: str, whichSlot: int):
    try:
      key = self._summon_map.get((whichPrism, whichSlot))
      if key is None:
        if 'prisms' in self.cfg and whichPrism in self.cfg['prisms']:
          key = whichPrism
      else: return None

      pcfg = self.cfg['prisms'][key]
      bars_roles = self._build_bars_for_prism(key, pcfg)  # { role: (RoleSpec, EnoPrismBars) }

      # Build binding items once, then feed to roles
      bindings = ((pcfg.get('bars') or {}).get('bindings') or [])
      items_by_role = {}
      for role, (rs, epb) in bars_roles.items():
        items = []
        for b in bindings:
          label = self._render_label(pcfg, b)
          color = self._choose_color_for_role(pcfg, role, b)
          width = self._binding_width(b)
          items.append(_binding_to_tuple(b, label=label, color_rgba=color, width=width))
        self._apply_ops(epb, rs, items)
        items_by_role[role] = epb

      # Assemble prism
      prismBars = [epb for _, epb in items_by_role.items()]
      epg = self._build_parse_grid(pcfg)
      ep = EnoPrism(prismBars=prismBars, prismName=key, parseGrid=epg)
      self.activePrisms.append(ep)
      return ep
    except Exception:
      self.err("summonPrism")
      return None

  ### Setup ###

  def setup(self):
    try:
      self.bars = []
      for name, bd in (self.background or {}).items():
        img = bd['image']
        pos = _to_tuple(bd.get('bottomleft', (0,0)))
        actor = EnoActor(img, bottomleft=pos, name=bd.get('name', name))
        if 'scale' in bd: actor.scaleV(float(bd['scale']))
        self.bars.append(actor)
    except Exception:
      self.err("init")

  ### update ###

  def update(self):
    if not self.initialized:
      self.setup(); self.initialized = True

  ### Draw ###

  def draw(self, screen):
    if self.activePrisms is None: return
    try:
      for bar in self.bars: bar.draw(screen)
      # Prism path drawing left to prism objects as before.
    except Exception:
      self.err("draw")

### end ###
