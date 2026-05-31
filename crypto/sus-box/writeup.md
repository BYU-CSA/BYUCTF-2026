## sus-box

This cryptosystem uses a randomized SBox; other than that, it's like one round of AES but even simpler.

Techniques from differential cryptanalysis on 1-round AES can be directly translated to breaking the cryptosystem, e.g. see [here](https://merri.cx/adventure-of-aes/).

In a nutshell, the solve script:
1. Obtains two known plaintext-ciphertext pairs $(m_1, c_1)$ and $(m_2, c_2)$ from the block cipher (note the 16-byte block size)
2. For each possible byte combination $b_1, b_2$ in the input, compute $b_1 \oplus b_2$ (the input difference) and $SBOX(b_1) \oplus SBOX(b_2)$ (the output difference). Store the pairs $(b_1,b_2)$ that map to each combination of input and output differences in a table.
3. For each byte $m_{1,i}, m_{2, i}$ in the messages and $c_{1,i}, c_{2, i}$ in the ciphertexts, use the table from step 2 to get the possible input bytes (a multiple of 2). Note these correspond to the input into the SBox, e.g. the *actual* plaintext bytes XORed with the corresponding k0 bytes. Call each of these possible bytes `byte_i_xor_k0_i`, replacing `i` with the actual byte index.
4. Using the possible `byte_i_xor_k0_i` values, iterate through the possible key pairs $(k_0, k_1)$ and try decrypting one of the known ciphertexts. See if it produces the known plaintext; if so, we have the right key. Note for the challenge's SBox configuration, there are 25165824 possible keys.
5. Use the decryption key to decrypt the provided ciphertext.

**Flag:** `byuctf{if_you_used_a_llm_youre_missing_out_learning_a_really_cool_attack_!}`
