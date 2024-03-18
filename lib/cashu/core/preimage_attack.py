import hashlib

from cashu.core.crypto.secp import PublicKey


def hash_to_curve_has_multiple_preimages(message_str: str) -> bool:
    """Generates a point from the message hash and checks if the point lies on the curve.
    If it does not, iteratively tries to compute a new point from the hash."""
    point = None
    msg_to_hash = message_str.encode("ascii")
    while point is None:
        _hash = hashlib.sha256(msg_to_hash).digest()
        try:
            point = PublicKey(b"\x02" + _hash, raw=True)
        except Exception:
            msg_to_hash = _hash
            try:
                message_str.encode("ascii")
            except Exception:
                return True
    return False


# # brute force all random strings of length 1-10
# for i in range(1, 11):
#     for si, s in enumerate(itertools.product(string.printable, repeat=i)):
#         s = "".join(s)
#         if si % 100000 == 0:
#             print(f"length: {i} iteration: {si} string: {s}")
#         if hash_to_curve_has_multiple_preimages(s):
#             print(s)
#             break
