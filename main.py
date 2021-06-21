import telebot
import random
import requests

url = "https://blockchain.info/ru/ticker"
keyboard_main = telebot.types.ReplyKeyboardMarkup(True)
keyboard_main.row('Камень ножницы бумага', 'Курс биткоина', "Калькулятор")
keyboard_rock = telebot.types.ReplyKeyboardMarkup(True)
keyboard_rock.row('Камень', 'Ножницы', 'Бумага')
keyboard_calc = telebot.types.ReplyKeyboardMarkup(True)
keyboard_calc.row('-', '+', '*', '/')
calc_num1 = 0.0
calc_action = ""
keyboard_remove = telebot.types.ReplyKeyboardRemove()
bot = telebot.TeleBot('1889199826:AAGG2BOzSmQVA34xcwzI_dSX3UkxewaxeQg')

@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(message.chat.id, "Привет! Я бот разработанный студентом второго курса ИКБСП. Я могу поиграть с "
                                      "Вами в \"камень, ножницы, бумага\", показать курс биткоина и предоставить Вам "
                                      "простенький калькулятор. Если возникнут трудности,"
                                      " напишите команду /help.", reply_markup=keyboard_main)

@bot.message_handler(commands=['help'])
def start_command(message):
    bot.send_message(message.chat.id, "Напишите \"Камень ножницы бумага\", чтобы поиграть. Чтобы я показал курс "
                                      "биткоина напишите \"Курс биткоина\", чтобы открыть калькулятор напишите "
                                      "\"Калькулятор\".")

@bot.message_handler(content_types=['text'])
def get_start_message(message):
    if message.text == "Камень ножницы бумага":
        bot.send_message(message.chat.id, "Выберите камень, ножницы или бумагу", reply_markup=keyboard_rock)
        bot.register_next_step_handler(message, rock_paper)
    elif message.text == "Курс биткоина":
        response = requests.get(url).json()
        bot.send_message(message.chat.id, "Курс Биткоина - " + str(response['USD']['15m']) + "$")
    elif message.text == "Калькулятор":
        bot.send_message(message.chat.id, "Запускаю калькулятор", reply_markup=keyboard_remove)
        bot.send_message(message.chat.id, "Напишите первое число:")
        bot.register_next_step_handler(message, calc_start)
    else:
        bot.send_message(message.chat.id, "Я вас не понял :(", reply_markup=keyboard_main)

def rock_paper(message):
    mes = message.text.lower()
    if mes != 'камень' and mes != 'ножницы' and mes != 'бумага':
        bot.send_message(message.chat.id, "Я вас не понял, повторите ввод правильно.")
        bot.register_next_step_handler(message, rock_paper)
        return
    bot_choice = random.randint(1, 3)
    if bot_choice == 1:
        bot_choice = "камень"
    elif bot_choice == 2:
        bot_choice = "ножницы"
    elif bot_choice == 3:
        bot_choice = "бумага"
    bot.send_message(message.chat.id, "Я выбрал - " + bot_choice + " , Вы выбрали - " + mes)
    if mes == "камень" and bot_choice == "камень":
        bot.send_message(message.chat.id, "У нас ничья :/", reply_markup=keyboard_main)
    elif mes == "ножницы" and bot_choice == "ножницы":
        bot.send_message(message.chat.id, "У нас ничья :/", reply_markup=keyboard_main)
    elif mes == "бумага" and bot_choice == "бумага":
        bot.send_message(message.chat.id, "У нас ничья :/", reply_markup=keyboard_main)
    elif mes == "камень" and bot_choice == "ножницы":
        bot.send_message(message.chat.id, "Увы! Я проиграл :( С победой!", reply_markup=keyboard_main)
    elif mes == "ножницы" and bot_choice == "камень":
        bot.send_message(message.chat.id, "Ура! Я победил :) Вы проиграли!", reply_markup=keyboard_main)
    elif mes == "камень" and bot_choice == "бумага":
        bot.send_message(message.chat.id, "Ура! Я победил :) Вы проиграли!", reply_markup=keyboard_main)
    elif mes == "бумага" and bot_choice == "камень":
        bot.send_message(message.chat.id, "Увы! Я проиграл :( С победой!", reply_markup=keyboard_main)
    elif mes == "бумага" and bot_choice == "ножницы":
        bot.send_message(message.chat.id, "Ура! Я победил :) Вы проиграли!", reply_markup=keyboard_main)
    elif mes == "ножницы" and bot_choice == "бумага":
        bot.send_message(message.chat.id, "Увы! Я проиграл :( С победой!", reply_markup=keyboard_main)

def calc_start(message):
    global calc_num1
    calc_num1 = float(message.text)
    bot.send_message(message.chat.id, "Введите операцию:", reply_markup=keyboard_calc)
    bot.register_next_step_handler(message, calc_op)

def calc_op(message):
    global calc_action
    calc_action = str(message.text)
    bot.send_message(message.chat.id, "Введите второе число:", reply_markup=keyboard_remove)
    bot.register_next_step_handler(message, calc_second)

def calc_second(message):
    calc_num2 = float(message.text)
    if calc_action == '+':
        bot.send_message(message.chat.id, "Результат: " + str(calc_num1 + calc_num2), reply_markup=keyboard_main)
    elif calc_action == '-':
        bot.send_message(message.chat.id, "Результат: " + str(calc_num1 - calc_num2), reply_markup=keyboard_main)
    elif calc_action == '*':
        bot.send_message(message.chat.id, "Результат: " + str(calc_num1 * calc_num2), reply_markup=keyboard_main)
    elif calc_action == '/':
        bot.send_message(message.chat.id, "Результат: " + str(calc_num1 / calc_num2), reply_markup=keyboard_main)

bot.polling(none_stop=True, interval=0)