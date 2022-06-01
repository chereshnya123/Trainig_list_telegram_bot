import pandas as pd
import numpy as np
import telebot
import config
import os
import dataframe_image as dfi
import datetime

table = pd.read_csv("ExTable.csv", dtype = 'object')
table.index = table["Упражнение"]
table = table.drop("Упражнение", 1)


bot = telebot.TeleBot(config.TOKEN)

@bot.message_handler(commands = ['register'])
def exercise_wrapper(msg):
    bot.send_message(msg.chat.id, "Введите \n[упражнение] [рабочий вес (в кг)]: \n")
    bot.register_next_step_handler(msg, exercise)

def exercise(msg):
    global table
    info = msg.text.split()
    info[0] = info[0].capitalize()
    now = datetime.datetime.now()

    if now.month < 10 and now.day < 10:
        date = "0" + str(now.day) +  ".0" + str(now.month) + "." + str(now.year)
    elif now.month < 10:
        date = str(now.day) +  ".0" + str(now.month) + "." + str(now.year) 
    elif now.day < 10:
        date = "0" + str(now.day) +  "." + str(now.month) + "." + str(now.year)
    else:
        date = str(now.day) +  "." + str(now.month) + "." + str(now.year)

    weight = str(info[-1])
    #date = str(info[-2])
    ExList = info[:-1]
    Ex = ''
    for word in ExList:
        Ex += word + " "
    Ex.capitalize()
    repeat = pd.DataFrame({"Упражнение" : [Ex], date : [weight]}, dtype = 'object')
    table.loc[Ex, date] = weight
    table = table.fillna("-")
    table.to_csv("cache\ExTable" + str(now.day) + "_" + str(now.month) + "_" + str(now.year) + "_" + str(now.hour) + str(now.minute) + str(now.second) + ".csv")
    table.to_csv("ExTable.csv")
    bot.send_message(msg.chat.id, "Успешно!")
    show(msg)


@bot.message_handler(commands = ["show"])
def show(msg):
    df = pd.read_csv("ExTable.csv", dtype = 'object')
    df.index = df["Упражнение"]
    df = df.drop("Упражнение", 1)
    df = df.style.set_properties(**{'text-align': 'left'})
    dfi.export(table,"mytable.png")
    img = open("mytable.png", 'rb')
    bot.send_photo(msg.chat.id, img)
    img.close()
    os.remove('D:\Мемгу\Прачик\Bot_Telegram\mytable.png')
    #print(bot.get_chat())






bot.infinity_polling()