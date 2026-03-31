# Enodia Remote Content
# Brygg Ullmer, Clemson University and CoPilot
# Begun 2026-03-31

import os, json, ssl, hashlib, datetime
from pathlib import Path
import requests
import certifi
from ataBase import AtaBase

class EnoRemoteContent(AtaBase):
  """
  Responsible for retrieving remote content with:
  - explicit TLS policy
  - content integrity verification
  - persistent provenance logging
  """

  cacheRoot    = "images/cache/"
  objectRoot   = ".objects/"
  trustLogFn   = "trust_decisions.json"

  url            = None
  localFn        = None    # human-legible filename
  expectedSha256 = None
  trustPolicy    = None
  riskClass      = "passive_visual"

  allowInsecure  = False   # must be enabled *by policy*, never implicitly

  ################# constructor #################

  def __init__(self, **kwargs):
    self.__dict__.update(kwargs)
    super().__init__()

  ################# stage #################

  def stage(self):
    try:
      content = self.fetch()
      sha = self.computeHash(content)

      if self.expectedSha256:
        if sha != self.expectedSha256:
          raise ValueError("hash mismatch: content integrity failure")

      self.store(content, sha)
      self.logTrustDecision(sha)
      return True

    except: self.err("stage"); return False

  ################# fetch #################

  def fetch(self) -> bytes:
    try:
      self.msg(f"fetch: {self.url}")
      return self.fetchStrict()

    except requests.exceptions.SSLError as e:
      if self.allowInsecure:
        self.msg("fetch: TLS failure permitted by policy")
        return self.fetchInsecure()
      raise

  def fetchStrict(self) -> bytes:
    r = requests.get(self.url,
             timeout=10,
             verify=certifi.where())
    r.raise_for_status()
    return r.content

  def fetchInsecure(self) -> bytes:
    r = requests.get(self.url,
             timeout=10,
             verify=False)
    r.raise_for_status()
    return r.content

  # ---------- integrity ----------

  def computeHash(self, content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()

  # ---------- storage ----------

  def store(self, content: bytes, sha: str):
    cacheDir = Path(self.cacheRoot)
    objDir   = cacheDir / self.objectRoot / sha[:2]
    objPath  = objDir / sha
    linkPath = cacheDir / self.localFn

    objDir.mkdir(parents=True, exist_ok=True)
    cacheDir.mkdir(parents=True, exist_ok=True)

    if not objPath.exists():
      objPath.write_bytes(content)

    # controlled naming for human legibility
    if not linkPath.exists():
      linkPath.symlink_to(objPath)

    self.msg(f"stored: {linkPath}")

  # ---------- provenance ----------

  def logTrustDecision(self, sha: str):
    tlp = Path(self.cacheRoot) / self.trustLogFn
    if tlp.exists():
      log = json.loads(tlp.read_text())
    else:
      log = {}

    log[self.url] = {
      "sha256": sha,
      "local_fn": self.localFn,
      "risk_class": self.riskClass,
      "trust_policy": self.trustPolicy,
      "allow_insecure": self.allowInsecure,
      "timestamp": datetime.datetime.now().isoformat()
    }

    tlp.write_text(json.dumps(log, indent=2))

### end ###
