# Enodia OS supports
# Brygg Ullmer, Clemson University and CoPilot
# Begun 2026-03-25

from pathlib import Path
import traceback
import requests
import certifi

############# filepat exists #############

def filepatExists(filepath: str) -> bool:
  p      = Path(filepath)
  result = any(p.parent.glob(p.stem + "*")) #allow any extension
  return result

############# filepat exists #############

def downloadRemote(url: str, localPath: str) -> bool:
  try:
    #url = "https://example.com/path/to/image.png"
    #local_path = "image.png"

    if filepatExists(localPath): 
      #self.msg("downloadRemote: file present, ignoring"); return None
      print("downloadRemote: file present, ignoring"); return None

    response = requests.get(url, timeout=10, verify=certifi.where())

    response.raise_for_status()  # Ensures HTTP errors raise an exception

    with open(local_path, "wb") as f: f.write(response.content)

    #if self.verbose: self.msg("downloaded to " + localPath)
  except:
    #self.err("downloadRemote")
    print("downloadRemote error:")
    traceback.print_exc(); 

### end ###

