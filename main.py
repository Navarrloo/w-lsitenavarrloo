import telebot
from telebot import types
from datetime import datetime

# Ваш токен бота
BOT_TOKEN = 'YOUR_BOT_TOKEN'
bot = telebot.TeleBot(BOT_TOKEN)

# Пример базы данных (замените на подключение к реальной базе данных)
user_database = {}
scammers_database = {}
guarantors = []
volunteers = []

# Команда /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "❤️ Спасибо за выбор нашего бота проверки на скам!\n\n"
                          "🐳 Попробуйте проверить человека - напишите:\n"
                          "чек @username или ID пользователя.\n\n"
                          "Для добавления скамеров используйте: /скам <ID> <причина> - <ссылка на доказательства>")

# Команда /check для проверки пользователя
@bot.message_handler(func=lambda message: message.text.startswith("чек "))
def check_command(message):
    user_input = message.text[4:].strip()
    if user_input.startswith("@"):
        user_id = user_input[1:]  # Убираем @
    else:
        user_id = user_input

    if user_id in scammers_database:
        user = scammers_database[user_id]
        response = f"""
👤 {user['name']}
💙 Репутация: {user['reputation']}
❓ Шанс скама: {user['scam_chance']}
📚 Описание: {user['description']}
"""
    else:
        response = f"""
❓ Человека нет в базе! Вероятность скама: 42%
"""
    bot.reply_to(message, response)

# Команда /скам для добавления скамеров
@bot.message_handler(commands=['скам'])
def add_scammer_step_1(message):
    try:
        args = message.text.split(maxsplit=2)
        if len(args) < 3:
            bot.reply_to(message, "❌ Неверный формат. Используйте:\n/скам <ID> <причина> - <ссылка на доказательства>")
            return
        
        user_id, reason_and_proof = args[1], args[2]
        reason, proof = reason_and_proof.split(' - ', 1)
        
        scammers_database[user_id] = {"reason": reason, "proof": proof}
        
        # Запрос репутации
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add("Плохая Репутация ⚠", "Возможно Скамер ⚠", "СКАММЕР ⚠", "Петух 🐔")
        bot.reply_to(message, "🤔 Выберите репутацию", reply_markup=markup)
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка: {e}")

# Обработчик выбора репутации
@bot.message_handler(func=lambda message: message.text in ["Плохая Репутация ⚠", "Возможно Скамер ⚠", "СКАММЕР ⚠", "Петух 🐔"])
def add_scammer_step_2(message):
    try:
        user_id = list(scammers_database.keys())[-1]  # Последний добавленный пользователь
        scammers_database[user_id]["reputation"] = message.text
        scammers_database[user_id]["name"] = f"User {user_id}"
        scammers_database[user_id]["scam_chance"] = "99%"
        scammers_database[user_id]["description"] = scammers_database[user_id]["reason"] + " - " + scammers_database[user_id]["proof"]
        
        scammer = scammers_database[user_id]
        bot.reply_to(
            message,
            f"""
👤 Пользователь с ID {user_id} добавлен в базу:
💙 Репутация: {scammer['reputation']}
❓ Причина: {scammer['reason']}
📚 Доказательства: {scammer['proof']}
"""
        )
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка: {e}")

# Команда для добавления гарантов
@bot.message_handler(commands=['add_guarantor'])
def add_guarantor(message):
    try:
        args = message.text.split(maxsplit=1)
        if len(args) < 2:
            bot.reply_to(message, "❌ Неверный формат. Используйте:\n/add_guarantor <@username>")
            return

        username = args[1]
        guarantors.append(username)
        bot.reply_to(message, f"✅ Гарант {username} добавлен!")
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка: {e}")

# Команда для добавления волонтёров
@bot.message_handler(commands=['add_volunteer'])
def add_volunteer(message):
    try:
        args = message.text.split(maxsplit=1)
        if len(args) < 2:
            bot.reply_to(message, "❌ Неверный формат. Используйте:\n/add_volunteer <@username>")
            return

        username = args[1]
        volunteers.append(username)
        bot.reply_to(message, f"✅ Волонтёр {username} добавлен!")
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка: {e}")

# Команда для просмотра гарантов
@bot.message_handler(commands=['list_guarantors'])
def list_guarantors(message):
    if guarantors:
        response = "🛡 Список гарантов:\n" + "\n".join(guarantors)
    else:
        response = "🛡 Список гарантов пуст."
    bot.reply_to(message, response)

# Команда для просмотра волонтёров
@bot.message_handler(commands=['list_volunteers'])
def list_volunteers(message):
    if volunteers:
        response = "🌴 Список волонтёров:\n" + "\n".join(volunteers)
    else:
        response = "🌴 Список волонтёров пуст."
    bot.reply_to(message, response)

# Запуск бота
print("Бот запущен...")
bot.infinity_polling()
