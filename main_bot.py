import telebot
from telebot import types
import config
from database_manager import SystemEngine

bot = telebot.TeleBot(config.MAIN_BOT_TOKEN)
engine = SystemEngine()

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    username = message.from_user.username or "Unknown"
    
    # تسجيل المستخدم
    engine.add_new_user(user_id, username)
    
    # معالجة الإحالة
    args = message.text.split()
    if len(args) > 1:
        referrer_id = args[1]
        if referrer_id.isdigit() and int(referrer_id) != user_id:
            engine.update_referral(int(referrer_id))

    # زرار الـ Web App
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # ملاحظة: لينك الـ Web App هنحطه هنا بعد ما ترفع ملف الـ HTML
    web_info = types.WebAppInfo("https://your-username.github.io/trend-cash-system/index.html")
    markup.add(types.KeyboardButton("🎡 فتح تريند كاش", web_app=web_info))
    
    bot.send_message(user_id, f"أهلاً بك يا {username} في بوت الربح!\nاستخدم الزرار تحت لبدء اللعب.", reply_markup=markup)

bot.polling(none_stop=True)
