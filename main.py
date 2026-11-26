# -*- coding: utf-8 -*-
import re
import unicodedata
from collections import OrderedDict

from kivy.app import App
from kivy.metrics import dp
from kivy.core.clipboard import Clipboard
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.graphics import Color, RoundedRectangle

APP_NAME = "WANO KINGDOM"
PURPLE = (0.48, 0.20, 0.82, 1)
DARK = (0.055, 0.045, 0.075, 1)
PANEL = (0.105, 0.085, 0.14, 1)
TEXT = (0.95, 0.93, 1, 1)
MUTED = (0.72, 0.68, 0.79, 1)

# =========================================================
# 1) فاحص الأرقام - قاعدة المستخدم الأصلية
# =========================================================
DATABASE_TEXT = r"""
+963935488281|مؤبد تبنيد|مذكور ضمن قائمة الأرقام المؤبدة
+201554834684|ملاحظة خاصة|مذكور: معاه أخذوه على واهس
+963985029991|مؤبد تبنيد|مذكور ضمن قائمة الأرقام المؤبدة
+967773432911|مؤبد تبنيد|مذكور ضمن قائمة الأرقام المؤبدة
+212681425627|مؤبد تبنيد|مذكور ضمن قائمة الأرقام المؤبدة
+970592415439|مؤبد تبنيد|مذكور ضمن قائمة الأرقام المؤبدة
+212770257774|حزب التوحيد - القياد|
+963933534673|حزب التوحيد - القياد|
+249118784025|حزب التوحيد - القياد|
+963932238372|حزب التوحيد - القياد|
+249127754761|حزب التوحيد - القياد|
+971562299347|حزب التوحيد - القياد|مذكور أيضاً كمؤبد تبنيد
+249964998486|حزب التوحيد - التوابع|
+9647861987605|حزب التوحيد - التوابع|
+212782627539|حزب التوحيد - التوابع|
+201145194261|حزب التوحيد - التوابع|
+218942794994|حزب التوحيد - التوابع|
+212787572249|حزب التوحيد - التوابع|
+967739433222|حزب التوحيد - التوابع|
+249990827915|حزب التوحيد - التوابع|
+212675640021|حزب التوحيد|مذكور ضمن أكثر من قائمة
+212681033772|حزب التوحيد|
+201552060969|حزب التوحيد|مذكور أيضاً ضمن قائمة المبندين
+201112830332|حزب التوحيد|مذكور أيضاً ضمن قائمة المبندين
+963942094321|حزب التوحيد|
+201069103885|نصاب فعاليات|
+9647810596846|منظمة تبنيد - الرئيس|
+96896256364|منظمة تبنيد - الأتباع|
+212716757469|منظمة تبنيد - الأتباع|
+218926686080|منظمة تبنيد - الأتباع|
+213553584891|منظمة تبنيد - الأتباع|
+201009943282|منظمة تبنيد - الأتباع|
+963937863130|منظمة تبنيد - الأتباع|
+6288809364091|منظمة تبنيد - الأتباع|
+963997095627|مؤبد تبنيد|
+967770237761|مؤبد تبنيد وقذف|
+212607490385|مبندين|دفعة المستقلين
+212618181742|مبندين|دفعة المستقلين
+212645309928|مبندين|دفعة المستقلين
+212664409303|مبندين|مكرر في المصدر
+212665867850|مبندين|
+212704101336|مبندين|
+212705805775|مبندين|
+212715991303|مبندين|
+212721816433|مبندين|
+212722290293|مبندين|
+212765770296|مبندين|
+212779186474|مبندين|
+212782068612|مبندين|
+212789679196|مبندين|
+213564030928|مبندين|
+213776232554|مبندين|
+94779584355|مبندين|
+249101472474|مؤبد تبنيد|
+966565135416|مؤبد تبنيد|
+201282597382|مؤبد تبنيد|
+201515567606|مؤبد تبنيد|
+201041773502|مؤبد تبنيد|مذكور معه تبنيد أرقام وتبنيد أساسي وتبنيد بلا جهة اتصال وسب
+201554888633|مؤبد تبنيد|
+201035694387|مبندين|
+201044197484|مبندين|
+201118270332|مبندين|
+201118273273|مبندين|
+212624386486|مبندين|
+212624497517|مبندين|
+212633820649|مبندين|
+212638915517|مبندين|
+212717716405|مبندين|
+212717939183|مبندين|
+212723819122|مبندين|
+212785121752|مبندين|
+212786093475|مبندين|
+212788196851|مبندين|
+963985391180|مبندين|
+963996242673|مبندين|
+966505724151|مبندين|
+967711796077|مبندين|
+967715842376|مبندين|
+967772004701|مبندين|
+84562412698|مبندين|
+905524468822|مبندين|
+817084308772|مبندين|
+818062444448|مبندين|
+962796836482|مبندين|
+212694206193|مذكور في القائمة|بدون تصنيف إضافي
+212788527636|مذكور في القائمة|بدون تصنيف إضافي
+963952709927|قليل أدب|
+201202034893|قليل أدب|
"""

ARABIC_DIGITS = str.maketrans("٠١٢٣٤٥٦٧٨٩", "0123456789")

def normalize_number(number):
    return re.sub(r"\D", "", number.translate(ARABIC_DIGITS))

def build_database():
    database = {}
    for line in DATABASE_TEXT.strip().splitlines():
        parts = line.strip().split("|", 2)
        if len(parts) < 2:
            continue
        number = normalize_number(parts[0])
        if not number:
            continue
        entry = (parts[1].strip(), parts[2].strip() if len(parts) > 2 else "")
        database.setdefault(number, [])
        if entry not in database[number]:
            database[number].append(entry)
    return database

NUMBER_DATABASE = build_database()

def check_number_text(user_number):
    cleaned = normalize_number(user_number)
    if not cleaned:
        return "❌ لم تدخل رقماً صحيحاً."
    if cleaned not in NUMBER_DATABASE:
        return f"✅ الرقم غير موجود بالقائمة\n\n📱 الرقم: +{cleaned}\nلم يتم العثور عليه في قاعدة البيانات."
    lines = ["⚠️ الرقم موجود بالقائمة", "", f"📱 الرقم: +{cleaned}",
             f"📌 عدد التصنيفات: {len(NUMBER_DATABASE[cleaned])}"]
    for i, (category, note) in enumerate(NUMBER_DATABASE[cleaned], 1):
        lines += ["", f"【{i}】 التصنيف: {category}"]
        if note:
            lines.append(f"📝 الملاحظة: {note}")
    return "\n".join(lines)

def number_statistics():
    categories = {}
    for entries in NUMBER_DATABASE.values():
        for category, _ in entries:
            categories[category] = categories.get(category, 0) + 1
    return "📊 إحصائيات قاعدة البيانات\n" + f"عدد الأرقام الفريدة: {len(NUMBER_DATABASE)}\n\n" + "\n".join(
        f"{k}: {v}" for k, v in categories.items()
    )

# =========================================================
# 2) الوورك - منطق المستخدم الأصلي
# =========================================================
WORK_ALIASES = {
    "توكيتو": ["ساتسوكي", "مونا", "اماني", "فريرن", "روميرو"],
    "ايزومي": ["هيماواري"], "غيو": ["ٱي"], "نينا": ["نينا"],
    "ثوركيل": ["شينوبو"], "غوهان": ["شينوا"],
    "باتشيرا": ["نيزوكو", "رويكا", "ميتسوري"],
    "ثورفين": ["ماي", "هيستوريا", "اليا", "واغوري"],
    "تشا": ["موزان", "ريم"], "رودو": ["ميسا", "ميكاسا"],
    "فرساس": ["ايميليا"], "ارثر": ["علا", "شمس", "نونا", "لايا"]
}

def clean_whatsapp(text):
    text = re.sub(r'[\u200B-\u200F\u202A-\u202E\u2066-\u2069\uFEFF]', '', text)
    return re.sub(r'[*_~`]', '', text).strip()

def normalize_name(raw):
    if not raw:
        return ""
    t = clean_whatsapp(raw)
    t = re.sub(r'[⟦⟧\[\]\(\)\{\}【】]', ' ', t)
    t = re.sub(r'\s*[\|\/\\•·\-–—]\s*[\d٠-٩\W_]*$', '', t)
    t = re.sub(r'[ً-ٰٟـ]', '', t)
    t = re.sub(r'[^؀-ۿa-zA-Z\s]', ' ', t)
    t = t.replace('أ', 'ا').replace('إ', 'ا').replace('آ', 'ا').replace('ى', 'ي')
    return re.sub(r'\s+', ' ', t.lower()).strip()

ALIAS_TO_OWNER = {}
for owner, aliases in WORK_ALIASES.items():
    for alias in aliases:
        ALIAS_TO_OWNER[normalize_name(owner) if False else alias] = normalize_name(owner)
# normalize aliases only after normalize_name is available
ALIAS_TO_OWNER = {normalize_name(alias): normalize_name(owner)
                  for owner, aliases in WORK_ALIASES.items() for alias in aliases}

def convert_alias(name):
    normalized = normalize_name(name)
    return ALIAS_TO_OWNER.get(normalized, normalized)

def process_work_forms(bulk_text):
    parties, admins = {}, {}
    party_count = admin_count = 0
    for line in bulk_text.splitlines():
        cleaned_line = clean_whatsapp(line)
        match = re.search(
            r'(الطرف|طرف|المسؤول|المسئول|مسؤول|مسئول|الاستقبال|استقبال)\s*[^؀-ۿa-zA-Z0-9⟦]*\s*(.+)$',
            cleaned_line, re.IGNORECASE)
        if not match:
            continue
        role, val = match.group(1), match.group(2).strip()
        bracket_match = re.search(r'⟦\s*([^⟧]+?)\s*⟧', val)
        if bracket_match:
            val = bracket_match.group(1).strip()
        else:
            val = re.sub(r'^[^\s؀-ۿa-zA-Z0-9⟦]+', '', val).replace('⟧', '').strip()
        if not val or re.match(r'^[\+\d٠-٩\s\-\(\)\.]+$', val):
            continue
        norm = convert_alias(val)
        if not norm:
            continue
        if 'طرف' in role:
            party_count += 1
            parties[norm] = parties.get(norm, 0) + 1
        else:
            admin_count += 1
            admins[norm] = admins.get(norm, 0) + 1
    sorted_parties = sorted(parties.items(), key=lambda x: x[1], reverse=True)
    sorted_admins = sorted(admins.items(), key=lambda x: x[1], reverse=True)
    total_forms = max(party_count, admin_count)
    return sorted_parties, sorted_admins, total_forms

def work_output(forms_data):
    p, a, total = process_work_forms(forms_data)
    deco = "*𖤓━───⌬【 ⛩️ 】⌬───━𖤓*"
    out = ["*【⛩️】حسبة الـوورك【⛩️】*", "", deco, "", "الطرف:"]
    out += [f"*✦ {n} 𖥔 ⟦{c}⟧*" for n, c in p] if p else ["لا يوجد"]
    out += ["", "الاستقبال:"]
    out += [f"*✦ {n} 𖥔 ⟦{c}⟧*" for n, c in a] if a else ["لا يوجد"]
    out += ["", f"الإجمالي:\n{total} استمارة", "", "*✦ المسؤول 𖥔 ⟦آرثر 🇮🇶 ⟧*", "", deco,
            "~*𝑾𝑨𝑵𝑶╎⊰⛩️⊱𝑲𝑰𝑵𝑮𝑫𝑶𝑴"]
    return "\n".join(out)

# =========================================================
# 3) ADS - منطق المستخدم الأصلي
# =========================================================
CATEGORIES = ("S", "M", "L")
ADMIN_NAME = "آرثر 🇮🇶"

def clean_ads_text(text):
    result = []
    for char in text:
        if char == "ـ":
            continue
        category = unicodedata.category(char)
        if category.startswith("S") or category == "Cf":
            continue
        if char in "*_~`":
            continue
        result.append(char)
    return "".join(result)

def normalize_ads(text):
    text = clean_ads_text(text)
    text = unicodedata.normalize("NFKC", text)
    text = re.sub(r"[\u064B-\u065F\u0670]", "", text)
    return re.sub(r"\s+", " ", text).strip().lower()

def split_messages(text):
    pattern = r"(?m)(?=^\[\s*[0-9٠-٩]{1,2}[^\n]{0,45}[،,])"
    parts = re.split(pattern, text.strip())
    return [part.strip() for part in parts if part.strip()]

def extract_category(message):
    text = clean_ads_text(message)
    matches = re.findall(r"التصنيف\s*[:：]?\s*([SML])(?=\s|[\]\[☆★◆*]|$)", text, re.IGNORECASE)
    if not matches:
        return None
    category = matches[0].upper()
    return category if category in CATEGORIES else None

BRACKETS = [("『", "』"), ("「", "」"), ("〖", "〗"), ("〘", "〙"), ("[", "]"), ("(", ")")]

def is_money_or_empty(value):
    value = value.strip()
    if not value:
        return True
    return bool(re.fullmatch(r"[\d٠-٩]+\s*(?:k|الف|ألف)?", value, re.IGNORECASE))

def extract_name_from_tail(tail):
    tail = clean_ads_text(tail).strip()
    for opening, closing in BRACKETS:
        pattern = re.escape(opening) + r"(.*?)" + re.escape(closing)
        for match in re.finditer(pattern, tail):
            name = match.group(1).strip()
            if not is_money_or_empty(name):
                return name
    tail = re.sub(r"^[\s:：\-–|]+", "", tail)
    tail = re.split(r"[:：]\s*[\d٠-٩]+\s*(?:k|الف|ألف)?", tail, maxsplit=1, flags=re.IGNORECASE)[0]
    tail = re.sub(r"^[\d٠-٩]+\s*(?:k|الف|ألف)?", "", tail, flags=re.IGNORECASE).strip()
    tail = tail.strip(" :：-–|[]()")
    if not tail or is_money_or_empty(tail) or len(tail) > 45:
        return None
    return tail

def extract_presenter(message):
    lines = message.splitlines()
    for i, original_line in enumerate(lines):
        line = clean_ads_text(original_line).strip()
        if not line:
            continue
        line = line.lstrip(" ╎│•❁❃✧☤")
        role_match = re.search(r"المقدم", line)
        if not role_match:
            continue
        prefix = line[:role_match.start()].strip()
        if prefix and not re.fullmatch(r"[\[\](){}『』「」〖〗〘〙\s:：\-–|]*", prefix):
            continue
        tail = line[role_match.end():]
        name = extract_name_from_tail(tail)
        if name:
            return name
        for next_line in lines[i + 1:i + 4]:
            cleaned_next = clean_ads_text(next_line).strip()
            if not cleaned_next:
                continue
            if re.search(r"المحاسب|الفائز|الخاسر|المركز|بقية المشاركين", cleaned_next):
                break
            if re.search(r"[\d٠-٩]+\s*(?:k|الف|ألف)", cleaned_next, re.IGNORECASE):
                name = extract_name_from_tail(cleaned_next)
                if name:
                    return name
        plain_tail = re.sub(r"^[\s:：\-–|]+", "", tail)
        plain_tail = re.split(r"[:：]\s*[\d٠-٩]+\s*(?:k|الف|ألف)?", plain_tail, maxsplit=1, flags=re.IGNORECASE)[0]
        plain_tail = plain_tail.strip(" :：-–|[]()")
        if (plain_tail and len(plain_tail) <= 45 and
            not re.search(r"المقدم|المحاسب|الفائز|الخاسر|التصنيف", plain_tail) and
            not is_money_or_empty(plain_tail)):
            return plain_tail
    return None

def extract_title(message):
    for line in message.splitlines():
        line = clean_ads_text(line).strip()
        if not line:
            continue
        normalized_line = normalize_ads(line)
        if "فعالية" in normalized_line or "اعلان" in normalized_line:
            normalized_line = normalized_line.replace("جوائز", "")
            return re.sub(r"\s+", " ", normalized_line).strip()
    return ""

def parse_ads_forms(text):
    messages = split_messages(text)
    records, detected_forms, failed_forms = [], 0, []
    for index, message in enumerate(messages, start=1):
        category = extract_category(message)
        if not category:
            continue
        detected_forms += 1
        presenter = extract_presenter(message)
        if not presenter:
            failed_forms.append({"number": index, "category": category,
                                 "reason": "لم يتم العثور على اسم المقدم"})
            continue
        records.append({"presenter": presenter.strip(), "key": normalize_ads(presenter),
                        "category": category, "title": normalize_ads(extract_title(message)),
                        "message_index": index})
    return records, len(messages), detected_forms, failed_forms

def ads_output(forms_data):
    records, messages_count, detected_forms, failed_forms = parse_ads_forms(forms_data)
    results = OrderedDict()
    totals = {"S": 0, "M": 0, "L": 0}
    for record in records:
        key, name, category = record["key"], record["presenter"], record["category"]
        if key not in results:
            results[key] = {"name": name, "S": 0, "M": 0, "L": 0}
        results[key][category] += 1
        totals[category] += 1
    output = ["*【⛩️】حسبة ADS【⛩️】*", "", "*𖤓━───⌬【 ⛩️ 】⌬───━𖤓*", ""]
    for person in results.values():
        counts = [f"{person[c]}{c}" for c in CATEGORIES if person[c] > 0]
        if counts:
            output.append(f"*✦ {person['name']} 𖥔 ⟦ {'|'.join(counts)} ⟧*")
    output += ["", f"*✦ المسؤول 𖥔 ⟦{ADMIN_NAME} ⟧*", "",
               "*𖤓━───⌬【 ⛩️ 】⌬───━𖤓*", "", "*【📊】مجموع التصنيفات【📊】*", ""]
    output += [f"*✦ تصنيف {c} 𖥔 ⟦ {totals[c]} ⟧*" for c in CATEGORIES]
    output += ["", f"*✦ مجموع الفعاليات 𖥔 ⟦ {sum(totals.values())} ⟧*", "",
               "*𖤓━───⌬【 ⛩️ 】⌬───━𖤓*", "~*𝑾𝑨𝑵𝑶╎⊰⛩️⊱𝑲𝑰𝑵𝑫𝑶𝑴*~"]
    report = [
        "📊 تقرير فحص استمارات ADS", "=" * 35,
        f"📨 عدد الرسائل المقروءة: {messages_count}",
        f"📋 عدد الاستمارات المكتشفة: {detected_forms}",
        f"✅ عدد الاستمارات المستخرجة بنجاح: {len(records)}",
        f"❌ عدد الاستمارات التي تعذر استخراجها: {len(failed_forms)}",
        f"🧮 عدد الاستمارات المحتسبة: {sum(totals.values())}", "-" * 35,
        f"تصنيف S: {totals['S']}", f"تصنيف M: {totals['M']}", f"تصنيف L: {totals['L']}", "-" * 35
    ]
    if failed_forms:
        report.append("⚠️ الاستمارات التي تحتاج مراجعة:")
        for item in failed_forms:
            report.append(f"استمارة رقم {item['number']} | التصنيف: {item['category']} | السبب: {item['reason']}")
    else:
        report.append("✅ جميع الاستمارات المكتشفة استُخرجت بنجاح.")
    return "\n".join(output) + "\n\n" + "\n".join(report)

# =========================================================
# 4) نقاط الترقية - منطق المستخدم الأصلي
# =========================================================
POINTS = {"طرف": 30, "استقبال": 10, "رسائل": 25, "S": 5, "M": 12, "L": 30}

def calculate_points(name, sides, reception, messages, s, m, l):
    side_points = sides * POINTS["طرف"]
    reception_points = reception * POINTS["استقبال"]
    message_points = (messages // 250) * POINTS["رسائل"]
    s_points, m_points, l_points = s * POINTS["S"], m * POINTS["M"], l * POINTS["L"]
    total = side_points + reception_points + message_points + s_points + m_points + l_points
    return {"name": name, "sides": sides, "reception": reception, "messages": messages,
            "S": s, "M": m, "L": l, "side_points": side_points,
            "reception_points": reception_points, "message_points": message_points,
            "s_points": s_points, "m_points": m_points, "l_points": l_points, "total": total}

def points_output(members_data):
    results, errors = [], []
    for line_number, line in enumerate(members_data.strip().splitlines(), start=1):
        line = line.strip()
        if not line:
            continue
        parts = [part.strip() for part in line.split("|")]
        if len(parts) != 7:
            errors.append(f"السطر {line_number}: يجب إدخال 7 خانات")
            continue
        name = parts[0]
        try:
            values = [int(value.replace(",", "")) for value in parts[1:]]
            if not name or any(value < 0 for value in values):
                raise ValueError
        except ValueError:
            errors.append(f"السطر {line_number}: بيانات غير صحيحة")
            continue
        results.append(calculate_points(name, *values))
    results.sort(key=lambda person: person["total"], reverse=True)
    output = ["*𖤓━───⌬【 ⛩️ 】⌬───━𖤓*", "*【⛩️】نقاط الترقية【⛩️】*",
              "*𖤓━───⌬【 ⛩️ 】⌬───━𖤓*", ""]
    for rank, person in enumerate(results, start=1):
        output += [f"*【{rank}】 {person['name']}*",
                   f"☆ الأطراف: {person['sides']} = {person['side_points']} نقطة",
                   f"☆ الاستقبال: {person['reception']} = {person['reception_points']} نقطة",
                   f"☆ الرسائل: {person['messages']} = {person['message_points']} نقطة",
                   f"☆ فعاليات S: {person['S']} = {person['s_points']} نقطة",
                   f"☆ فعاليات M: {person['M']} = {person['m_points']} نقطة",
                   f"☆ فعاليات L: {person['L']} = {person['l_points']} نقطة",
                   f"*✦ المجموع: ⟦ {person['total']} نقطة ⟧*", "", "━━━━━━━━━━━━━━", ""]
    output += ["*【📊】الإحصائيات العامة【📊】*", "", f"*عدد الأعضاء: {len(results)}*",
               f"*مجموع النقاط: {sum(p['total'] for p in results)}*", "",
               "*𖤓━───⌬【 ⛩️ 】⌬───━𖤓*", "~*𝑾𝑨𝑵𝑶╎⊰⛩️⊱𝑲𝑰𝑵𝑫𝑶𝑴*~"]
    if errors:
        output += ["", "⚠️ أخطاء الإدخال:"] + errors
    return "\n".join(output)

# =========================================================
# واجهة Kivy - أسود وبنفسجي
# =========================================================
class Panel(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.padding = dp(14)
        self.spacing = dp(10)
        with self.canvas.before:
            Color(*PANEL)
            self.bg = RoundedRectangle(radius=[dp(16)])
        self.bind(pos=self._update_bg, size=self._update_bg)
    def _update_bg(self, *_):
        self.bg.pos = self.pos
        self.bg.size = self.size

def make_label(text, size=16, color=TEXT, height=None, bold=False):
    lbl = Label(text=text, font_size=sp(size), color=color, size_hint_y=None,
                height=dp(height or (size * 2.0)), halign="right", valign="middle",
                bold=bold, text_size=(None, None))
    lbl.bind(width=lambda inst, w: setattr(inst, "text_size", (w, None)))
    return lbl

def sp(value):
    return dp(value)

def make_button(text, callback, height=52):
    btn = Button(text=text, size_hint_y=None, height=dp(height),
                 background_normal="", background_down="",
                 background_color=PURPLE, color=(1, 1, 1, 1),
                 font_size=dp(16), bold=True)
    btn.bind(on_release=lambda *_: callback())
    return btn

def make_input(hint, multiline=False, height=52):
    ti = TextInput(hint_text=hint, multiline=multiline, size_hint_y=None,
                   height=dp(height), padding=[dp(12), dp(12)],
                   background_normal="", background_active="",
                   background_color=(0.14, 0.12, 0.18, 1),
                   foreground_color=TEXT, hint_text_color=MUTED,
                   cursor_color=(0.8, 0.55, 1, 1), font_size=dp(15))
    return ti

class BaseToolScreen(Screen):
    title_text = ""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        root = BoxLayout(orientation="vertical", padding=dp(14), spacing=dp(10))
        self.add_widget(root)
        root.add_widget(make_label(self.title_text, 23, (0.82, 0.58, 1, 1), 48, True))
        self.body = BoxLayout(orientation="vertical", spacing=dp(9))
        root.add_widget(self.body)
        root.add_widget(make_button("رجوع للرئيسية", lambda: setattr(self.manager, "current", "home"), 48))

    def show_result(self, text):
        self.result.text = text

class NumberScreen(BaseToolScreen):
    title_text = "فاحص الأرقام"
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.number = make_input("أدخل الرقم مع أو بدون +")
        self.body.add_widget(self.number)
        self.body.add_widget(make_button("فحص الرقم", self.run_check))
        self.body.add_widget(make_button("إحصائيات القائمة", self.run_stats))
        self.result = make_input("ستظهر النتيجة هنا", True, 300)
        self.body.add_widget(self.result)
        self.body.add_widget(make_button("نسخ النتيجة", lambda: Clipboard.copy(self.result.text), 44))
    def run_check(self):
        self.show_result(check_number_text(self.number.text))
    def run_stats(self):
        self.show_result(number_statistics())

class TextToolScreen(BaseToolScreen):
    def __init__(self, mode, **kwargs):
        self.mode = mode
        self.title_text = {"work": "حسبة الوورك", "ads": "حسبة ADS", "points": "نقاط الترقية"}[mode]
        super().__init__(**kwargs)
        hint = {
            "work": "الصق رسائل/استمارات الوورك هنا",
            "ads": "الصق رسائل استمارات ADS هنا",
            "points": "كل عضو بسطر بهذا الترتيب:\nاللقب|الأطراف|الاستقبال|الرسائل|S|M|L"
        }[mode]
        self.source = make_input(hint, True, 190)
        self.body.add_widget(self.source)
        self.body.add_widget(make_button("احسب النتيجة", self.run_calculation))
        self.result = make_input("النتيجة ستظهر هنا", True, 300)
        self.body.add_widget(self.result)
        self.body.add_widget(make_button("نسخ النتيجة", lambda: Clipboard.copy(self.result.text), 44))
    def run_calculation(self):
        try:
            if self.mode == "work":
                result = work_output(self.source.text)
            elif self.mode == "ads":
                result = ads_output(self.source.text)
            else:
                result = points_output(self.source.text)
            self.result.text = result
        except Exception as exc:
            self.result.text = "حدث خطأ أثناء الحساب:\n" + str(exc)

class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        root = BoxLayout(orientation="vertical", padding=dp(18), spacing=dp(12))
        self.add_widget(root)
        root.add_widget(make_label("الإعدادات ومعلومات التطبيق", 22, (0.82, 0.58, 1, 1), 55, True))
        info = ("WANO KINGDOM\n"
                "الإصدار: 1.0.0\n\n"
                "الأدوات:\n"
                "• فاحص الأرقام\n• حسبة الوورك\n• حسبة ADS\n• نقاط الترقية\n\n"
                "التصميم: أسود وبنفسجي\n"
                "تعمل الحسابات محلياً داخل التطبيق.\n\n"
                "تنبيه: فاحص الأرقام يبحث داخل القائمة المحلية فقط، "
                "ولا يتحقق من حالة الحظر الفعلية في واتساب.")
        root.add_widget(make_label(info, 16, TEXT, 310))
        root.add_widget(make_button("العودة", lambda: setattr(self.manager, "current", "home")))

class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        root = BoxLayout(orientation="vertical", padding=dp(18), spacing=dp(13))
        self.add_widget(root)
        root.add_widget(Widget(size_hint_y=0.25))
        root.add_widget(make_label("⛩️ WANO KINGDOM", 27, (0.82, 0.58, 1, 1), 60, True))
        root.add_widget(make_label("لوحة الأدوات", 16, MUTED, 35))
        grid = GridLayout(cols=2, spacing=dp(10), size_hint_y=None)
        grid.bind(minimum_height=grid.setter("height"))
        tools = [
            ("فاحص الأرقام", "numbers"), ("حسبة الوورك", "work"),
            ("حسبة ADS", "ads"), ("نقاط الترقية", "points")
        ]
        for label, target in tools:
            grid.add_widget(make_button(label, lambda t=target: setattr(self.manager, "current", t), 90))
        root.add_widget(grid)
        root.add_widget(make_button("الإعدادات ومعلومات التطبيق", lambda: setattr(self.manager, "current", "settings"), 52))
        root.add_widget(Widget(size_hint_y=0.2))

class WanoApp(App):
    def build(self):
        self.title = APP_NAME
        Window = __import__("kivy.core.window", fromlist=["Window"]).Window
        Window.clearcolor = DARK
        sm = ScreenManager(transition=FadeTransition())
        sm.add_widget(HomeScreen(name="home"))
        sm.add_widget(NumberScreen(name="numbers"))
        sm.add_widget(TextToolScreen("work", name="work"))
        sm.add_widget(TextToolScreen("ads", name="ads"))
        sm.add_widget(TextToolScreen("points", name="points"))
        sm.add_widget(SettingsScreen(name="settings"))
        return sm

if __name__ == "__main__":
    WanoApp().run()
