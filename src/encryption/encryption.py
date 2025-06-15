import encryption.ecc as ecc
import encryption.spn as spn
import os

def encrypt_ecc(key: bytes):
    curve = ecc.EllipticCurve()
    G = ecc.G128
    with open("src/encryption/parameters/key.pub", "rb") as f:
        public_key = (int.from_bytes(f.readline().strip(), "big"), int.from_bytes(f.readline().strip(), "big"))

    C1, cipherkey = ecc.encrypt(key, public_key, curve, G)
    return C1, cipherkey

def decrypt_ecc(C1, cipherkey: bytes):
    curve = ecc.EllipticCurve()
    with open("src/encryption/parameters/key.sec", "rb") as f:
        private_key = int.from_bytes(f.readline().strip(), "big")
    plaintext = ecc.decrypt(cipherkey, C1, private_key, curve)
    return plaintext

def encrypt_spn(plaintext: str, key: bytes):
    return spn.encrypt(plaintext, key)

def decrypt_spn(ciphertext: bytes, key: bytes):
    return spn.decrypt(ciphertext, key)

def decrypt_key_from_id(row):
    C1_x, C1_y, cipherkey = row
    C1_x = int.from_bytes(C1_x, "big")
    C1_y = int.from_bytes(C1_y, "big")
    key = decrypt_ecc((C1_x, C1_y), cipherkey)
    return key