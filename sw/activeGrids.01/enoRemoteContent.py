# Enodia Remote Content
# Brygg Ullmer, Clemson University and CoPilot
# Begun 2026-03-31

import os, json, hashlib, datetime
from pathlib import Path
import requests, certifi
from ataBase import AtaBase

class EnoRemoteContent(AtaBase):
  """
  Retrieve remote content with:
    - explicit TLS policy
    - byte-exact raw preservation
    - cryptographic integrity (SHA-256)
    - explicit normalized derivatives for usability
    - persistent provenance logging
  """

  cacheRoot  = "images/cache/"
  objectRoot = ".objects/"
  trustLogFn = "trust_decisions.json"

  url      = None
  localFn    = None    # human-legible filename
  expectedSha256 = None
  trustPolicy  = None
  riskClass    = "passive_visual"
  allowInsecure  = False

  ################# constructor #################

  def __init__(self, **kwargs):
    self.__dict__.update(kwargs)
    super().__init__()

  ############### stage ###############

  def stage(self):
    try:
      content = self.fetch()
      sha = self.computeHash(content)

      if self.expectedSha256 and sha != self.expectedSha256:
        raise ValueError("hash mismatch: content integrity failure")

      objPath = self.storeRaw(content, sha)
      derivInfo = self.writeNormalizedDerivative(content)

      self.logTrustDecision(sha, derivInfo)
      return True

    except Exception:
      self.err("stage")
      return False

  ############### fetch ###############

  def fetch(self) -> bytes:
    try:
      self.msg(f"fetch: {self.url}")
      return self.fetchStrict()
    except requests.exceptions.SSLError:
      if self.allowInsecure:
        self.msg("fetch: TLS failure permitted by policy")
        return self.fetchInsecure()
      raise

  ############### fetch strict ###############

  def fetchStrict(self) -> bytes:
    r = requests.get(self.url, timeout=10, verify=certifi.where())
    r.raise_for_status()
    return r.content

  ############### fetch insecure ###############

  def fetchInsecure(self) -> bytes:
    r = requests.get(self.url, timeout=10, verify=False)
    r.raise_for_status()
    return r.content

  ############### integrity###############

  def computeHash(self, content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()

  ############### storage ###############

  def storeRaw(self, content: bytes, sha: str) -> Path:
    cacheDir = Path(self.cacheRoot)
    objDir   = cacheDir / self.objectRoot / sha[:2]
    objPath  = objDir / sha

    objDir.mkdir(parents=True, exist_ok=True)
    cacheDir.mkdir(parents=True, exist_ok=True)

    if not objPath.exists():
      objPath.write_bytes(content)

    return objPath

  ############### normalization ###############

  def writeNormalizedDerivative(self, content: bytes):
    """
    Writes a tool-compatible derivative if a known format
    with a prefixed header is detected.

    Returns a dict describing derivation, or None.
    """

    sigs = [
      ("jpeg", b"\xFF\xD8"),
      ("png",  b"\x89PNG\r\n\x1a\n"),
      ("pdf",  b"%PDF-"),
    ]

    for fmt, sig in sigs:
      idx = content.find(sig)
      if idx == -1:
        continue

      if idx == 0:
        # canonical already
        Path(self.cacheRoot, self.localFn).write_bytes(content)
        self.msg(f"stored canonical {fmt}: {self.localFn}")
        return {
          "format": fmt,
          "prefix_bytes": 0,
          "derivation": "none"
        }

      # prefixed but repairable
      normalized = content[idx:]
      outPath = Path(self.cacheRoot) / self.localFn
      if not outPath.exists():
        outPath.write_bytes(normalized)

      self.msg(
        f"non-canonical {fmt}: stripped {idx} prefix bytes "
        f"→ wrote normalized derivative"
      )

      return {
        "format": fmt,
        "prefix_bytes": idx,
        "derivation": "prefix_stripped"
      }

    # unknown format
    self.msg("unknown or unsupported format; no derivative written")
    return None

  ############### provenance ###############

  def logTrustDecision(self, sha: str, derivInfo):
    tlp = Path(self.cacheRoot) / self.trustLogFn
    log = json.loads(tlp.read_text()) if tlp.exists() else {}

    log[self.url] = {
      "sha256": sha,
      "local_fn": self.localFn,
      "risk_class": self.riskClass,
      "trust_policy": self.trustPolicy,
      "allow_insecure": self.allowInsecure,
      "derivation": derivInfo,
      "timestamp": datetime.datetime.now().isoformat()
    }

    tlp.write_text(json.dumps(log, indent=2))

### end ###
