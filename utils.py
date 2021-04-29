import json

def save_delete_file(lstsave):
    with open('delete_save.json', 'w') as data_file:
        json.dump(lstsave, data_file)


def updateChat(mesid, chatid, time):
    with open('delete_save.json', 'r') as data_file:
        data = json.load(data_file)
        objAdd = {
            "message_id": mesid,
            "chat_id": chatid,
            "time": time
        }

        data.append(objAdd)
        save_delete_file(data)

def readOldChat():
    with open('delete_save.json', 'r') as dl_file:
        data = json.load(dl_file)
        return data