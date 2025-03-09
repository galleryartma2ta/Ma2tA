# 🛍 Ma2tA - سیستم فروشگاهی آنلاین  

![Ma2tA](https://via.placeholder.com/1920x400/007bff/fff?text=Ma2tA+Online+Shop)

**Ma2tA** یک پلتفرم فروشگاهی کامل با قابلیت‌های وب، API و اپ موبایل است که با معماری مدرن و پشتیبانی از پرداخت ایرانی (زرین‌پال) توسعه یافته است.

---

## فهرست 📜
- [معماری پروژه](#-معماری-پروژه)
- [تکنولوژی‌ها](#%EF%B8%8F-تکنولوژیها)
- [پیش‌نیازها](#-پیشنیازها)
- [نصب و راه‌اندازی](#%EF%B8%8F-نصب-و-راهاندازی)
- [پیکربندی](#%EF%B8%8F-پیکربندی)
- [اجرا](#-اجرا)
- [مستندات API](#-مستندات-api)
- [پرداخت زرین‌پال](#-پرداخت-زرینپال)
- [مشارکت](#-مشارکت)
- [خطاهای رایج](#-خطاهای-رایج)
- [لایسنس](#-لایسنس)

---

## 🏗 معماری پروژه
```bash
├── 📁 .github/                # تنظیمات GitHub (CI/CD، Issue Templates)
├── 📁 backend/               # سرویس بک‌اند (Go + Gin + PostgreSQL)
├── 📁 frontend/              # وب اپلیکیشن (SvelteKit + Tailwind)
├── 📁 mobile/                # اپ موبایل (Flutter)
├── 📁 docker/                # کانفیگ‌های Docker و Nginx
├── 📁 scripts/               # اسکریپت‌های نصب، دپلوی و دیباگ
├── 📁 docs/                  # مستندات فنی و معماری
├── 📁 uploads/               # محل ذخیره فایل‌های آپلود شده
├── 📁 i18n/                  # فایل‌های چندزبانه
├── .gitignore               # فایل Gitignore
├── README.md                # این فایل
├── docker-compose.yml       # تنظیمات Docker Compose
├── LICENSE                  # مجوز MIT
└── Makefile                 # اتوماتیک‌سازی فرآیندها
```

---

## ⚙️ تکنولوژی‌ها
### بک‌اند
- **زبان:** Go 1.21+
- **فریمورک:** Gin
- **دیتابیس:** PostgreSQL
- **کش:** Redis
- **پرداخت:** زرین‌پال
- **امنیت:** JWT, Rate Limiting, CORS

### فرانت‌اند
- **فریمورک:** SvelteKit
- **استایل:** Tailwind CSS + DaisyUI
- **تولید:** Vite
- **بین‌المللی‌سازی:** i18n

### موبایل
- **فریمورک:** Flutter 3.13+
- **مدیریت حالت:** Riverpod
- **پکیج‌ها:** Dio, WebView, Cached Network Image

### DevOps
- **کانتینریزاسیون:** Docker + Docker Compose
- **مانیتورینگ:** Prometheus + Grafana
- **CI/CD:** GitHub Actions

---

## 📋 پیش‌نیازها
1. **ویندوز ۱۰/۱۱** با قابلیت WSL2 ([راهنمای فعالسازی](https://learn.microsoft.com/fa-ir/windows/wsl/install))
2. **Docker Desktop** ([دانلود](https://www.docker.com/products/docker-desktop/))
3. **VS Code** با اکستنشن‌های:
   - Remote - WSL
   - Dev Containers
   - Go, Svelte, Flutter

---

## 🛠️ نصب و راه‌اندازی

### ۱. کلون پروژه
```bash
git clone https://github.com/galleryartma2ta/Ma2tA.git
cd Ma2tA
```

### ۲. راه‌اندازی محیط توسعه با Docker
```bash
docker-compose up -d --build
```

### ۳. دسترسی به کانتینر توسعه
```bash
docker exec -it ma2ta-dev bash
```

### ۴. تنظیمات اولیه دیتابیس
رمز عبور پیش‌فرض برای PostgreSQL: `13271327`

برای اتصال به دیتابیس:
```bash
psql -U ma2ta -d ma2ta_gallery
```

---

## ⚙️ پیکربندی

### متغیرهای محیطی (در docker-compose.yml)
```yaml
environment:
  - POSTGRES_HOST=postgres
  - POSTGRES_PORT=5432
  - POSTGRES_DB=ma2ta_gallery
  - POSTGRES_USER=ma2ta
  - POSTGRES_PASSWORD=13271327
  - REDIS_URL=redis://redis:6379
  - NODE_ENV=development
```

### پورت‌های پیش‌فرض
- **API:** `8080`
- **وب‌سایت:** `3000`
- **دیتابیس:** `5432`
- **Redis:** `6379`
- **PgAdmin:** `5050`

---

## 🚀 اجرای سرویس‌ها

### مدیریت کانتینرها
```bash
# اجرای همه سرویس‌ها
docker-compose up -d

# متوقف کردن سرویس‌ها
docker-compose down

# مشاهده لاگ‌ها
docker-compose logs -f
```

### دسترسی به سرویس‌ها
- **وب‌سایت:** http://localhost:3000
- **API:** http://localhost:8080
- **PgAdmin:** http://localhost:5050
  - ایمیل: `admin@ma2ta.com`
  - رمز: `Ma2taAdmin123!`

---

## 📡 مستندات API
- Swagger UI: http://localhost:8080/swagger/index.html
- ReDoc: http://localhost:8080/docs

---

## 💳 پرداخت زرین‌پال
- مستندات یکپارچه‌سازی در `docs/payment-integration.md`
- تنظیمات درگاه در `backend/config/payment.go`
- نمونه کد پرداخت در `docs/examples/payment`

---

## 🤝 مشارکت
1. پروژه را Fork کنید
2. Branch جدید بسازید (`git checkout -b feature/amazing-feature`)
3. تغییرات را Commit کنید (`git commit -m 'feat: Add amazing feature'`)
4. Branch را Push کنید (`git push origin feature/amazing-feature`)
5. Pull Request ایجاد کنید

---

## 🚨 خطاهای رایج

### مشکل دسترسی به volume‌های Docker
```bash
sudo chown -R $USER:$USER uploads/
sudo chmod -R 777 uploads/
```

### خطای اتصال به دیتابیس
1. اطمینان از اجرای PostgreSQL:
```bash
docker-compose ps
```
2. تست اتصال:
```bash
docker exec -it ma2ta-postgres pg_isready -U ma2ta
```

### مشکل CORS
در `backend/middleware/cors.go`:
```go
config := cors.DefaultConfig()
config.AllowOrigins = []string{"http://localhost:3000"}
```

---

## 📜 لایسنس
این پروژه تحت مجوز [MIT](LICENSE) منتشر شده است.

---

**📧 پشتیبانی:** [support@ma2ta.com](mailto:support@ma2ta.com) | **🌐 وبسایت:** [https://ma2ta.com](https://ma2ta.com)