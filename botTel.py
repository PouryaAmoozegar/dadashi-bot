import telebot
import jdatetime
from datetime import datetime
import random
import time
import os
# import threading
from concurrent.futures import ThreadPoolExecutor
# ================= TOKEN =================


Token = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(Token)

# ================= STATE =================
state = {
    "mood": "normal",
    "xp": {},
    "last_fal": {}
}

# ================= THREAD =================
executor = ThreadPoolExecutor(max_workers=10)
user_last_call = {}
# ================= DATA =================
roast_bank = [
    "😂 آروم باش داداشی، زیادی جدی گرفتی!",
    "😎 من داداشی‌ام، نه گوگل!",
    "🤖 یه کم مهربون‌تر حرف بزن رفیق 😄",
    "🔥 اینو از من نپرس، از بقیه بپرس 😏",
    "😆 اوه اوه! چه سوالی پرسیدی!",
    "🤝 داداشی همیشه کنارت هست 😉",
    "😴 من رباتم ولی از تو باحال‌ترم 😎"
]
jokes = [
    "😂 یه روزی یکی گفت زندگی آسونه... هنوز گمش کردیمش!",
    "😎 مغزم هنگ کرده ولی هنوز کار می‌کنم!",
    "🤣 اینترنت قطعه؟ نه، زندگیه!"
]

fals = [
    "🌹 ستاره اقبال تو در حال درخشیدن است.",
    "🔮 روزی پر از انرژی مثبت در پیش داری.",
    "🦋 تلاش‌های تو نتیجه خواهد داد.",
    "🌙 کسی به تو فکر می‌کند.",
    "🍀 اتفاق خوب نزدیک است.",
    "☀️ به هدفت نزدیک شدی."
]
# ================= HELPERS =================


def update_xp(user_id):
    state["xp"][user_id] = state["xp"].get(user_id, 0) + 1
    xp = state["xp"][user_id]

    if xp % 10 == 0:
        return f"🎉 لول آپ کردی!\nXP: {xp}"
    return None


# def get_mood():
#     return state["mood"]


def change_mood():
    if state["mood"] == "normal":
        state["mood"] = "funny"
    elif state["mood"] == "funny":
        state["mood"] = "angry"
    else:
        state["mood"] = "normal"
    return state["mood"]


def send_fal(chat_id, message_id):
    try:
        time.sleep(2)
        result = random.choice(fals)

        bot.send_message(chat_id, f"📜 فال شما:\n\n{result}")
        bot.delete_message(chat_id, message_id)

    except Exception as e:
        print("Fal error:", e)
# =================MAIN HANDLER =================


@bot.message_handler(func=lambda m: True)
def handler(m):
    text = (m.text or "").lower()
    user_id = m.from_user.id

    # ---------- XP ----------
    xp_msg = update_xp(user_id)
    if xp_msg:
        bot.reply_to(m, xp_msg)

    # ---------- CHAT ----------
    if text in ["سلام", "salam"]:
        bot.reply_to(m, "سلام داداش 😎")

    elif text in ["خوبی", "چطوری"]:
        bot.reply_to(m, "من داداشی‌ام 😏 تو چطوری؟")

    elif "ربات" in text:
        bot.reply_to(m, "داداشی در خدمته 🤖")

    elif text in ["😂", "🤣"]:
        bot.reply_to(m, "می‌خندی ولی من جدی‌ام 😆")

    elif "اسم" in text:
        bot.reply_to(m, "من داداشی‌ام 😎")

    elif "سن" in text:
        bot.reply_to(m, "من جاودانه‌ام 🤖")

    elif "عشق" in text:
        bot.reply_to(m, "عشق؟ اول خودتو درست کن 😏")

    elif "کمک" in text:
        bot.reply_to(m, "داداشی همیشه کنارت هست 🤝")

    # ---------- ROAST ----------
    elif any(x in text for x in ["خفه", "برو", "چرت"]):
        bot.reply_to(m, random.choice(roast_bank))

    # ---------- FUN ----------
    elif text == "حال بده":
        bot.reply_to(m, random.choice(jokes))

    # ---------- MOOD ----------
    elif text == "مود":
        new_mood = change_mood()
        bot.reply_to(m, f"😎 مود تغییر کرد: {new_mood}")

    # ---------- DATE ----------
    elif text in ["امروز چندمه", "تاریخ"]:
        now = datetime.now()
        shamsi = jdatetime.datetime.fromgregorian(datetime=now)

        bot.reply_to(m,
                     f"📅 {shamsi.strftime('%Y/%m/%d')}\n"
                     f"⏰ {shamsi.strftime('%H:%M:%S')}"
                     )
# ---------- FAL ----------
    elif text == "فال":
        user_id = m.from_user.id
        now = time.time()

        if user_id in state["last_fal"]:
            if now - state["last_fal"][user_id] < 10:
                bot.reply_to(m, "⏳ هر 10 ثانیه یک بار فال بگیر!")
                return

    state["last_fal"][user_id] = now

    wait_msg = bot.reply_to(m, "🔮 در حال گرفتن فال شما...")

    try:
        time.sleep(2)
        result = random.choice(fals)

        bot.send_message(
            m.chat.id,
            f"📜✨ فال شما ✨📜\n\n{result}\n\n🍀 شانس همراهت!"
        )

        bot.delete_message(m.chat.id, wait_msg.message_id)

    except Exception as e:
        print("FAL ERROR:", e)
        bot.reply_to(m, "❌ خطا در گرفتن فال!")


# # /////////////////////
# mood = "normal"  # normal / angry / funny

# ///////////////


# @bot.message_handler(func=lambda m: True)
# def main_handler(m):
#     text = (m.text or "").lower()
#     user_id = m.from_user.id
# ================= JOIN HANDLER =================
@bot.message_handler(content_types=['new_chat_members'])
def welcome(m):
    bot.reply_to(m, f"👋 خوش آمدی {m.from_user.first_name}")


@bot.chat_join_request_handler(func=lambda r: True)
def approve(r):
    bot.approve_chat_join_request(r.chat.id, r.from_user.id)
    bot.send_message(r.chat.id, f"کاربر {r.from_user.first_name} پذیرفته شد!")

    # ================= ADMIN COMMANDS =================


@bot.message_handler(func=lambda m: m.text == "پین")
def pin(m):
    if m.reply_to_message:
        bot.pin_chat_message(m.chat.id, m.reply_to_message.message_id)


@bot.message_handler(func=lambda m: m.text == "بن")
def ban(m):
    if m.reply_to_message:
        bot.ban_chat_member(m.chat.id, m.reply_to_message.from_user.id)


@bot.message_handler(func=lambda m: m.text == "حذف بن")
def unban(m):
    if m.reply_to_message:
        bot.unban_chat_member(m.chat.id, m.reply_to_message.from_user.id)


@bot.message_handler(func=lambda m: m.text == "سکوت")
def mute(m):
    if m.reply_to_message:
        bot.restrict_chat_member(
            m.chat.id,
            m.reply_to_message.from_user.id,
            can_send_messages=False
        )


@bot.message_handler(func=lambda m: m.text == "حذف سکوت")
def unmute(m):
    if m.reply_to_message:
        bot.restrict_chat_member(
            m.chat.id,
            m.reply_to_message.from_user.id,
            can_send_messages=True
        )

        # ///////////////


@bot.message_handler(content_types=['new_chat_members'])
def welcome(m):
    bot.reply_to(m, f"کاربر {m.from_user.first_name}\nبه گروه خوش آمدید!")


@bot.chat_join_request_handler(func=lambda r: True)
def approve(r):
    bot.approve_chat_join_request(r.chat.id, r.from_user.id)
    bot.send_message(
        r.chat.id, f"کاربر {r.from_user.first_name}\nدر گروه اکسپت شد!")


@bot.message_handler(func=lambda m: m.text == "پین")
def pin(m):
    bot.pin_chat_message(m.chat.id, m.reply_to_message.id)
    bot.reply_to(m, "پیام مورد نظر سنجاق شد!")


@bot.message_handler(func=lambda m: m.text == "آن پین")
def unpin(m):
    bot.unpin_chat_message(m.chat.id, m.reply_to_message.id)
    bot.reply_to(m, "پیام مورد نظر از سنجاق خارج شد!")


@bot.message_handler(func=lambda m: m.text == "افزودن ادمین")
def promote(m):
    bot.promote_chat_member(
        m.chat.id,
        m.reply_to_message.json["from"]["id"],
        can_change_info=True,
        can_delete_messages=True,
        can_invite_users=True,
        can_restrict_members=True,
        can_pin_messages=True,
        # can_promote_members=True,
        can_manage_chat=True,
        # can_manage_video_chats=True,
        # can_manage_topics=True,
        can_post_messages=True,
        can_edit_messages=True,
        can_manage_voice_chats=True,
        # can_manage_topics=False
    )
    bot.reply_to(m, "ادمین شد!")


@bot.message_handler(func=lambda m: m.text == "حذف ادمین")
def demote(m):
    bot.promote_chat_member(
        m.chat.id,
        m.reply_to_message.json["from"]["id"],
        can_change_info=False,
        can_delete_messages=False,
        can_invite_users=False,
        can_restrict_members=False,
        can_pin_messages=False,
        can_promote_members=False,
        can_manage_chat=False,
        can_manage_video_chats=False,
        # can_manage_topics=False,
        can_post_messages=False,
        can_edit_messages=False,
        can_manage_voice_chats=False,
        # can_manage_topics=False
    )
    bot.reply_to(m, "برکنار شد!")


@bot.message_handler(func=lambda m: m.text == "بن")
def ban(m):
    bot.ban_chat_member(m.chat.id, m.reply_to_message.from_user.id)
    # بعد از ایدی انتیل دیت بزاری انبن خودکار میکنه
    bot.reply_to(m, f"کاربر {m.reply_to_message.from_user.id}\nبن شد!")


@bot.message_handler(func=lambda m: m.text == "حذف بن")
def unban(m):
    bot.unban_chat_member(m.chat.id, m.reply_to_message.from_user.id)
    bot.reply_to(
        m, f"کاربر {m.reply_to_message.from_user.id}\nآن بن شد!")


@bot.message_handler(func=lambda m: m.text == "سکوت")
def restrict(m):
    bot.restrict_chat_member(
        m.chat.id,
        m.reply_to_message.from_user.id,
        can_send_messages=False,
        # can_send_media_messages=False,
        # can_send_other_messages=False,
        can_add_web_page_previews=False
    )
    bot.reply_to(
        m, "سکوت شد")


@bot.message_handler(func=lambda m: m.text == "حذف سکوت")
def derestrict(m):
    bot.restrict_chat_member(
        m.chat.id,
        m.reply_to_message.from_user.id,
        can_send_messages=True,
        # can_send_media_messages=True,
        # can_send_other_messages=True,
        can_add_web_page_previews=True
    )
    bot.reply_to(
        m, "حذف سکوت شد")
# ///////////////تاریخ و ساعت


@bot.message_handler(func=lambda m: m.text in ["امروز چندمه", "تاریخ"])
def today(m):
    now = datetime.now()

    shamsi = jdatetime.datetime.fromgregorian(datetime=now)

    text = (
        f"📅 تاریخ شمسی:\n"
        f"{shamsi.strftime('%Y/%m/%d')}\n\n"
        f"⏰ ساعت:\n"
        f"{shamsi.strftime('%H:%M:%S')}"
    )

    bot.reply_to(m, text)
# /////////////////
# فالللللل ///////


# ///////////////////
# نسخه قوی تر فال


# --- Thread pool برای کنترل فشار ---
# executor = ThreadPoolExecutor(max_workers=20)

# --- Rate limit ساده (هر کاربر هر 10 ثانیه 1 بار) ---
# user_last_call = {}
# --- فال‌ها (خارج از تابع برای performance) ---
fals = [
    "🌹 فال امروزت 🌹\n\n✨ ستاره اقبال تو در حال درخشیدن است.\n💫 به زودی خبری خوشحال‌کننده دریافت می‌کنی.\n🍀 به نشانه‌های خوب اطرافت توجه کن.",

    "🔮 فال امروزت 🔮\n\n🌞 روزی پر از انرژی مثبت در پیش داری.\n🤝 دیداری غیرمنتظره می‌تواند مسیرت را تغییر دهد.\n🌺 با لبخند به استقبال اتفاقات برو.",

    "🦋 فال امروزت 🦋\n\n💎 تلاش‌های گذشته‌ات به ثمر خواهد نشست.\n📈 فرصتی برای پیشرفت در انتظارت است.\n⭐ به توانایی‌های خودت اعتماد کن.",

    "🌙 فال امروزت 🌙\n\n❤️ شخصی به تو فکر می‌کند.\n📨 پیامی یا خبری دریافت خواهی کرد که باعث خوشحالی‌ات می‌شود.\n🌹 قدر لحظه‌های خوب را بدان.",

    "🍃 فال امروزت 🍃\n\n🌈 پس از هر سختی، آسانی می‌آید.\n🚀 زمان آن رسیده که برای هدفت قدمی بزرگ برداری.\n✨ شجاعتت کلید موفقیت توست.",

    "☀️ فال امروزت ☀️\n\n🎯 هدفت از آنچه فکر می‌کنی نزدیک‌تر است.\n💰 فرصتی ارزشمند در مسیرت قرار می‌گیرد.\n🍀 به ندای قلبت اعتماد کن.",

    "🌟 فال امروزت 🌟\n\n🕊 آرامش در راه است.\n🌸 اتفاقی کوچک می‌تواند لبخند بزرگی روی لبانت بیاورد.\n💖 امروز مهربانی‌ات چند برابر به خودت بازمی‌گردد.",
    "🌺 فال امروزت 🌺\n\n✨ آرزویی که مدت‌ها در دل داری، یک قدم به واقعیت نزدیک‌تر شده است.\n🍀 صبور باش و مسیرت را ادامه بده.\n💎 پاداش تلاش‌هایت در راه است.",

    "🕊 فال امروزت 🕊\n\n🌤 ابرهای نگرانی کم‌کم کنار می‌روند.\n🌈 روزهای روشن‌تری در انتظارت هستند.\n❤️ به خودت و توانایی‌هایت ایمان داشته باش.",

    "🌟 فال امروزت 🌟\n\n🎁 یک غافلگیری خوشایند در راه توست.\n🤝 از کمک دیگران استقبال کن.\n✨ گاهی بهترین اتفاقات زمانی رخ می‌دهند که انتظارش را نداری.",

    "🍃 فال امروزت 🍃\n\n🚀 زمان شروع یک تجربه جدید فرا رسیده است.\n🌹 از تغییر نترس؛ ممکن است خوشبختی پشت همان تغییر باشد.\n⭐ شجاع باش و قدم بردار.",

    "🌙 فال امروزت 🌙\n\n📖 درسی ارزشمند از یک اتفاق ساده خواهی گرفت.\n💫 این درس راه آینده‌ات را روشن‌تر می‌کند.\n🍀 به نشانه‌های اطرافت دقت کن.",

    "☀️ فال امروزت ☀️\n\n😊 لبخندی که امروز هدیه می‌دهی، چند برابر به خودت بازمی‌گردد.\n🌸 مهربانی تو بی‌پاسخ نخواهد ماند.\n💖 قلبت را از کینه خالی نگه دار.",

    "🦋 فال امروزت 🦋\n\n🎯 فرصت مهمی در نزدیکی تو قرار دارد.\n👀 با دقت به اطرافت نگاه کن.\n🌟 موفقیت از آنِ کسانی است که آماده‌اند.",

    "🌹 فال امروزت 🌹\n\n💌 خبری از دوستی قدیمی یا آشنایی دور دریافت خواهی کرد.\n✨ این خبر لبخند بر لبانت می‌نشاند.\n🍀 به روابط ارزشمندت بیشتر توجه کن.",

    "🔮 فال امروزت 🔮\n\n💰 نشانه‌هایی از بهبود شرایط مالی دیده می‌شود.\n📈 تصمیم‌های عاقلانه امروز، آینده بهتری می‌سازند.\n🌟 با برنامه پیش برو.",

    "🌈 فال امروزت 🌈\n\n❤️ قلبت به آرامشی که دنبالش هستی نزدیک‌تر می‌شود.\n🕯 گذشته را رها کن و به آینده نگاه کن.\n✨ بهترین روزها هنوز در راه‌اند.",

    "🏆 فال امروزت 🏆\n\n🔥 انگیزه‌ای تازه در وجودت شکل می‌گیرد.\n🚀 پروژه یا هدفی که رها کرده بودی دوباره جان می‌گیرد.\n💪 به خودت اعتماد کن.",

    "🌠 فال امروزت 🌠\n\n🎊 اتفاقی کوچک می‌تواند شادی بزرگی برایت به همراه داشته باشد.\n🌸 قدر لحظه‌های ساده را بدان.\n🍀 خوش‌شانسی در کنار توست."
]

# --- تابع اصلی ارسال ---


# def send_fal(bot, m, wait_msg):
#     try:
#         result = random.choice(fals)

#         bot.send_message(
#             m.chat.id,
#             f"📜✨ فال شما آماده است ✨📜\n\n{result}\n\n🍀 روز خوبی داشته باشی 🍀"
#         )

#         bot.delete_message(m.chat.id, wait_msg.message_id)

#     except Exception as e:
#         print("Error in send_fal:", e)


# # --- هندلر ---
# @bot.message_handler(func=lambda m: m.text == "فال")
# def fal(m):

#     user_id = m.from_user.id
#     now = time.time()

#     # --- rate limit ---
#     if user_id in user_last_call:
#         if now - user_last_call[user_id] < 10:
#             bot.reply_to(m, "⏳ لطفاً کمی صبر کن (هر 10 ثانیه یک بار فال)")
#             return

#     user_last_call[user_id] = now

# #     # --- پیام انتظار ---
#     wait_msg = bot.reply_to(
#         m,
#         "🔮 در حال گرفتن فال شما...\n⏳ لطفاً کمی صبر کنید ..."
#     )

# //////////////// پایان فال


# @bot.message_handler(func=lambda m: m.text == "حذف")✕
# def delete(m):
#     bot.delete_message(m.chat.id, m.reply_to_message.id)✕
#     bot.reply_to(m, "پیام مورد نظر حذف شد!")

# @bot.message_handler(func=lambda m: m.text == "بن")✕
# def ban(m):✕
#     bot.kick_chat_member(m.chat.id, m.reply_to_message.✕from_user.id)
#     bot.reply_to(m, "کاربر مورد نظر بن شد!")✕

# @bot.message_handler(func=lambda m: m.text == "آن بن")✕
# def unban(m):
#     bot.unban_chat_member(m.chat.id, m.reply_to_message.✕from_user.id)
#     bot.reply_to(m, "کاربر مورد نظر آنبن شد!")✕

# @bot.message_handler(func=lambda m: m.text == "ادمین")✕
# def admin(m):
#     bot.promote_chat_member(m.chat.id, m.reply_to_message.✕from_user.id, can_change_info=True, can_delete_messages=True,
#                             can_invite_users=True, ✕can_restrict_members=True, can_pin_messages=True, can_promote_members=True)
#     bot.reply_to(m, "کاربر مورد نظر ادمین شد!")✕


# @bot.message_handler(func=lambda m: m.text == "آن ادمین")✕
# def unadmin(m):
#     bot.promote_chat_member(m.chat.id, m.reply_to_message.✕from_user.id, can_change_info=True, can_delete_messages=True,
#                             can_invite_users=True, ✕can_restrict_members=True, can_pin_messages=True, ✕can_promote_members=True)
#     bot.reply_to(m, "کاربر مورد نظر آنادمین شد!")✕


# ================= START =================
bot.infinity_polling()
