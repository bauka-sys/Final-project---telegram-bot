import telebot
from telebot import types
import mysql.connector
import hashlib
import sqlite3

# Telebot bot
API_TOKEN = '6268661496:AAH1ofEEaKFcEsxcJhikMM4KzYTtzUxe-mw'
bot = telebot.TeleBot(API_TOKEN)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="12345",
    database="database_2"
)
cursor = db.cursor()


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, 'If you want to use the functionality of this bot press buttons in the bottom\n '
                                      'also you can type a this symbol and do it manually "/"')


@bot.message_handler(commands=['start'])
def login(message):
    user_id = message.chat.id
    bot.send_message(message.chat.id,
                     "Привет! Я technoboost bot. Хотите персональный компьютер? Пропишите /catalog и получите полный "
                     "список наших"
                     "компьютеров, пропишите /budget чтобы получить список наших компьютеров, которые влезают в ваш бюджет")
    if is_user_logged_in(user_id):
        bot.send_message(message.chat.id, 'You has a current account\n'
                                          'Enter your login')
        bot.register_next_step_handler(message, sign_in_process_username)
    else:
        bot.send_message(message.chat.id, 'You have to register\n''Enter login')
        bot.register_next_step_handler(message, process_username_step)


def is_user_logged_in(user_id):
    cursor.execute("SELECT * FROM users WHERE telegram_id = %s", (user_id,))
    return cursor.fetchone() is not None


def process_username_step(message):
    username = message.text
    print(username)
    while is_username_taken(username):
        bot.send_message(message.chat.id, "Этот логин уже занят. Введите другой логин:")
        return
    bot.send_message(message.chat.id, "Введите ваш пароль:")
    bot.register_next_step_handler(message, process_password_step, username)


def process_password_step(message, username):
    password = message.text
    print(password)
    hashed_password = hashlib.md5(password.encode()).hexdigest()
    cursor.execute("INSERT INTO users (telegram_id, username, password_hash) VALUES (%s, %s, %s)",
                   (message.from_user.id, username, hashed_password))
    db.commit()
    bot.send_message(message.chat.id, "Регистрация успешна!")
    start(message)


def is_username_taken(username):
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    return cursor.fetchone() is not None


# Sign in

def sign_in_process_username(message):
    username = message.text
    print(username)
    if username_check_sign_in(username):
        bot.send_message(message.chat.id, "Type a password")
        bot.register_next_step_handler(message, sign_in_process_password, username)

    else:
        bot.send_message(message.chat.id, "Incorrect username, try again. /start")
        return


def sign_in_process_password(message, username):
    password = message.text
    password_hash = hashlib.md5(password.encode()).hexdigest()

    if is_password_right(username, password_hash, message):
        bot.send_message(message.chat.id, "You successfully logged in")


def username_check_sign_in(username):
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    return cursor.fetchone() is not None


def is_password_right(username, password_hash, message):
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user_data = cursor.fetchone()

    if user_data:
        stored_password_hash = user_data[1]  # Assuming the password hash is stored in the second column
        if password_hash == stored_password_hash:
            return True  # Authentication successful
        else:
            bot.send_message(message.chat.id, "Incorrect password")  # Incorrect password
    else:
        bot.send_message(message.chat.id, "User not found")  # User not found
    return False


def start(message):
    message_text = (
        '<b>Hello! This bot can do many functions like:</b>\n'
        '💵 Exchange Rates\n'
        '🧮 Calculator\n'
        '💳 Online payment\n'
        '🗂 Show products that you want to buy'
    )

    bot.send_message(chat_id=message.chat.id, text=message_text, parse_mode='html')
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    bt1 = types.KeyboardButton(text="💵 Exchange Rates")
    bt3 = types.KeyboardButton(text="🛍 Catalog")
    bt4 = types.KeyboardButton(text="⚙️Settings")
    kb.add(bt1, bt3, bt4)
    bot.send_message(message.chat.id, 'Choose what you want', reply_markup=kb)


admins = [1773177526, 919921601]


@bot.message_handler(commands=['show_all_users'])
def show_all_users(message):
    state = False
    for i in range(len(admins)):
        if message.chat.id in admins:
            state = True
            break
        else:
            continue

    if not state:
        return bot.send_message(message.chat.id, 'Извините, Создатели не разрешают мне общаться с незнакомыми '
                                                 'пользователями')
    cursor.execute("SELECT * FROM users")
    all_users = cursor.fetchall()
    for user in all_users:
        bot.send_message(message.chat.id, str(user))


@bot.message_handler(func=lambda message: '⚙️Settings' in message.text)
def handle_settings(message):
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    item1 = types.KeyboardButton("Change the username")
    item2 = types.KeyboardButton("Change the password")
    item3 = types.KeyboardButton("add number phone")
    back = types.KeyboardButton("Back to Main Menu")

    markup.add(item1, item2, item3, back)
    bot.send_message(message.chat.id, "Choose an option:", reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == "Change the username")
def handle_option1(message):
    cursor.execute("SELECT FROM users where username")
    bot.send_message(message.chat.id, "You selected Option 1.")


@bot.message_handler(func=lambda message: message.text == "Change the password")
def handle_option2(message):
    cursor.execute("SELECT FROM users where username")
    bot.send_message(message.chat.id, "You selected Option 2.")


@bot.message_handler(func=lambda message: message.text == "add number phone")
def handle_option3(message):
    bot.send_message(message.chat.id, "You selected Option 3.")


@bot.message_handler(func=lambda message: message.text == "Back to Main Menu")
def handle_back(message):
    markup = types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id, "Back to the main menu.", reply_markup=markup)


@bot.message_handler(func=lambda message: '🛍 Catalog' in message.text)
def handle_catalog(message):
    # здесь коннект к нашим датабейзам
    conn = sqlite3.connect('catalog.db')
    cursor = conn.cursor()

    # здесь телега бот получает данные с датабаз
    cursor.execute('SELECT name, price, link FROM products')
    products = cursor.fetchall()

    # здесь происходит отправка пользователю каталога. if products проверяет, не пусто ли в дата базах. for проходится по
    # всем товарам в дата базах. tovar дают значение цены названия и картинки, bot.send отправляет значения переменной tovar
    if products:
        for product in products:
            tovar = f"{product[0]}\nЦена: {product[1]} тенге\nСсылка: {product[2]}\n\n"
            bot.send_message(message.chat.id, tovar)
    else:
        bot.send_message(message.chat.id, "Каталог товаров пуст.")

    conn.close()


@bot.message_handler()
def get_messages(message):
    if message.text == "Привет":
        bot.send_message(message.chat.id, f'Привет {message.from_user.first_name}', parse_mode='html')
    else:
        bot.send_message(message.chat.id, 'Я тебя не понял. Нажмите /help для подробной информации', parse_mode='html')


try:
    bot.polling()
except Exception as e:
    print(f"Error: {e}")
