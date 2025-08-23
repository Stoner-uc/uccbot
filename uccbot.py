import telebot
from telebot import types

TOKEN = '7995500908:AAEPFWvH8ejBm0_3nFcpMiQqRtx60iNikTQ'
bot = telebot.TeleBot(TOKEN)

# Foydalanuvchi holatini saqlash
user_data = {}

# Admin ID (buyurtmalar shu IDga boradi)
admin_id = 7157341901  # 👈 Sizning ID'ingiz

# /start komandasi
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("📞 Admin bilan bog'lanish")
    btn2 = types.KeyboardButton("💳 UC narxi yoki karta")
    btn3 = types.KeyboardButton("📝 Buyurtma berish")
    markup.add(btn1, btn2, btn3)

    bot.send_message(
        message.chat.id,
        "Assalomu alaykum!\nQuyidagi tugmalardan birini tanlang 👇",
        reply_markup=markup
    )

# Tugmalarni boshqarish
@bot.message_handler(func=lambda message: message.text == "📞 Admin bilan bog'lanish")
def contact_admin(message):
    bot.send_message(message.chat.id,
        "Admin bilan bog‘lanish uchun:\n📱 @stoner_uc\n📞 Tel: +998 77 348 20 29")

@bot.message_handler(func=lambda message: message.text == "💳 UC narxi yoki karta")
def send_price(message):
    bot.send_message(message.chat.id,
        "💳 UC va GROWTH PACK narxlari: Shu kanaldan to'liq bilishingiz mumkin  @stonernarx \n\n"
        "• 60 UC – 13,000 so‘m\n"
        "• 325 UC – 56,000 so‘m\n"
        "• 660 UC – 113,000 so‘m\n\n"
        "💰 To‘lov karta: AnorBank Humo – 9860 6067 4312 1174 (Khasanboyev X)\n"
        "💰 To‘lov karta: AgroBank Visa – 4073 4200 5493 2532 (Abdullayeva G)\n"
        "Hamma kartalar: @stonercard  +99877482029 hamma kartalar shu raqamga ulangan\n\n"
        "📸 Chek bo'lmasa to‘lov 0 ga teng 1000 sumga ham nasiyaga savdo yoq hatto sizga ham🫵!"
    )

# Buyurtma jarayoni boshlanishi
@bot.message_handler(func=lambda message: message.text == "📝 Buyurtma berish")
def order_start(message):
    user_data[message.chat.id] = {}
    bot.send_message(message.chat.id, "Pubg ID ingizni kiriting:")
    bot.register_next_step_handler(message, get_name)

def get_name(message):
    user_data[message.chat.id]['name'] = message.text
    bot.send_message(message.chat.id, "Uc miqdori va nikingizni kiriting:")
    bot.register_next_step_handler(message, get_phone)

def get_phone(message):
    user_data[message.chat.id]['phone'] = message.text
    bot.send_message(message.chat.id, "To‘lov chekini (rasm) yuboring:")
    bot.register_next_step_handler(message, get_check)

def get_check(message):
    if message.content_type == 'photo':
        file_id = message.photo[-1].file_id
        user_data[message.chat.id]['check'] = file_id

        data = user_data[message.chat.id]

        caption = (
            f"🆕 Yangi buyurtma:\n\n"
            f"👤 Pubg ID: {data['name']}\n"
            f"📞 Uc miqdori va nik: {data['phone']}"
        )

        # ✅ Buyurtmani sizga yuboradi (adminga)
        bot.send_photo(admin_id, file_id, caption=caption)
        bot.send_message(message.chat.id, "✅ Buyurtmangiz qabul qilindi Chekni tekshirib Admin sizga tez orada aloqaga chiqadi @stoner_uc !")

    else:
        bot.send_message(message.chat.id, "❗ Iltimos, rasm (chek) yuboring.")
        bot.register_next_step_handler(message, get_check)

# Botni ishga tushirish
bot.polling()