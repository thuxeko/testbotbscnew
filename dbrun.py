from pymongo import MongoClient
import requests
from pycoingecko import CoinGeckoAPI
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
                    'active': True if item_json['chat']['type'] == 'private' else False
                }
                user_group.insert_one(item_insert)
                print('Insert user thành công')
            else:
                print('Bỏ qua bản ghi tồn tại')
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

                    print('Insert token thành công')
                else:
                    print('Token không tồn tại')
            else:
                print('Contract đã tồn tại')
    except Exception as e:
        print(e)
        # logs_data.insert_one({
        #     'exception': e,
        #     'function': 'insertToDb'
        # })
        print('Có lỗi xảy ra. Vui lòng check log')


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

def getUserGroup(chatid):
    userGroup = user_group.find_one({"chat_id": chatid})
    return userGroup


def getConfig(key):
    configGet = config_data.find_one({"key": key})
    return configGet['value']


def findTokenWithSymbol(symbol, chain):
    token = token_list.aggregate([
        {
            '$project':
            {
                'symbol': {'$toUpper': "$symbol"},
                'contract': {'$toString': '$contract'},
                'network': {'$toString': '$network'},
                'active': {'$toBool': '$active'},
                'name': {'$toString': '$name'}
            }
        },
        {
            '$match': {'symbol':  symbol.upper(), 'network': chain}
        },
        {"$limit": 1}
    ])
    return next(token, None)


# region Check ETH Gas
def checkGasEth():
    # Get Price ETH
    cg = CoinGeckoAPI()
    get_price = cg.get_price(ids='ethereum', vs_currencies='usd')
    price_eth = get_price['ethereum']['usd']

    # Read Config
    gasTransfer = getConfig('gaslimit_transfer')
    gasSwap = getConfig('gaslimit_uniswap')

    # Get Gwei
    api_key = getConfig('api_key_etherscan')
    api_gas = 'https://api.etherscan.io/api?module=gastracker&action=gasoracle&apikey=' + \
        str(api_key)

    check_gas = requests.get(api_gas)
    res = json.loads(check_gas.text.encode('utf8').decode('utf8'))

    if res['status'] == '1':
        # Fast
        txFast = calculatorPrice(gasTransfer, int(
            res['result']['FastGasPrice']), price_eth)
        txFastSwap = calculatorPrice(gasSwap, int(
            res['result']['FastGasPrice']), price_eth)

        txt_fast = 'Tốc độ ✈️: {fast} - Chuyển: {fasttfeth} ETH | {fasttffiat} $ - Swap: {fastsweth} ETH | {fastswfiat} $'.format(
            fast=res['result']['FastGasPrice'], fasttfeth=txFast['txEth'], fasttffiat=txFast['txFiat'], fastsweth=txFastSwap['txEth'], fastswfiat=txFastSwap['txFiat'])

        # Medium
        txMedium = calculatorPrice(gasTransfer, int(
            res['result']['ProposeGasPrice']), price_eth)
        txMediumSwap = calculatorPrice(gasSwap, int(
            res['result']['ProposeGasPrice']), price_eth)

        txt_medium = 'Tốc độ 🚘: {medium} - Chuyển: {mediumtfeth} ETH | {mediumtffiat} $ - Swap: {mediumsweth} ETH | {mediumswfiat} $'.format(
            medium=res['result']['ProposeGasPrice'], mediumtfeth=txMedium['txEth'], mediumtffiat=txMedium['txFiat'], mediumsweth=txMediumSwap['txEth'], mediumswfiat=txMediumSwap['txFiat'])

        # Low
        txLow = calculatorPrice(gasTransfer, int(
            res['result']['SafeGasPrice']), price_eth)
        txLowSwap = calculatorPrice(gasSwap, int(
            res['result']['SafeGasPrice']), price_eth)

        txt_low = 'Tốc độ 🚴‍: {low} - Chuyển: {lowtfeth} ETH | {lowtffiat} $ - Swap: {lowsweth} ETH | {lowswfiat} $'.format(
            low=res['result']['SafeGasPrice'], lowtfeth=txLow['txEth'], lowtffiat=txLow['txFiat'], lowsweth=txLowSwap['txEth'], lowswfiat=txLowSwap['txFiat'])

        text_out = 'Tỷ giá ETH: {ethprice}$\n\n{fast}\n{medium}\n{low}'.format(
            ethprice=price_eth, fast=txt_fast, medium=txt_medium, low=txt_low)

        return text_out
    else:
        return 'Lỗi rồi sếp ơi :(('


def calculatorPrice(gaslimit, gwei, ethprice):
    calEth = gaslimit/1e9 * gwei
    calFiat = calEth * ethprice

    objRes = {
        'txEth': format(calEth, '.7f'),
        'txFiat': format(calFiat, '.5f')
    }

    return objRes
# endregion
