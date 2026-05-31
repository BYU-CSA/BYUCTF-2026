FROM debian

RUN apt-get update && \
    apt-get -y upgrade && \
    apt-get -y install git curl g++ build-essential

RUN curl https://sh.rustup.rs -sSf | bash -s -- -y

WORKDIR /usr/src/app

COPY . .

ENV APP_SECRET_KEY="$(openssl rand -hex 32)"

RUN ["/bin/bash", "-c", "source $HOME/.cargo/env; cargo build --release"]

EXPOSE 8080

ENTRYPOINT ["/bin/bash", "-c", "source $HOME/.cargo/env; cargo run --release"]
