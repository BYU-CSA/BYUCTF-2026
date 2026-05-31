## Power Tower

To solve the challenge, we apply Euler's Theorem recursively to the encryption exponent. That is,

$$e_1^{e_2}\pmod{\phi(n)}=e_1^{e_2\pmod{\phi(\phi(n))}}\pmod{\phi(n)}$$

Applying this iteratively gives us a fast method to compute the power tower (mod $\phi(n)$) if we can compute

$$\phi(n),\phi^2(n),\phi^3(n),\dots,\phi^{25}(n)$$

efficiently. Because the known factors of $n$ are already small, we can get factorizations for each $\phi^{k}(n)$ using trial division.
