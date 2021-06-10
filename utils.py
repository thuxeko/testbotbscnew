import json
import cloudscraper

# region Chat
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

# endregion

def readConfigJson():
    with open('config.json', 'r') as dl_file:
        data = json.load(dl_file)
        return data


def checkToken(contract: str, network: str):
    url = "https://api.dex.guru/v1/tokens/{contract}?network={network}"
    scraper = cloudscraper.create_scraper()
    for x in range(5):
        res = scraper.get(url.format(
            contract=contract.lower(), network=network.lower()))
        if res.status_code == 200:
            return json.loads(res.text)
        elif x == 4 and res.status_code != 200:
            return False
