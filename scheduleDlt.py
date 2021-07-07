import time
import schedule
from datetime import date, datetime
from telegram import Bot
import json
import requests

# Config

# Include
import utils
import dbrun

TOKEN = dbrun.getConfig('bot_token')
bot = Bot(TOKEN)


def dltChat():
    try:
        with open('delete_save.json', 'r') as dl_file:
            data = json.load(dl_file)
            time_now = int(time.time())

            lst_dlt = list(filter(lambda x: x["time"] <= time_now, data))
            lst_save = list(filter(lambda x: x["time"] > time_now, data))

            if(len(lst_dlt) > 0):
                for x in lst_dlt:
                    data = requests.get('https://api.telegram.org/bot{key}/deleteMessage?chat_id={chatid}&message_id={mesid}'.format(
                        key=TOKEN, chatid=x['chat_id'], mesid=x['message_id']))

                    res = json.loads(data.text.encode('utf8').decode('utf8'))
                    if res['ok']:
                        print('Chat_ID: {chatid} - Mes_ID: {mesid} Delete Success'.format(
                            chatid=x['chat_id'], mesid=x['message_id']))
                    else:
                        print('Chat_ID: {chatid} - Mes_ID: {mesid} Delete Fail: {fail}'.format(
                            chatid=x['chat_id'], mesid=x['message_id'], fail=res['description']))

            utils.save_delete_file(lst_save)
    except Exception as e:
        print(e)
        dbrun.writeLog('dltChat', str(e))


schedule.every(1).minutes.do(dltChat)

while True:
    schedule.run_pending()
    time.sleep(1)
