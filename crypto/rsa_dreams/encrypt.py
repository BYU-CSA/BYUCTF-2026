from Crypto.Util.number import getPrime
from Crypto.Util.number import bytes_to_long

flag = b"REDACTED"

p = getPrime(256)
q = getPrime(256)
n = p*q
hint = p + q
e = 0x10001

c = pow(bytes_to_long(flag), e, n)

print(f"c = {c}")
print(f"n = {n}")
print(f"e = {e}")
print(f"hint = {hint}")
