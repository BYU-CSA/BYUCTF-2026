# Hurtful

This one is for the nerds

Files:
- [enc.py](./enc.py)
- [output.txt](./output.txt)

### Solve

This is something called a [Stereotyped Message](https://gsdt.github.io/blog/2018/07/20/stereotyped-message-attack/) attack, meaning if you know a part of the message being encrypted and the public key. You do need to know the length of the unknown field of the message so that you can set up the right polynomial to attack.

The solve script brute forces the flag length to set up the polynomial to solve. Starting around a good minimum for length of the flag, you can get the full thing in less than a minute iirc.

Flag: `byuctf{cuz_st3r30typ3s_hurt_92de04}`