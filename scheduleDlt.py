import time
import schedule
from datetime import date, datetime
from telegram import Bot
import json

# Config
from tlConfig.credentials import bot_token, URL

# Include
import checkbsc
import utils

TOKEN = bot_token
# PORT = int(os.environ.get('PORT', 8443))
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
                    bot_delete = bot.delete_message(
                        chat_id=x['chat_id'], message_id=x['message_id'])
                    print(bot_delete)
                    # print('Delete message id: {mesid}'.format(mesid=x['message_id']))
                    # if not bot_delete:
                    #     lst_save.append(x)

            # utils.save_delete_file(lst_save)
    except Exception as e:
        print(e)

schedule.every(15).seconds.do(dltChat)

while True:
    schedule.run_pending()
    time.sleep(1)
