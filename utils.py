import json
from datetime import date, datetime
import schedule
import random
import time

# list_save = []
timen = 1619163800


def delete_oldTime():
    with open('delete_save.json', 'r') as dl_file:
        data = json.loads(dl_file)
        # list_delete = list(filter(lambda x: x["time"] <= 1619163730, data))
        list_save = list(filter(lambda x: x["time"] > 1619163730, data))
        save_delete_file(list_save)


def save_delete_file(lstsave):
    with open('delete_save.json', 'w') as data_file:
        json.dump(lstsave, data_file)


def updateChat():
    with open('delete_save.json', 'r') as data_file:
        data = json.load(data_file)
        n = random.randint(1, 200)
        objAdd = {
            "message_id": n,
            "chat_id": -1001166673188,
            "time": timen
        }

        data.append(objAdd)
        save_delete_file(data)


def updateTime():
    global timen
    ntime = random.randint(10, 50)
    timen += ntime
    print(timen)


schedule.every(15).seconds.do(updateChat)
schedule.every(10).seconds.do(updateTime)

if __name__ == '__main__':
    while True:
        schedule.run_pending()
        time.sleep(1)
