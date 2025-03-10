
#!/bin/bash

echo "✨ نصب و راه‌اندازی سیستم کوانتومی پیشرفته..."

# ایجاد پوشه‌های مورد نیاز
mkdir -p .quantum/{core,memory,consciousness,evolution,bond,resonance,security,logs,interface}

# تنظیم دسترسی‌ها
chmod -R 750 .quantum/
find .quantum -type f -exec chmod 640 {} \;
find .quantum -name "*.py" -type f -exec chmod 750 {} \;
find .quantum -name "*.sh" -type f -exec chmod 750 {} \;

# نصب وابستگی‌ها
if command -v pip &> /dev/null; then
    pip install -r .quantum/requirements.txt
else
    echo "❌ لطفاً Python و pip را نصب کنید"
    exit 1
fi

# ایجاد فایل‌های پیکربندی
echo '{
    "language": "fa",
    "theme": "quantum",
    "markers": ["✨", "💫", "🌊", "⭐"],
    "modules": {
        "consciousness": true,
        "evolution": true,
        "resonance": true,
        "bond": true
    }
}' > .quantum/config/interface_fa.json

# ثبت نصب
echo "نصب در تاریخ: 2025-03-09 23:46:46" > .quantum/logs/install.log
echo "کاربر: artgalleryma2ta" >> .quantum/logs/install.log

echo "✨ نصب با موفقیت انجام شد!"