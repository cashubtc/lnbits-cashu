import hashlib
from typing import Tuple

from secp import PrivateKey, PublicKey


def hash_to_curve(message: bytes) -> PublicKey:
    """Generates a point from the message hash and checks if the point lies on the curve.
    If it does not, iteratively tries to compute a new point from the hash."""
    point = None
    msg_to_hash = message
    while point is None:
        _hash = hashlib.sha256(msg_to_hash).digest()
        try:
            # will error if point does not lie on curve
            point = PublicKey(b"\x02" + _hash, raw=True)
        except Exception:
            msg_to_hash = _hash
    return point


class BobKeys:
    w: PrivateKey = PrivateKey(hashlib.sha256(b"w").digest())
    w_: PrivateKey = PrivateKey(hashlib.sha256(b"w_").digest())
    x0: PrivateKey = PrivateKey(hashlib.sha256(b"x0").digest())
    x1: PrivateKey = PrivateKey(hashlib.sha256(b"x1").digest())
    ya: PrivateKey = PrivateKey(hashlib.sha256(b"ya").digest())

    # generators
    Gv: PublicKey = hash_to_curve("Gv".encode())
    Gw: PublicKey = hash_to_curve("Gw".encode())
    Gw_: PublicKey = hash_to_curve("Gw_".encode())
    Gx0: PublicKey = hash_to_curve("Gx0".encode())
    Gx1: PublicKey = hash_to_curve("Gx1".encode())
    Ga: PublicKey = hash_to_curve("Ga".encode())
    Gg: PublicKey = hash_to_curve("Gg".encode())

    Cw: PublicKey
    Is: PublicKey
    iparams: Tuple[PublicKey, PublicKey]

    def __init__(self):
        self.Cw = self.Gw.mult(self.w) + self.Gw_.mult(self.w_)
        self.Is = self.Gv - (
            self.Gx0.mult(self.x0) + self.Gx1.mult(self.x1) + self.Ga.mult(self.ya)
        )
        print("Bob")
        print("Cw", self.Cw.serialize().hex())
        print("I", self.I.serialize().hex())

        self.iparams = (self.Cw, self.Is)


def step1_alice(a: PrivateKey, Gg: PublicKey, Gh: PublicKey):
    r = PrivateKey()
    Ma: PublicKey = Gg.mult(a) + Gh.mult(r)
    print("Alice")
    print("Ma", Ma.serialize().hex())
    return Ma


def step2_bob(Ma: PublicKey, bob: BobKeys):
    # compute MAC key
    t: PrivateKey = PrivateKey(hashlib.sha256(b"t").digest())
    assert t.private_key
    hash_to_curve(t.private_key.hex().encode())
    #  bob.Gw.mult(bob.w) + (bob.x0 + bob.x1)

    print("Bob")
    print("t", t.private_key.hex())


# def step3_


def main():
    bob = BobKeys()
    a = PrivateKey(bytes([0] * 31 + [1]))
    Ma = step1_alice(a, bob.Gg, bob.Gw)
    step2_bob(Ma, bob)


if __name__ == "__main__":
    main()
