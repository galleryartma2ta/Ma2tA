# راهنمای نصب و راه‌اندازی Ma2tA

## پیش‌نیازها

- Docker >= 20.10
- Docker Compose >= 2.0
- Go >= 1.21
- Node.js >= 18
- Flutter >= 3.13

## نصب با Docker

```bash
# کلون کردن مخزن
git clone https://github.com/galleryartma2ta/Ma2tA.git
cd Ma2tA

# ساخت و اجرای کانتینرها
docker-compose up -d

# بررسی لاگ‌ها
docker-compose logs -f