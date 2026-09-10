"""Privacy-preserving identifier helpers.

The functions in this module canonicalize identifiers and derive deterministic
HMAC-based pseudonyms for controlled or public releases. They do not encrypt
source data and do not manage secret-key storage.
"""

from __future__ import annotations

import hashlib
import hmac
import math
import numbers

__all__ = ["canonical_identifier", "hmac_pseudonym"]


def canonical_identifier(value: object) -> str:
    """Convert an identifier to a stable textual representation.

    Parameters
    ----------
    value : object
        Identifier value to canonicalize. Integral numeric values and finite
        real values with zero fractional part are rendered as integers; other
        values are stripped after conversion to text.

    Returns
    -------
    str
        Canonical textual identifier suitable for deterministic linkage.

    Notes
    -----
    This normalization is designed primarily for identifiers imported from
    spreadsheets, where the same identifier may appear as an integer, a float
    with a zero fractional part, or a string.
    """
    if isinstance(value, numbers.Integral):
        return str(int(value))
    if isinstance(value, numbers.Real):
        x = float(value)
        if math.isfinite(x) and x.is_integer():
            return str(int(x))
    return str(value).strip()


def hmac_pseudonym(value: object, key: bytes, namespace: str, length: int = 32) -> str:
    """Create a deterministic keyed pseudonym for an identifier.

    Parameters
    ----------
    value : object
        Identifier to pseudonymize. The value is first normalized with
        :func:`canonical_identifier`.
    key : bytes
        Secret HMAC key. It must be stored separately from released data.
    namespace : str
        Domain-separation label, such as ``"stu"`` or ``"prof"``. The label
        is incorporated into both the HMAC message and returned pseudonym.
    length : int, default=32
        Number of hexadecimal digest characters retained after the namespace
        prefix.

    Returns
    -------
    str
        Pseudonym in the form ``"<namespace>_<digest-prefix>"``.

    Notes
    -----
    HMAC-SHA256 is used instead of an unsalted hash because university
    identifiers commonly occupy a relatively small and guessable domain.
    Determinism supports stable linkage across authorized datasets, but the
    function does not provide encryption or key management.
    """
    message = f"{namespace}:{canonical_identifier(value)}".encode("utf-8")
    digest = hmac.new(key, message, hashlib.sha256).hexdigest()
    return f"{namespace}_{digest[:length]}"
