from __future__ import annotations

import hashlib
import hmac
import math
import numbers


def canonical_identifier(value: object) -> str:
    """Canonicalize identifiers so numeric Excel representations link reliably."""
    if isinstance(value, numbers.Integral):
        return str(int(value))
    if isinstance(value, numbers.Real):
        x = float(value)
        if math.isfinite(x) and x.is_integer():
            return str(int(x))
    return str(value).strip()


def hmac_pseudonym(value: object, key: bytes, namespace: str, length: int = 32) -> str:
    """Return a deterministic keyed pseudonym.

    HMAC is used instead of a plain/unsalted hash because university IDs live
    in a relatively small, guessable domain. The secret key must be stored
    separately from any public release.
    """
    message = f"{namespace}:{canonical_identifier(value)}".encode("utf-8")
    digest = hmac.new(key, message, hashlib.sha256).hexdigest()
    return f"{namespace}_{digest[:length]}"
