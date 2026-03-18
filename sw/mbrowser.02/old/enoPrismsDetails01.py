# enoPrismsDetails.py — YAML-driven variant of EnoPrismsTei
# Brygg Ullmer, Clemson University — refactor scaffold by Copilot (2026-03-16)

from ataBase import *
from enoActor import *
from enoPrism import *
from enoPrismBar import *
from enoPrismBars import *
from enoParseGrid import *

import os
from typing import Any, Dict, List, Tuple

try:
    import yaml
except Exception as e:
    raise RuntimeError("PyYAML is required to use enoPrismsDetails") from e

def _to_tuple(v):
    if isinstance(v, list):
        return tuple(_to_tuple(x) for x in v)
    return v

def _deep_resolve(value, resolver):
    if isinstance(value, dict):
        return {k: _deep_resolve(v, resolver) for k, v in value.items()}
    elif isinstance(value, list):
        return [ _deep_resolve(v, resolver) for v in value ]
    elif isinstance(value, str):
        return resolver(value)
    else:
        return value

class EnoPrismsDetails(AtaBase):
    """
    YAML-configurable drop-in for EnoPrismsTei. Construct with
        EnoPrismsDetails('yaml/prismsAcmTei01.yaml')
    and it will expose summonPrism/update/draw consistent with the
    hard-coded class.
    """
    def __init__(self, yaml_path:str, **kwargs):
        self.__dict__.update(kwargs)
        self.yaml_path = yaml_path
        with open(yaml_path, 'r', encoding='utf-8') as f:
            self.cfg = yaml.safe_load(f)

        # State
        self.activePrisms: List[Any] = []
        self.bars: List[Any] = []
        self.parseTouchByPrism: Dict[str, Any] = {}
        self.initialized = False

        # Expose globals & colors as attributes for parity with prior code
        self.globals = dict(self.cfg.get('globals', {}))
        self.colors  = {k: tuple(v) for k, v in (self.cfg.get('colors', {}) or {}).items()}
        for k, v in self.globals.items(): setattr(self, k, v)
        for k, v in self.colors.items():   setattr(self, k, v)

        # Build summon map: (prism, slot) -> key under prisms
        self._summon_map = {}
        for m in (self.cfg.get('summon_bindings') or []):
            self._summon_map[(str(m['prism']), int(m['slot']))] = str(m.get('use', m['prism']))

    # ---------------- helpers ----------------
    def _resolve_token(self, s:str):
        if isinstance(s, str) and s.startswith('$'):
            name = s[1:]
            if name in self.globals: return self.globals[name]
            if name in self.colors:  return self.colors[name]
            raise KeyError(f"Unknown token {s} in {self.yaml_path}")
        return s

    def _resolve(self, obj):
        return _deep_resolve(obj, self._resolve_token)

    def _build_bars(self, bar_defs:List[Dict[str, Any]]):
        bars = []
        for bd in bar_defs:
            params  = self._resolve(bd.get('params', {}))
            params  = {k: (_to_tuple(v) if isinstance(v, (list,)) else v) for k,v in params.items()}
            epb = EnoPrismBars(**params)

            # attributes to set post-init
            set_attrs = self._resolve(bd.get('set_attrs', {})) or {}
            for ak, av in set_attrs.items():
                setattr(epb, ak, av)

            bindings = self._resolve(bd.get('bindings', []))

            # Execute either single method for all bindings, or a sequence
            if 'add_sequence' in bd:
                seq = bd['add_sequence']
                idx = 0
                for step in seq:
                    method = getattr(epb, step['method'])
                    cnt    = int(step.get('count', len(bindings) - idx))
                    extra  = self._resolve(step.get('args', []))
                    for _ in range(cnt):
                        b = bindings[idx]
                        method(b, *extra)
                        idx += 1
            else:
                mname = bd.get('bindings_method', 'addBarL')
                method = getattr(epb, mname)
                for b in bindings:
                    method(b)

            bars.append(epb)
        return bars

    def _build_prism(self, key:str):
        pd = self.cfg['prisms'][key]
        prismName = pd.get('prismName', key)

        pb = self._build_bars(pd.get('bars', []))

        # Parse grid
        pg = self._resolve(pd.get('parseGrid', {}))
        epg = EnoParseGrid(**{k: (_to_tuple(v) if isinstance(v, list) else v) for k,v in pg.items() if k not in ('gridBindings',)})
        if 'gridBindings' in pg:
            epg.setGridBindings(pg['gridBindings'])

        ep = EnoPrism(prismBars=pb, prismName=prismName, parseGrid=epg)
        return ep

    # ---------------- API expected by EnoPrisms ----------------
    def summonPrism(self, whichPrism:str, whichSlot:int):
        try:
            key = self._summon_map.get((whichPrism, whichSlot))
            if key is None:
                return None
            p = self._build_prism(key)
            self.activePrisms.append(p)
            return p
        except Exception:
            self.err("summonPrism")
            return None

    def setup(self):
        try:
            bys = self.globals.get('barYShift')
            self.bars = []
            for bd in (self.cfg.get('background_bars') or []):
                bd = self._resolve(bd)
                img = bd['image']
                pos = _to_tuple(bd.get('bottomleft', (0,0)))
                name = bd.get('name', img)
                actor = EnoActor(img, bottomleft=pos, name=name)
                if 'scale' in bd:
                    actor.scaleV(float(bd['scale']))
                self.bars.append(actor)
        except Exception:
            self.err("init")

    def update(self):
        if not self.initialized:
            self.setup(); self.initialized = True

    def draw(self, screen):
        if self.activePrisms is None: return
        try:
            for bar in self.bars:
                bar.draw(screen)
            # Parity with original class: prism path drawing was commented out
            # for prism in self.activePrisms:
            #     for ppath in prism:
            #         if ppath is not None: ppath.draw(screen)
        except Exception:
            self.err("draw")
