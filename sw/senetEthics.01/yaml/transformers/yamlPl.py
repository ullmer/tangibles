### yaml to prolog transformer 
# by brygg ullmer (clemson) and copilot
# begun 2026-03-24

import yaml

# Convert Python list to Prolog list syntax
def emit_theme_abbrev(key, themes):
  items = ", ".join(themes)
  return f"themeAbbrev({key}) := [{items}]."

def yaml_to_prolog_dsl(path):
  with open(path, "r") as f:
    data = yaml.safe_load(f)

  cats = data["categories"]
  lines = []

  for key, obj in cats.items():
    themes = list(obj["themes"].keys())
    lines.append(emit_theme_abbrev(key, themes))

  return "\n".join(lines)

if __name__ == "__main__":
  print(yaml_to_prolog_dsl("figures_themes03.yaml"))

### end ###
