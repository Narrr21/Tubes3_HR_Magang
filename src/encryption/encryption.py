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

# if __name__ == "__main__":
#     # Example usage

#     plaintext = "Life is brilliant. Beautiful. It enchants us, to the point of obsession. Some are true to their purpose, though they are but shells, flesh and mind. One man lost his own body, but lingered on, as a head. Others chase the charms of love, however elusive. What is it that drives you?"

#     key = os.urandom(32)
#     ciphertext = spn.encrypt(plaintext, key)

#     (C1_x, C1_y), cipherkey = encrypt_ecc(key)



# with open("src/encryption/ciphertext.bin", "wb") as f:
#     f.write(len(ciphertext).to_bytes(4, "big"))
#     f.write(ciphertext)

#     f.write(C1_x.to_bytes(32, "big"))
#     f.write(C1_y.to_bytes(32, "big"))

#     f.write(len(cipherkey).to_bytes(4, "big"))
#     f.write(cipherkey)


# with open("src/encryption/ciphertext.bin", "rb") as f:
#     ciphertext_len = int.from_bytes(f.read(4), "big")
#     ciphertext = f.read(ciphertext_len)

#     C1_x = int.from_bytes(f.read(32), "big")
#     C1_y = int.from_bytes(f.read(32), "big")

#     cipherkey_len = int.from_bytes(f.read(4), "big")
#     cipherkey = f.read(cipherkey_len)

#     new_key = decrypt_ecc((C1_x, C1_y), cipherkey)
#     decrypted_text = spn.decrypt(ciphertext, new_key)
#     with open("src/encryption/decrypted.bin", "w") as f:
#         f.write(f"Decrypted text: {decrypted_text}\n")
