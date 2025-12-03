# filename: reminder_bot.py
import asyncio
import logging
from datetime import datetime, date, time as dtime
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, StateFilter
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage

# ---------- CONFIG ----------
API_TOKEN = "8517091775:AAHOo8ZudoDFs9NrJoBf47yMpsNXDrnSLEg"
GROUP_USERNAME = "@starbit_chat"
CHANNEL_USERNAME = "@starbit_dev"

# ---------- LOGGING ----------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ---------- LANG DATA ----------
lang_data = {
    "uz": {  # Kiril
        "greet": "🌟 Салом! Тилни танланг:",
        "main_menu": "📌 Асосий меню:",
        "add_timer": "➕ Таймер қўшиш",
        "view_delete_timer": "🗑️ Таймерларни кўриш / ўчириш",
        "change_lang": "🌍 Тилни ўзгартириш",
        "set_type": "📌 Эслатма турини танланг:",
        "set_time": "⏰ Эслатма вақтни киритинг (HH:MM):",
        "choose_day": "📅 Бугун ёки келажак сана?",
        "set_date": "📅 Санани киритинг (YYYY-MM-DD):",
        "set_text": "📝 Эслатма матнини киритинг:",
        "reminder_set": "✅ Эслатма муваффақиятли ўрнатилди!",
        "error_time": "❌ Илтимос HH:MM форматда киритинг. Масалан: 14:30",
        "error_date": "❌ Илтимос YYYY-MM-DD форматда киритинг. Масалан: 2025-12-05",
        "time_passed": "❌ Эслатма вақти ўтиб кетган! Илтимос келажак вақт киритинг.",
        "reminder_msg": "⏰ Эслатма!\n {text}",
        "reminder_deleted": "✅ Эслатма ўчирилди!",
        "no_reminders": "📭 Сизда эслатмалар мавжуд эмас!",
        "cancel": "❌ Бекор қилиш",
        "private": "Шахсий",
        "group": "Гуруҳ",
        "channel": "Канал",
        "today": "Бугун ✅",
        "future": "Келажак 📅"
    },
    "oz": {  # Lotin
        "greet": "🌟 Salom! Tilni tanlang:",
        "main_menu": "📌 Asosiy menyu:",
        "add_timer": "➕ Taymer qoʻshish",
        "view_delete_timer": "🗑️ Taymerlarni koʻrish / oʻchirish",
        "change_lang": "🌍 Tilni oʻzgartirish",
        "set_type": "📌 Eslatma turini tanlang:",
        "set_time": "⏰ Eslatma vaqtini kiriting (HH:MM):",
        "choose_day": "📅 Bugun yoki kelajak sana?",
        "set_date": "📅 Sanani kiriting (YYYY-MM-DD):",
        "set_text": "📝 Eslatma matnini kiriting:",
        "reminder_set": "✅ Eslatma muvaffaqiyatli oʻrnatildi!",
        "error_time": "❌ HH:MM formatda kiriting. Masalan: 14:30",
        "error_date": "❌ YYYY-MM-DD formatda kiriting. Masalan: 2025-12-05",
        "time_passed": "❌ Eslatma vaqti oʻtib ketgan! Kelajak vaqt kiriting.",
        "reminder_msg": "⏰ Eslatma!\n {text}",
        "reminder_deleted": "✅ Eslatma oʻchirildi!",
        "no_reminders": "📭 Eslatmalar mavjud emas!",
        "cancel": "❌ Bekor qilish",
        "private": "Shaxsiy",
        "group": "Guruh",
        "channel": "Kanal",
        "today": "Bugun ✅",
        "future": "Kelajak 📅"
    },
    "ru": {  # Rus
        "greet": "🌟 Привет! Выберите язык:",
        "main_menu": "📌 Главное меню:",
        "add_timer": "➕ Добавить таймер",
        "view_delete_timer": "🗑️ Просмотр / удаление таймеров",
        "change_lang": "🌍 Сменить язык",
        "set_type": "📌 Выберите тип напоминания:",
        "set_time": "⏰ Введите время (HH:MM):",
        "choose_day": "📅 Сегодня или будущая дата?",
        "set_date": "📅 Введите дату (YYYY-MM-DD):",
        "set_text": "📝 Введите текст:",
        "reminder_set": "✅ Напоминание установлено!",
        "error_time": "❌ Формат HH:MM. Например: 14:30",
        "error_date": "❌ Формат YYYY-MM-DD. Например: 2025-12-05",
        "time_passed": "❌ Время прошло! Введите будущее время.",
        "reminder_msg": "⏰ Напоминание!\n {text}",
        "reminder_deleted": "✅ Удалено!",
        "no_reminders": "📭 Нет напоминаний.",
        "cancel": "❌ Отмена",
        "private": "Личное",
        "group": "Группа",
        "channel": "Канал",
        "today": "Сегодня ✅",
        "future": "Будущее 📅"
    },
    "en": {  # Ingliz
        "greet": "🌟 Hello! Choose language:",
        "main_menu": "📌 Main menu:",
        "add_timer": "➕ Add Timer",
        "view_delete_timer": "🗑️ View / Delete Timers",
        "change_lang": "🌍 Change Language",
        "set_type": "📌 Choose reminder type:",
        "set_time": "⏰ Enter time (HH:MM):",
        "choose_day": "📅 Today or future date?",
        "set_date": "📅 Enter date (YYYY-MM-DD):",
        "set_text": "📝 Enter text:",
        "reminder_set": "✅ Reminder set!",
        "error_time": "❌ Format HH:MM. Example: 14:30",
        "error_date": "❌ Format YYYY-MM-DD",
        "time_passed": "❌ Time passed. Choose future.",
        "reminder_msg": "⏰ Reminder!\n {text}",
        "reminder_deleted": "✅ Deleted!",
        "no_reminders": "📭 No reminders.",
        "cancel": "❌ Cancel",
        "private": "Private",
        "group": "Group",
        "channel": "Channel",
        "today": "Today ✅",
        "future": "Future 📅"
    }
}

# ---------- STATES ----------
class ReminderStates(StatesGroup):
    choosing_type = State()
    choosing_day = State()
    entering_date = State()
    entering_time = State()
    entering_text = State()
    viewing = State()

# ---------- GLOBAL STORAGE ----------
user_lang = {}
tasks = {}
next_task_id = {}
reminder_tasks = {}

def get_lang(user_id: int) -> str:
    return user_lang.get(user_id, "uz")

def generate_task_id(user_id: int) -> int:
    nid = next_task_id.get(user_id, 1)
    next_task_id[user_id] = nid + 1
    return nid

async def schedule_reminder(bot: Bot, user_id: int, r_type: str, text: str, r_date: date, r_time: dtime):
    now = datetime.now()
    remind_dt = datetime.combine(r_date, r_time)
    if remind_dt <= now:
        return
    wait_seconds = (remind_dt - now).total_seconds()
    try:
        await asyncio.sleep(wait_seconds)
        msg = lang_data[get_lang(user_id)]["reminder_msg"].format(text=text)
        if r_type == "private":
            await bot.send_message(user_id, msg)
        elif r_type == "group":
            await bot.send_message(GROUP_USERNAME, msg)
        elif r_type == "channel":
            await bot.send_message(CHANNEL_USERNAME, msg)
    except asyncio.CancelledError:
        pass

# ---------- BOT ----------
bot = Bot(API_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# ---------- HELPERS ----------
async def clean_and_edit(callback: CallbackQuery, text: str, markup=None):
    try:
        await callback.message.edit_reply_markup(reply_markup=None)
    except:
        pass
    try:
        await callback.message.edit_text(text, reply_markup=markup)
    except:
        await callback.message.answer(text, reply_markup=markup)

async def main_menu(user_id: int):
    lang = get_lang(user_id)
    kb = InlineKeyboardBuilder()
    kb.button(text=lang_data[lang]["add_timer"], callback_data="menu_add")
    kb.button(text=lang_data[lang]["view_delete_timer"], callback_data="menu_view")
    kb.button(text=lang_data[lang]["change_lang"], callback_data="menu_lang")
    kb.adjust(1)
    await bot.send_message(user_id, lang_data[lang]["main_menu"], reply_markup=kb.as_markup())

async def edit_main_menu_callback(callback: CallbackQuery):
    lang = get_lang(callback.from_user.id)
    kb = InlineKeyboardBuilder()
    kb.button(text=lang_data[lang]["add_timer"], callback_data="menu_add")
    kb.button(text=lang_data[lang]["view_delete_timer"], callback_data="menu_view")
    kb.button(text=lang_data[lang]["change_lang"], callback_data="menu_lang")
    kb.adjust(1)
    await clean_and_edit(callback, lang_data[lang]["main_menu"], kb.as_markup())

# ---------- HANDLERS ----------
@dp.message(Command("start"))
async def start_handler(message: Message, state: FSMContext):
    kb = InlineKeyboardBuilder()
    kb.button(text="🇺🇿 O’z", callback_data="lang_oz")
    kb.button(text="🇺🇿 Ўз", callback_data="lang_uz")
    kb.button(text="🇷🇺 Ru", callback_data="lang_ru")
    kb.button(text="🇬🇧 En", callback_data="lang_en")
    kb.adjust(2)
    await message.answer("🌍 Tilni tanlang / Choose language:", reply_markup=kb.as_markup())
    await state.clear()

@dp.callback_query(F.data.startswith("lang_"))
async def lang_selected(call: CallbackQuery):
    lang = call.data.split("_")[1]
    user_lang[call.from_user.id] = lang
    try:
        await call.message.edit_text(lang_data[lang]["greet"])
    except:
        await call.message.answer(lang_data[lang]["greet"])
    await edit_main_menu_callback(call)
    await call.answer()

@dp.callback_query(F.data == "menu_lang")
async def menu_lang(call: CallbackQuery):
    kb = InlineKeyboardBuilder()
    kb.button(text="🇺🇿 O’z", callback_data="lang_oz")
    kb.button(text="🇺🇿 Ўз", callback_data="lang_uz")
    kb.button(text="🇷🇺 Ru", callback_data="lang_ru")
    kb.button(text="🇬🇧 En", callback_data="lang_en")
    kb.adjust(2)
    await clean_and_edit(call, "🌍 Tilni tanlang / Choose language:", kb.as_markup())
    await call.answer()

# ---------- MENU ADD / VIEW ----------
@dp.callback_query(F.data == "menu_add")
async def menu_add(call: CallbackQuery, state: FSMContext):
    lang = get_lang(call.from_user.id)
    kb = InlineKeyboardBuilder()
    kb.button(text=lang_data[lang]["private"], callback_data="type_private")
    kb.button(text=lang_data[lang]["group"], callback_data="type_group")
    kb.button(text=lang_data[lang]["channel"], callback_data="type_channel")
    kb.adjust(1)
    await clean_and_edit(call, lang_data[lang]["set_type"], kb.as_markup())
    await state.set_state(ReminderStates.choosing_type)
    await call.answer()

@dp.callback_query(F.data == "menu_view")
async def menu_view(call: CallbackQuery, state: FSMContext):
    lang = get_lang(call.from_user.id)
    user_tasks = tasks.get(call.from_user.id, [])
    if not user_tasks:
        await clean_and_edit(call, lang_data[lang]["no_reminders"])
        await edit_main_menu_callback(call)
        await call.answer()
        return
    kb = InlineKeyboardBuilder()
    for t in user_tasks:
        txt = f"{t['text']} ({t['date']} {t['time']})"
        kb.button(text=txt, callback_data=f"delete_{t['id']}")
    kb.button(text=lang_data[lang]["cancel"], callback_data="cancel")
    kb.adjust(1)
    await clean_and_edit(call, lang_data[lang]["view_delete_timer"], kb.as_markup())
    await state.set_state(ReminderStates.viewing)
    await call.answer()

# ---------- CHOOSING TYPE / TIME / DAY / DATE / TEXT ----------
@dp.callback_query(F.data.startswith("type_"), StateFilter(ReminderStates.choosing_type))
async def choose_type(call: CallbackQuery, state: FSMContext):
    chosen = call.data.split("_")[1]
    await state.update_data(reminder_type=chosen)
    lang = get_lang(call.from_user.id)
    await clean_and_edit(call, lang_data[lang]["set_time"], None)
    await state.set_state(ReminderStates.entering_time)
    await call.answer()

@dp.message(StateFilter(ReminderStates.entering_time))
async def enter_time(message: Message, state: FSMContext):
    lang = get_lang(message.from_user.id)
    text = message.text.strip()
    try:
        entered_time = datetime.strptime(text, "%H:%M").time()
    except:
        await message.answer(lang_data[lang]["error_time"])
        return
    now = datetime.now()
    if datetime.combine(now.date(), entered_time) <= now:
        await message.answer(lang_data[lang]["time_passed"])
        return
    await state.update_data(reminder_time=entered_time)
    kb = InlineKeyboardBuilder()
    kb.button(text=lang_data[lang]["today"], callback_data="day_today")
    kb.button(text=lang_data[lang]["future"], callback_data="day_future")
    kb.adjust(2)
    await message.answer(lang_data[lang]["choose_day"], reply_markup=kb.as_markup())
    await state.set_state(ReminderStates.choosing_day)

# ---------- DAY / DATE HANDLERS ----------
@dp.callback_query(F.data == "day_today", StateFilter(ReminderStates.choosing_day))
async def choose_day_today(call: CallbackQuery, state: FSMContext):
    now = datetime.now()
    data = await state.get_data()
    r_time: dtime = data["reminder_time"]
    if datetime.combine(now.date(), r_time) <= now:
        lang = get_lang(call.from_user.id)
        await clean_and_edit(call, lang_data[lang]["time_passed"])
        await call.answer()
        return
    await state.update_data(reminder_date=now.date())
    lang = get_lang(call.from_user.id)
    await clean_and_edit(call, lang_data[lang]["set_text"], None)
    await state.set_state(ReminderStates.entering_text)
    await call.answer()

@dp.callback_query(F.data == "day_future", StateFilter(ReminderStates.choosing_day))
async def choose_day_future(call: CallbackQuery, state: FSMContext):
    lang = get_lang(call.from_user.id)
    await clean_and_edit(call, lang_data[lang]["set_date"], None)
    await state.set_state(ReminderStates.entering_date)
    await call.answer()

@dp.message(StateFilter(ReminderStates.entering_date))
async def enter_date(message: Message, state: FSMContext):
    lang = get_lang(message.from_user.id)
    text = message.text.strip()
    try:
        entered_date = datetime.strptime(text, "%Y-%m-%d").date()
    except:
        await message.answer(lang_data[lang]["error_date"])
        return
    data = await state.get_data()
    r_time: dtime = data["reminder_time"]
    if datetime.combine(entered_date, r_time) <= datetime.now():
        await message.answer(lang_data[lang]["time_passed"])
        return
    await state.update_data(reminder_date=entered_date)
    await message.answer(lang_data[lang]["set_text"])
    await state.set_state(ReminderStates.entering_text)

# ---------- ENTER TEXT / SAVE REMINDER ----------
@dp.message(StateFilter(ReminderStates.entering_text))
async def enter_text(message: Message, state: FSMContext):
    user_id = message.from_user.id
    lang = get_lang(user_id)
    data = await state.get_data()
    task_id = generate_task_id(user_id)
    r_type = data["reminder_type"]
    r_date = data["reminder_date"]
    r_time = data["reminder_time"]
    r_text = message.text.strip()
    task_info = {"id": task_id, "type": r_type, "date": r_date, "time": r_time, "text": r_text}
    tasks.setdefault(user_id, []).append(task_info)
    bg_task = asyncio.create_task(schedule_reminder(bot, user_id, r_type, r_text, r_date, r_time))
    reminder_tasks.setdefault(user_id, {})[task_id] = bg_task
    await message.answer(lang_data[lang]["reminder_set"])
    await state.clear()
    await main_menu(user_id)

# ---------- DELETE / CANCEL ----------
@dp.callback_query(StateFilter(ReminderStates.viewing), F.data.startswith("delete_"))
async def delete_timer(call: CallbackQuery, state: FSMContext):
    lang = get_lang(call.from_user.id)
    user_id = call.from_user.id
    chosen_id = int(call.data.split("_")[1])
    user_tasks = tasks.get(user_id, [])
    tasks[user_id] = [t for t in user_tasks if t["id"] != chosen_id]
    old = reminder_tasks.get(user_id, {}).pop(chosen_id, None)
    if old:
        old.cancel()
    await clean_and_edit(call, lang_data[lang]["reminder_deleted"])
    await edit_main_menu_callback(call)
    await state.clear()
    await call.answer()

@dp.callback_query(StateFilter(ReminderStates.viewing), F.data == "cancel")
async def cancel_view(call: CallbackQuery, state: FSMContext):
    await edit_main_menu_callback(call)
    await state.clear()
    await call.answer()

# ---------- RUN ----------
if __name__ == "__main__":
    logging.info("Bot ishlayapti...")
    dp.run_polling(bot)
