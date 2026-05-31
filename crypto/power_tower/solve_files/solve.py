import math
from utils import *

from pwn import *

PRINT_M = False
PRIME_BITS = 16

p = remote("127.0.0.1", 1450)
for _ in range(3):
    p.recvline()
    
n = int(p.recvline().decode()[4:])
c = int(p.recvline().decode()[4:])
exps = [int(b) for b in p.recvline().decode()[4:-35].split("^")]
if PRINT_M:
    m = int(p.recvline().decode()[4:])

num_exps = len(exps)

primes = generate_primes_up_to(2**PRIME_BITS)
factors = factorize_with_known_primes(n, primes)
phis = compute_phis(factors, num_exps, primes)

# Now use the algorithm to compute d
dexps = exps.copy()
dexps[0] = pow(exps[0], -1, phis[0])

d = power_tower_mod_n(dexps, phis[0], phis[1:])
m_dec = pow(c, d, n)
if PRINT_M:
    assert m == m_dec

p.sendline(str(m_dec).encode())
flag = p.recvline()[39:].decode().strip()
print("Flag:", flag)
