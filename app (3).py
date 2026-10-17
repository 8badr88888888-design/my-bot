# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════
#           KRIS PREMIUM BOT - v4.8 (Triple API Smart)
#           Developer : 『𝘿𝙍𝙆』𝑲ㅤ𝑹ㅤ𝑰ㅤ𝑺 𖤍
#           Telegram : @VKQ7Y
# ═══════════════════════════════════════════════════

import telebot
import requests
import threading
import time
import json
import os
import re
import secrets
import string
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

# ═══════════ الإعدادات ═══════════
BOT_TOKEN = "8868419967:AAE2bFnOg6Fn8Jqn3iTKI7gtVvxRZBzJHCI"

OWNER_ID = 8568410458
ADMIN_ID = 8296590657
ADMINS = {OWNER_ID, ADMIN_ID}

DEVELOPER = "@VKQ7Y"
DEVELOPER_ID = 8212071474
DEV_NAME = "𝑲ㅤ𝑹ㅤ𝑰ㅤ𝑺"
GROUP_LINK = "https://t.me/krisvipspam"
CHANNEL_LINK = "https://t.me/krisvipspam"
CHANNEL_USERNAME = "@krisvipspam"

# ═══════════ APIs ═══════════
API_MAIN_URL = "http://78.154.103.42:10305"
API_VISIT_URL = "http://78.154.103.42:10305"
API_LIKE_URL = "http://78.154.103.8:15127"
API_LIKE_KEY = "ayan"
API_INFO_URL = "https://out-bar-info.vercel.app/info?uid={uid}"

# ✅ APIs التوكنات (3 مصادر)
API_JWT_NEW = "https://jihad-jwt.lovable.app/api/public/token?uid={uid}&password={password}"
API_JWT_FALLBACK_1 = "http://de26.spaceify.eu:26080/jwt?u={uid}&pw={password}"
API_JWT_FALLBACK_2 = "https://ff-jwt-gen-api.lovable.app/api/public/token?uid={uid}&password={password}"

# ═══════════ إعدادات ═══════════
BATCH_SIZE = 15
BATCH_DELAY = 5
DEFAULT_CHECK_INTERVAL = 15
DEFAULT_SLOTS = 3
MAX_SLOTS = 100
ACCOUNT_CLEAN_INTERVAL = 7200
FAILED_THRESHOLD = 20
TOKEN_VALIDITY = 3300

SPEED_CONFIG_FILE = "speed_config.json"
TOKENS_FILE = "tokens_cache.json"
speed_config = {
    "batch_size": 15,
    "batch_delay": 5,
    "check_interval": 15,
}
speed_lock = threading.Lock()

bot = telebot.TeleBot(BOT_TOKEN)
SERVER_ME = "https://clientbp.ppmainecoonghj.com/"

GROUPS_FILE = "groups.json"
ADMINS_FILE = "admins.json"
FORCE_CHANNELS_FILE = "force_channels.json"
USERS_FILE = "users.json"
BANNED_FILE = "banned.json"
ACCESS_FILE = "access.json"
LOGS_FILE = "logs.json"
KEYS_FILE = "keys.json"
USER_INFO_FILE = "user_info.json"
ACTIVE_FILE = "active_spams.json"

force_channels = []
banned_users = set()
enabled_groups = set()
access_users = {}
operation_logs = []
keys_db = {}
user_info = {}

user_active_spams = {}
user_queues = {}
user_slots_lock = threading.Lock()
active_save_lock = threading.Lock()

bot_stats = {
    "total_users": set(),
    "total_messages": 0,
    "start_count": 0,
    "checks": 0,
    "spams": 0,
    "likes_sent": 0,
    "visits_sent": 0,
    "clan_spams": 0,
    "start_time": time.time(),
}

ACCOUNTS_LIST = [
"8301446606:xkrisi2np",
"8301446609:xkrisq5ee",
"8301446627:xkrismoqi",
"8301446608:xkrisfvcd",
"8301446613:xkriskcsu",
"8301446636:xkrispf5k",
"8301446623:xkrishvm9",
"8301446624:xkrisnqs0",
"8301446601:xkrish3c8",
"8301446598:xkris4exs",
"8301446603:xkris78x9",
"8301446641:xkriseq69",
"8301446610:xkrisivp2",
"8301446638:xkris27r1",
"8301446605:xkriswhg6",
"8301446637:xkrisd74s",
"8301446625:xkrisjraw",
"8301446602:xkris1yyk",
"8301446599:xkrist5zk",
"8301446950:xkris350r",
"8301446963:xkris2hb1",
"8301446974:xkris0s4c",
"8301446969:xkrisqpsq",
"8301446964:xkris2796",
"8301446949:xkris03n7",
"8301446607:xkrisenmy",
"8301446981:xkrisbw6m",
"8301446957:xkris1ozu",
"8301446995:xkris0ft4",
"8301448920:xkrisanx3",
"8301449151:xkris16ee",
"8301449146:xkris67m0",
"8301449188:xkrisz022",
"8301449154:xkrisknar",
"8301449232:xkrisryx8",
"8301449183:xkrisb630",
"8301449350:xkris0r2g",
"8301449254:xkrisddf9",
"8301449184:xkrisrb2b",
"8301449417:xkrislqgf",
"8301449491:xkriszk8l",
"8301449303:xkris5mc9",
"8301449540:xkristdr5",
"8301449530:xkrisnm5s",
"8301449537:xkrisvot2",
"8301449574:xkrisb02z",
"8301449637:xkris63jj",
"8301449597:xkrisjuhw",
"8301449632:xkrisfn9o",
"8301449536:xkrisynur",
"8301449619:xkrisl51h",
"8301449638:xkrisw2q6",
"8301449666:xkrishaff",
"8301449622:xkrisoxei",
"8301449573:xkrisw7ze",
"8301449743:xkrispjk9",
"8301449749:xkris30ax",
"8301449729:xkrisskoj",
"8301452977:xkrisq135",
"8301453017:xkrisvy50",
"8301453016:xkrismfpl",
"8301453085:xkrishiez",
"8301453147:xkrisyweq",
"8301453083:xkrisdenx",
"8301453180:xkrisl4k5",
"8301453087:xkrisr9sv",
"8301453154:xkrisjafi",
"8301453254:xkrispafh",
"8301453298:xkris5cpl",
"8301453311:xkrisrwtp",
"8301453292:xkris13ze",
"8301453397:xkris8ouz",
"8301453318:xkrisjapx",
"8301453399:xkrish5is",
"8301453348:xkrisd36i",
"8301453414:xkrisyifs",
"8301453362:xkrisqos4",
"8301453438:xkrisuuxb",
"8301453744:xkrismz18",
"8301453509:xkristytb",
"8301453901:xkris6agh",
"8301453913:xkrisrnj9",
"8301453880:xkrisyg5n",
"8301453878:xkris5bkz",
"8301453921:xkrisiw3f",
"8301453883:xkriss5v4",
"8301456380:xkrisiqob",
"8301456430:xkriskdae",
"8301456511:xkristuuo",
"8301456562:xkrishxty",
"8301456468:xkriszqqe",
"8301456581:xkris6l6s",
"8301456797:xkriswc0v",
"8301456834:xkrisoqog",
"8301456796:xkrisce7n",
"8301456845:xkrissb0a",
"8301457033:xkrisjcwb",
"8301457003:xkriswhtj",
"8301456969:xkrisvrtu",
"8301457070:xkris05ud",
]

# ═══════════ Speed Config ═══════════
def load_speed_config():
    global speed_config, BATCH_SIZE, BATCH_DELAY, DEFAULT_CHECK_INTERVAL
    try:
        if os.path.exists(SPEED_CONFIG_FILE):
            with open(SPEED_CONFIG_FILE, "r") as f:
                data = json.load(f)
                speed_config.update(data)
    except Exception:
        pass
    BATCH_SIZE = speed_config["batch_size"]
    BATCH_DELAY = speed_config["batch_delay"]
    DEFAULT_CHECK_INTERVAL = speed_config["check_interval"]


def save_speed_config():
    try:
        with open(SPEED_CONFIG_FILE, "w") as f:
            json.dump(speed_config, f, indent=2)
    except Exception:
        pass


def apply_speed():
    global BATCH_SIZE, BATCH_DELAY, DEFAULT_CHECK_INTERVAL
    BATCH_SIZE = speed_config["batch_size"]
    BATCH_DELAY = speed_config["batch_delay"]
    DEFAULT_CHECK_INTERVAL = speed_config["check_interval"]


# ═══════════ حفظ / تحميل ═══════════
def load_data():
    global enabled_groups, ADMINS, force_channels, banned_users, access_users, operation_logs, keys_db, user_info
    enabled_groups = set()
    banned_users = set()
    access_users = {}
    operation_logs = []
    keys_db = {}
    user_info = {}

    if os.path.exists(GROUPS_FILE):
        try:
            with open(GROUPS_FILE, 'r') as f:
                enabled_groups = set(json.load(f))
        except Exception:
            pass

    if os.path.exists(BANNED_FILE):
        try:
            with open(BANNED_FILE, 'r') as f:
                banned_users = set(json.load(f))
        except Exception:
            pass

    if os.path.exists(ADMINS_FILE):
        try:
            with open(ADMINS_FILE, 'r') as f:
                ADMINS = set(json.load(f))
        except Exception:
            pass
    ADMINS.add(OWNER_ID)
    ADMINS.add(ADMIN_ID)

    if os.path.exists(FORCE_CHANNELS_FILE):
        try:
            with open(FORCE_CHANNELS_FILE, 'r', encoding='utf-8') as f:
                saved = json.load(f)
                if saved:
                    force_channels = saved
        except Exception:
            pass

    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, 'r') as f:
                bot_stats["total_users"] = set(json.load(f))
        except Exception:
            pass

    if os.path.exists(ACCESS_FILE):
        try:
            with open(ACCESS_FILE, 'r') as f:
                access_users = {int(k): v for k, v in json.load(f).items()}
        except Exception:
            pass

    if os.path.exists(LOGS_FILE):
        try:
            with open(LOGS_FILE, 'r', encoding='utf-8') as f:
                operation_logs = json.load(f)
        except Exception:
            pass

    if os.path.exists(KEYS_FILE):
        try:
            with open(KEYS_FILE, 'r', encoding='utf-8') as f:
                keys_db = json.load(f)
        except Exception:
            pass

    if os.path.exists(USER_INFO_FILE):
        try:
            with open(USER_INFO_FILE, 'r', encoding='utf-8') as f:
                user_info = {int(k): v for k, v in json.load(f).items()}
        except Exception:
            pass


def save_data():
    try:
        with open(GROUPS_FILE, 'w') as f:
            json.dump(list(enabled_groups), f)
        with open(ADMINS_FILE, 'w') as f:
            json.dump(list(ADMINS), f)
        with open(FORCE_CHANNELS_FILE, 'w', encoding='utf-8') as f:
            json.dump(force_channels, f, ensure_ascii=False, indent=2)
        with open(USERS_FILE, 'w') as f:
            json.dump(list(bot_stats["total_users"]), f)
        with open(BANNED_FILE, 'w') as f:
            json.dump(list(banned_users), f)
        with open(ACCESS_FILE, 'w') as f:
            json.dump({str(k): v for k, v in access_users.items()}, f)
        with open(LOGS_FILE, 'w', encoding='utf-8') as f:
            json.dump(operation_logs[-500:], f, ensure_ascii=False, indent=2)
        with open(KEYS_FILE, 'w', encoding='utf-8') as f:
            json.dump(keys_db, f, ensure_ascii=False, indent=2)
        with open(USER_INFO_FILE, 'w', encoding='utf-8') as f:
            json.dump({str(k): v for k, v in user_info.items()}, f, ensure_ascii=False, indent=2)
    except Exception:
        pass


def add_log(user_id, action, details="", username=""):
    operation_logs.append({
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "user_id": user_id,
        "username": username,
        "action": action,
        "details": details,
    })
    save_data()


def update_user_info(user_id, username="", first_name=""):
    try:
        if user_id not in user_info:
            user_info[user_id] = {
                "username": username or "",
                "first_name": first_name or "",
                "joined_at": time.time(),
            }
        else:
            if username:
                user_info[user_id]["username"] = username
            if first_name:
                user_info[user_id]["first_name"] = first_name
        save_data()
    except Exception as e:
        print(f"[update_user_info] {e}")


# ═══════════ حفظ / استعادة العمليات ═══════════
def save_active_spams():
    if not active_save_lock.acquire(blocking=False):
        return
    try:
        data = {"active": {}, "queues": {}, "saved_at": time.time()}

        with user_slots_lock:
            for user_id, spams in user_active_spams.items():
                data["active"][str(user_id)] = {}
                for target_uid, info in spams.items():
                    data["active"][str(user_id)][target_uid] = {
                        "type": info.get("type", "smart"),
                        "hours": info.get("hours", 0),
                        "started_at": info.get("started_at", 0),
                        "chat_id": info.get("chat_id", 0),
                        "count": info.get("count", 0),
                    }

            for user_id, queue in user_queues.items():
                data["queues"][str(user_id)] = []
                for task in queue:
                    data["queues"][str(user_id)].append({
                        "chat_id": task.get("chat_id", 0),
                        "target_uid": task.get("target_uid", ""),
                        "hours": task.get("hours", 0),
                        "type": task.get("type", "smart"),
                    })

        with open(ACTIVE_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"[save_active_spams] {e}")
    finally:
        active_save_lock.release()


def restore_active_spams():
    global user_active_spams, user_queues
    try:
        if not os.path.exists(ACTIVE_FILE):
            print("[restore] لا يوجد ملف سابق")
            return

        with open(ACTIVE_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)

        now = time.time()
        restored = 0
        queued = 0
        expired = 0

        for user_id_str, spams in data.get("active", {}).items():
            user_id = int(user_id_str)

            if not is_admin(user_id) and user_id not in access_users:
                continue
            if not is_admin(user_id) and access_users.get(user_id, 0) < now:
                continue

            for target_uid, info in spams.items():
                hours = info.get("hours", 0)
                started_at = info.get("started_at", 0)
                chat_id = info.get("chat_id", 0)
                task_type = info.get("type", "smart")
                count = info.get("count", 0)

                if hours > 0:
                    end_time = started_at + (hours * 3600)
                    if now > end_time:
                        expired += 1
                        continue

                if user_id not in user_active_spams:
                    user_active_spams[user_id] = {}

                user_active_spams[user_id][target_uid] = {
                    "type": task_type,
                    "target": target_uid,
                    "hours": hours,
                    "started_at": started_at,
                    "chat_id": chat_id,
                    "count": count,
                }

                if task_type == "visit":
                    threading.Thread(
                        target=visit_worker,
                        args=(chat_id, target_uid, count, user_id),
                        daemon=True
                    ).start()
                else:
                    threading.Thread(
                        target=smart_send_worker,
                        args=(chat_id, target_uid, user_id, hours),
                        daemon=True
                    ).start()

                restored += 1

        for user_id_str, queue in data.get("queues", {}).items():
            user_id = int(user_id_str)

            if not is_admin(user_id) and user_id not in access_users:
                continue
            if not is_admin(user_id) and access_users.get(user_id, 0) < now:
                continue

            user_queues[user_id] = []
            for task in queue:
                user_queues[user_id].append({
                    "chat_id": task.get("chat_id", 0),
                    "target_uid": task.get("target_uid", ""),
                    "user_id": user_id,
                    "hours": task.get("hours", 0),
                    "type": task.get("type", "smart"),
                })
                queued += 1

        if restored > 0 or queued > 0:
            print(f"[✓] استعادة: {restored} عملية شغالة | {queued} في الطابور | {expired} منتهية")
        else:
            print(f"[restore] لا عمليات للاستعادة ({expired} منتهية)")
    except Exception as e:
        print(f"[restore_active_spams] {e}")


def active_spams_saver_worker():
    print("[saver] بدأ حفظ العمليات الشغالة كل 15 ثانية")
    while True:
        try:
            time.sleep(15)
            save_active_spams()
        except Exception as e:
            print(f"[active_spams_saver] {e}")


load_data()
load_speed_config()


# ═══════════ حماية الحسابات + تخزين التوكنات ═══════════
bot_accounts = []
last_reload = 0
reload_lock = threading.Lock()
failed_attempts = {}
BANNED_ACCOUNTS = set()

TOKEN_CHECK_INTERVAL = 1500
TOKEN_MIN_REMAINING = 300

tokens_cache = {}
tokens_cache_lock = threading.Lock()

# ✅ حالة API الجديد (jihad-jwt)
_new_api_status = {"working": None, "last_check": 0}
_new_api_lock = threading.Lock()
NEW_API_TEST_TIMEOUT = 6

BLOCKED_PATTERNS = [
    r"<script", r"javascript:", r"eval\(", r"exec\(",
    r"__import__", r"os\.system", r"subprocess",
]


def sanitize_input(text):
    if not isinstance(text, str):
        return text
    if len(text) > 500:
        text = text[:500]
    for pattern in BLOCKED_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            return None
    return text.strip()


def is_safe_uid(uid):
    if not uid or not isinstance(uid, str):
        return False
    if not uid.isdigit():
        return False
    if len(uid) < 5 or len(uid) > 15:
        return False
    return True


# ═══════════ تحميل / حفظ التوكنات ═══════════
def load_tokens_cache():
    global tokens_cache
    try:
        if os.path.exists(TOKENS_FILE):
            with open(TOKENS_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                now = time.time()
                with tokens_cache_lock:
                    tokens_cache = {
                        k: v for k, v in data.items()
                        if v.get("expires_at", 0) > now
                    }
                print(f"[tokens] تم تحميل {len(tokens_cache)} توكن صالح")
    except Exception as e:
        print(f"[load_tokens_cache] {e}")


def save_tokens_cache():
    try:
        with tokens_cache_lock:
            with open(TOKENS_FILE, 'w', encoding='utf-8') as f:
                json.dump(tokens_cache, f, ensure_ascii=False)
    except Exception as e:
        print(f"[save_tokens_cache] {e}")


def clear_expired_tokens():
    try:
        now = time.time()
        with tokens_cache_lock:
            expired = [k for k, v in tokens_cache.items() if v.get("expires_at", 0) <= now]
            for k in expired:
                del tokens_cache[k]
        if expired:
            save_tokens_cache()
            print(f"[tokens] حذف {len(expired)} توكن منتهي")
        return len(expired)
    except Exception as e:
        print(f"[clear_expired_tokens] {e}")
        return 0


# ═══════════ اختبار API الجديد (jihad-jwt) ═══════════
def _test_new_api():
    """اختبار سريع: هل API الجديد (jihad-jwt) شغال؟"""
    with _new_api_lock:
        now = time.time()
        if _new_api_status["working"] is not None and (now - _new_api_status["last_check"]) < 300:
            return _new_api_status["working"]

    test_uid = "8150543073"
    test_pw = "xkriszub6"
    try:
        url = API_JWT_NEW.format(uid=test_uid, password=test_pw)
        r = requests.get(url, timeout=NEW_API_TEST_TIMEOUT)
        if r.status_code == 200:
            data = r.json()
            if data.get("token") and data.get("account_Id"):
                print(f"[api-test] ✅ API الجديد (jihad-jwt) شغال")
                with _new_api_lock:
                    _new_api_status["working"] = True
                    _new_api_status["last_check"] = now
                return True
    except Exception as e:
        print(f"[api-test] ❌ API الجديد فشل: {str(e)[:60]}")

    with _new_api_lock:
        _new_api_status["working"] = False
        _new_api_status["last_check"] = now
    return False


# ═══════════ Login Functions ═══════════
def _fetch_token_from_new_api(uid, password):
    """يطلب توكن من API الجديد (jihad-jwt)"""
    try:
        url = API_JWT_NEW.format(uid=uid, password=password)
        r = requests.get(url, timeout=8)
        if r.status_code != 200:
            return None
        data = r.json()
        jwt_token = data.get("token")
        account_id = data.get("account_Id")
        region = data.get("region") or data.get("lockRegion") or "ME"
        if jwt_token and account_id:
            return {
                "jwt": jwt_token,
                "account_id": str(account_id),
                "region": region,
                "source": "new"
            }
    except Exception as e:
        print(f"[new-api] {uid}: {str(e)[:60]}")
    return None


def _fetch_token_from_fallback_1(uid, password):
    """يطلب توكن من API الاحتياطي الأول (de26.spaceify.eu)"""
    try:
        url = API_JWT_FALLBACK_1.format(uid=uid, password=password)
        r = requests.get(url, timeout=10)
        if r.status_code != 200:
            return None
        data = r.json()
        jwt_token = data.get("jwt")
        account_id = data.get("account_uid")
        region = (data.get("jwt_info") or {}).get("noti_region", "ME")
        if jwt_token and account_id:
            return {
                "jwt": jwt_token,
                "account_id": str(account_id),
                "region": region,
                "source": "fallback_1"
            }
    except Exception as e:
        print(f"[fallback-1] {uid}: {str(e)[:60]}")
    return None


def _fetch_token_from_old_api(uid, password):
    """يطلب توكن من API الاحتياطي الثاني (ff-jwt-gen-api)"""
    try:
        url = API_JWT_FALLBACK_2.format(uid=uid, password=password)
        r = requests.get(url, timeout=12)
        if r.status_code != 200:
            return None
        data = r.json()
        token = data.get("token") or data.get("access_token")
        account_id = data.get("account_id")
        region = data.get("region", "ME")
        if token and account_id:
            return {
                "jwt": token,
                "account_id": str(account_id),
                "region": region,
                "source": "fallback_2"
            }
    except Exception as e:
        print(f"[fallback-2] {uid}: {str(e)[:60]}")
    return None


def _save_token_to_cache(uid, result):
    """يحفظ التوكن في الكاش"""
    failed_attempts[uid] = 0
    with tokens_cache_lock:
        tokens_cache[uid] = {
            "jwt": result["jwt"],
            "account_id": result["account_id"],
            "region": result.get("region", "ME"),
            "source": result.get("source", "unknown"),
            "expires_at": time.time() + TOKEN_VALIDITY
        }
    return {
        "jwt": result["jwt"],
        "account_id": result["account_id"],
        "server_url": SERVER_ME,
        "uid": uid
    }


def _login_with_new_api(uid, password):
    """login كامل: API جديد + احتياطي 1 + احتياطي 2"""
    with tokens_cache_lock:
        cached = tokens_cache.get(uid)
    if cached and cached.get("expires_at", 0) > time.time() + 300:
        return {
            "jwt": cached["jwt"],
            "account_id": cached["account_id"],
            "server_url": SERVER_ME,
            "uid": uid
        }

    if uid in BANNED_ACCOUNTS:
        return None

    # جرّب API الجديد (jihad-jwt)
    result = _fetch_token_from_new_api(uid, password)
    if not result:
        # احتياطي 1 (de26)
        result = _fetch_token_from_fallback_1(uid, password)
    if not result:
        # احتياطي 2 (ff-jwt-gen)
        result = _fetch_token_from_old_api(uid, password)

    if result:
        return _save_token_to_cache(uid, result)
    else:
        failed_attempts[uid] = failed_attempts.get(uid, 0) + 1
        if failed_attempts[uid] >= FAILED_THRESHOLD:
            BANNED_ACCOUNTS.add(uid)
        return None


def _login_with_old_api(uid, password):
    """login كامل: احتياطي 1 + احتياطي 2 فقط"""
    with tokens_cache_lock:
        cached = tokens_cache.get(uid)
    if cached and cached.get("expires_at", 0) > time.time() + 300:
        return {
            "jwt": cached["jwt"],
            "account_id": cached["account_id"],
            "server_url": SERVER_ME,
            "uid": uid
        }

    if uid in BANNED_ACCOUNTS:
        return None

    result = _fetch_token_from_fallback_1(uid, password)
    if not result:
        result = _fetch_token_from_old_api(uid, password)

    if result:
        return _save_token_to_cache(uid, result)
    else:
        failed_attempts[uid] = failed_attempts.get(uid, 0) + 1
        if failed_attempts[uid] >= FAILED_THRESHOLD:
            BANNED_ACCOUNTS.add(uid)
        return None


def reload_accounts():
    global bot_accounts, last_reload
    if not reload_lock.acquire(blocking=False):
        return
    try:
        clear_expired_tokens()

        use_new_api = _test_new_api()

        if use_new_api:
            print(f"[reload] استخدام API الجديد (jihad-jwt)")
        else:
            print(f"[reload] استخدام APIs الاحتياطية")

        new_accounts = []
        with ThreadPoolExecutor(max_workers=2) as executor:
            futures = {}
            for acc in ACCOUNTS_LIST:
                if ":" not in acc:
                    continue
                uid, pw = acc.split(":", 1)
                time.sleep(0.3)

                if use_new_api:
                    futures[executor.submit(_login_with_new_api, uid, pw)] = acc
                else:
                    futures[executor.submit(_login_with_old_api, uid, pw)] = acc

            for future in as_completed(futures):
                try:
                    session = future.result(timeout=20)
                    if session:
                        new_accounts.append(session)
                except Exception:
                    pass

        if new_accounts:
            if not bot_accounts or len(new_accounts) >= len(bot_accounts):
                bot_accounts = new_accounts
                print(f"[✓] الحسابات: {len(new_accounts)}/{len(ACCOUNTS_LIST)}")

        save_tokens_cache()
        last_reload = time.time()
        print(f"[reload] تم: {len(new_accounts)} حساب | محظور: {len(BANNED_ACCOUNTS)} | كاش: {len(tokens_cache)}")
    except Exception as e:
        print(f"[!] {e}")
    finally:
        reload_lock.release()


def token_refresh_worker():
    print(f"[refresh] بدأ الفحص كل {TOKEN_CHECK_INTERVAL // 60} دقيقة")
    time.sleep(60)
    while True:
        try:
            time.sleep(TOKEN_CHECK_INTERVAL)
            now = time.time()

            with tokens_cache_lock:
                total = len(tokens_cache)
                expiring_soon = sum(
                    1 for v in tokens_cache.values()
                    if v.get("expires_at", 0) - now < TOKEN_MIN_REMAINING
                )
                missing = max(0, len(ACCOUNTS_LIST) - total)

            need_reload = (expiring_soon > 5 or missing > 5)

            if need_reload:
                print(f"[refresh] {expiring_soon} قرب انتهائه | {missing} ناقص → جاري التجديد")
                with _new_api_lock:
                    _new_api_status["working"] = None
                reload_accounts()
            else:
                print(f"[refresh] لا حاجة للتجديد ({total} توكن صالح)")

        except Exception as e:
            print(f"[refresh] {e}")


def account_clean_worker():
    print("[cleaner] بدأ فحص الحسابات كل ساعتين")
    while True:
        try:
            time.sleep(ACCOUNT_CLEAN_INTERVAL)
            cleared = len(BANNED_ACCOUNTS)
            BANNED_ACCOUNTS.clear()
            failed_attempts.clear()
            clear_expired_tokens()
            with _new_api_lock:
                _new_api_status["working"] = None
            print(f"[cleaner] تم مسح {cleared} حساب محظور")
            reload_accounts()
        except Exception as e:
            print(f"[account_clean_worker] {e}")


threading.Thread(target=load_tokens_cache, daemon=True).start()
time.sleep(2)
threading.Thread(target=reload_accounts, daemon=True).start()
threading.Thread(target=token_refresh_worker, daemon=True).start()
threading.Thread(target=account_clean_worker, daemon=True).start()


# ═══════════ صلاحيات ═══════════
def is_admin(user_id):
    return user_id in ADMINS


def is_owner(user_id):
    return user_id == OWNER_ID


def has_access(user_id):
    if is_admin(user_id):
        return True
    if user_id in access_users:
        if access_users[user_id] > time.time():
            return True
        else:
            del access_users[user_id]
            save_data()
    return False


def is_group_enabled(chat_id):
    return chat_id in enabled_groups


def can_use(user_id, chat_type, chat_id):
    if chat_type == 'private':
        return has_access(user_id)
    return is_group_enabled(chat_id)


def get_user_slots(user_id):
    if is_admin(user_id):
        return MAX_SLOTS
    for key, data in keys_db.items():
        if data.get("used_by") == user_id:
            return data.get("slots", DEFAULT_SLOTS)
    return DEFAULT_SLOTS


def get_user_active_slots(user_id):
    with user_slots_lock:
        return len(user_active_spams.get(user_id, {}))


def get_user_free_slots(user_id):
    return max(0, get_user_slots(user_id) - get_user_active_slots(user_id))


# ═══════════ نظام المفاتيح ═══════════
def generate_key(prefix="KRIS"):
    chars = string.ascii_uppercase + string.digits
    part1 = "".join(secrets.choice(chars) for _ in range(4))
    part2 = "".join(secrets.choice(chars) for _ in range(4))
    part3 = "".join(secrets.choice(chars) for _ in range(4))
    return f"{prefix}-{part1}-{part2}-{part3}"


def create_key(admin_id, hours, slots=DEFAULT_SLOTS):
    key = generate_key()
    while key in keys_db:
        key = generate_key()
    keys_db[key] = {
        "created_by": admin_id,
        "created_at": time.time(),
        "duration_hours": int(hours),
        "slots": int(slots),
        "used_by": None,
        "used_at": None,
        "active": True,
    }
    save_data()
    return key


def redeem_key(user_id, key):
    key = key.strip().upper()

    if key not in keys_db:
        return False, "❌ المفتاح غير موجود"

    data = keys_db[key]

    if not data.get("active", True):
        return False, "❌ المفتاح معطل"

    if data.get("used_by") is not None:
        return False, "❌ المفتاح مستخدم بالفعل"

    hours = data.get("duration_hours", 0)
    if hours <= 0:
        return False, "❌ المفتاح غير صالح"

    slots = data.get("slots", DEFAULT_SLOTS)
    expire = time.time() + (hours * 3600)

    if user_id in access_users and access_users[user_id] > time.time():
        access_users[user_id] = access_users[user_id] + (hours * 3600)
    else:
        access_users[user_id] = expire

    data["used_by"] = user_id
    data["used_at"] = time.time()
    save_data()

    remaining = access_users[user_id] - time.time()
    days = int(remaining // 86400)
    hrs = int((remaining % 86400) // 3600)

    return True, f"""✅ تم تفعيل المفتاح

⏱️ المدة: {hours} ساعة ({days}ي {hrs}س متبقي)
🎰 الأماكن: {slots}
⏱️ المتبقي الكلي: {days} يوم و {hrs} ساعة"""


# ═══════════ الاشتراك الإجباري ═══════════
sub_cache = {}
sub_cache_lock = threading.Lock()


def is_subscribed(user_id):
    if not force_channels:
        return True
    now = time.time()
    with sub_cache_lock:
        cached = sub_cache.get(user_id)
        if cached and now - cached["time"] < 300:
            return cached["status"]
    all_ok = True
    for ch in force_channels:
        username = ch.get("username", "").strip()
        if not username:
            continue
        try:
            target = username if username.startswith('@') else f"@{username}"
            member = bot.get_chat_member(target, user_id)
            if member.status not in ['member', 'administrator', 'creator']:
                all_ok = False
                break
        except Exception:
            all_ok = True
    with sub_cache_lock:
        sub_cache[user_id] = {"status": all_ok, "time": now}
    return all_ok


def check_subscription(message):
    user_id = message.from_user.id
    if is_admin(user_id):
        return True
    if user_id in banned_users:
        bot.reply_to(message, "🚫 <b>أنت محظور</b>", parse_mode="HTML")
        return False
    if is_subscribed(user_id):
        return True

    markup = telebot.types.InlineKeyboardMarkup()
    for ch in force_channels:
        markup.add(telebot.types.InlineKeyboardButton(
            text=f"📢 {ch.get('title', 'قناة')}", url=ch.get("link", "#")
        ))
    markup.add(telebot.types.InlineKeyboardButton(text="✅ تحقق", callback_data="check_sub"))
    bot.reply_to(message, f"""╔══════════════════════════╗
║   🔒 𝐒𝐔𝐁𝐒𝐂𝐑𝐈𝐏𝐓𝐈𝐎𝐍 🔒   ║
╚══════════════════════════╝

   اشترك أول 👇 ثم اضغط ✅

🌐 {GROUP_LINK}""", reply_markup=markup, parse_mode="HTML")
    return False


@bot.callback_query_handler(func=lambda c: c.data == "check_sub")
def cb_check_sub(call):
    with sub_cache_lock:
        sub_cache.pop(call.from_user.id, None)
    if is_subscribed(call.from_user.id):
        bot.answer_callback_query(call.id, "✅ تم التحقق", show_alert=True)
        try:
            bot.delete_message(call.message.chat.id, call.message.message_id)
        except Exception:
            pass
    else:
        bot.answer_callback_query(call.id, "❌ لسه مشتركتش", show_alert=True)


def get_remaining_time(user_id):
    if is_admin(user_id):
        return "♾️ دائم (أدمن)"
    if user_id in access_users:
        expire = access_users[user_id]
        if expire > time.time():
            remaining = int(expire - time.time())
            days = remaining // 86400
            hours = (remaining % 86400) // 3600
            minutes = (remaining % 3600) // 60
            if days > 0:
                return f"{days} يوم و {hours} ساعة"
            elif hours > 0:
                return f"{hours} ساعة و {minutes} دقيقة"
            else:
                return f"{minutes} دقيقة"
    return "غير محدد"


# ═══════════ APIs مساعدة ═══════════
def check_api_health():
    try:
        r = requests.get(f"{API_VISIT_URL}/", timeout=5)
        if r.status_code == 200:
            return {"status": "healthy", "service": "HAMO API"}
    except Exception:
        pass
    return {"status": "down", "service": "HAMO API"}


def get_player_info(uid):
    try:
        url = API_INFO_URL.format(uid=uid)
        r = requests.get(url, timeout=15)
        if r.status_code != 200:
            return None
        data = r.json()

        basic = data.get("BasicInformation") or data.get("basicInfo") or {}
        clan = data.get("GuildInformation") or data.get("clanBasicInfo") or {}
        social = data.get("SocialInformation") or data.get("socialInfo") or {}

        nickname = basic.get("Name") or basic.get("nickname")
        if not nickname:
            return None

        return {
            "name": nickname,
            "uid": str(basic.get("UID") or basic.get("accountId", uid)),
            "level": basic.get("Level") or basic.get("level", "N/A"),
            "region": basic.get("Region") or basic.get("region", "N/A"),
            "likes": basic.get("Likes") or basic.get("liked", "N/A"),
            "clan_id": clan.get("GuildID") or clan.get("clanId", ""),
            "clan_name": clan.get("GuildName") or clan.get("clanName", "بدون كلان"),
            "clan_level": clan.get("GuildLevel") or clan.get("clanLevel", "0"),
            "clan_members": clan.get("LiveMembers") or clan.get("memberNum", "0"),
            "clan_capacity": clan.get("MaxMembers") or clan.get("capacity", "0"),
            "clan_captain": clan.get("CaptainID") or clan.get("captainId", "N/A"),
            "signature": social.get("Signature") or social.get("signature", ""),
        }
    except Exception as e:
        print(f"[get_player_info] {e}")
        return None


def send_clan_spam_via_api(clan_id):
    try:
        r = requests.get(f"{API_MAIN_URL}/start", params={"uidclan": str(clan_id)}, timeout=300)
        if r.status_code == 200:
            try:
                data = r.json()
            except Exception:
                return {"success": False, "message": f"رد غير صالح: {r.text[:200]}"}
            results = data.get("results", [])
            succeeded = [x for x in results if x.get("success") is True]
            failed = [x for x in results if x.get("success") is not True]
            total = len(results)
            if total == 0:
                return {"success": False, "message": data.get("error", "لا توجد حسابات")}
            if len(succeeded) > 0:
                return {
                    "success": True,
                    "clan_id": str(clan_id),
                    "succeeded": len(succeeded),
                    "failed": len(failed),
                    "total": total
                }
            return {
                "success": False,
                "message": f"كل الحسابات فشلت ({len(failed)})",
                "succeeded": 0,
                "failed": len(failed),
                "total": total
            }
        return {"success": False, "message": f"HTTP {r.status_code} | {r.text[:200]}"}
    except requests.exceptions.Timeout:
        return {"success": False, "message": "انتهت المهلة"}
    except requests.exceptions.ConnectionError:
        return {"success": False, "message": f"API غير متصل — {API_MAIN_URL}"}
    except Exception as e:
        return {"success": False, "message": str(e)}


def stop_clan_spam_via_api():
    try:
        r = requests.get(f"{API_MAIN_URL}/laveall", timeout=300)
        if r.status_code == 200:
            try:
                data = r.json()
            except Exception:
                return {"success": True, "succeeded": 0, "total": 0}
            results = data.get("results", [])
            succeeded = [x for x in results if x.get("success") is True]
            if len(succeeded) > 0 or data.get("success") is True:
                return {"success": True, "succeeded": len(succeeded), "total": len(results)}
            return {"success": False, "message": f"فشل الإيقاف ({len(results)} حساب)"}
        return {"success": False, "message": f"HTTP {r.status_code}"}
    except Exception as e:
        return {"success": False, "message": str(e)}


# ═══════════ الواجهة ═══════════
def get_welcome_text(user_id):
    remaining = get_remaining_time(user_id)
    slots_used = get_user_active_slots(user_id)
    slots_max = get_user_slots(user_id)

    if is_admin(user_id):
        return f"""👑 مرحباً بك في <b>{DEV_NAME}</b> - لوحة الأدمن

⏳ الوقت: {remaining}
🎰 أماكنك: {slots_used}/{slots_max}

━━━━━━━━━━━━━━━━━━━━━
👤 <b>أوامر الأعضاء:</b>
   🚀 بدء سبام صداقة دائم
   👣 سبام زوار
   🏛️ سبام كلان
   🔍 جلب آيدي كلان
   🛑 إيقاف العمليات
   📊 حالة الخدمة

👑 <b>أوامر الأدمن:</b>
   🔐 إضافة مفتاح
   ⚡ سرعة السبام
   👥 المستخدمون
   🔑 المفاتيح
   📋 سجل العمليات

━━━━━━━━━━━━━━━━━━━━━
👇 اختر من الأسفل:"""
    else:
        return f"""👋 مرحباً بك في <b>{DEV_NAME}</b>

⏳ الوقت المتبقي: {remaining}
🎰 الأماكن المتاحة: {slots_used}/{slots_max}

━━━━━━━━━━━━━━━━━━━━━
📌 <b>الأوامر المتاحة:</b>
   🚀 بدء سبام صداقة دائم
   👣 سبام زوار
   🏛️ سبام كلان
   🔍 جلب آيدي كلان
   🛑 إيقاف العمليات
   📊 حالة الخدمة

━━━━━━━━━━━━━━━━━━━━━
👇 اختر من الأسفل:"""


def get_main_markup(user_id):
    markup = telebot.types.InlineKeyboardMarkup(row_width=2)

    markup.add(
        telebot.types.InlineKeyboardButton("🚀 سبام صداقة دائم", callback_data="menu_smart"),
        telebot.types.InlineKeyboardButton("👣 سبام زوار", callback_data="menu_visit"),
    )
    markup.add(
        telebot.types.InlineKeyboardButton("🏛️ سبام كلان", callback_data="menu_clan_spam"),
        telebot.types.InlineKeyboardButton("🔍 جلب آيدي كلان", callback_data="menu_clan_id"),
    )
    markup.add(
        telebot.types.InlineKeyboardButton("🛑 إيقاف العمليات", callback_data="menu_stop"),
        telebot.types.InlineKeyboardButton("📊 حالة الخدمة", callback_data="menu_status"),
    )

    if is_admin(user_id):
        markup.add(
            telebot.types.InlineKeyboardButton("📋 سجل العمليات", callback_data="menu_logs"),
            telebot.types.InlineKeyboardButton("⚙️ الحسابات", callback_data="menu_accounts"),
        )
        markup.add(
            telebot.types.InlineKeyboardButton("🔐 إضافة مفتاح", callback_data="menu_add_key"),
            telebot.types.InlineKeyboardButton("⚡ سرعة السبام", callback_data="menu_speed"),
        )
        markup.add(
            telebot.types.InlineKeyboardButton("👥 المستخدمون", callback_data="menu_users"),
            telebot.types.InlineKeyboardButton("🔑 المفاتيح", callback_data="menu_keys_list"),
        )

    markup.add(
        telebot.types.InlineKeyboardButton("❓ مساعدة", callback_data="menu_help"),
    )
    return markup


@bot.message_handler(commands=['start', 'help'])
def start(message):
    try:
        user_id = message.from_user.id
        chat_type = message.chat.type
        bot_stats["total_users"].add(user_id)
        bot_stats["start_count"] += 1

        update_user_info(user_id,
                        message.from_user.username or "",
                        message.from_user.first_name or "")

        save_data()

        if chat_type == 'private' and not has_access(user_id):
            markup = telebot.types.InlineKeyboardMarkup()
            markup.add(telebot.types.InlineKeyboardButton(
                text="🔑 إدخال مفتاح", callback_data="menu_redeem_key"
            ))
            markup.add(telebot.types.InlineKeyboardButton(
                text="👑 تواصل مع المطور", url=f"https://t.me/{DEVELOPER.replace('@', '')}"
            ))
            bot.reply_to(message, f"""╔══════════════════════════╗
║    🔒 𝐀𝐂𝐂𝐄𝐒𝐒 𝐃𝐄𝐍𝐈𝐄𝐃 🔒    ║
╚══════════════════════════╝

   هذا البوت يتطلب مفتاح تفعيل

   🔑 اضغط على زر "إدخال مفتاح"

   أو تواصل مع المطور 👇

━━━━━━━━━━━━━━━━━━━━━
💎 {DEVELOPER}
👑 {DEV_NAME}""", reply_markup=markup, parse_mode="HTML")
            return

        bot.reply_to(message, get_welcome_text(user_id),
                     reply_markup=get_main_markup(user_id), parse_mode="HTML")
    except Exception as e:
        print(f"[start] {e}")


@bot.callback_query_handler(func=lambda c: c.data == "menu_main")
def cb_main(call):
    try:
        bot.edit_message_text(
            get_welcome_text(call.from_user.id),
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=get_main_markup(call.from_user.id),
            parse_mode="HTML"
        )
    except Exception:
        pass


@bot.callback_query_handler(func=lambda c: c.data == "menu_help")
def cb_help(call):
    user_id = call.from_user.id
    if is_admin(user_id):
        text = f"""╔══════════════════════════╗
║     👑 𝐀𝐃𝐌𝐈𝐍 𝐇𝐄𝐋𝐏
╚══════════════════════════╝

👤 <b>أوامر الأعضاء:</b>
   🚀 بدء سبام صداقة دائم
   👣 سبام زوار
   🏛️ سبام كلان
   🔍 جلب آيدي كلان
   🛑 إيقاف العمليات
   📊 حالة الخدمة

👑 <b>أوامر الأدمن:</b>
   🔐 إضافة مفتاح
   ⚡ سرعة السبام
   👥 المستخدمون
   🔑 المفاتيح
   📋 سجل العمليات
   ⚙️ الحسابات

━━━━━━━━━━━━━━━━━━━━━
💎 {DEVELOPER}
👑 {DEV_NAME}"""
    else:
        text = f"""╔══════════════════════════╗
║     ❓ 𝐇𝐄𝐋𝐏 𝐌𝐄𝐍𝐔
╚══════════════════════════╝

📌 <b>الأوامر المتاحة:</b>

🚀 بدء سبام صداقة دائم
👣 سبام زوار
🏛️ سبام كلان
🔍 جلب آيدي كلان
🛑 إيقاف العمليات
📊 حالة الخدمة

━━━━━━━━━━━━━━━━━━━━━
💎 {DEVELOPER}
👑 {DEV_NAME}"""

    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton("🔙 رجوع", callback_data="menu_main"))
    try:
        bot.edit_message_text(text, chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              reply_markup=markup, parse_mode="HTML")
    except Exception:
        pass


# ═══════════════════════════════════════════════════
#   ⚙️ قائمة الحسابات
# ═══════════════════════════════════════════════════
@bot.callback_query_handler(func=lambda c: c.data == "menu_accounts")
def cb_menu_accounts(call):
    try:
        if not is_admin(call.from_user.id):
            bot.answer_callback_query(call.id, "❌ للأدمن فقط", show_alert=True)
            return

        user_id = call.from_user.id

        active_smart = 0
        active_visit = 0
        with user_slots_lock:
            for uid, info in user_active_spams.get(user_id, {}).items():
                if info.get("type") == "visit":
                    active_visit += 1
                else:
                    active_smart += 1

        max_slots = get_user_slots(user_id)

        with tokens_cache_lock:
            valid_tokens = sum(1 for v in tokens_cache.values() if v.get("expires_at", 0) > time.time())
            new_api_count = sum(1 for v in tokens_cache.values() if v.get("source") == "new")
            fb1_count = sum(1 for v in tokens_cache.values() if v.get("source") == "fallback_1")
            fb2_count = sum(1 for v in tokens_cache.values() if v.get("source") == "fallback_2")

        with _new_api_lock:
            api_status = "✅ شغال" if _new_api_status["working"] else ("❌ فشل" if _new_api_status["working"] is False else "⏳ لم يُختبر")

        text = f"""╔══════════════════════════╗
║   ⚙️ 𝐀𝐂𝐂𝐎𝐔𝐍𝐓𝐒 𝐒𝐓𝐀𝐓𝐔𝐒
╚══════════════════════════╝

┏━━━━━━━━━━━━━━━━━━━━━┓
┃  🎰 𝐘𝐎𝐔𝐑 𝐒𝐋𝐎𝐓𝐒
┗━━━━━━━━━━━━━━━━━━━━━┛
   🚀 سبام صداقة : {active_smart}
   👣 سبام زوار : {active_visit}
   🏛️ سبام كلان : بواسطة API
   📊 المجموع    : {active_smart + active_visit}/{max_slots}

┏━━━━━━━━━━━━━━━━━━━━━┓
┃  📈 𝐒𝐘𝐒𝐓𝐄𝐌
┗━━━━━━━━━━━━━━━━━━━━━┛
   👥 الحسابات  : {len(bot_accounts)}/{len(ACCOUNTS_LIST)}
   🛡️ محظورة    : {len(BANNED_ACCOUNTS)}
   💾 كاش توكن  : {valid_tokens}
   🆕 jihad-jwt : {new_api_count}
   🥈 de26      : {fb1_count}
   🥉 ff-jwt    : {fb2_count}
   🌐 حالة API  : {api_status}

┏━━━━━━━━━━━━━━━━━━━━━┓
┃  ⚡ 𝐒𝐏𝐄𝐄𝐃
┗━━━━━━━━━━━━━━━━━━━━━┛
   • الدفعة: {BATCH_SIZE}
   • التأخير: {BATCH_DELAY}s

┏━━━━━━━━━━━━━━━━━━━━━┓
┃  📡 𝐀𝐏𝐈
┗━━━━━━━━━━━━━━━━━━━━━┛
   • الكلان  : {API_MAIN_URL}
   • الزوار  : {API_VISIT_URL}

━━━━━━━━━━━━━━━━━━━━━
💎 {DEVELOPER}
👑 {DEV_NAME}"""

        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton("🔄 تحديث", callback_data="menu_accounts"))
        markup.add(telebot.types.InlineKeyboardButton("🔙 رجوع", callback_data="menu_main"))
        bot.edit_message_text(text, chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              reply_markup=markup, parse_mode="HTML")
    except Exception as e:
        print(f"[cb_menu_accounts] {e}")


# ═══════════════════════════════════════════════════
#   🏛️ سبام كلان
# ═══════════════════════════════════════════════════
@bot.callback_query_handler(func=lambda c: c.data == "menu_clan_spam")
def cb_menu_clan_spam(call):
    text = f"""╔══════════════════════════╗
║   🏛️ 𝐂𝐋𝐀𝐍 𝐒𝐏𝐀𝐌
╚══════════════════════════╝

📝 أرسل آيدي الكلان:

   مثال: <code>3105508490</code>

⚠️ سيتم إرسال طلبات انضمام
   من كل الحسابات المتاحة

━━━━━━━━━━━━━━━━━━━━━
💎 {DEVELOPER}
👑 {DEV_NAME}"""

    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton("🔙 رجوع", callback_data="menu_main"))
    try:
        bot.edit_message_text(text, chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              reply_markup=markup, parse_mode="HTML")
        bot.register_next_step_handler(call.message, receive_clan_spam_id)
    except Exception:
        pass


def receive_clan_spam_id(message):
    try:
        user_id = message.from_user.id

        if not check_subscription(message):
            return
        if not can_use(user_id, message.chat.type, message.chat.id):
            return

        clan_id = sanitize_input(message.text.strip())
        if not clan_id or not clan_id.isdigit():
            bot.reply_to(message, "❌ آيدي الكلان غير صحيح")
            return

        msg = bot.reply_to(message, f"""╔══════════════════════════╗
║   🏛️ 𝐒𝐓𝐀𝐑𝐓𝐈𝐍𝐆 𝐂𝐋𝐀𝐍
╚══════════════════════════╝

   🆔 الكلان : <code>{clan_id}</code>

   جاري البدء...

👑 {DEV_NAME}""", parse_mode="HTML")

        result = send_clan_spam_via_api(clan_id)
        bot_stats["clan_spams"] = bot_stats.get("clan_spams", 0) + 1
        save_data()
        add_log(user_id, "/clan_spam", f"clan_id={clan_id}",
                message.from_user.username or "")

        if result.get("success"):
            s = result.get("succeeded", 0)
            f = result.get("failed", 0)
            t = result.get("total", 0)
            success_msg = f"""╔══════════════════════════╗
║   ✅ 𝐂𝐋𝐀𝐍 𝐒𝐏𝐀𝐌 ✅
╚══════════════════════════╝

   🏛️ تم بدء سبام الكلان
   🆔 <code>{clan_id}</code>
   🔥 الحالة : ON FIRE

┏━━━━━━━━━━━━━━━━━━━━━┓
┃  📊 𝐑𝐄𝐒𝐔𝐋𝐓
┗━━━━━━━━━━━━━━━━━━━━━┛
   ✅ ناجحة   : {s}
   ❌ فاشلة   : {f}
   📊 المجموع : {t}

👑 {DEV_NAME}
💎 {DEVELOPER}"""
            bot.edit_message_text(success_msg, chat_id=message.chat.id, message_id=msg.message_id, parse_mode="HTML")
        else:
            fail_msg = f"""╔══════════════════════════╗
║   ❌ 𝐂𝐋𝐀𝐍 𝐅𝐀𝐈𝐋𝐄𝐃 ❌
╚══════════════════════════╝

   🆔 <code>{clan_id}</code>
   ❌ السبب : {result.get('message', 'خطأ')}

👑 {DEV_NAME}"""
            bot.edit_message_text(fail_msg, chat_id=message.chat.id, message_id=msg.message_id, parse_mode="HTML")
    except Exception as e:
        print(f"[receive_clan_spam_id] {e}")


# ═══════════════════════════════════════════════════
#   🔍 جلب آيدي كلان
# ═══════════════════════════════════════════════════
@bot.callback_query_handler(func=lambda c: c.data == "menu_clan_id")
def cb_menu_clan_id(call):
    text = f"""╔══════════════════════════╗
║   🔍 𝐆𝐄𝐓 𝐂𝐋𝐀𝐍 𝐈𝐃
╚══════════════════════════╝

📝 أرسل آيدي اللاعب:

   مثال: <code>13265775096</code>

━━━━━━━━━━━━━━━━━━━━━
✅ يجيب آيدي الكلان + أسماء الأعضاء

💎 {DEVELOPER}
👑 {DEV_NAME}"""

    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton("🔙 رجوع", callback_data="menu_main"))
    try:
        bot.edit_message_text(text, chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              reply_markup=markup, parse_mode="HTML")
        bot.register_next_step_handler(call.message, receive_clan_id_uid)
    except Exception:
        pass


def receive_clan_id_uid(message):
    try:
        user_id = message.from_user.id

        if not check_subscription(message):
            return
        if not can_use(user_id, message.chat.type, message.chat.id):
            return

        uid = sanitize_input(message.text.strip())
        if not is_safe_uid(uid):
            bot.reply_to(message, "❌ UID غير صحيح")
            return

        msg = bot.reply_to(message, "🔍 جاري البحث...")

        info = get_player_info(uid)
        bot_stats["checks"] = bot_stats.get("checks", 0) + 1
        save_data()

        if not info:
            return bot.edit_message_text(
                f"❌ مش لاقي اللاعب <code>{uid}</code>",
                chat_id=message.chat.id, message_id=msg.message_id, parse_mode="HTML"
            )

        clan_id = info.get("clan_id", "")
        if not clan_id:
            return bot.edit_message_text(
                f"""╔══════════════════════════╗
║   📋 𝐏𝐋𝐀𝐘𝐄𝐑 𝐈𝐍𝐅𝐎
╚══════════════════════════╝

👤 <b>{info.get('name', 'غير معروف')}</b>
🆔 <code>{uid}</code>
🌍 {info.get('region', 'N/A')}

⚠️ اللاعب ليس في كلان

👑 {DEV_NAME}""",
                chat_id=message.chat.id, message_id=msg.message_id, parse_mode="HTML"
            )

        text = f"""╔══════════════════════════╗
║   🏛️ 𝐂𝐋𝐀𝐍 𝐈𝐍𝐅𝐎
╚══════════════════════════╝

┏━━━━━━━━━━━━━━━━━━━━━┓
┃  👤 𝐏𝐋𝐀𝐘𝐄𝐑
┗━━━━━━━━━━━━━━━━━━━━━┛
   👤 الاسم  : <b>{info.get('name', 'غير معروف')}</b>
   🆔 UID   : <code>{uid}</code>
   🌍 السيرفر : {info.get('region', 'N/A')}
   📊 المستوى : {info.get('level', 'N/A')}

┏━━━━━━━━━━━━━━━━━━━━━┓
┃  🏛️ 𝐂𝐋𝐀𝐍
┗━━━━━━━━━━━━━━━━━━━━━┛
   🏛️ الاسم  : <b>{info.get('clan_name', 'بدون')}</b>
   🆔 الكلان : <code>{clan_id}</code>
   📊 المستوى : {info.get('clan_level', '0')}
   👥 الأعضاء : {info.get('clan_members', '0')}/{info.get('clan_capacity', '0')}
   👑 القائد  : <code>{info.get('clan_captain', 'N/A')}</code>

━━━━━━━━━━━━━━━━━━━━━
💎 {DEVELOPER}
👑 {DEV_NAME}"""

        markup = telebot.types.InlineKeyboardMarkup(row_width=1)
        markup.add(telebot.types.InlineKeyboardButton(
            text="🏛️ بدء سبام هذا الكلان",
            callback_data=f"clan_spam_quick_{clan_id}"
        ))

        bot.edit_message_text(text, chat_id=message.chat.id,
                              message_id=msg.message_id,
                              reply_markup=markup, parse_mode="HTML")
    except Exception as e:
        print(f"[receive_clan_id_uid] {e}")


@bot.callback_query_handler(func=lambda c: c.data.startswith("clan_spam_quick_"))
def cb_clan_spam_quick(call):
    try:
        clan_id = call.data.replace("clan_spam_quick_", "")
        bot.answer_callback_query(call.id, f"🏛️ جاري بدء السبام على {clan_id}...", show_alert=False)

        bot.edit_message_text(
            f"""╔══════════════════════════╗
║   🏛️ 𝐒𝐓𝐀𝐑𝐓𝐈𝐍𝐆 𝐂𝐋𝐀𝐍
╚══════════════════════════╝

   🆔 الكلان : <code>{clan_id}</code>

   جاري البدء...

👑 {DEV_NAME}""",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            parse_mode="HTML"
        )

        result = send_clan_spam_via_api(clan_id)
        bot_stats["clan_spams"] = bot_stats.get("clan_spams", 0) + 1
        save_data()
        add_log(call.from_user.id, "/clan_spam_quick", f"clan_id={clan_id}",
                call.from_user.username or "")

        if result.get("success"):
            s = result.get("succeeded", 0)
            f = result.get("failed", 0)
            t = result.get("total", 0)
            success_msg = f"""╔══════════════════════════╗
║   ✅ 𝐂𝐋𝐀𝐍 𝐒𝐏𝐀𝐌 ✅
╚══════════════════════════╝

   🏛️ تم بدء سبام الكلان
   🆔 <code>{clan_id}</code>
   🔥 الحالة : ON FIRE

┏━━━━━━━━━━━━━━━━━━━━━┓
┃  📊 𝐑𝐄𝐒𝐔𝐋𝐓
┗━━━━━━━━━━━━━━━━━━━━━┛
   ✅ ناجحة   : {s}
   ❌ فاشلة   : {f}
   📊 المجموع : {t}

👑 {DEV_NAME}"""
            bot.edit_message_text(success_msg, chat_id=call.message.chat.id,
                                  message_id=call.message.message_id, parse_mode="HTML")
        else:
            fail_msg = f"""╔══════════════════════════╗
║   ❌ 𝐂𝐋𝐀𝐍 𝐅𝐀𝐈𝐋𝐄𝐃 ❌
╚══════════════════════════╝

   🆔 <code>{clan_id}</code>
   ❌ {result.get('message', 'خطأ')}

👑 {DEV_NAME}"""
            bot.edit_message_text(fail_msg, chat_id=call.message.chat.id,
                                  message_id=call.message.message_id, parse_mode="HTML")
    except Exception as e:
        print(f"[cb_clan_spam_quick] {e}")


# ═══════════════════════════════════════════════════
#   👥 قائمة المستخدمين
# ═══════════════════════════════════════════════════
@bot.callback_query_handler(func=lambda c: c.data == "menu_users")
def cb_menu_users(call):
    try:
        if not is_admin(call.from_user.id):
            bot.answer_callback_query(call.id, "❌ للأدمن فقط", show_alert=True)
            return

        if not access_users and not user_info:
            bot.answer_callback_query(call.id, "📋 لا يوجد مستخدمون", show_alert=True)
            return

        now = time.time()
        lines = ["╔══════════════════════════╗",
                 "║   👥 المستخدمون",
                 "╚══════════════════════════╝",
                 ""]

        active_users = [(uid, exp) for uid, exp in access_users.items() if exp > now]
        expired_users = [(uid, exp) for uid, exp in access_users.items() if exp <= now]

        lines.append(f"📊 <b>الكل: {len(access_users)}</b> | نشط: {len(active_users)} | منتهي: {len(expired_users)}")
        lines.append("")

        markup = telebot.types.InlineKeyboardMarkup(row_width=1)

        count = 0
        for uid, expire in sorted(active_users, key=lambda x: x[1], reverse=True)[:20]:
            info = user_info.get(uid, {})
            username = info.get("username", "")
            first_name = info.get("first_name", "")

            key_info = ""
            for k, v in keys_db.items():
                if v.get("used_by") == uid:
                    key_info = f"🔑 {k[:15]}... | 🎰 {v.get('slots', DEFAULT_SLOTS)}"
                    break

            remaining = int(expire - now)
            days = remaining // 86400
            hours = (remaining % 86400) // 3600

            display_name = first_name or username or str(uid)
            user_tag = f"@{username}" if username else f"<code>{uid}</code>"

            lines.append(f"👤 <b>{display_name}</b>")
            lines.append(f"   🆔 {user_tag}")
            lines.append(f"   ⏱️ {days}ي {hours}س")
            if key_info:
                lines.append(f"   {key_info}")
            lines.append("")

            markup.add(telebot.types.InlineKeyboardButton(
                f"🗑️ حذف {display_name[:20]}",
                callback_data=f"del_user_{uid}"
            ))

            count += 1
            if count >= 20:
                break

        markup.add(telebot.types.InlineKeyboardButton("🔄 تحديث", callback_data="menu_users"))
        markup.add(telebot.types.InlineKeyboardButton("🔙 رجوع", callback_data="menu_main"))

        try:
            bot.edit_message_text("\n".join(lines), chat_id=call.message.chat.id,
                                  message_id=call.message.message_id,
                                  reply_markup=markup, parse_mode="HTML")
        except Exception:
            bot.send_message(call.message.chat.id, "\n".join(lines), reply_markup=markup, parse_mode="HTML")
    except Exception as e:
        print(f"[cb_menu_users] {e}")


@bot.callback_query_handler(func=lambda c: c.data.startswith("del_user_"))
def cb_del_user(call):
    try:
        if not is_admin(call.from_user.id):
            bot.answer_callback_query(call.id, "❌ للأدمن فقط", show_alert=True)
            return

        user_id = int(call.data.replace("del_user_", ""))

        if user_id in access_users:
            del access_users[user_id]

        with user_slots_lock:
            if user_id in user_active_spams:
                user_active_spams[user_id].clear()
                del user_active_spams[user_id]
            if user_id in user_queues:
                user_queues[user_id].clear()
                del user_queues[user_id]

        save_data()
        save_active_spams()
        add_log(call.from_user.id, "/deluser", f"deleted={user_id}",
                call.from_user.username or "")

        bot.answer_callback_query(call.id, f"✅ تم حذف {user_id}", show_alert=True)
        cb_menu_users(call)
    except Exception as e:
        print(f"[cb_del_user] {e}")


# ═══════════════════════════════════════════════════
#   🔑 قائمة المفاتيح
# ═══════════════════════════════════════════════════
@bot.callback_query_handler(func=lambda c: c.data == "menu_keys_list")
def cb_menu_keys_list(call):
    try:
        if not is_admin(call.from_user.id):
            bot.answer_callback_query(call.id, "❌ للأدمن فقط", show_alert=True)
            return

        if not keys_db:
            bot.answer_callback_query(call.id, "📋 لا توجد مفاتيح", show_alert=True)
            return

        lines = ["╔══════════════════════════╗",
                 "║   🔑 المفاتيح",
                 "╚══════════════════════════╝",
                 ""]

        used = sum(1 for k, v in keys_db.items() if v.get("used_by"))
        available = len(keys_db) - used
        lines.append(f"📊 <b>الكل: {len(keys_db)}</b> | ✅ مستخدم: {used} | 🟢 متاح: {available}")
        lines.append("")

        markup = telebot.types.InlineKeyboardMarkup(row_width=1)

        for i, (key, data) in enumerate(list(keys_db.items())[-15:], 1):
            if data.get("used_by"):
                used_by = data["used_by"]
                info = user_info.get(used_by, {})
                username = info.get("username", "")
                first_name = info.get("first_name", "")

                display = first_name or username or str(used_by)
                user_tag = f"@{username}" if username else f"<code>{used_by}</code>"

                used_at = data.get("used_at", 0)
                used_time = datetime.fromtimestamp(used_at).strftime("%Y-%m-%d %H:%M") if used_at else "?"

                status = f"✅ {display}"
            else:
                status = "🟢 متاح"
                user_tag = "—"
                used_time = "—"

            hours = data.get("duration_hours", 0)
            slots = data.get("slots", DEFAULT_SLOTS)
            days = hours // 24

            lines.append(f"{i}. <code>{key}</code>")
            lines.append(f"   {status}")
            lines.append(f"   👤 {user_tag}")
            lines.append(f"   📅 {used_time}")
            lines.append(f"   ⏱️ {days}ي | 🎰 {slots}")
            lines.append("")

        markup.add(telebot.types.InlineKeyboardButton("🔄 تحديث", callback_data="menu_keys_list"))
        markup.add(telebot.types.InlineKeyboardButton("🔙 رجوع", callback_data="menu_main"))

        try:
            bot.edit_message_text("\n".join(lines), chat_id=call.message.chat.id,
                                  message_id=call.message.message_id,
                                  reply_markup=markup, parse_mode="HTML")
        except Exception:
            bot.send_message(call.message.chat.id, "\n".join(lines), reply_markup=markup, parse_mode="HTML")
    except Exception as e:
        print(f"[cb_menu_keys_list] {e}")


# ═══════════════════════════════════════════════════
#   🔑 نظام المفاتيح
# ═══════════════════════════════════════════════════
@bot.callback_query_handler(func=lambda c: c.data == "menu_redeem_key")
def cb_menu_redeem_key(call):
    text = f"""╔══════════════════════════╗
║   🔑 إدخال مفتاح التفعيل
╚══════════════════════════╝

📝 أرسل المفتاح الخاص بك

   الصيغة: <code>KRIS-XXXX-XXXX-XXXX</code>

━━━━━━━━━━━━━━━━━━━━━
💎 {DEVELOPER}
👑 {DEV_NAME}"""

    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton("🔙 رجوع", callback_data="menu_main"))

    try:
        if call.message.text or call.message.caption:
            bot.edit_message_text(text, chat_id=call.message.chat.id,
                                  message_id=call.message.message_id,
                                  reply_markup=markup, parse_mode="HTML")
        else:
            bot.send_message(call.message.chat.id, text, reply_markup=markup, parse_mode="HTML")
        bot.register_next_step_handler(call.message, receive_redeem_key)
    except Exception:
        bot.send_message(call.message.chat.id, text, reply_markup=markup, parse_mode="HTML")
        bot.register_next_step_handler(call.message, receive_redeem_key)


def receive_redeem_key(message):
    try:
        if not message.text:
            bot.reply_to(message, "❌ أرسل المفتاح كنص")
            return

        key = message.text.strip()
        user_id = message.from_user.id

        success, msg = redeem_key(user_id, key)
        add_log(user_id, "/redeem", f"key={key[:8]}... ok={success}",
                message.from_user.username or "")

        update_user_info(user_id,
                        message.from_user.username or "",
                        message.from_user.first_name or "")

        if success:
            bot.reply_to(message, f"""╔══════════════════════════╗
║   ✅ 𝐊𝐄𝐘 𝐀𝐂𝐓𝐈𝐕𝐀𝐓𝐄𝐃
╚══════════════════════════╝

{msg}

━━━━━━━━━━━━━━━━━━━━━
💎 {DEVELOPER}
👑 {DEV_NAME}""", parse_mode="HTML")
        else:
            bot.reply_to(message, f"❌ {msg}")
    except Exception as e:
        print(f"[receive_redeem_key] {e}")


@bot.callback_query_handler(func=lambda c: c.data == "menu_add_key")
def cb_menu_add_key(call):
    if not is_admin(call.from_user.id):
        bot.answer_callback_query(call.id, "❌ للأدمن فقط", show_alert=True)
        return

    text = f"""╔══════════════════════════╗
║   🔐 إضافة مفتاح جديد
╚══════════════════════════╝

📝 الصيغة:
   <code>الأيام الساعات الأماكن</code>

━━━━━━━━━━━━━━━━━━━━━
أمثلة:
   • <code>1 0 2</code>   → يوم + 2 أماكن
   • <code>7 12 5</code>  → 7 أيام و 12 ساعة + 5 أماكن

⚠️ الحد الأقصى: 365 يوم، 100 مكان

━━━━━━━━━━━━━━━━━━━━━
💎 {DEVELOPER}
👑 {DEV_NAME}"""

    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton("🔙 رجوع", callback_data="menu_main"))

    try:
        bot.edit_message_text(text, chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              reply_markup=markup, parse_mode="HTML")
        bot.register_next_step_handler(call.message, receive_add_key)
    except Exception:
        pass


def receive_add_key(message):
    try:
        if not is_admin(message.from_user.id):
            return

        parts = message.text.strip().split()

        if len(parts) < 2:
            bot.reply_to(message, "❌ الصيغة: <code>الأيام الساعات الأماكن</code>", parse_mode="HTML")
            return

        try:
            days = int(parts[0])
            hours = int(parts[1]) if len(parts) > 1 else 0
            slots = int(parts[2]) if len(parts) > 2 else DEFAULT_SLOTS
        except ValueError:
            bot.reply_to(message, "❌ أرسل أرقام فقط")
            return

        if days < 0 or hours < 0 or slots < 1:
            bot.reply_to(message, "❌ القيم غير صحيحة")
            return

        total_hours = (days * 24) + hours

        if total_hours <= 0:
            bot.reply_to(message, "❌ المدة يجب أن تكون > 0")
            return

        if days > 365:
            bot.reply_to(message, "❌ الحد الأقصى 365 يوم")
            return

        if slots > MAX_SLOTS:
            bot.reply_to(message, f"❌ الحد الأقصى {MAX_SLOTS} أماكن")
            return

        key = create_key(message.from_user.id, total_hours, slots)

        add_log(message.from_user.id, "/addkey",
                f"key={key} hours={total_hours} slots={slots}",
                message.from_user.username or "")

        bot.reply_to(message, f"""╔══════════════════════════╗
║   ✅ 𝐊𝐄𝐘 𝐂𝐑𝐄𝐀𝐓𝐄𝐃
╚══════════════════════════╝

🔑 المفتاح:
<code>{key}</code>

⏱️ المدة: {days} يوم و {hours} ساعة
🎰 الأماكن: {slots}

📤 أرسل المفتاح للمستخدم

━━━━━━━━━━━━━━━━━━━━━
💎 {DEVELOPER}
👑 {DEV_NAME}""", parse_mode="HTML")

    except Exception as e:
        print(f"[receive_add_key] {e}")


# ═══════════════════════════════════════════════════
#   ⚡ سرعة السبام
# ═══════════════════════════════════════════════════
def get_speed_text():
    speed_label = "🐢 بطيء"
    if BATCH_SIZE >= 50:
        speed_label = "🔥🔥🔥 جنون"
    elif BATCH_SIZE >= 20:
        speed_label = "🔥🔥 سريع جداً"
    elif BATCH_SIZE >= 10:
        speed_label = "🔥 سريع"
    elif BATCH_SIZE >= 5:
        speed_label = "⚡ متوسط"

    return f"""╔══════════════════════════╗
║   ⚡ 𝐒𝐏𝐀𝐌 𝐒𝐏𝐄𝐄𝐃
╚══════════════════════════╝

📊 الإعدادات الحالية:
   • حجم الدفعة: <b>{BATCH_SIZE}</b>
   • التأخير: <b>{BATCH_DELAY}</b> ثانية
   • فترة الفحص: <b>{DEFAULT_CHECK_INTERVAL}</b> ثانية
   • التقييم: {speed_label}

━━━━━━━━━━━━━━━━━━━━━

⚙️ الإعدادات الجاهزة:

   🐢 بطيء    → دفعة 3  | تأخير 15s
   ⚡ عادي    → دفعة 5  | تأخير 10s
   🔥 سريع    → دفعة 15 | تأخير 5s
   🔥🔥 أسرع  → دفعة 25 | تأخير 3s
   🔥🔥🔥 جنون → دفعة 50 | تأخير 1s"""


def get_speed_markup():
    markup = telebot.types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        telebot.types.InlineKeyboardButton("🐢 بطيء", callback_data="speed_preset_slow"),
        telebot.types.InlineKeyboardButton("⚡ عادي", callback_data="speed_preset_normal"),
    )
    markup.add(
        telebot.types.InlineKeyboardButton("🔥 سريع", callback_data="speed_preset_fast"),
        telebot.types.InlineKeyboardButton("🔥🔥 أسرع", callback_data="speed_preset_faster"),
    )
    markup.add(
        telebot.types.InlineKeyboardButton("🔥🔥🔥 جنون", callback_data="speed_preset_insane"),
    )
    markup.add(
        telebot.types.InlineKeyboardButton("✏️ مخصص", callback_data="speed_custom"),
        telebot.types.InlineKeyboardButton("🔄 تحديث", callback_data="menu_speed"),
    )
    markup.add(
        telebot.types.InlineKeyboardButton("♻️ استعادة الافتراضي", callback_data="speed_reset"),
    )
    markup.add(
        telebot.types.InlineKeyboardButton("🔙 رجوع", callback_data="menu_main"),
    )
    return markup


@bot.callback_query_handler(func=lambda c: c.data == "menu_speed")
def cb_menu_speed(call):
    try:
        if not is_admin(call.from_user.id):
            bot.answer_callback_query(call.id, "❌ للأدمن فقط", show_alert=True)
            return
        bot.edit_message_text(
            get_speed_text(),
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=get_speed_markup(),
            parse_mode="HTML"
        )
    except Exception:
        pass


@bot.callback_query_handler(func=lambda c: c.data.startswith("speed_preset_"))
def cb_speed_preset(call):
    try:
        if not is_admin(call.from_user.id):
            bot.answer_callback_query(call.id, "❌ للأدمن فقط", show_alert=True)
            return

        preset = call.data.replace("speed_preset_", "")

        presets = {
            "slow":    {"batch_size": 3,  "batch_delay": 15, "check_interval": 20},
            "normal":  {"batch_size": 5,  "batch_delay": 10, "check_interval": 15},
            "fast":    {"batch_size": 15, "batch_delay": 5,  "check_interval": 15},
            "faster":  {"batch_size": 25, "batch_delay": 3,  "check_interval": 10},
            "insane":  {"batch_size": 50, "batch_delay": 1,  "check_interval": 5},
        }

        if preset not in presets:
            bot.answer_callback_query(call.id, "❌ إعداد غير معروف", show_alert=True)
            return

        with speed_lock:
            speed_config.update(presets[preset])
            apply_speed()
            save_speed_config()

        add_log(call.from_user.id, "/speed", f"preset={preset}",
                call.from_user.username or "")

        bot.answer_callback_query(call.id,
            f"✅ تم التطبيق: دفعة {BATCH_SIZE} | تأخير {BATCH_DELAY}s",
            show_alert=True)

        bot.edit_message_text(
            get_speed_text(),
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=get_speed_markup(),
            parse_mode="HTML"
        )
    except Exception as e:
        print(f"[cb_speed_preset] {e}")


@bot.callback_query_handler(func=lambda c: c.data == "speed_reset")
def cb_speed_reset(call):
    try:
        if not is_admin(call.from_user.id):
            bot.answer_callback_query(call.id, "❌ للأدمن فقط", show_alert=True)
            return

        with speed_lock:
            speed_config.update({"batch_size": 15, "batch_delay": 5, "check_interval": 15})
            apply_speed()
            save_speed_config()

        bot.answer_callback_query(call.id, "♻️ تم استعادة الافتراضي", show_alert=True)

        bot.edit_message_text(
            get_speed_text(),
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=get_speed_markup(),
            parse_mode="HTML"
        )
    except Exception as e:
        print(f"[cb_speed_reset] {e}")


@bot.callback_query_handler(func=lambda c: c.data == "speed_custom")
def cb_speed_custom(call):
    try:
        if not is_admin(call.from_user.id):
            bot.answer_callback_query(call.id, "❌ للأدمن فقط", show_alert=True)
            return

        bot.answer_callback_query(call.id)
        bot.edit_message_text(
            f"""╔══════════════════════════╗
║   ✏️ 𝐂𝐔𝐒𝐓𝐎𝐌 𝐒𝐏𝐄𝐄𝐃
╚══════════════════════════╝

📝 أرسل 3 أرقام:
   <code>batch delay interval</code>

مثال: <code>15 5 10</code>""",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            parse_mode="HTML"
        )
        bot.register_next_step_handler(call.message, receive_custom_speed)
    except Exception as e:
        print(f"[cb_speed_custom] {e}")


def receive_custom_speed(message):
    try:
        if not is_admin(message.from_user.id):
            return

        parts = message.text.strip().split()

        if len(parts) != 3:
            bot.reply_to(message, "❌ أرسل 3 أرقام: batch delay interval")
            return

        try:
            batch = int(parts[0])
            delay = int(parts[1])
            interval = int(parts[2])
        except ValueError:
            bot.reply_to(message, "❌ أرقام فقط")
            return

        if not (1 <= batch <= 100):
            bot.reply_to(message, "❌ batch: 1-100")
            return
        if not (0 <= delay <= 60):
            bot.reply_to(message, "❌ delay: 0-60")
            return
        if not (1 <= interval <= 120):
            bot.reply_to(message, "❌ interval: 1-120")
            return

        with speed_lock:
            speed_config.update({
                "batch_size": batch,
                "batch_delay": delay,
                "check_interval": interval,
            })
            apply_speed()
            save_speed_config()

        add_log(message.from_user.id, "/speed/custom",
                f"batch={batch} delay={delay} interval={interval}",
                message.from_user.username or "")

        bot.reply_to(message, f"""✅ <b>تم التحديث</b>

⚙️ الدفعة: {BATCH_SIZE}
⏱️ التأخير: {BATCH_DELAY}s
🔄 الفحص: {DEFAULT_CHECK_INTERVAL}s""", parse_mode="HTML")

    except Exception as e:
        print(f"[receive_custom_speed] {e}")


# ═══════════════════════════════════════════════════
#   👣 سبام زوار
# ═══════════════════════════════════════════════════
@bot.callback_query_handler(func=lambda c: c.data == "menu_visit")
def cb_menu_visit(call):
    text = f"""╔══════════════════════════╗
║   👣 𝐒𝐄𝐍𝐃 𝐕𝐈𝐒𝐈𝐓𝐎𝐑𝐒
╚══════════════════════════╝

📝 أرسل البيانات بالصيغة:

   <code>UID العدد</code>

مثال:
   <code>123456789 500</code>

⚠️ الحد الأقصى: 5000 زائر
🎰 أماكنك: {get_user_active_slots(call.from_user.id)}/{get_user_slots(call.from_user.id)}

━━━━━━━━━━━━━━━━━━━━━
💎 {DEVELOPER}
👑 {DEV_NAME}"""

    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton("🔙 رجوع", callback_data="menu_main"))
    try:
        bot.edit_message_text(text, chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              reply_markup=markup, parse_mode="HTML")
        bot.register_next_step_handler(call.message, receive_visit_data)
    except Exception:
        pass


def receive_visit_data(message):
    try:
        user_id = message.from_user.id

        if not check_subscription(message):
            return
        if not can_use(user_id, message.chat.type, message.chat.id):
            return

        parts = message.text.strip().split()
        if len(parts) < 2:
            bot.reply_to(message, "❌ الصيغة: <code>UID العدد</code>", parse_mode="HTML")
            return

        uid = sanitize_input(parts[0])
        if not is_safe_uid(uid):
            bot.reply_to(message, "❌ UID غير صحيح")
            return

        try:
            count = int(parts[1])
            if count < 1 or count > 5000:
                bot.reply_to(message, "❌ العدد: 1-5000")
                return
        except ValueError:
            bot.reply_to(message, "❌ العدد غير صحيح")
            return

        with user_slots_lock:
            current = len(user_active_spams.get(user_id, {}))
            max_slots = get_user_slots(user_id)

            if current >= max_slots:
                bot.reply_to(message, f"""❌ <b>الأماكن ممتلئة</b>

🎰 أماكنك: {current}/{max_slots}
⏳ انتظر انتهاء عملية""", parse_mode="HTML")
                return

            if user_id not in user_active_spams:
                user_active_spams[user_id] = {}
            user_active_spams[user_id][f"visit_{uid}"] = {
                "type": "visit",
                "target": uid,
                "count": count,
                "started_at": time.time(),
                "chat_id": message.chat.id,
            }

        save_active_spams()
        add_log(user_id, "/visit", f"uid={uid} count={count}",
                message.from_user.username or "")

        threading.Thread(
            target=visit_worker,
            args=(message.chat.id, uid, count, user_id),
            daemon=True
        ).start()

        bot.reply_to(message, f"""✅ <b>بدأ إرسال الزوار</b>

🎯 UID: <code>{uid}</code>
👣 العدد: {count}
🎰 الأماكن: {get_user_active_slots(user_id)}/{get_user_slots(user_id)}

💎 {DEVELOPER}
👑 {DEV_NAME}""", parse_mode="HTML")

    except Exception as e:
        print(f"[receive_visit_data] {e}")


def visit_worker(chat_id, target_uid, count, user_id):
    try:
        try:
            r = requests.get(
                f"{API_VISIT_URL}/visit/{target_uid}",
                params={"count": count},
                timeout=180
            )

            result = None
            try:
                result = r.json()
            except Exception:
                result = {"status": "error", "msg": "invalid response"}

            if result.get("status") == "error" and "refresh" in str(result.get("msg", "")).lower():
                try:
                    bot.send_message(chat_id, "⏳ جاري تحضير الخدمة... (30 ثانية)")
                except Exception:
                    pass

                requests.get(f"{API_VISIT_URL}/refresh", timeout=60)
                time.sleep(30)

                r = requests.get(
                    f"{API_VISIT_URL}/visit/{target_uid}",
                    params={"count": count},
                    timeout=180
                )
                try:
                    result = r.json()
                except Exception:
                    result = {"status": "error", "msg": "invalid response"}

            if r.status_code == 200 and result.get("status") == "success":
                bot_stats["visits_sent"] = bot_stats.get("visits_sent", 0) + 1
                save_data()

                sent = result.get("Request Sent", count)
                tokens = result.get("Tokens Used", 0)

                try:
                    bot.send_message(chat_id, f"""╔══════════════════════════╗
║   ✅ 𝐕𝐈𝐒𝐈𝐓𝐎𝐑𝐒 𝐒𝐄𝐍𝐓
╚══════════════════════════╝

🎯 UID: <code>{target_uid}</code>
👣 أُرسل: {sent}
🔑 التوكنات: {tokens}""", parse_mode="HTML")
                except Exception:
                    pass
            else:
                err = result.get("msg", result.get("error", "خطأ غير معروف"))
                try:
                    bot.send_message(chat_id, f"""❌ <b>فشل إرسال الزوار</b>

🎯 UID: <code>{target_uid}</code>
❌ السبب: {err}""", parse_mode="HTML")
                except Exception:
                    pass

        finally:
            with user_slots_lock:
                if user_id in user_active_spams:
                    user_active_spams[user_id].pop(f"visit_{target_uid}", None)
                    if not user_active_spams[user_id]:
                        del user_active_spams[user_id]

            save_active_spams()
            release_user_slot(user_id, f"visit_{target_uid}")

    except Exception as e:
        print(f"[visit_worker] {e}")
        try:
            with user_slots_lock:
                if user_id in user_active_spams:
                    user_active_spams[user_id].pop(f"visit_{target_uid}", None)
            save_active_spams()
        except Exception:
            pass


# ═══════════════════════════════════════════════════
#   🚀 سبام صداقة دائم
# ═══════════════════════════════════════════════════
@bot.callback_query_handler(func=lambda c: c.data == "menu_smart")
def cb_menu_smart(call):
    text = f"""╔══════════════════════════╗
║  🚀 𝐏𝐄𝐑𝐌𝐀𝐍𝐄𝐍𝐓 𝐅𝐑𝐈𝐄𝐍𝐃 𝐒𝐏𝐀𝐌
╚══════════════════════════╝

📝 أرسل UID المستهدف:

   يمكنك إرسال أكثر من شخص بفاصلة:
   2342672180, 987654321

⏱️ المدة: تختارها في الخطوة التالية
🔄 فترة الفحص: {DEFAULT_CHECK_INTERVAL}s
📦 الدفعة: {BATCH_SIZE}
🎰 أماكنك: {get_user_active_slots(call.from_user.id)}/{get_user_slots(call.from_user.id)}

━━━━━━━━━━━━━━━━━━━━━
⚠️ الأماكن محدودة — حسب اشتراكك

💎 {DEVELOPER}
👑 {DEV_NAME}"""

    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton("🔙 رجوع", callback_data="menu_main"))
    try:
        bot.edit_message_text(text, chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              reply_markup=markup, parse_mode="HTML")
        bot.register_next_step_handler(call.message, receive_smart_uids)
    except Exception:
        pass


pending_smart_uids = {}


def receive_smart_uids(message):
    try:
        text = message.text.strip()
        uids = []
        for part in re.split(r'[,\n\s]+', text):
            part = part.strip()
            if part and is_safe_uid(part):
                uids.append(part)

        if not uids:
            bot.reply_to(message, "❌ لم يتم العثور على UIDs صحيحة")
            return

        user_id = message.from_user.id
        pending_smart_uids[user_id] = uids

        text = f"""╔══════════════════════════╗
║   ⏱️ 𝐂𝐇𝐎𝐎𝐒𝐄 𝐃𝐔𝐑𝐀𝐓𝐈𝐎𝐍
╚══════════════════════════╝

🎯 المستهدفون: {len(uids)} شخص
🎰 أماكنك: {get_user_active_slots(user_id)}/{get_user_slots(user_id)}

━━━━━━━━━━━━━━━━━━━━━

⏱️ اختر المدة:"""

        markup = telebot.types.InlineKeyboardMarkup(row_width=3)
        markup.add(
            telebot.types.InlineKeyboardButton("1 ساعة", callback_data="dur_1"),
            telebot.types.InlineKeyboardButton("2 ساعة", callback_data="dur_2"),
            telebot.types.InlineKeyboardButton("3 ساعات", callback_data="dur_3"),
        )
        markup.add(
            telebot.types.InlineKeyboardButton("6 ساعات", callback_data="dur_6"),
            telebot.types.InlineKeyboardButton("12 ساعة", callback_data="dur_12"),
            telebot.types.InlineKeyboardButton("24 ساعة", callback_data="dur_24"),
        )
        markup.add(
            telebot.types.InlineKeyboardButton("48 ساعة", callback_data="dur_48"),
            telebot.types.InlineKeyboardButton("72 ساعة", callback_data="dur_72"),
            telebot.types.InlineKeyboardButton("7 أيام", callback_data="dur_168"),
        )
        markup.add(
            telebot.types.InlineKeyboardButton("♾️ دائم", callback_data="dur_permanent"),
        )
        markup.add(
            telebot.types.InlineKeyboardButton("⏱️ مخصص", callback_data="dur_custom"),
        )
        markup.add(
            telebot.types.InlineKeyboardButton("🔙 رجوع", callback_data="menu_main"),
        )

        bot.reply_to(message, text, reply_markup=markup, parse_mode="HTML")

    except Exception as e:
        print(f"[receive_smart_uids] {e}")


@bot.callback_query_handler(func=lambda c: c.data.startswith("dur_"))
def cb_duration(call):
    try:
        user_id = call.from_user.id

        if user_id not in pending_smart_uids:
            bot.answer_callback_query(call.id, "⚠️ لا توجد عملية معلقة", show_alert=True)
            return

        uids = pending_smart_uids[user_id]
        duration_str = call.data.replace("dur_", "")

        if duration_str == "custom":
            bot.answer_callback_query(call.id)
            bot.edit_message_text(
                f"""⏱️ أرسل عدد الساعات (رقم):
مثال: 5""",
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                parse_mode="HTML"
            )
            bot.register_next_step_handler(call.message, receive_custom_duration)
            return

        if duration_str == "permanent":
            hours = 0
        else:
            hours = int(duration_str)

        with user_slots_lock:
            current = len(user_active_spams.get(user_id, {}))
            max_slots = get_user_slots(user_id)
            free = max_slots - current

            if free <= 0:
                bot.answer_callback_query(call.id, "❌ الأماكن ممتلئة", show_alert=True)
                return

            to_run = min(free, len(uids))

        accepted = 0
        queued = 0
        rejected = 0

        for i, uid in enumerate(uids):
            if i < to_run:
                status = queue_smart_task(call.message.chat.id, uid, user_id, hours, force_run=True)
            else:
                status = queue_smart_task(call.message.chat.id, uid, user_id, hours, force_run=False)

            if status == "running":
                accepted += 1
            elif status == "queued":
                queued += 1
            else:
                rejected += 1

        save_active_spams()
        add_log(user_id, "/smart", f"UIDs: {len(uids)} hours={hours}",
                call.from_user.username or "")

        duration_text = "♾️ دائم" if hours == 0 else f"{hours} ساعة"

        result_text = f"""╔══════════════════════════╗
║  📊 نتيجة العملية
╚══════════════════════════╝

🎯 المستهدفون: {len(uids)}

✅ شغالة: {accepted}
⏳ في الانتظار: {queued}
❌ مرفوض: {rejected}

⏱️ المدة: {duration_text}
🎰 أماكنك: {get_user_active_slots(user_id)}/{get_user_slots(user_id)}

👑 {DEV_NAME}"""

        bot.edit_message_text(result_text, chat_id=call.message.chat.id,
                              message_id=call.message.message_id, parse_mode="HTML")

        del pending_smart_uids[user_id]

    except Exception as e:
        print(f"[cb_duration] {e}")


def receive_custom_duration(message):
    try:
        user_id = message.from_user.id
        if user_id not in pending_smart_uids:
            return

        try:
            hours = int(message.text.strip())
            if hours < 1 or hours > 720:
                bot.reply_to(message, "❌ المدة: 1-720 ساعة")
                return
        except ValueError:
            bot.reply_to(message, "❌ رقم صحيح فقط")
            return

        uids = pending_smart_uids[user_id]

        with user_slots_lock:
            current = len(user_active_spams.get(user_id, {}))
            max_slots = get_user_slots(user_id)
            free = max_slots - current
            to_run = min(free, len(uids))

        accepted = 0
        queued = 0

        for i, uid in enumerate(uids):
            if i < to_run:
                status = queue_smart_task(message.chat.id, uid, user_id, hours, force_run=True)
            else:
                status = queue_smart_task(message.chat.id, uid, user_id, hours, force_run=False)

            if status == "running":
                accepted += 1
            elif status == "queued":
                queued += 1

        save_active_spams()
        add_log(user_id, "/smart", f"UIDs: {len(uids)} hours={hours}",
                message.from_user.username or "")

        bot.reply_to(message, f"""✅ <b>بدأ السبام الدائم</b>

🎯 المستهدفون: {len(uids)}
✅ شغالة: {accepted}
⏳ في الانتظار: {queued}

⏱️ المدة: {hours} ساعة
🎰 أماكنك: {get_user_active_slots(user_id)}/{get_user_slots(user_id)}

👑 {DEV_NAME}""", parse_mode="HTML")

        del pending_smart_uids[user_id]

    except Exception as e:
        print(f"[receive_custom_duration] {e}")


def queue_smart_task(chat_id, target_uid, user_id, hours, force_run=False):
    try:
        with user_slots_lock:
            if user_id not in user_active_spams:
                user_active_spams[user_id] = {}

            current = len(user_active_spams[user_id])
            max_slots = get_user_slots(user_id)

            if force_run and current < max_slots:
                if target_uid in user_active_spams[user_id]:
                    return "rejected"

                user_active_spams[user_id][target_uid] = {
                    "type": "smart",
                    "target": target_uid,
                    "hours": hours,
                    "started_at": time.time(),
                    "chat_id": chat_id,
                }

                threading.Thread(
                    target=smart_send_worker,
                    args=(chat_id, target_uid, user_id, hours),
                    daemon=True
                ).start()
                return "running"
            else:
                if user_id not in user_queues:
                    user_queues[user_id] = []
                user_queues[user_id].append({
                    "chat_id": chat_id,
                    "target_uid": target_uid,
                    "user_id": user_id,
                    "hours": hours,
                    "type": "smart",
                })
                return "queued"
    except Exception as e:
        print(f"[queue_smart_task] {e}")
        return "rejected"


def release_user_slot(user_id, target_uid):
    try:
        with user_slots_lock:
            if user_id in user_active_spams:
                user_active_spams[user_id].pop(target_uid, None)
                if not user_active_spams[user_id]:
                    del user_active_spams[user_id]

            if user_id in user_queues and user_queues[user_id]:
                max_slots = get_user_slots(user_id)
                current = len(user_active_spams.get(user_id, {}))

                if current < max_slots:
                    task = user_queues[user_id].pop(0)

                    if user_id not in user_active_spams:
                        user_active_spams[user_id] = {}

                    user_active_spams[user_id][task["target_uid"]] = {
                        "type": task.get("type", "smart"),
                        "target": task["target_uid"],
                        "hours": task.get("hours", 0),
                        "started_at": time.time(),
                        "chat_id": task["chat_id"],
                    }

                    threading.Thread(
                        target=smart_send_worker,
                        args=(task["chat_id"], task["target_uid"], user_id, task.get("hours", 0)),
                        daemon=True
                    ).start()

                    try:
                        bot.send_message(task["chat_id"],
                            f"▶️ بدأ من الطابور: <code>{task['target_uid']}</code>",
                            parse_mode="HTML")
                    except Exception:
                        pass
    except Exception as e:
        print(f"[release_user_slot] {e}")


def smart_send_worker(chat_id, target_uid, user_id, hours):
    try:
        if hours == 0:
            end_time = float('inf')
        else:
            end_time = time.time() + (hours * 3600)

        while True:
            with user_slots_lock:
                if user_id not in user_active_spams:
                    return
                if target_uid not in user_active_spams[user_id]:
                    return

            if time.time() > end_time:
                try:
                    bot.send_message(chat_id,
                        f"⏰ انتهت المدة\n🎯 <code>{target_uid}</code>",
                        parse_mode="HTML")
                except Exception:
                    pass
                release_user_slot(user_id, target_uid)
                save_active_spams()
                return

            try:
                send_likes_with_batches(target_uid, chat_id)
            except Exception as e:
                print(f"[smart_send] {e}")

            time.sleep(DEFAULT_CHECK_INTERVAL)

    except Exception as e:
        print(f"[smart_send_worker] {e}")
        try:
            release_user_slot(user_id, target_uid)
            save_active_spams()
        except Exception:
            pass


# ═══════════════════════════════════════════════════
#   🛑 إيقاف العمليات
# ═══════════════════════════════════════════════════
@bot.callback_query_handler(func=lambda c: c.data == "menu_stop")
def cb_menu_stop(call):
    text = """╔══════════════════════════╗
║   🛑 𝐒𝐓𝐎𝐏
╚══════════════════════════╝

📌 اختر نوع الإيقاف:"""

    markup = telebot.types.InlineKeyboardMarkup(row_width=1)
    markup.add(telebot.types.InlineKeyboardButton(
        "🔴 إيقاف محدد", callback_data="stop_specific"
    ))

    if is_admin(call.from_user.id):
        markup.add(telebot.types.InlineKeyboardButton(
            "⚠️ إيقاف جميع العمليات (أدمن)", callback_data="stop_all"
        ))
    else:
        markup.add(telebot.types.InlineKeyboardButton(
            "⚠️ إيقاف كل عملياتي", callback_data="stop_my"
        ))

    markup.add(telebot.types.InlineKeyboardButton("🔙 رجوع", callback_data="menu_main"))

    try:
        bot.edit_message_text(text, chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              reply_markup=markup, parse_mode="HTML")
    except Exception:
        pass


@bot.callback_query_handler(func=lambda c: c.data == "stop_specific")
def cb_stop_specific(call):
    bot.answer_callback_query(call.id)
    bot.edit_message_text(
        """🔴 أرسل UID(s) التي تريد إيقافها:""",
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        parse_mode="HTML"
    )
    bot.register_next_step_handler(call.message, receive_stop_specific)


def receive_stop_specific(message):
    try:
        user_id = message.from_user.id
        text = message.text.strip()
        uids = [p.strip() for p in re.split(r'[,\n\s]+', text) if p.strip()]

        if not uids:
            bot.reply_to(message, "❌ لا توجد UIDs")
            return

        stopped = 0
        not_found = 0

        for uid in uids:
            found = False

            if is_admin(user_id):
                search_users = list(user_active_spams.keys())
            else:
                search_users = [user_id]

            for uid_owner in search_users:
                if uid_owner in user_active_spams and uid in user_active_spams[uid_owner]:
                    release_user_slot(uid_owner, uid)
                    stopped += 1
                    found = True
                    break

            if not found:
                for uid_owner in search_users:
                    if uid_owner in user_queues:
                        for i, task in enumerate(user_queues[uid_owner]):
                            if task["target_uid"] == uid:
                                user_queues[uid_owner].pop(i)
                                stopped += 1
                                found = True
                                break
                        if found:
                            break

            if not found:
                not_found += 1

        save_active_spams()
        add_log(user_id, "/stop", f"UIDs: {', '.join(uids[:3])}",
                message.from_user.username or "")

        bot.reply_to(message, f"""✅ تم الإيقاف: {stopped}
❌ غير موجود: {not_found}""", parse_mode="HTML")

    except Exception as e:
        print(f"[receive_stop_specific] {e}")


@bot.callback_query_handler(func=lambda c: c.data == "stop_my")
def cb_stop_my(call):
    try:
        user_id = call.from_user.id
        total = 0

        with user_slots_lock:
            if user_id in user_active_spams:
                total += len(user_active_spams[user_id])
                user_active_spams[user_id].clear()
                del user_active_spams[user_id]

            if user_id in user_queues:
                total += len(user_queues[user_id])
                user_queues[user_id].clear()

        save_active_spams()
        add_log(user_id, "/stop/my", f"stopped={total}",
                call.from_user.username or "")

        bot.answer_callback_query(call.id, f"✅ تم إيقاف {total} عملية", show_alert=True)

        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton("🔙 رجوع", callback_data="menu_main"))

        bot.edit_message_text(
            f"""╔══════════════════════════╗
║  🛑 𝐀𝐋𝐋 𝐒𝐓𝐎𝐏𝐏𝐄𝐃
╚══════════════════════════╝

✅ تم إيقاف كل عملياتك
📊 العدد: {total}""",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=markup,
            parse_mode="HTML"
        )
    except Exception as e:
        print(f"[cb_stop_my] {e}")


@bot.callback_query_handler(func=lambda c: c.data == "stop_all")
def cb_stop_all(call):
    try:
        if not is_admin(call.from_user.id):
            bot.answer_callback_query(call.id, "❌ للأدمن فقط", show_alert=True)
            return

        total_active = 0
        total_queued = 0
        users_affected = set()

        with user_slots_lock:
            for uid in list(user_active_spams.keys()):
                count = len(user_active_spams[uid])
                if count > 0:
                    users_affected.add(uid)
                    total_active += count
                user_active_spams[uid].clear()
            user_active_spams.clear()

            for uid in list(user_queues.keys()):
                count = len(user_queues[uid])
                if count > 0:
                    users_affected.add(uid)
                    total_queued += count
                user_queues[uid].clear()
            user_queues.clear()

        try:
            empty_data = {"active": {}, "queues": {}, "saved_at": time.time()}
            with open(ACTIVE_FILE, 'w', encoding='utf-8') as f:
                json.dump(empty_data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"[stop_all] فشل مسح الملف: {e}")

        add_log(call.from_user.id, "/stop/all",
                f"active={total_active} queued={total_queued} users={len(users_affected)}",
                call.from_user.username or "")

        bot.answer_callback_query(call.id,
            f"✅ تم إيقاف {total_active + total_queued} عملية",
            show_alert=True)

        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton("🔙 رجوع", callback_data="menu_main"))

        bot.edit_message_text(
            f"""╔══════════════════════════╗
║   🛑 𝐅𝐔𝐋𝐋 𝐒𝐓𝐎𝐏𝐏𝐄𝐃
╚══════════════════════════╝

✅ تم إيقاف جميع العمليات في النظام

┏━━━━━━━━━━━━━━━━━━━━━┓
┃  📊 𝐑𝐄𝐒𝐔𝐋𝐓
┗━━━━━━━━━━━━━━━━━━━━━┛
   🔴 عمليات شغالة : {total_active}
   ⏳ في الطابور    : {total_queued}
   👥 المستخدمون    : {len(users_affected)}
   🗑️ ملف الحفظ     : تم تفريغه

━━━━━━━━━━━━━━━━━━━━━
👑 {DEV_NAME}""",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=markup,
            parse_mode="HTML"
        )
    except Exception as e:
        print(f"[cb_stop_all] {e}")


# ═══════════════════════════════════════════════════
#   📊 حالة الخدمة
# ═══════════════════════════════════════════════════
@bot.callback_query_handler(func=lambda c: c.data == "menu_status")
def cb_menu_status(call):
    user_id = call.from_user.id
    api_status = check_api_health()

    my_active = get_user_active_slots(user_id)
    my_max = get_user_slots(user_id)
    my_queued = len(user_queues.get(user_id, []))

    with tokens_cache_lock:
        valid_tokens = sum(1 for v in tokens_cache.values() if v.get("expires_at", 0) > time.time())

    text = f"""╔══════════════════════════╗
║   📊 حالة الخدمة
╚══════════════════════════╝

💚 Health Check:
   • API: {api_status['status']}
   • الدفعة: {BATCH_SIZE}
   • التأخير: {BATCH_DELAY}s
   • الفحص: {DEFAULT_CHECK_INTERVAL}s

┏━━━━━━━━━━━━━━━━━━━━━┓
┃  👤 حسابك
┗━━━━━━━━━━━━━━━━━━━━━┛
   • أماكنك: {my_active}/{my_max}
   • في الطابور: {my_queued}

┏━━━━━━━━━━━━━━━━━━━━━┓
┃  📈 النظام
┗━━━━━━━━━━━━━━━━━━━━━┛
   • الحسابات: {len(bot_accounts)}/{len(ACCOUNTS_LIST)}
   • محظورة: {len(BANNED_ACCOUNTS)}
   • كاش: {valid_tokens}

━━━━━━━━━━━━━━━━━━━━━
💎 {DEVELOPER}
👑 {DEV_NAME}"""

    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton("🔄 تحديث", callback_data="menu_status"))
    markup.add(telebot.types.InlineKeyboardButton("🔙 رجوع", callback_data="menu_main"))
    try:
        bot.edit_message_text(text, chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              reply_markup=markup, parse_mode="HTML")
    except Exception:
        pass


# ═══════════════════════════════════════════════════
#   📋 سجل العمليات
# ═══════════════════════════════════════════════════
@bot.callback_query_handler(func=lambda c: c.data == "menu_logs")
def cb_menu_logs(call):
    user_id = call.from_user.id

    if not is_admin(user_id):
        bot.answer_callback_query(call.id, "❌ للأدمن فقط", show_alert=True)
        return

    lines = ["╔══════════════════════════╗",
             "║  📋 سجل العمليات",
             "╚══════════════════════════╝",
             ""]

    logs_to_show = operation_logs[-15:][::-1]

    if not logs_to_show:
        lines.append("📭 لا توجد عمليات")
    else:
        for i, log in enumerate(logs_to_show, 1):
            action = log.get("action", "?")
            icon = "✅"
            if "stop" in action:
                icon = "🛑"
            elif "send" in action or "smart" in action:
                icon = "🚀"
            elif "visit" in action:
                icon = "👣"
            elif "clan" in action:
                icon = "🏛️"

            username = log.get("username", "")
            user_tag = f"@{username}" if username else f"<code>{log.get('user_id', '?')}</code>"

            lines.append(f"{i}. {icon} <b>{action}</b>")
            lines.append(f"   📝 {log.get('details', '')}")
            lines.append(f"   👤 {user_tag}")
            lines.append(f"   🕐 {log.get('time', '')}")
            lines.append("")

    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton("🔄 تحديث", callback_data="menu_logs"))
    markup.add(telebot.types.InlineKeyboardButton("🔙 رجوع", callback_data="menu_main"))

    try:
        bot.edit_message_text("\n".join(lines), chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              reply_markup=markup, parse_mode="HTML")
    except Exception:
        pass


# ═══════════════════════════════════════════════════
#   🎯 إرسال سبام الصداقة
# ═══════════════════════════════════════════════════
def send_likes_with_batches(target_uid, chat_id):
    if not bot_accounts:
        return

    current_batch_size = BATCH_SIZE
    current_batch_delay = BATCH_DELAY

    batches = [bot_accounts[i:i + current_batch_size] for i in range(0, len(bot_accounts), current_batch_size)]
    for i, batch in enumerate(batches):
        batch_sent = 0
        batch_failed = 0
        with ThreadPoolExecutor(max_workers=min(current_batch_size, 10)) as executor:
            futures = [executor.submit(execute_friend_action, acc, target_uid) for acc in batch]
            for f in as_completed(futures):
                try:
                    if f.result(timeout=15):
                        batch_sent += 1
                    else:
                        batch_failed += 1
                except Exception:
                    batch_failed += 1
        print(f"[Batch {i+1}/{len(batches)}] ✅ {batch_sent} | ❌ {batch_failed}")

        if i < len(batches) - 1:
            time.sleep(current_batch_delay)


def buildpacket(fd):
    pk = bytearray()
    for f, v in fd.items():
        ev = []
        n = (f << 3) | (2 if isinstance(v, (dict, str, bytes)) else 0)
        while True:
            b = n & 0x7F
            n >>= 7
            if n: b |= 0x80
            ev.append(b)
            if not n: break
        pk.extend(bytes(ev))
        if isinstance(v, int):
            ev2 = []
            while True:
                b = v & 0x7F
                v >>= 7
                if v: b |= 0x80
                ev2.append(b)
                if not v: break
            pk.extend(bytes(ev2))
    return pk


def execute_friend_action(session, target_uid):
    try:
        obb = requests.get(
            "https://version.ffmax.purplevioleto.com/live/ver.php?lang=ar&device=android",
            timeout=8).json().get("latest_release_version", "2.101.X")
        payload = buildpacket({1: int(session["account_id"]), 2: int(target_uid), 3: 22}).hex()
        key = bytes([89, 103, 38, 116, 99, 37, 68, 69, 117, 104, 54, 37, 90, 99, 94, 56])
        iv = bytes([54, 111, 121, 90, 68, 114, 50, 50, 69, 51, 121, 99, 104, 106, 77, 37])
        enc = bytes.fromhex(AES.new(key, AES.MODE_CBC, iv).encrypt(
            pad(bytes.fromhex(payload), 16)).hex())
        headers = {
            "Authorization": f"Bearer {session['jwt']}",
            "ReleaseVersion": obb,
            "X-GA": "v1 1",
            "X-Unity-Version": "2022.3.47f1",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        requests.post(f"{session['server_url']}RequestAddingFriend",
                      headers=headers, data=enc, timeout=10)
        return True
    except Exception:
        return False


# ═══════════ الأوامر الإدارية ═══════════
@bot.message_handler(commands=['access'])
def cmd_access(message):
    try:
        if not is_owner(message.from_user.id):
            return bot.reply_to(message, "❌ للمالك فقط")
        args = message.text.split()
        if len(args) < 3:
            return bot.reply_to(message, "❌ /access user_id hours")
        try:
            uid = int(args[1])
            hours = int(args[2])
            expire = time.time() + (hours * 3600)
            access_users[uid] = expire
            save_data()
            add_log(message.from_user.id, "/access", f"{uid} {hours}h",
                    message.from_user.username or "")
            bot.reply_to(message, f"✅ تم منح الوصول لـ <code>{uid}</code> — {hours} ساعة", parse_mode="HTML")
        except ValueError:
            bot.reply_to(message, "❌ أرقام غير صحيحة")
    except Exception as e:
        print(f"[access] {e}")


@bot.message_handler(commands=['revoke'])
def cmd_revoke(message):
    try:
        if not is_owner(message.from_user.id):
            return bot.reply_to(message, "❌ للمالك فقط")
        args = message.text.split()
        if len(args) < 2:
            return bot.reply_to(message, "❌ /revoke user_id")
        try:
            uid = int(args[1])
            if uid in access_users:
                del access_users[uid]
                save_data()
                add_log(message.from_user.id, "/revoke", str(uid),
                        message.from_user.username or "")
                bot.reply_to(message, f"✅ تم إلغاء وصول <code>{uid}</code>", parse_mode="HTML")
            else:
                bot.reply_to(message, "⚠️ ما عنده وصول")
        except ValueError:
            bot.reply_to(message, "❌ user_id غير صحيح")
    except Exception as e:
        print(f"[revoke] {e}")


@bot.message_handler(commands=['users'])
def cmd_users(message):
    try:
        if not is_owner(message.from_user.id):
            return bot.reply_to(message, "❌ للمالك فقط")
        if not access_users:
            return bot.reply_to(message, "📋 لا يوجد مستخدمون")
        lines = ["👥 <b>المستخدمون:</b>\n"]
        now = time.time()
        for i, (uid, expire) in enumerate(sorted(access_users.items()), 1):
            if expire > now:
                remaining_hours = int((expire - now) / 3600)
                status = f"✅ {remaining_hours}h"
            else:
                status = "⏰ منتهي"
            lines.append(f"{i}. <code>{uid}</code> — {status}")
        lines.append(f"\n📊 المجموع: {len(access_users)}")
        bot.reply_to(message, "\n".join(lines), parse_mode="HTML")
    except Exception as e:
        print(f"[users] {e}")


@bot.message_handler(commands=['keys'])
def cmd_keys(message):
    try:
        if not is_admin(message.from_user.id):
            return bot.reply_to(message, "❌ للأدمن فقط")
        if not keys_db:
            return bot.reply_to(message, "📋 لا توجد مفاتيح")
        lines = ["🔑 <b>المفاتيح:</b>\n"]
        active_count = 0
        used_count = 0
        for i, (key, data) in enumerate(list(keys_db.items())[-20:], 1):
            if data.get("used_by"):
                status = "✅ مستخدم"
                used_count += 1
            else:
                status = "🟢 متاح"
                active_count += 1
            slots = data.get("slots", DEFAULT_SLOTS)
            lines.append(f"{i}. <code>{key}</code>\n   {status} | {data.get('duration_hours', 0)}h | 🎰 {slots}")
        lines.append(f"\n📊 متاح: {active_count} | مستخدم: {used_count} | الكل: {len(keys_db)}")
        bot.reply_to(message, "\n".join(lines), parse_mode="HTML")
    except Exception as e:
        print(f"[keys] {e}")


@bot.message_handler(commands=['broadcast'])
def cmd_broadcast(message):
    try:
        if not is_owner(message.from_user.id):
            return bot.reply_to(message, "❌ للمالك فقط")
        if not access_users:
            return bot.reply_to(message, "📋 لا يوجد مستخدمون")
        text = message.text.replace("/broadcast", "", 1).strip()
        if not text:
            return bot.reply_to(message, "❌ اكتب رسالة")
        sent = 0
        for uid in list(access_users.keys()):
            try:
                bot.send_message(uid, text)
                sent += 1
                time.sleep(0.3)
            except Exception:
                pass
        add_log(message.from_user.id, "/broadcast", f"to {sent}",
                message.from_user.username or "")
        bot.reply_to(message, f"✅ تمت الإذاعة لـ {sent} مستخدم")
    except Exception as e:
        print(f"[broadcast] {e}")


@bot.message_handler(commands=['addch'])
def cmd_addch(message):
    try:
        if not is_owner(message.from_user.id):
            return bot.reply_to(message, "❌ للمالك فقط")
        args = message.text.replace("/addch", "", 1).strip()
        if not args:
            return bot.reply_to(message, "❌ /addch @USERNAME | LINK | TITLE")
        parts = [p.strip() for p in args.split("|")] if "|" in args else args.split()
        if len(parts) < 3:
            return bot.reply_to(message, "❌ الصيغة غير صحيحة")
        username, link, title = parts[0], parts[1], " ".join(parts[2:])
        if not username.startswith("@"):
            username = "@" + username
        if not link.startswith("http"):
            link = f"https://t.me/{username.replace('@', '')}"
        force_channels.append({"username": username, "link": link, "title": title})
        save_data()
        bot.reply_to(message, f"✅ تم إضافة القناة: {title}")
    except Exception as e:
        print(f"[addch] {e}")


@bot.message_handler(commands=['tokens'])
def cmd_tokens(message):
    """عرض معلومات كاش التوكنات"""
    try:
        if not is_admin(message.from_user.id):
            return bot.reply_to(message, "❌ للأدمن فقط")

        now = time.time()
        with tokens_cache_lock:
            valid = [k for k, v in tokens_cache.items() if v.get("expires_at", 0) > now]
            new_api = sum(1 for v in tokens_cache.values() if v.get("source") == "new")
            fb1 = sum(1 for v in tokens_cache.values() if v.get("source") == "fallback_1")
            fb2 = sum(1 for v in tokens_cache.values() if v.get("source") == "fallback_2")

        with _new_api_lock:
            if _new_api_status["working"] is True:
                api_status = "✅ شغال"
            elif _new_api_status["working"] is False:
                api_status = "❌ فشل"
            else:
                api_status = "⏳ لم يُختبر"

        bot.reply_to(message, f"""💾 <b>كاش التوكنات</b>

📊 إجمالي: {len(tokens_cache)}
✅ صالح: {len(valid)}
🆕 jihad-jwt: {new_api}
🥈 de26: {fb1}
🥉 ff-jwt: {fb2}
🛡️ محظور: {len(BANNED_ACCOUNTS)}
❌ فشل: {len(failed_attempts)}

🌐 حالة API الجديد: {api_status}

⏱️ صلاحية التوكن: {TOKEN_VALIDITY // 60} دقيقة
🔄 فحص التجديد: كل {TOKEN_CHECK_INTERVAL // 60} دقيقة""", parse_mode="HTML")
    except Exception as e:
        print(f"[tokens] {e}")


@bot.message_handler(commands=['refresh'])
def cmd_refresh(message):
    """إجبار تجديد التوكنات (للأدمن)"""
    try:
        if not is_admin(message.from_user.id):
            return bot.reply_to(message, "❌ للأدمن فقط")

        bot.reply_to(message, "🔄 جاري تجديد التوكنات...")

        with tokens_cache_lock:
            tokens_cache.clear()
        save_tokens_cache()

        with _new_api_lock:
            _new_api_status["working"] = None

        threading.Thread(target=reload_accounts, daemon=True).start()

        time.sleep(3)
        bot.reply_to(message, "✅ بدأ التجديد — استخدم /tokens بعد دقيقة")
    except Exception as e:
        print(f"[refresh] {e}")


@bot.message_handler(commands=['testapi'])
def cmd_testapi(message):
    """اختبار API الجديد يدوياً"""
    try:
        if not is_admin(message.from_user.id):
            return bot.reply_to(message, "❌ للأدمن فقط")

        bot.reply_to(message, "🔍 جاري اختبار API الجديد (jihad-jwt)...")

        with _new_api_lock:
            _new_api_status["working"] = None

        result = _test_new_api()

        if result:
            bot.reply_to(message, "✅ API الجديد (jihad-jwt) شغال")
        else:
            bot.reply_to(message, "❌ API الجديد فشل — سيتم استخدام الاحتياطي")
    except Exception as e:
        print(f"[testapi] {e}")


# ═══════════ التشغيل ═══════════
import logging
logging.basicConfig(level=logging.CRITICAL)
telebot.logger.setLevel(logging.CRITICAL)

print(f"""
╭───────────────────────────────╮
   {DEV_NAME} — PREMIUM BOT v4.8
   🆕 jihad-jwt (الأساسي) ✅
   🥈 de26.spaceify (احتياطي 1)
   🥉 ff-jwt-gen (احتياطي 2)
   🧪 Smart API Test
   💾 Token Cache (No Ban)
   ⚡ Speed: Batch={BATCH_SIZE} Delay={BATCH_DELAY}s
   Accounts : {len(ACCOUNTS_LIST)}
   Owner    : {OWNER_ID}
   Admin    : {ADMIN_ID}
   Developer: {DEVELOPER}
╰───────────────────────────────╯
""")

print()
print("[*] جاري استعادة العمليات الشغالة...")
time.sleep(3)
restore_active_spams()

threading.Thread(target=active_spams_saver_worker, daemon=True).start()

retry_delay = 5
while True:
    try:
        bot.infinity_polling(timeout=60, long_polling_timeout=60, skip_pending=True, none_stop=True)
    except Exception as e:
        print(f"[!] Bot crashed: {e}")
        time.sleep(retry_delay)
        retry_delay = min(retry_delay * 2, 120)
        continue
    else:
        retry_delay = 5