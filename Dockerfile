FROM registry.docker.ir/alpine:3.21

# تنظیم متغیرهای محیطی
ENV GOPATH=/go \
    PATH=$PATH:/usr/local/go/bin:/go/bin \
    NODE_VERSION=20.11.1 \
    GO_VERSION=1.21.6

# نصب پکیج‌های ضروری
RUN apk update && apk add --no-cache \
    bash \
    git \
    curl \
    wget \
    build-base \
    python3 \
    nodejs \
    npm \
    postgresql-client \
    && rm -rf /var/cache/apk/*

# نصب Go با استفاده از mirror جایگزین
RUN wget https://golang.org/dl/go${GO_VERSION}.linux-amd64.tar.gz || \
    wget https://gomirrors.org/dl/go/go${GO_VERSION}.linux-amd64.tar.gz || \
    wget https://dl.gocn.vip/go${GO_VERSION}.linux-amd64.tar.gz && \
    tar -C /usr/local -xzf go${GO_VERSION}.linux-amd64.tar.gz && \
    rm go${GO_VERSION}.linux-amd64.tar.gz

# ایجاد دایرکتوری‌های مورد نیاز
RUN mkdir -p /app /go/src /go/bin /go/pkg

WORKDIR /app

CMD ["/bin/bash"]