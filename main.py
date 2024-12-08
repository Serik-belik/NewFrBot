import telebot
from telebot import types
import json

bot = telebot.TeleBot('7601716276:AAGQ9fHikwUXNsVDFxsrSRS6BZO28_I1naE')
ChatID = 457274387

Mode = ""
Topic = ""
Questions = None
Question = None
i = int()

def load_data():
    files = {"Grammaire": "grammaire.json", "Lexic": "lexic.json"}
    with open(files[Mode], encoding='utf-8') as file:
        return json.load(file)

def select_chapter():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        types.KeyboardButton("Lexic"),
        types.KeyboardButton("Grammaire")
    )
    bot.send_message(ChatID, "Select Mode", reply_markup=markup)

def select_topic():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for key in load_data().keys():
        markup.add(types.KeyboardButton(key))
    bot.send_message(ChatID, "Select Topic", reply_markup=markup)

def grammaire(message = ""):

    def send_task():
        from random import randint
        global Question
        Question = randint(0, len(Questions) - 1)
        if len(Questions[Question]['V']):
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            for answer in Questions[Question]['V']:
                markup.add(types.KeyboardButton(answer))

            bot.send_message(ChatID, f"{i+1}. {Questions[Question]['Q']}", reply_markup=markup)
        else:
            bot.send_message(ChatID, f"{i + 1}. {Questions[Question]['Q']}")

    def check_task():
        if message == Questions[Question]['C']:
            bot.send_message(ChatID, 'Correct ', reply_markup=types.ReplyKeyboardRemove())
            del Questions[Question]
            global i
            i += 1
            if Questions: send_task()
        else:
            bot.send_message(ChatID, 'Incorrect ', reply_markup=types.ReplyKeyboardRemove())
            send_task()

    if not message:
        tasks = load_data()[Topic]
        global Questions, i
        i = 0
        Questions = tasks['Questions'].copy()
        bot.send_message(ChatID, tasks['Task'] + f"\nIt y a {len(Questions)} total", reply_markup=types.ReplyKeyboardRemove())
        send_task()
    else:
        check_task()

def lexic(message = ""):

    def send_task():
        from random import choice, shuffle
        global Question
        Question = choice(tuple(Questions.keys()))
        all_answers = load_data()[Topic]
        answers = [Questions[Question], ]
        while len(answers) != 4:
            answer = choice(tuple(all_answers.values()))
            if answer not in answers: answers.append(answer)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        shuffle(answers)
        for answer in answers:
            markup.add(types.KeyboardButton(answer))

        bot.send_message(ChatID, f"{i+1}. {Question}", reply_markup=markup)

    def check_task():
        if message == Questions[Question]:
            bot.send_message(ChatID, 'Correct ', reply_markup=types.ReplyKeyboardRemove())
            del Questions[Question]
            global i
            i += 1
            if Questions: send_task()
        else:
            bot.send_message(ChatID, 'Incorrect ', reply_markup=types.ReplyKeyboardRemove())
            send_task()

    if not message:
        tasks = load_data()[Topic]
        global Questions, i
        i = 0
        Questions = tasks.copy()
        bot.send_message(ChatID, f"Choose a correct variant\nIt y a {len(Questions)} total", reply_markup=types.ReplyKeyboardRemove())
        send_task()
    else:
        check_task()

@bot.message_handler(commands=['start'])
def main(message):
    select_chapter()

@bot.message_handler()
def message_handler(message):
    global Mode, Topic
    if not Mode:
        Mode = message.text
        select_topic()
    elif not Topic:
        Topic = message.text
        {"Grammaire": grammaire, "Lexic": lexic}[Mode]()
    elif Topic:
        {"Grammaire": grammaire, "Lexic": lexic}[Mode](message.text)
        if not Questions:
            Mode = ""
            Topic = ""
            select_chapter()


bot.polling()
