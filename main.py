import os
import shutil
import asyncio
import uuid
import json
import base64
import requests
import time
import random
from concurrent.futures import ThreadPoolExecutor, as_completed
from aiogram import Bot, Dispatcher, F, Router
from aiogram.types import Message, FSInputFile
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

# ==========================================
# تنظیمات توکن
# ==========================================
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("❌ مقدار BOT_TOKEN پیدا نشد! لطفا آن را در Railway تنظیم کن.")

router = Router()

SESSION_BASE_DIR = "bot_sessions"
if os.path.exists(SESSION_BASE_DIR):
    shutil.rmtree(SESSION_BASE_DIR, ignore_errors=True)
os.makedirs(SESSION_BASE_DIR, exist_ok=True)

# ==========================================
# لیست پروکسی‌های اختصاصی و جدید شما
# ==========================================
PROXY_LIST = [
    "http://iwmg03hsrost:99bny9w5sy9n2qb@209.50.182.0:3129",
    "http://iwmg03hsrost:99bny9w5sy9n2qb@216.26.250.28:3129",
    "http://iwmg03hsrost:99bny9w5sy9n2qb@45.3.50.239:3129",
    "http://iwmg03hsrost:99bny9w5sy9n2qb@193.56.28.32:3129",
    "http://iwmg03hsrost:99bny9w5sy9n2qb@216.26.246.236:3129",
    "http://iwmg03hsrost:99bny9w5sy9n2qb@45.3.33.245:3129",
    "http://iwmg03hsrost:99bny9w5sy9n2qb@45.3.51.182:3129",
    "http://iwmg03hsrost:99bny9w5sy9n2qb@209.50.160.106:3129",
    "http://iwmg03hsrost:99bny9w5sy9n2qb@104.207.45.233:3129",
    "http://iwmg03hsrost:99bny9w5sy9n2qb@104.207.60.215:3129",
    "http://iwmg03hsrost:99bny9w5sy9n2qb@209.50.168.28:3129",
    "http://iwmg03hsrost:99bny9w5sy9n2qb@216.26.252.21:3129",
    "http://iwmg03hsrost:99bny9w5sy9n2qb@216.26.234.95:3129",
    "http://iwmg03hsrost:99bny9w5sy9n2qb@216.26.247.53:3129",
    "http://iwmg03hsrost:99bny9w5sy9n2qb@104.207.51.76:3129",
    "http://iwmg03hsrost:99bny9w5sy9n2qb@45.3.35.18:3129",
    "http://iwmg03hsrost:99bny9w5sy9n2qb@45.3.38.10:3129",
    "http://iwmg03hsrost:99bny9w5sy9n2qb@65.111.20.86:3129",
    "http://iwmg03hsrost:99bny9w5sy9n2qb@151.123.176.16:3129",
    "http://iwmg03hsrost:99bny9w5sy9n2qb@104.207.32.246:3129",
    "http://iwmg03hsrost:99bny9w5sy9n2qb@216.26.238.164:3129",
    "http://iwmg03hsrost:99bny9w5sy9n2qb@209.50.174.67:3129",
    "http://iwmg03hsrost:99bny9w5sy9n2qb@209.50.162.118:3129",
    "http://iwmg03hsrost:99bny9w5sy9n2qb@151.123.176.178:3129",
    "http://iwmg03hsrost:99bny9w5sy9n2qb@209.50.167.195:3129",
    "http://iwmg03hsrost:99bny9w5sy9n2qb@65.111.0.68:3129",
    "http://iwmg03hsrost:99bny9w5sy9n2qb@65.111.0.139:3129",
    "http://iwmg03hsrost:99bny9w5sy9n2qb@65.111.5.193:3129",
    "http://iwmg03hsrost:99bny9w5sy9n2qb@45.3.37.73:3129",
    "http://iwmg03hsrost:99bny9w5sy9n2qb@65.111.31.105:3129",
    "http://iwmg03hsrost:99bny9w5sy9n2qb@104.207.62.21:3129",
    "http://iwmg03hsrost:99bny9w5sy9n2qb@195.63.31.34:3129",
    "http://iwmg03hsrost:99bny9w5sy9n2qb@216.26.241.199:3129",
    "http://iwmg03hsrost:99bny9w5sy9n2qb@216.26.255.126:3129",
    "http://iwmg03hsrost:99bny9w5sy9n2qb@104.207.55.32:3129",
    "http://iwmg03hsrost:99bny9w5sy9n2qb@209.50.186.162:3129",
    "http://iwmg03hsrost:99bny9w5sy9n2qb@216.26.250.182:3129",
    "http://iwmg03hsrost:99bny9w5sy9n2qb@65.111.31.140:3129",
    "http://iwmg03hsrost:99bny9w5sy9n2qb@104.207.35.137:3129",
    "http://iwmg03hsrost:99bny9w5sy9n2qb@209.50.185.21:3129",
    "http://iwmg03hsrost:99bny9w5sy9n2qb@65.111.9.62:3129",
    "http://iwmg03hsrost:99bny9w5sy9n2qb@65.111.1.73:3129",
    "http://iwmg03hsrost:99bny9w5sy9n2qb@65.111.6.189:3129",
    "http://iwmg03hsrost:99bny9w5sy9n2qb@209.50.179.28:3129",
    "http://iwmg03hsrost:99bny9w5sy9n2qb@45.3.42.243:3129",
    "http://iwmg03hsrost:99bny9w5sy9n2qb@65.111.31.243:3129",
    "http://iwmg03hsrost:99bny9w5sy9n2qb@216.26.225.35:3129",
    "http://iwmg03hsrost:99bny9w5sy9n2qb@65.111.1.202:3129",
    "http://iwmg03hsrost:99bny9w5sy9n2qb@45.3.37.108:3129",
    "http://iwmg03hsrost:99bny9w5sy9n2qb@216.26.226.244:3129",
    "http://iwmg03hsrost:99bny9w5sy9n2qb@104.207.44.138:3129",
    "http://iwmg03hsrost:99bny9w5sy9n2qb@45.3.47.156:3129",
    "http://iwmg03hsrost:99bny9w5sy9n2qb@216.26.242.121:3129",
    "http://iwmg03hsrost:99bny9w5sy9n2qb@216.26.236.69:3129",
    "http://iwmg03hsrost:99bny9w5sy9n2qb@216.26.231.58:3129",
    "http://iwmg03hsrost:99bny9w5sy9n2qb@104.207.59.244:3129",
    "http://iwmg03hsrost:99bny9w5sy9n2qb@209.50.176.218:3129",
    "http://iwmg03hsrost:99bny9w5sy9n2qb@104.207.35.144:3129",
    "http://iwmg03hsrost:99bny9w5sy9n2qb@45.3.36.178:3129",
    "http://iwmg03hsrost:99bny9w5sy9n2qb@104.207.34.116:3129",
    "http://iwmg03hsrost:99bny9w5sy9n2qb@217.181.92.124:3129",
    "http://iwmg03hsrost:99bny9w5sy9n2qb@104.207.48.240:3129",
    "http://iwmg03hsrost:99bny9w5sy9n2qb@45.3.33.85:3129",
    "http://iwmg03hsrost:99bny9w5sy9n2qb@45.3.33.252:3129",
    "http://iwmg03hsrost:99bny9w5sy9n2qb@217.181.90.59:3129",
    "http://iwmg03hsrost:99bny9w5sy9n2qb@216.26.236.86:3129",
    "http://iwmg03hsrost:99bny9w5sy9n2qb@216.26.228.209:3129",
    "http://iwmg03hsrost:99bny9w5sy9n2qb@65.111.22.163:3129",
    "http://iwmg03hsrost:99bny9w5sy9n2qb@104.207.45.222:3129",
    "http://iwmg03hsrost:99bny9w5sy9n2qb@104.207.46.38:3129",
    "http://iwmg03hsrost:99bny9w5sy9n2qb@217.181.91.56:3129",
    "http://iwmg03hsrost:99bny9w5sy9n2qb@65.111.29.212:3129",
    "http://iwmg03hsrost:99bny9w5sy9n2qb@216.26.253.104:3129",
    "http://iwmg03hsrost:99bny9w5sy9n2qb@104.207.63.224:3129",
    "http://iwmg03hsrost:99bny9w5sy9n2qb@104.207.43.43:3129",
    "http://iwmg03hsrost:99bny9w5sy9n2qb@104.207.39.211:3129",
    "http://iwmg03hsrost:99bny9w5sy9n2qb@216.26.238.210:3129",
    "http://iwmg03hsrost:99bny9w5sy9n2qb@104.207.58.72:3129",
    "http://iwmg03hsrost:99bny9w5sy9n2qb@65.111.9.68:3129",
    "http://iwmg03hsrost:99bny9w5sy9n2qb@216.26.232.67:3129",
    "http://iwmg03hsrost:99bny9w5sy9n2qb@65.111.30.73:3129",
    "http://iwmg03hsrost:99bny9w5sy9n2qb@45.3.45.140:3129",
    "http://iwmg03hsrost:99bny9w5sy9n2qb@45.3.37.210:3129",
    "http://iwmg03hsrost:99bny9w5sy9n2qb@209.50.189.67:3129",
    "http://iwmg03hsrost:99bny9w5sy9n2qb@45.3.47.116:3129",
    "http://iwmg03hsrost:99bny9w5sy9n2qb@104.207.37.227:3129",
    "http://iwmg03hsrost:99bny9w5sy9n2qb@216.26.241.229:3129",
    "http://iwmg03hsrost:99bny9w5sy9n2qb@65.111.15.34:3129",
    "http://iwmg03hsrost:99bny9w5sy9n2qb@65.111.22.126:3129",
    "http://iwmg03hsrost:99bny9w5sy9n2qb@104.207.35.17:3129",
    "http://iwmg03hsrost:99bny9w5sy9n2qb@104.207.35.8:3129",
    "http://iwmg03hsrost:99bny9w5sy9n2qb@209.50.189.9:3129",
    "http://iwmg03hsrost:99bny9w5sy9n2qb@209.50.170.5:3129",
    "http://iwmg03hsrost:99bny9w5sy9n2qb@65.111.5.195:3129",
    "http://iwmg03hsrost:99bny9w5sy9n2qb@45.3.51.129:3129",
    "http://iwmg03hsrost:99bny9w5sy9n2qb@209.50.170.102:3129",
    "http://iwmg03hsrost:99bny9w5sy9n2qb@45.3.42.18:3129",
    "http://iwmg03hsrost:99bny9w5sy9n2qb@65.111.29.45:3129",
    "http://iwmg03hsrost:99bny9w5sy9n2qb@216.26.239.146:3129",
    "http://iwmg03hsrost:99bny9w5sy9n2qb@216.26.250.3:3129"
]

def get_random_proxy():
    """انتخاب تصادفی یک پروکسی از لیست برای توزیع بار"""
    selected = random.choice(PROXY_LIST)
    return {
        "http": selected,
        "https": selected
    }

# ==========================================
# تست سلامت پروکسی در استارتاپ
# ==========================================
def test_proxy_on_startup():
    print("🔍 [تست استارتاپ] در حال بررسی رندوم یکی از پروکسی‌ها...")
    try:
        proxies = get_random_proxy()
        ip_used = proxies['http'].split('@')[1].split(':')[0]
        response = requests.get("https://api.ipify.org?format=json", proxies=proxies, timeout=20)
        if response.status_code == 200:
            print(f"✅ ارتباط با پروکسی {ip_used} موفقیت‌آمیز بود! آی‌پی خروجی: {response.json().get('ip')}")
            return True
    except Exception as e:
        print(f"❌ خطای استارتاپ: امکان اتصال به پروکسی وجود ندارد. {type(e).__name__}")
    return False

# ==========================================
# توابع هسته ربات
# ==========================================
def get_tokens_from_file(file_path):
    access_token, refresh_token = None, None
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for cookie in data.get('cookies', []):
                if cookie.get('name') == 'tokenMS':
                    access_token = cookie.get('value')
                elif cookie.get('name') == 'refresh_token':
                    refresh_token = cookie.get('value')
            if not access_token or not refresh_token:
                for origin in data.get('origins', []):
                    for item in origin.get('localStorage', []):
                        if item.get('name') == 'tokenMS':
                            access_token = item.get('value')
                        elif item.get('name') == 'refresh_token':
                            refresh_token = item.get('value')
    except Exception:
        pass
    return access_token, refresh_token

def update_file_with_new_tokens(file_path, old_acc, new_acc, old_ref, new_ref):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        if old_acc and new_acc:
            content = content.replace(old_acc, new_acc)
        if old_ref and new_ref:
            content = content.replace(old_ref, new_ref)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
    except Exception:
        pass

def get_user_id_from_token(token):
    try:
        payload = token.split('.')[1]
        payload += '=' * (-len(payload) % 4)
        decoded_bytes = base64.urlsafe_b64decode(payload)
        return json.loads(decoded_bytes).get('cerberusId') or json.loads(decoded_bytes).get('alternativeCustomerId')
    except Exception:
        return None

def refresh_okala_token(refresh_token, proxies):
    url = "https://apigateway.okala.com/api/v1/accounts/tokens"
    payload = {
        "grant_type": "refresh_token",
        "client_id": "customer_client_id",
        "client_secret": "u_M{'57j!%LI21#",
        "scope": "offline_access",
        "refresh_token": refresh_token
    }
    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 Chrome/137.0.0.0 Mobile"
    }
    try:
        response = requests.post(url, data=payload, headers=headers, proxies=proxies, timeout=45)
        if response.status_code == 200:
            data = response.json()
            return data.get('access_token'), data.get('refresh_token')
    except Exception:
        pass
    return None, None

def check_single_account(token, proxies):
    user_uuid = get_user_id_from_token(token)
    if not user_uuid:
        return "error_uuid"
    
    api_url = f"https://apigateway.okala.com/api/discount/v1/discounts/customer/{user_uuid}"
    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/json, text/plain, */*',
        'source': 'okala',
        'ui-version': '2.0',
        'origin': 'https://www.okala.com',
        'X-Correlation-Id': str(uuid.uuid4()),
        'X-User-Unique-Id': str(uuid.uuid4()),
        'session-id': str(uuid.uuid4()),
        'sec-ch-ua': '"Chromium";v="137", "Not/A)Brand";v="24"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 Chrome/137.0.0.0 Mobile'
    }
    
    try:
        response = requests.get(api_url, headers=headers, proxies=proxies, timeout=45)
        if response.status_code == 200:
            discounts = response.json().get('data', [])
            if not discounts:
                return 0
            valid_amounts = [d.get('discountAmount', 0) for d in discounts if d.get('discountAmount')]
            return max(valid_amounts) if valid_amounts else 0
        elif response.status_code == 401:
            return "expired"
        else:
            return f"error_api_{response.status_code}"
    except Exception as e:
        return f"error_net_{type(e).__name__}"

# ==========================================
# Worker با انتخاب رندوم پروکسی به ازای هر تلاش
# ==========================================
def worker_check_account(file_path, filename):
    time.sleep(random.uniform(0.1, 0.5))
    
    acc_token, ref_token = get_tokens_from_file(file_path)
    if not acc_token:
        return filename, file_path, "no_token"
        
    print(f"🔄 [شروع] بررسی موازی اکانت: {filename}")
    
    result = "error_net_init"
    for attempt in range(3):
        current_proxy = get_random_proxy()
        proxy_ip = current_proxy['http'].split('@')[1].split(':')[0]
        
        result = check_single_account(acc_token, proxies=current_proxy)
        if "error_net" not in str(result):
            break
            
        print(f"   ⚠️ [تلاش مجدد] فایل {filename} با آی‌پی {proxy_ip} ارور داد. تغییر پروکسی...")
        time.sleep(2)
        
    if "error_net" in str(result):
        return filename, file_path, result
    
    if result == "expired" and ref_token:
        print(f"   ♻️ [رفرش] توکن {filename} نیاز به تمدید دارد...")
        new_acc, new_ref = None, None
        for attempt in range(3):
            current_proxy = get_random_proxy()
            new_acc, new_ref = refresh_okala_token(ref_token, proxies=current_proxy)
            if new_acc: break
            time.sleep(2)
            
        if new_acc:
            update_file_with_new_tokens(file_path, acc_token, new_acc, ref_token, new_ref)
            for attempt in range(3):
                current_proxy = get_random_proxy()
                result = check_single_account(new_acc, proxies=current_proxy)
                if "error_net" not in str(result):
                    break
                time.sleep(1)
        else:
            print(f"   ❌ [ناموفق] رفرش توکن {filename} انجام نشد.")
            
    return filename, file_path, result

# ==========================================
# مدیریت موازی با کارگرها
# ==========================================
def process_and_categorize(extracted_dir, session_dir):
    src_accounts, src_data = None, None
    for root, dirs, files in os.walk(extracted_dir):
        if 'accounts' in dirs and not src_accounts:
            src_accounts = os.path.join(root, 'accounts')
        if 'data' in dirs and not src_data:
            src_data = os.path.join(root, 'data')

    if not src_accounts:
        return None, None, "❌ پوشه 'accounts' داخل فایل زیپ پیدا نشد."

    categories = {}
    stats = {"total": 0, "discounts": 0, "nodiscounts": 0, "expired": 0, "errors": 0}
    
    nodiscount_path = os.path.join(session_dir, "No_Discount")
    os.makedirs(os.path.join(nodiscount_path, 'accounts'), exist_ok=True)
    os.makedirs(os.path.join(nodiscount_path, 'data'), exist_ok=True)
    if src_data and os.path.exists(os.path.join(src_data, 'accounts.json')):
        shutil.copy2(os.path.join(src_data, 'accounts.json'), os.path.join(nodiscount_path, 'data'))

    all_files = [f for f in os.listdir(src_accounts) if os.path.isfile(os.path.join(src_accounts, f))]
    stats["total"] = len(all_files)
    
    print(f"\n🚀 شروع بررسی {stats['total']} اکانت با پروکسی‌های توزیع‌شده...\n")
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {
            executor.submit(worker_check_account, os.path.join(src_accounts, filename), filename): filename 
            for filename in all_files
        }
        
        for future in as_completed(futures):
            filename, file_path, result = future.result()
            
            if result == "no_token":
                shutil.copy2(file_path, os.path.join(nodiscount_path, 'accounts'))
                stats["errors"] += 1
                continue

            if isinstance(result, int) and result > 0:
                stats["discounts"] += 1
                amount_hezar_toman = int(result / 10000)
                print(f"   🎉 [نتیجه موفق] {filename} -> تخفیف {amount_hezar_toman} هزار تومانی")
                
                cat_id = f"dl_{amount_hezar_toman}"
                if cat_id not in categories:
                    cat_path = os.path.join(session_dir, f"Discount_{amount_hezar_toman}T")
                    os.makedirs(os.path.join(cat_path, 'accounts'), exist_ok=True)
                    os.makedirs(os.path.join(cat_path, 'data'), exist_ok=True)
                    if src_data and os.path.exists(os.path.join(src_data, 'accounts.json')):
                        shutil.copy2(os.path.join(src_data, 'accounts.json'), os.path.join(cat_path, 'data'))
                    categories[cat_id] = {
                        "title": f"🎁 تخفیف {amount_hezar_toman} هزار تومانی",
                        "path": cat_path,
                        "count": 0,
                        "file_name": f"Discount_{amount_hezar_toman}T_Final"
                    }
                
                shutil.copy2(file_path, os.path.join(categories[cat_id]['path'], 'accounts'))
                categories[cat_id]['count'] += 1
                
            else:
                shutil.copy2(file_path, os.path.join(nodiscount_path, 'accounts'))
                if result == 0:
                    print(f"   ➖ [نتیجه] {filename} -> بدون تخفیف.")
                    stats["nodiscounts"] += 1
                elif result == "expired":
                    print(f"   🔒 [نتیجه] {filename} -> کاملاً منقضی شده.")
                    stats["expired"] += 1
                else:
                    print(f"   ❌ [نتیجه خطای شبکه] {filename} -> ارور پروکسی: {result}")
                    stats["errors"] += 1

    total_nodiscounts = stats["nodiscounts"] + stats["expired"] + stats["errors"]
    if total_nodiscounts > 0:
        categories["dl_nodiscount"] = {
            "title": "➖ بدون تخفیف (یا منقضی/ارور)",
            "path": nodiscount_path,
            "count": total_nodiscounts,
            "file_name": "No_Discount_Final"
        }

    return categories, stats, None

# ==========================================
# هندلرهای تلگرام (ارسال خودکار تمام فایل‌ها)
# ==========================================
@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "سلام ! 👋\n\n" +
        "به ربات نسخه V16 (ارسال مستقیم و اتوماتیک فایل‌ها) خوش آمدی ⚡️\n\n" +
        "فایل زیپ اکانت‌ها را برای من بفرست تا با بالاترین سرعت بررسی کنم و تمام فایل‌های دسته‌بندی‌شده را مستقیم برای تو ارسال کنم.\n\n" +
        "📊 هر زیپ توسط سرورهای اختصاصی و ۱۰ ورکر موازی بررسی می‌شود."
    )

@router.message(F.document)
async def handle_zip_document(message: Message, bot: Bot, state: FSMContext):
    if not message.document.file_name.lower().endswith('.zip'):
        await message.answer("❌ لطفاً فقط فایل زیپ (.zip) ارسال کن.")
        return

    msg = await message.answer("⏳ در حال دانلود و استخراج فایل زیپ...")

    session_id = str(uuid.uuid4())
    session_dir = os.path.join(SESSION_BASE_DIR, session_id)
    os.makedirs(session_dir, exist_ok=True)
    
    extracted_dir = os.path.join(session_dir, "extracted")
    zip_path = os.path.join(session_dir, "uploaded.zip")
    
    file_info = await bot.get_file(message.document.file_id)
    await bot.download_file(file_info.file_path, zip_path)
    
    try:
        shutil.unpack_archive(zip_path, extracted_dir)
    except Exception:
        await msg.edit_text("❌ فایل زیپ مشکل دارد و باز نمی‌شود.")
        return

    await msg.edit_text(
        "⚡️ در حال بررسی هوشمند اکانت‌ها...\n\n" +
        "⏳ ترافیک بین سرورهای مجزا تقسیم می‌شود تا هیچ اتصالی قطع نشود. لطفاً منتظر بمانید..."
    )
    
    categories, stats, error_msg = await asyncio.to_thread(
        process_and_categorize, extracted_dir, session_dir
    )

    if error_msg:
        await msg.edit_text(error_msg)
        shutil.rmtree(session_dir, ignore_errors=True)
        return

    await msg.delete()

    if not categories:
        await message.answer("⚠️ متأسفانه هیچ فایل سالمی برای بررسی پیدا نشد.")
        shutil.rmtree(session_dir, ignore_errors=True)
        return

    # ارسال پیام اطلاع‌رسانی
    await message.answer("✅ بررسی تمام شد! در حال آماده‌سازی و ارسال فایل‌های زیپ...")

    # زیپ کردن و ارسال خودکار تمام دسته‌بندی‌ها
    for cat_id, info in categories.items():
        if info['count'] > 0:
            zip_path_base = os.path.join(session_dir, info["file_name"])
            final_zip_path = shutil.make_archive(zip_path_base, 'zip', info["path"])
            
            await message.answer_document(
                document=FSInputFile(final_zip_path),
                caption=f"{info['title']}\n✅ تعداد: {info['count']} اکانت"
            )

    # ارسال گزارش نهایی
    report_text = (
        "📊 <b>گزارش نهایی بررسی اکانت‌ها:</b>\n\n" +
        f"📁 کل اکانت‌های بررسی شده: <b>{stats['total']}</b>\n\n" +
        f"🎁 دارای تخفیف: <b>{stats['discounts']}</b> اکانت\n" +
        f"➖ بدون تخفیف/سوخته/خطا: <b>{stats['nodiscounts'] + stats['expired'] + stats['errors']}</b> اکانت\n\n" +
        "🧹 حافظه موقت ربات پاکسازی شد."
    )
    await message.answer(report_text, parse_mode="HTML")

    # پاکسازی خودکار پوشه جلسه برای جلوگیری از پر شدن سرور
    shutil.rmtree(session_dir, ignore_errors=True)

async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(router)
    
    # تست رندوم پروکسی‌ها
    test_proxy_on_startup()
    
    print("🤖 Bot is up and running on Railway (V16: Auto-Send All Zips)...")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
