import random
from typing import Optional, Tuple

G128 = (
    int("6B17D1F2E12C4247F8BCE6E563A440F277037D812DEB33A0F4A13945D898C296", 16),
    int("4FE342E2FE1A7F9B8EE7EB4A7C0F9E162CBCE33576B315ECECBB6406837BF51F", 16)
)
p128 = 2**128 - 2**97 - 1
a128 = -3
b128 = int("E87579C11079F43DD824993C2CEE5ED3", 16)

Point = Optional[Tuple[int, int]]
class EllipticCurve:
    def __init__(self, a : int=a128, b : int=b128, p : int=p128):
        """
        Elliptic curve: y^2 = x^3 + ax + b (mod p).
        """
        self.a = a
        self.b = b
        self.p = p

    def is_on_curve(self, x : int, y : int)-> bool:
        return (y**2 - (x**3 + self.a * x + self.b)) % self.p == 0

def point_addition(P : Point, Q : Point, curve : EllipticCurve) -> Point | None:
    if P is None: return Q
    if Q is None: return P

    x1, y1 = P
    x2, y2 = Q

    if x1 == x2:
        if (y1 != y2): return None
        else: return point_doubling(P, curve)
    
    m = ((y2 - y1) * pow(x2 - x1, -1, curve.p)) % curve.p
    x3 = (m**2 - x1 - x2) % curve.p
    y3 = (m * (x1 - x3) - y1) % curve.p
    return (x3, y3)  # Return new point

def point_doubling(P : Point, curve : EllipticCurve):
    if P is None: return None
    
    x, y = P

    m = ((3 * x**2 + curve.a) * pow(2 * y, -1, curve.p)) % curve.p
    x3 = (m**2 - 2 * x) % curve.p
    y3 = (m * (x - x3) - y) % curve.p
    return (x3, y3)  # Return new point

def scalar_multiplication(k : int, P : Point, curve : EllipticCurve) -> Point | None:
    """
    k * P on the elliptic curve using the double-and-add algorithm.
    """
    if k == 0 or P is None:  return None

    result = None  # Start with the point at infinity
    addend = P

    while k:
        if k & 1:  # if bit of k == 1
            result = point_addition(result, addend, curve)
        addend = point_doubling(addend, curve)
        k >>= 1  # divide by 2

    return result

def generate_keys(curve : EllipticCurve, G : Point=G128) -> Tuple[int, Point]:
    d = random.randint(1, curve.p - 1)
    Q = scalar_multiplication(d, G, curve)
    return d, Q

def gen_keystream(seed: int, length: int) -> bytes:
    keystream = bytearray()

    a = 1664525
    c = 1013904223
    m = 2**32
    
    current_seed = seed
    for _ in range(length):
        current_seed = (a * current_seed + c) % m
        keystream.append(current_seed & 0xFF)
    return bytes(keystream)


def encrypt(plaintext: bytes, public_key: Point, curve: EllipticCurve, G: Point) -> Tuple[Point, bytes]:
    k = random.randint(1, curve.p - 1)
    C1 = scalar_multiplication(k, G, curve)
    kQ = scalar_multiplication(k, public_key, curve)
    
    shared_x = kQ[0]
    keystream = gen_keystream(shared_x, len(plaintext))
    
    ciphertext_bytes = bytes([p_byte ^ k_byte for p_byte, k_byte in zip(plaintext, keystream)])
    
    return C1, ciphertext_bytes


def decrypt(ciphertext: bytes, R: Point, private_key: int, curve: EllipticCurve) -> bytes:
    kQ = scalar_multiplication(private_key, R, curve)
    
    shared_x = kQ[0]
    keystream = gen_keystream(shared_x, len(ciphertext))
    
    plaintext = bytes([c_byte ^ k_byte for c_byte, k_byte in zip(ciphertext, keystream)])
    
    return plaintext