
# ===========================
#   TELEGRAM BOT BY YOU 😄
# ===========================

import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# --------------------------------------------
# 🔧 این ۳ مقدار رو با اطلاعات خودت پر کن 👇
BOT_TOKEN = "8476596566:AAEVPvxn75R05FkVRyPZBcAb7dpbjcZMDX0"   # 🔹 توکن دریافتی از BotFather
ADMIN_ID =   314226829              # 🔹 عدد آیدی عددی شما از @userinfobot
CARD_NUMBER = "6219861870434106" # 🔹 شماره کارت بانکی شما
SUPPORT_ID = "@shayabd"         # 🔹 آیدی تلگرام شما برای پشتیبانی
# --------------------------------------------

bot = telebot.TeleBot(BOT_TOKEN)

# ---------- دکمه اصلی ----------
def main_menu_keyboard():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("🛒 خرید سرویس", callback_data="buy_menu"))
    return kb

# ---------- منوی خرید ----------
def buy_menu_keyboard():
    kb = InlineKeyboardMarkup()
    kb.row(
        InlineKeyboardButton("🔙 برگشت", callback_data="back"),
        InlineKeyboardButton("🟢 یک ماهه — 30 گیگ", callback_data="30gb")
    )
    kb.add(InlineKeyboardButton("🔵 یک ماهه — 40 گیگ", callback_data="40gb"))
    return kb

# ---------- دکمه پرداخت کردم ----------
def payment_done_keyboard(service_type):
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("✅ پرداخت کردم", callback_data=f"paid_{service_type}"))
    return kb


# ---------- شروع ربات ----------
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_first = message.from_user.first_name or "دوست عزیز"
    text = f"سلام {user_first}! 🌟\nبا خرید سرویس ما از هر محدودیتی رد شو خوش اومدی.\nبرای خرید از دکمه زیر استفاده کن 👇"
    bot.send_message(message.chat.id, text, reply_markup=main_menu_keyboard())


# ---------- واکنش به دکمه‌ها ----------
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "buy_menu":
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="📦 لطفاً یکی از سرویس‌های زیر را انتخاب کنید:",
            reply_markup=buy_menu_keyboard()
        )

    elif call.data == "back":
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="بازگشت به منوی اصلی 👇",
            reply_markup=main_menu_keyboard()
        )

    elif call.data == "30gb":
        bot.answer_callback_query(call.id)
        text = (
            "✅ سفارش شما ثبت شد:\n"
            "📦 سرویس: یک ماهه — 30 گیگ\n"
            "💰 قیمت: 98.000 تومان\n"
            f"💳 شماره کارت: {CARD_NUMBER}\n"
            f"📩 برای تایید پرداخت و دریافت سرویس، به آیدی زیر پیام دهید:\n{SUPPORT_ID}"
        )
        bot.send_message(call.message.chat.id, text, reply_markup=payment_done_keyboard("30gb"))

    elif call.data == "40gb":
        bot.answer_callback_query(call.id)
        text = (
            "✅ سفارش شما ثبت شد:\n"
            "📦 سرویس: یک ماهه — 40 گیگ\n"
            "💰 قیمت: 118.000 تومان\n"
            f"💳 شماره کارت: {CARD_NUMBER}\n"
            f"📩 برای تایید پرداخت و دریافت سرویس، به آیدی زیر پیام دهید:\n{SUPPORT_ID}"
        )
        bot.send_message(call.message.chat.id, text, reply_markup=payment_done_keyboard("40gb"))

    elif call.data.startswith("paid_"):
        service_type = call.data.split("_")[1]
        user = call.from_user

        confirmation = (
            f"📢 اطلاع به ادمین:\n\n"
            f"👤 نام کاربر: {user.first_name or 'بدون نام'}\n"
            f"🏷 یوزرنیم: @{user.username or 'بدون_یوزرنیم'}\n"
            f"🧾 سرویس خریداری‌شده: {service_type} یک ماهه\n"
            f"💬 وضعیت: اعلام پرداخت توسط کاربر ✅"
        )

        bot.send_message(ADMIN_ID, confirmation)
        bot.answer_callback_query(call.id, "✅ پرداخت شما ثبت شد، منتظر تایید بمانید.")
        bot.send_message(call.message.chat.id, "پرداخت شما ثبت شد ✅\nبه زودی پشتیبانی با شما تماس می‌گیرد. 🙏")

    else:
        bot.answer_callback_query(call.id, "عملیات نامشخص.")


# ---------- اجرای همیشگی ربات ----------
if __name__ == "__main__":
    print("✅ Bot is running...")
    bot.infinity_polling(timeout=10, long_polling_timeout=5)
