"""Key generators for CMAT pseudonymization demonstrations.

The seeded generator is intentionally reproducible and is ONLY for examples,
not for production secrets. Real HMAC keys must be generated from a
cryptographically secure random source and stored outside Git.
"""

from __future__ import annotations

import random
import secrets


def generate_seeded_demo_key(seed: int | str) -> str:
    """Return a reproducible 64-hex-character demonstration key.

    This function uses ``random.Random`` so that the same seed gives the same
    demonstration key. Because the seed may be known or guessable, the result
    must never be used as a real research-data secret.
    """
    rng = random.Random(seed)
    return rng.getrandbits(256).to_bytes(32, "big").hex()


def generate_secure_key() -> str:
    """Return a 256-bit random key encoded as 64 hexadecimal characters.

    This is the appropriate pattern for a real HMAC secret. The returned text
    should be stored separately from Git and from released datasets.
    """
    return secrets.token_hex(32)


if __name__ == "__main__":
    demo_seed = "CMAT-demo-2026"
    print("Demo key (seeded; DO NOT use in production):")
    print(generate_seeded_demo_key(demo_seed))
    print("\nSecure key (random; store outside Git):")
    print(generate_secure_key())
