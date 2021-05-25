from pymongo import MongoClient
import json
import utils

dataConfig = utils.readConfigJson()

client = MongoClient(dataConfig['mongo_connect'])
db = client['tl_chatbot']  # Database

user_group = db["user_group"]  # Collect(Table)
token_list = db["token_list"]  # Collect(Table)
config_data = db["config_data"]  # Collect(Table)
logs_data = db["logs_data"]  # Collect(Table)


def insertToDb(item: str, typeTb: int, network: str = None):
    status = ''
    try:
        if typeTb == 1:  # User
            item_json = json.loads(item)
            # Check exist
            objCheck = user_group.find_one(
                {"chat_id": item_json['chat']['id']})  # Check Exist
            if not objCheck:
                item_insert = {
                    'type': 1 if item_json['chat']['type'] == 'private' else 2,
                    'chat_id': item_json['chat']['id'],
                    'title': None if item_json['chat']['type'] == 'private' else item_json['chat']['title'],
                    'user_id': item_json['from']['id'] if item_json['chat']['type'] == 'private' else None,
                    'user_name': item_json['from']['username'] if item_json['chat']['type'] == 'private' else None,
                    'name_user': item_json['from']['first_name'] if item_json['chat']['type'] == 'private' else None,
                    'administrator': False,
                    'active': True
                }

                user_group.insert_one(item_insert)
                status = 'Insert user thành công: {chatid}'.format(
                    chatid=item_json['chat']['id'])
            else:
                status = 'Bản ghi đã tồn tại: {chatid}'.format(
                    chatid=item_json['chat']['id'])
        elif typeTb == 2:  # Token
            objCheck = token_list.find_one(
                {"contract": item, 'network': network})  # Check Exist DB
            if not objCheck:
                # Check Contract Dexguru
                token = utils.checkToken(item, network)
                if token:
                    item_insert = {
                        'contract': item,
                        'symbol': token['symbol'],
                        'name': token['name'],
                        'network': network,
                        'active': True
                    }

                    token_list.insert_one(item_insert)

                    status = 'Insert token thành công: {contract}'.format(
                        contract=item)
                else:
                    status = 'Token không tồn tại: {contract}'.format(
                        contract=item)
            else:
                status = 'Contract đã tồn tại: {contract}'.format(
                    contract=item)

        return status
    except Exception as e:
        logs_data.insert_one({
            'exception': e,
            'function': 'insertToDb'
        })
        status = 'Có lỗi xảy ra. Vui lòng check log'
        return status


def writeLog(function, ex):
    item_insert = {
        'function': function,
        'exception': ex
    }

    logs_data.insert_one(item_insert)


def insertSpeed(contract: str, symbol: str, name: str, network: str):
    objCheck = token_list.find_one(
        {"contract": contract, 'network': network})  # Check Exist DB
    if not objCheck:
        item_insert = {
            'contract': contract,
            'symbol': symbol,
            'name': name,
            'network': network,
            'active': True
        }

        token_list.insert_one(item_insert)

        return 'Insert token thành công: {contract}'.format(
            contract=contract)
    else:
        return 'Contract đã tồn tại: {contract}'.format(
            contract=contract)


def checkUserAdmin(userid):
    userAdmin = user_group.find_one({"user_id": userid})
    return userAdmin['administrator']


def getConfig(key):
    configGet = config_data.find_one({"key": key})
    return configGet['value']

def findTokenWithSymbol(symbol, chain):
    token = token_list.find_one({"symbol": symbol, "network": chain})
    return token