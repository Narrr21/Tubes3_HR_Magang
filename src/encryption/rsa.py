from src.utility import *
import time

def modulus_and_phi(p, q):
    n = p * q
    phi_n = (p - 1) * (q - 1)
    return n, phi_n

def generate_rsa_keys(bits=128):
    p = generate_prime(bits // 2)
    q = generate_prime(bits // 2)

    n, phi_n = modulus_and_phi(p,q)

    e = 65537
    d = mod_inverse(e, phi_n)

    return (e,n), (d,n)

def encrypt(plaintext, public_key):
    e, n = public_key
    ciphertext = [str(mod_exp(ord(char), e, n)) for char in plaintext]
    ciphertext = ' '.join(ciphertext)
    return ciphertext

def decrypt(ciphertext, private_key):
    d, n = private_key
    ciphertext_list = list(map(int, ciphertext.split()))
    plaintext_list = [chr(mod_exp(char, d, n)) for char in ciphertext_list]
    plaintext = ''.join(plaintext_list)
    return plaintext

def rsa_encryption_runtime(bits=128):
    start = time.time()
    public_key, private_key = generate_rsa_keys(bits)
    keygen_time = time.time() - start

    plaintext = read_file("plaintext.txt")

    start = time.time()
    ciphertext = encrypt(plaintext, public_key)
    encryption_time = time.time() - start

    print(f"Key Generation Time: {keygen_time:.9f} seconds")
    print(f"Encryption Time: {encryption_time:.9f} seconds")
    
    write = f"d = {private_key[0]}\n\nC = {ciphertext}\n\nKey Generation Time: {keygen_time:.9f} seconds\nEncryption Time: {encryption_time:.9f} seconds"
    write_file(f"rsa/ciphertext-rsa-{bits}.txt", write)

    return ciphertext, private_key

def rsa_decryption_runtime(bits, private_key, ciphertext):
    start = time.time()
    plaintext = decrypt(ciphertext, private_key)
    decryption_time = time.time() - start

    print(f"Decryption Time: {decryption_time:.9f} seconds")

    write = f"P = {plaintext}\n\nDecryption Time: {decryption_time:.9f} seconds"
    write_file(f"rsa/decrypted-rsa-{bits}.txt", write )

if __name__ == "__main__":
    key_sizes = [128, 192, 256]
    for bits in key_sizes:
        print(f"\nTesting RSA with {bits}-bit keys:")
        cipher, key = rsa_encryption_runtime(bits)
        rsa_decryption_runtime(bits, key, cipher)
        print(f"Encryption saved to ciphertext-rsa-{bits}.txt")
        print(f"Encryption saved to decrypted-rsa-{bits}.txt")

