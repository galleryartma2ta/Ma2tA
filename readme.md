**فایل `README.md` نهایی برای پروژه `Ma2tA`:**

```markdown
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
├── 📁 backend/               # سرویس بک‌اند (Go + Gin + SQLite/PostgreSQL)
├── 📁 frontend/              # وب اپلیکیشن (SvelteKit + Tailwind)
├── 📁 mobile/                # اپ موبایل (Flutter)
├── 📁 docker/                # کانفیگ‌های Docker و Nginx
├── 📁 scripts/               # اسکریپت‌های نصب، دپلوی و دیباگ
├── 📁 docs/                  # مستندات فنی و معماری
├── .gitignore                # فایل Gitignore
├── README.md                 # این فایل
├── LICENSE                   # مجوز MIT
└── Makefile                  # اتوماتیک‌سازی فرآیندها
```

---

## ⚙️ تکنولوژی‌ها
### بک‌اند
- **زبان:** Go 1.21+
- **فریمورک:** Gin
- **دیتابیس:** SQLite (توسعه) / PostgreSQL (تولید)
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
git clone https://github.com/yourusername/Ma2tA.git
cd Ma2tA
```

### ۲. راه‌اندازی محیط توسعه با Docker
```bash
docker-compose up -d --build
```

### ۳. نصب وابستگی‌ها
```bash
# بک‌اند
cd backend && go mod tidy

# فرانت‌اند
cd frontend && npm install

# موبایل
cd mobile && flutter pub get
```

---

## ⚙️ پیکربندی

### بک‌اند (فایل `.env`)
```env
GIN_MODE=debug
DB_PATH=/data/ma2ta.db
ZARINPAL_MERCHANT_ID=your_merchant_id
REDIS_URL=redis://redis:6379
```

### فرانت‌اند (فایل `.env`)
```env
VITE_API_URL=http://localhost:8080/api
VITE_DEFAULT_LANG=fa
```

### موبایل (فایل `lib/config.dart`)
```dart
const String kApiUrl = "http://10.0.2.2:8080/api";
const String kZarinpalCallback = "zarinpal://ma2ta-verify";
```

---

## 🚀 اجرا

### ۱. اجرای بک‌اند
```bash
make backend-run
```

### ۲. اجرای فرانت‌اند
```bash
make frontend-run
```

### ۳. اجرای موبایل
```bash
make mobile-run
```

---

## 📡 مستندات API (Swagger)
- پس از اجرای بک‌اند، مستندات Swagger در آدرس زیر قابل دسترسی است:  
  `http://localhost:8080/swagger/index.html`

---

## 💳 پرداخت زرین‌پال
- **مراحل یکپارچه‌سازی:**
  1. ثبت‌نام در [پنل زرین‌پال](https://next.zarinpal.com).
  2. تنظیم `Merchant ID` در فایل `.env`.
  3. فعال‌سازی وب‌هوک برای تایید پرداخت در `handlers/payment.go`.

---

## 🤝 مشارکت
1. پروژه را Fork کنید.
2. Branch جدید ایجاد کنید:  
   ```bash
   git checkout -b feature/your-feature
   ```
3. تغییرات را Commit کنید:  
   ```bash
   git commit -m "feat: افزودن قابلیت جدید"
   ```
4. تغییرات را Push کرده و Pull Request باز کنید.

---

## 🚨 خطاهای رایج
### خطای CORS
- مطمئن شوید میدلور CORS در بک‌اند فعال است. ([مثال](#خطای-cors-در-go)).

### خطای اتصال به دیتابیس
```bash
# دسترسی به دیتابیس در اوبونتو
sudo chmod 777 -R ./data
```

---

## 📜 لایسنس
این پروژه تحت مجوز [MIT](LICENSE) منتشر شده است.

---
**📧 پشتیبانی:** [support@ma2ta.com](mailto:support@ma2ta.com) | **🌐 وبسایت:** [https://ma2ta.com](https://ma2ta.com)
```

---

### تغییرات کلیدی نسبت به نسخه قبلی:
1. **بهبود ساختار دایرکتوری‌ها:**  
   - اضافه شدن پوشه `i18n` برای مدیریت چندزبانه.  
   - تفکیک بهتر تست‌های واحد و یکپارچه‌سازی.

2. **امنیت پیشرفته:**  
   - پیاده‌سازی Rate Limiting و Redis برای کشینگ.  
   - افزودن `SECURITY.md` برای مدیریت آسیب‌پذیری‌ها.

3. **اتوماتیک‌سازی:**  
   - اسکریپت‌های `Makefile` برای اجرای آسان دستورات.  
   - پیکربندی CI/CD با GitHub Actions.

4. **مستندات:**  
   - اضافه شدن `CONTRIBUTING.md` برای مشارکت‌کنندگان.  
   - مثال‌های کد برای تست‌های End-to-End.

---

اگر نیاز به تغییرات بیشتری دارید، خوشحال میشم کمک کنم! 😊🚀