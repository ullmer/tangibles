### yaml to prolog transformer
# by brygg ullmer (clemson) and copilot
# begun 2026-03-24

import yaml, sys

try:    yfn = sys.argv[1]
except: print("expect filename as argument"); sys.exit(-1)

# Convert Python list to Prolog list syntax
# Two-space indentation preserved per BU preference

def emit_list(lst):
  items = ", ".join(lst)
  return f"[{items}]"

def emit_theme_abbrev(key, themes):
  return f"themeAbbrev({key}) := {emit_list(themes)}."

# --- New helpers for PEOPLE section ---

def camelize(s):
  """Convert YAML names like 'Arthur Sze' into camelCase atoms: arthurSze"""
  parts = str(s).replace('-', ' ').replace('_',' ').split()
  if not parts:
    return ""
  first = parts[0].lower()
  rest = ''.join(p.capitalize() for p in parts[1:])
  return first + rest

def emit_person_abbrev(person_key, person_dict):
  name_atom = camelize(person_dict.get('name', person_key))
  abbrev = person_dict.get('abbrev', person_key)
  return f"personAbbrev({name_atom}, {abbrev.lower()})."

def emit_person_domains(person_key, person_dict):
  name_atom = camelize(person_dict.get('name', person_key))
  domains = person_dict.get('domains', [])
  # camelCase each domain
  doms = [camelize(d) for d in domains]
  return f"personDomains({name_atom}) := {emit_list(doms)}."

def emit_person_themes(person_key, person_dict):
  name_atom = camelize(person_dict.get('name', person_key))
  themes = person_dict.get('themes', [])
  return f"personThemes({name_atom})  := {emit_list(themes)}."

# --- Main YAML to Prolog transformation ---

def yaml_to_prolog_dsl(path):
  with open(path, "r") as f:
    data = yaml.safe_load(f)

  lines = []

  # --- categories (themes) ---
  cats = data.get("categories", {})
  for key, obj in cats.items():
    themes = list(obj.get("themes", {}).keys())
    lines.append(emit_theme_abbrev(key, themes))

  # --- people ---
  people = data.get("people", {})
  for pkey, pobj in people.items():
    lines.append(emit_person_abbrev(pkey, pobj))
    lines.append(emit_person_domains(pkey, pobj))
    lines.append(emit_person_themes(pkey, pobj))
    lines.append('')

  return "\n".join(lines)

if __name__ == "__main__":
  print(yaml_to_prolog_dsl(yfn))
### end ###
