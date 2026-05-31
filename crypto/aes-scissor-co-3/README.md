# AES Scissor Co 3

### Description

Okay, I vibe coded the final version. This time I listened to the AI and let it use AES GCM, which is bulletproof. It even authenticates the ciphertext so a bitflip attack can't happen (that's what AI said, anyways)

Files:
- [aes-scissor-co-3.zip](./aes-scissor-co-3.zip)

### Setup

You need a `.env` file before you can start this challenge. This can be generated with this command: 

```sh
echo "APP_SECRET_KEY=\"$(openssl rand -hex 32)\"" > .env
```

This can also be used to re-generate said env file if needed. Docker can be started with `docker compose up -d`, which will take a minute or two because it builds the crate.

### Solve

There's a solve script in the `./solve` folder ([solve.sage](./solve/solve.sage)). Basically, the IV generation is time-based, so you can get two ciphertext with the same IV pretty easily. Then, you can not only bit flip the ciphertext, but you can also forge a mac. There are some weird components outside of the usually basic version of this challenge- no AAD, a ciphertext that needs to be padded, and url-safe base64, but it's simple enough once you get past that.

Flag: `byuctf{n0m_n0m_c00k13_a4fb6c0f}`