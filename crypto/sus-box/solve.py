import itertools
import tqdm
import math
from custom_cipher import RandomCipher
import hashlib

sbox = [210, 76, 176, 35, 87, 148, 91, 184, 175, 70, 158, 187, 61, 33, 103, 68, 225, 94, 216, 151, 136, 80, 52, 82, 49, 62, 44, 240, 243, 168, 118, 181, 21, 217, 211, 153, 177, 25, 190, 245, 51, 137, 113, 122, 141, 74, 27, 199, 18, 55, 37, 60, 197, 128, 248, 123, 31, 124, 131, 180, 155, 20, 3, 242, 81, 163, 247, 12, 221, 121, 93, 191, 110, 34, 147, 195, 192, 145, 159, 4, 86, 220, 98, 100, 154, 6, 235, 206, 79, 135, 222, 169, 189, 218, 170, 146, 54, 47, 227, 10, 64, 249, 13, 39, 236, 106, 102, 24, 156, 230, 28, 32, 207, 244, 186, 99, 40, 160, 174, 254, 204, 8, 228, 41, 182, 50, 120, 30, 167, 15, 140, 178, 212, 253, 63, 107, 150, 193, 171, 36, 78, 119, 9, 14, 23, 111, 251, 139, 117, 19, 138, 56, 172, 83, 85, 114, 116, 105, 48, 233, 166, 58, 46, 133, 194, 65, 11, 89, 185, 183, 16, 38, 229, 203, 255, 26, 132, 165, 57, 162, 84, 7, 129, 2, 1, 42, 246, 196, 152, 143, 250, 142, 101, 59, 201, 90, 241, 95, 130, 66, 29, 214, 69, 77, 198, 67, 43, 17, 5, 252, 215, 232, 179, 73, 75, 213, 200, 239, 238, 188, 223, 108, 96, 202, 226, 237, 97, 231, 161, 71, 219, 209, 53, 45, 109, 208, 149, 22, 134, 115, 88, 72, 224, 127, 157, 205, 126, 104, 92, 0, 144, 164, 112, 173, 125, 234]

sbox_inv = [None]*256
for i in range(256):
    sbox_inv[sbox[i]] = i
    
ciphertext = bytes.fromhex("f841cff08a6c0640848efc500a1c6a6cf206546e55542912b2f3540ae043933cda69dd45d778ea9701410416413b67f9f57e9feff06caabb3811149b020155a4d469dd93c10bd2c9cc34be7881a66a243a11acc9b10bf1496d206ca9d5d92ce4f6a853d2bba7db40584196503b015bc3")      

plaintext = b"I have a secret, please don't share: "

pt1 = plaintext[0:16]
pt2 = plaintext[16:32]

ct1 = ciphertext[0:16]
ct2 = ciphertext[16:32]

# Step 1: generate the descriptive DDT
# (table of inputs that could correspond to known (input_diff, output_diff) pairs)
ddt = [[]] * 256
for i in range(256):
    for j in range(256):
        diff_input = i ^ j
        diff_output = sbox[i] ^ sbox[j]

        if len(ddt[diff_input]) != 0:
            ddt[diff_input][diff_output].update(set([i, j]))
        else:
            ddt[diff_input] = [set() for _ in range(256)]
            ddt[diff_input][diff_output] = set([i, j])

known_input_diffs = [a ^ b for a, b in zip(pt1, pt2)]
known_output_diffs = [a ^ b for a, b in zip(ct1, ct2)]

# Step 2: generate the possible input bytes
poss_input_bytes = list()
for input_diff, output_diff in zip(known_input_diffs, known_output_diffs):
    poss_input_bytes.append(ddt[input_diff][output_diff])

# Step 3: try all the possible keys to decrypt ct1 until successful
poss_inputs = itertools.product(*poss_input_bytes)
actual_key = None

for pt1_xor_k0 in tqdm.tqdm(poss_inputs, total=math.prod([len(s) for s in poss_input_bytes])):
    
    # get the candidates k0 and k1
    k0 = [a ^ b for a, b in zip(pt1, pt1_xor_k0)]
    k0, k1 = bytes(k0), hashlib.md5(bytes(k0)).digest()
    
    # attempt decryption with these keys
    chunk = [c for c in ct1]
    chunk = bytes([a ^ b for a, b in zip(chunk, k1)])
    chunk = [sbox_inv[c] for c in chunk]
    chunk = bytes([a ^ b for a, b in zip(chunk, k0)])
    
    if chunk == pt1:
        print(f"Master key found! {k0}")
        actual_key = k0
        break

# Step 4: decrypt the ciphertext
cipher = RandomCipher(actual_key, sbox=sbox)
flag_text = cipher.decrypt_bytes(ciphertext)
print(flag_text)