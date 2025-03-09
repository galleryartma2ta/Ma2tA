#!/bin/bash

# بررسی وجود فایل‌های پروژه
if [ ! -f "/app/go.mod" ]; then
    echo "Initializing Go module..."
    cd /app && go mod init ma2ta
fi

# نصب وابستگی‌های Go
if [ -f "/app/go.mod" ]; then
    cd /app && go mod tidy
fi

# نصب وابستگی‌های Node.js
if [ -f "/app/frontend/package.json" ]; then
    cd /app/frontend && npm install
fi

# اجرای شل
exec /bin/bash