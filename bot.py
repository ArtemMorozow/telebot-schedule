#!/usr/bin/env python
# -*- coding: utf-8 -*-
import telebot
from telebot import types
import requests
import json
import datetime, time
import config

def main():
    bot = telebot.TeleBot(config.token)

    # Преобразование DateTime в UNIX time
    def unix_callback():
        # 1636329600436
        # 1636363459000
        today = datetime.datetime.today()
        today = today - datetime.timedelta(days=today.weekday())
        print(today)
        return str(int(time.mktime(today.timetuple()) * 1000))[:5] + '29600' + str(
            int(time.mktime(today.timetuple()) * 1000))[10:]

    # Возврат ответа
    def response_back(url):
        response = requests.get(url)
        return json.loads(response.text)

    @bot.message_handler(commands=['start'])
    def start_message(message):
        buttons = []
        todos_list_for_stud = response_back(config.url_division_list_for_studs)

        #Динамическое создание клавиатуры
        markup = types.InlineKeyboardMarkup(row_width=3)
        for i in range(len(todos_list_for_stud)):
            buttons.append(types.InlineKeyboardButton(text=todos_list_for_stud[i]['shortTitle'],
                                                      callback_data=todos_list_for_stud[i]['idDivision']))
        markup.add(*buttons)

        bot.send_message(message.chat.id, 'Вас приветствует бот расписания занятий ОГУ им. И.С.Тургенева!', reply_markup=markup)


    def kurslist_callback(call):
        #Формирование ссылки на json курсов
        config.idDivision = call.data
        buttons = []
        todos_list_for_stud = response_back(config.url_division_list_for_studs)

        for i in range(len(todos_list_for_stud)):
            if todos_list_for_stud[i]['idDivision'] == int(config.idDivision):
                url_kurslist = config.main_url + str(todos_list_for_stud[i]['idDivision']) + '/kurslist'

        todos_kurslist = response_back(url_kurslist)

        # Динамическое создание клавиатуры
        markup = types.InlineKeyboardMarkup(row_width=5)
        for i in range(len(todos_kurslist)):
            buttons.append(types.InlineKeyboardButton(text=todos_kurslist[i]['kurs'],
                                                      callback_data=todos_kurslist[i]['kurs']))
        markup.add(*buttons)

        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text='Выберите курс', reply_markup=markup)


    def callback_grouplist(call):
        config.course = call.data
        print(config.course)
        buttons = []
        todos_list_for_stud = response_back(config.url_division_list_for_studs)

        for i in range(len(todos_list_for_stud)):
            if todos_list_for_stud[i]['idDivision'] == int(config.idDivision):
                url_grouplist = config.main_url + str(todos_list_for_stud[i]['idDivision']) + '/' + str(config.course) + '/grouplist'
                print(url_grouplist)
        todos_grouplist = response_back(url_grouplist)


        # Динамическое создание клавиатуры
        markup = types.InlineKeyboardMarkup(row_width=4)
        for i in range(len(todos_grouplist)):
            buttons.append(types.InlineKeyboardButton(text=todos_grouplist[i]['title'], callback_data=str(i)))
        markup.add(*buttons)

        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text='Выберите группу', reply_markup=markup)

    def callback_shedule(call):

        group = int(call.data)
        todos_list_for_stud = response_back(config.url_division_list_for_studs)

        for i in range(len(todos_list_for_stud)):
            if todos_list_for_stud[i]['idDivision'] == int(config.idDivision):
                url_grouplist = config.main_url + str(todos_list_for_stud[i]['idDivision']) + '/' + str(config.course) + '/grouplist'

        todos_grouplist = response_back(url_grouplist)

        url_printshedule = config.main_url + '/' + str(todos_grouplist[group]['idgruop']) + '///' + unix_callback() + '/printschedule'
        todos_printshedule = response_back(url_printshedule)
        print(todos_printshedule)

        list_shedule = []
        time = ['🕘8:30 – 10:00', '🕘10:10 – 11:40', '🕘12:00 – 13:30', '🕘13:40 – 15:10',
                '🕘15:20 – 16:50', '🕘17:00 – 18:30', '🕘18:40 – 20:10', '🕘20:15 – 21:45']
        out = ''
        place = ''

        if len(todos_printshedule) == 0:
            out = '🐫У вас нет пар на этой неделе🐫'
        else:

            #Сортировка по дням недели и парам
            for DayWeek in range(1, 7):
                for NumberLesson in range(1, 9):
                    for i in range(len(todos_printshedule) - 1):
                        if todos_printshedule[str(i)]['DayWeek'] == DayWeek and todos_printshedule[str(i)]['NumberLesson'] == NumberLesson:
                            list_shedule.append(todos_printshedule[str(i)])
            print(*list_shedule)

            for i in range(len(list_shedule)):
                if list_shedule[i]['DayWeek'] == 1 and (list_shedule[i-1]['DayWeek'] < list_shedule[i]['DayWeek'] or i == 0):
                    out += '\n' + '💥Понедельник:' + '\n'

                if list_shedule[i]['DayWeek'] == 2 and (list_shedule[i-1]['DayWeek'] < list_shedule[i]['DayWeek'] or i == 0):
                    out += '\n' + '💥Вторник:' + '\n'

                if list_shedule[i]['DayWeek'] == 3 and (list_shedule[i-1]['DayWeek'] < list_shedule[i]['DayWeek'] or i == 0):
                    out += '\n' + '💥Среда:' + '\n'

                if list_shedule[i]['DayWeek'] == 4 and (list_shedule[i-1]['DayWeek'] < list_shedule[i]['DayWeek'] or i == 0):
                    out += '\n' + '💥Четверг:' + '\n'

                if list_shedule[i]['DayWeek'] == 5 and (list_shedule[i-1]['DayWeek'] < list_shedule[i]['DayWeek'] or i == 0):
                    out += '\n' + '💥Пятница:' + '\n'

                if list_shedule[i]['DayWeek'] == 6 and (list_shedule[i-1]['DayWeek'] < list_shedule[i]['DayWeek'] or i == 0):
                    out += '\n' + '💥Суббота:' + '\n'

                if list_shedule[i]['NumberRoom'] == 'ДОТ':
                    place = list_shedule[i]['NumberRoom'] + ': ' + list_shedule[i]['link']
                else:
                    list_shedule[i]['Korpus'] + '-' + list_shedule[i]['NumberRoom']

                out += '[' + str(list_shedule[i]['NumberLesson']) + '] ' + list_shedule[i]['TitleSubject'] + ' (' + list_shedule[i]['TypeLesson'] + ')' + '\n' + time[list_shedule[i]['NumberLesson']-1] + '\n' + '👨‍🏫' + list_shedule[i]['Family'] + ' ' + list_shedule[i]['Name'][0] + '.' + list_shedule[i]['SecondName'][0] + '\n' + place + '\n\n'

        markup = types.InlineKeyboardMarkup()
        button = types.InlineKeyboardButton(text='Заново', callback_data='/start')
        markup.add(button)

        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                              text=out, reply_markup=markup)


    #Обработчик
    @bot.callback_query_handler(func=lambda call:True)
    def callback(call):
        print(call.message.text)
        if call.message.text == 'Вас приветствует бот расписания занятий ОГУ им. И.С.Тургенева!':
            #bot.send_message(call.message.chat.id, call.data)
            kurslist_callback(call)
        elif call.message.text == 'Выберите курс':
            callback_grouplist(call)
        elif call.message.text == 'Выберите группу':
            callback_shedule(call)
        else:
            start_message(call.message)

    bot.polling(none_stop=True)

if __name__ == "__main__":
    main()