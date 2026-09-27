# Hidify subscription — راهنما (فارسی)

من چه کار کردم
- یک شاخه جدید `subscription-templates` در مخزن ایجاد کردم.
- در آن شاخه فایل‌های زیر اضافه شدند:
  1) templates/hidify-subscription.txt — توضیحِ سریع و نکات ایمنی
  2) templates/proxies.yaml.example — نمونه‌ای از فرمتِ ورودی
  3) scripts/generate_hidify_subs.py — اسکریپت پایتون برای تولید فایلِ subscription قابل استفاده در Hidify
  4) subscription/ (خروجی تا وقتی که شما فایلِ templates/proxies.yaml را پر نکنی خالی است)

نحوه استفاده (گام‌به‌گام)
1) فایلِ templates/proxies.yaml.example را به templates/proxies.yaml کپی کن و فیلدها را با مقادیر واقعی پر کن (UUID، پسورد و غیره).
2) (ترجیحاً محلی و نه در مخزن عمومی) فایل templates/proxies.yaml را پر کن.
3) روی سیستمِ خود pip install pyyaml کن:
   pip install pyyaml
4) اسکریپت را اجرا کن:
   python3 scripts/generate_hidify_subs.py -i templates/proxies.yaml -o subscription/hidify-subscription.txt
5) خروجی را در اپ Hidify به‌عنوان subscription بارگذاری کن یا فایل را در یک endpoint امن منتشر کن.

اگر می‌خواهی من ادامه بدهم
- می‌توانم فایل templates/proxies.yaml را با اطلاعاتی که امن ارسال می‌کنی پر کنم و خروجی را تولید و در شاخه قرار دهم.
- همچنین می‌توانم یک Pull Request با این تغییرات ایجاد کنم یا endpoint ساده‌ای بسازم که فایل اشتراک را سرو کند (نیاز به هاست/دامنه دارد).

نکتهٔ مهم امنیتی
- اگر این مخزن عمومی است، لطفاً هیچ اطلاعات حساس (UUID، پسورد) را مستقیماً در گیت‌هاب عمومی نگذار. در عوض فایل را محلی اجرا کن یا از راه‌های امن (رمزنگاری/ secrets) استفاده کن.

لینک شاخه:
https://github.com/pouria08/popvpn2/tree/subscription-templates
