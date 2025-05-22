import secrets
import random

def is_prime(n):
    """ Miller-Rabin primality test """
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False

    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    a = random.randint(2, n - 2)
    x = mod_exp(a, d, n)
    if x != 1 and x != n - 1:
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def generate_prime(bits):
    """ Generate a prime number with a specified number of bits """
    lower_bound = 2**(bits - 1)
    upper_bound = 2**bits - 1

    while True:
        candidate = random.randint(lower_bound, upper_bound)
        if is_prime(candidate):
            return candidate

def generate_aes_key(size):
    """ Generate a number in bytes with a specified number of bits """
    if size not in [128, 192, 256]:
        raise ValueError("Key size must be 128, 192, or 256 bits")
    return secrets.token_bytes(size // 8)

def mod_exp(base, exp, mod):
    result = 1
    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % mod
        base = (base * base) % mod
        exp //= 2
    return result

def mod_inverse(a, m):
    m0, x0, x1 = m, 0, 1
    while a > 1:
        q = a // m
        a, m = m, a % m
        x0, x1 = x1 - q * x0, x0
    return x1 + m0 if x1 < 0 else x1

def read_file(filename, mode='r'):
    with open("test/" + filename, mode) as file:
        content = file.readline().strip()
    return content

def write_file(filename, content, mode='w'):
    with open("test/" + filename, mode) as file:
        file.write(content)

if __name__ == "__main__":
    # with open("test/coba.txt", "w") as f:
    #     f.write(str(generate_prime(1024)))
    print(read_file("plaintext.txt"))