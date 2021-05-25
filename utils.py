import json
import requests
from pycoingecko import CoinGeckoAPI
import cloudscraper
import dbrun

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

# region Check ETH Gas
def checkGasEth():
    # Get Price ETH
    cg = CoinGeckoAPI()
    get_price = cg.get_price(ids='ethereum', vs_currencies='usd')
    price_eth = get_price['ethereum']['usd']

    # Read Config
    gasTransfer = dbrun.getConfig('gaslimit_transfer')
    gasSwap = dbrun.getConfig('gaslimit_uniswap')

    # Get Gwei
    api_key = dbrun.getConfig('api_key_etherscan')
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


def readConfigJson():
    with open('config.json', 'r') as dl_file:
        data = json.load(dl_file)
        return data


def checkToken(contract, network):
    url = "https://api.dex.guru/v1/tokens/{contract}-{network}"
    scraper = cloudscraper.create_scraper()
    res = scraper.get(url.format(
        contract=contract, network=network))
    if res.status_code == 200:
        return json.loads(res.text)
    else:
        return False
