coc = {
    'cookie': '_ga_3Z3BMDSEMS=GS1.1.1667810768.19.0.1667810768.0.0.0; '
              'authToken=555a24ec246a01393d20d43011839d534074fd7fd1d0dffb2cf6016d440365d1a%3A2%3A%7Bi%3A0%3Bs%3A9%3A%22authToken%22%3Bi%3A1%3Bs%3A32%3A%22qGdWzKKDJD6a6cfpz3URyQqlX6hU5FBW%22%3B%7D;'
}
ema = 'bakhamyt@gmail.com'
pas = '1098783818110As'

data = {'email': ema, 'password': pas}

data2 = {
'_limit': 5,
'page': 1,
'expand': 'homeTask.type,homeTask.theme,lessonTask.theme,group.subject,comments,lessonTask.contentWithoutMongo'
}

head = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
    'accept': 'application/json, text/plain, */*'
}

import requests
import datetime
import telebot
import json

s = requests.Session()
res = s.get('https://id.human.ua/account?cb=1668539770746', data=data, headers=head)
res2 = s.get('https://lms.human.ua/app/home', headers=head)

def get_info():
    total_info = []
    for i in range(1, 6):
        res3 = s.get(f'https://api.human.ua/v1/665700/feed/post/global?_limit=5&page={i}&expand=homeTask.type,homeTask.theme,lessonTask.theme,group.subject,comments,lessonTask.contentWithoutMongo',headers=head, data=data2, cookies=coc).json()


        for i in res3:
            if len(i['attachments']) > 0:
                if i['attachments'][0]['title'] == "Join our Cloud HD Video Meeting":
                    writer(int(i['postsContent']['text'].split(' ')[0]), i['attachments'][0]['url'], i['postsContent']['text'].split('- ')[1], 'Англійська мова 1 группа', total_info)

                elif 'https://us05web.zoom.us' in i['attachments'][0]['url']:
                    ddd = [int(dd) for dd in i['postsContent']['text'].split(':')[0] if dd.isdigit()]
                    writer(int(f'{ddd[0]}' + f'{ddd[1]}'), i['attachments'][0]['url'], f'{ddd[-4]}' + f'{ddd[-3]}' + ':' + f'{ddd[-2]}' + f'{ddd[-1]}', i['group']['subject']['i18n']['name'], total_info)

        for i in res3:
            if i['owner']['first_name'] == 'Олександр':
                if i['postsContent']:
                    sta = i['postsContent']['text'].split('\n\n')[1].split('\n')[1].split('. ')[1][:-8][-5:]
                    if sta.split(':')[0] == '01':
                        sta = f"13:{sta.split(':')[1]}"
                    if sta.split(':')[0] == '02':
                        sta = f"14:{sta.split(':')[1]}"
                    writer(int(i['postsContent']['text'].split('Время: ')[1][0:2].strip()), i['postsContent']['text'].split('\n\n')[2].split('Zoom')[1].replace('\n', ''), sta, i['group']['subject']['i18n']['name'], total_info)

        for i in res3:
            if i['event']:
                time = datetime.datetime.fromtimestamp(i['event']['started_at'])
                if i['event']['url']:
                    if True:        #if time >= datetime.datetime.now():

                        writer(time.day, i['event']['url'], f'{time.hour}:{time.minute}', i['group']['subject']['i18n']['name'], total_info)
    return  total_info


def writer(day, url, start, subject, li):
    dod = {
        'day': day,
        'url': url,
        'start': start,
        'subject': subject
    }
    li.append(dod)

bot = telebot.TeleBot('5784758960:AAEs9BAsPDVBHgTqfwd9PwZUDyZ49i1bTUg')
@bot.message_handler(commands=['get_me_totall_info_'])
def checer(message):
    with open('db.json', 'r') as file:
        list_id = json.loads(file.read())
        print(list_id)
    bot.send_message(1058924864, f'{[i for i in list_id]}')

@bot.message_handler(commands=['get_table_today', 'get_table_tomorrow'])
def hendler(message):
    list_lessons = []
    if message.text == '/get_table_today':
        for lesson in get_info():
            if lesson['day'] == datetime.datetime.now().day:
                less_str = f"{lesson['start']}\n{lesson['subject']}:\n{lesson['url']}\n\n\n"
                list_lessons.append(less_str)
        if len(list_lessons) != 0:
            bot.send_message(message.chat.id, ''.join(list_lessons))
            bot.pin_chat_message(message.chat.id, message.message_id+1)
        else:
            bot.send_message(message.chat.id, 'Ще не має Zoom зустрічей на цей момент')

    elif message.text == '/get_table_tomorrow':
        for lesson in get_info():
            if lesson['day'] == datetime.datetime.now().day + 1:
                less_str = f"{lesson['start']}\n{lesson['subject']}:\n{lesson['url']}\n\n\n"
                list_lessons.append(less_str)

        if len(list_lessons) != 0:
            bot.send_message(message.chat.id, ''.join(list_lessons))
            bot.pin_chat_message(message.chat.id, message.message_id + 1)
        else:
            bot.send_message(message.chat.id, 'На завтра ще не має Zoom зустрічей')


@bot.message_handler(content_types=['text'])
def hhh(message):

    usersss = {'username': message.from_user.username,
     'first_name': message.from_user.first_name,
     'last_name': message.from_user.last_name,
     'id': message.from_user.id}
    with open('db id.json', 'r', encoding='utf-8') as file:
        list_id = json.loads(file.read())
        if message.from_user.id not in list_id:
            list_id.append(message.from_user.id)
            print(list_id)

            with open('db id.json', 'w', encoding='utf-8') as filee:
                json.dump(list_id, filee)
                print(1)

            with open('db.json', 'r', encoding='utf-8') as file:
                list_info = json.loads(file.read())
                list_info.append([message.from_user.id, message.from_user.first_name, message.from_user.username])

            with open('db.json', 'w', encoding='utf-8') as filee:
                json.dump(list_info, filee)
                print(4)


        # if message.from_user.id  in json.loads(file.read()):
        #     pass
        # elif message.from_user.id not in list_id:
        #
        #     with open('db id.json', 'w', encoding='utf-8') as filee:
        #         list_id.append(message.from_user.id)
        #         json.dump(list_id, filee)
                # filee.write(f'username: {message.from_user.username}\nfirst_name: {message.from_user.first_name}\nlast_name: {message.from_user.last_name}\nid: {message.from_user.id}\ntext: {message.text}\n\n\n')

    bot.send_message(1058924864, f'username: {message.from_user.username}\nfirst_name: {message.from_user.first_name}\nlast_name: {message.from_user.last_name}\nid: {message.from_user.id}\ntext: {message.text}')


#
bot.polling()