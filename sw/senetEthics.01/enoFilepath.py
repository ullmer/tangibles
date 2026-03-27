# Enodia OS supports
# Brygg Ullmer, Clemson University and CoPilot
# Begun 2026-03-25

from pathlib import Path

############# filepat exists #############

def filepatExists(filepath: str) -> bool:
  p      = Path(filepath)
  result = any(p.parent.glob(p.stem + ".*")) #allow any extension
  return result

### end ###

