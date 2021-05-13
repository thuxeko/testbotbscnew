import json
import requests

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

def checkGasEth():
    api_key = 'xxx'
    api_gas = 'https://api.etherscan.io/api?module=gastracker&action=gasoracle&apikey=' + api_key

    check_gas = requests.get(api_gas)
    res = json.loads(check_gas.text.encode('utf8').decode('utf8'))

    if res['status'] == '1':
        text_out = 'Tốc độ bàn thờ: <b>{fast}</b> gwei/nTốc độ ô tô: <b>{medium}</b> gwei/nTốc độ xe đạp: <b>{low}</b> gwei'.format(
        fast=res['result']['FastGasPrice'], medium=res['result']['ProposeGasPrice'], low=res['result']['SafeGasPrice'])
    
        return text_out
    else:
        return 'Lỗi rồi sếp ơi :(('

    