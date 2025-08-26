import telebot
from telebot import types
import sql_for_bot
import email_file

my_token = "bot_token" 
bot = telebot.TeleBot(my_token)
my_id = "admin_id"
question_file = open("вопросы.txt", "r", encoding="UTF-8")
blocks = question_file.read().split("\n\n")
questions = []
answers = []
admin_pass = "23gp48A"
admin_panels = {}


def send_statistic_tg():
    stat = sql_for_bot.get_statistics()
    bot.send_message(my_id, stat)


def get_table():
    global questions, answers
    questions, answers = sql_for_bot.get_sql_table()
    # print(questions)
    # print(answers)


@bot.message_handler(commands=["admin"])
def ask_admin_password(message):
    admin_panels[message.from_user.id] = False
    mesg = bot.send_message(message.from_user.id, "Введите пароль:")
    bot.register_next_step_handler(mesg, check_admin_password)


def check_admin_password(message):
    if message.text == admin_pass:
        bot.delete_message(message.from_user.id, message.message_id)
        admin_panels[message.from_user.id] = True
        show_admin_panel(message)
    else:
        bot.send_message(message.from_user.id, "Неправильный пароль. Напишите /start если хотите задать вопрос")


def show_admin_panel(message):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    btn_back = types.KeyboardButton("Назад")
    btn_email = types.KeyboardButton("Получить статистику(почта)")
    btn_chat = types.KeyboardButton("Получить статистику(в чате)")
    markup.add(btn_email, btn_chat, btn_back)
    bot.send_message(message.from_user.id, "Вам доступна панель администратора", reply_markup=markup)


@bot.message_handler(func=lambda message: admin_panels.get(message.from_user.id, False) and message.text == "Получить статистику(в чате)")
def send_stat_in_chat(message):
    stat = sql_for_bot.get_statistics()
    bot.send_message(message.from_user.id, stat)


@bot.message_handler(func=lambda message: admin_panels.get(message.from_user.id, False) and message.text == "Получить статистику(почта)")
def send_stat_by_email(message):
    email_file.email_sending(sql_for_bot.get_statistics())
    bot.send_message(message.from_user.id, "Статистика отправлена на почту")


@bot.message_handler(func=lambda message: admin_panels.get(message.from_user.id, False) and message.text == "Назад")
def exit_admin_panel(message):
    admin_panels[message.from_user.id] = False
    mesg = bot.send_message(message.from_user.id, "Админ-панель закрыта", reply_markup=types.ReplyKeyboardRemove())
    bot.register_next_step_handler(mesg, reply_to_start)


@bot.message_handler(commands=["start"])
def reply_to_start(message):
    mesg = bot.send_message(message.from_user.id, "Я бот отвечающий на часто задаваемые вопросы. Напишите свой вопрос и я отвечу")
    bot.register_next_step_handler(mesg, reply_to_user)
    admin_panels[message.from_user.id] = False

# admin_panels.get(message.from_user.id) or


@bot.message_handler(content_types=['text'])
def reply_to_user(message):
    if message.text == "/admin":
        # print("Hello")
        mesg = bot.send_message(message.from_user.id, "Введите пароль:")
        bot.register_next_step_handler(mesg, check_admin_password)
        return
    qs_number = 0
    times = sql_for_bot.get_times()
    get_table()
    is_replied = False
    for i in range(len(questions)):
        sp = questions[i].split(", ")
        for j in sp:
            if j.lower() in message.text.lower():
                qs_number = i
                times[i] += 1
                bot.send_message(message.from_user.id, answers[i])
                is_replied = True
                sql_for_bot.change_times(questions[i])
                break
    if not is_replied:
        bot.send_message(message.from_user.id, "Обратитесь к менеджеру")


print("Бот запущен")
bot.infinity_polling()


# @bot.message_handler(commands=["admin"])
# def admin_panel(message):
#     markup = types.ReplyKeyboardMarkup(row_width=2)
#     button_back = types.KeyboardButton("Назад")
#     button_st_email = types.KeyboardButton("Получить статистику(почта)")
#     button_st_chat = types.KeyboardButton("Получить статистику(в чате)")
#     markup.add(button_back)
#     if message.text == admin_pass:
#         panel = True
#         markup.add(button_st_email, button_st_chat)
#         bot.send_message(message.from_user.id, "Вам доступна панель администратора", reply_markup=markup)
#
#         if message.text == "Получить статистику(в чате)":
#             bot.send_message(message.chat.id, sql_for_bot.get_sql_table())
#         elif message.text == "Получить статистику(почта)":
#             bot.send_message(message.chat.id, "Статистика отправлена на почту")
#             email_file.email_sending(sql_for_bot.get_sql_table())
#         elif message.text == "Назад":
#             panel = False
#             mesg = bot.send_message(message.chat.id, "Напишите /start если хотите задать вопрос", reply_markup=types.ReplyKeyboardRemove())
#             bot.register_next_step_handler(mesg, reply_to_start)
#         else:
#             bot.send_message(message.chat.id, "Я вас не понимаю")
#     elif message.text != admin_pass:
#         bot.send_message(message.chat.id, "Неправильный пароль. Напишите /start если хотите задать вопрос")



# for j in range(len(questions)):
#     sql_for_bot.add_sql(questions[j], answers[j])


# email_file.email_every_monday()
