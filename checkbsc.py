import requests
import json


def getTokenWithSymbol(symbol, typeCm):
    urlRequest = 'https://api.pancakeswap.info/api/tokens'
    data = requests.get(urlRequest)
    res = json.loads(data.text.encode('utf8').decode('utf8'))
    resValues = res['data'].values()
    filterValues = list(filter(
        lambda value: value['symbol'].upper() == symbol.upper(), list(resValues)))

    if(len(filterValues) > 0):
        # Get Contract
        contractToken = list(res['data'].keys())[
            list(resValues).index(filterValues[0])]

        if typeCm == 1:
            # String Link PancakeSwap & Poocoin Chart
            pooChart = '<a href="{link}">💩_PooChart_💩</a>'.format(
                link='https://poocoin.app/tokens/{contract}'.format(contract=contractToken))
            pancakeLink = '<a href="{linkPc}">🥞_Buy Token_🥞</a>'.format(
                linkPc='https://exchange.pancakeswap.finance/#/swap?inputCurrency={contract}'.format(contract=contractToken))

            # String Text
            token_symbol = 'Token: ' + \
                filterValues[0]['name'] + ' - ' + filterValues[0]['symbol']

            symbol_usd = '1 {symbol} = {priceusd} USD'.format(
                symbol=filterValues[0]['symbol'], priceusd=filterValues[0]['price'][:filterValues[0]['price'].index('.') + 14])

            symbol_bnb = '1 {symbol} = {pricebnb} BNB'.format(
                symbol=filterValues[0]['symbol'], pricebnb=filterValues[0]['price_BNB'][:filterValues[0]['price_BNB'].index('.') + 14])

            totalin1usd = str(1/(float(filterValues[0]['price'])))
            totalin1bnb = str(1/(float(filterValues[0]['price_BNB'])))
            usd_symbol = '1 USD = {total} {symbol}'.format(
                symbol=filterValues[0]['symbol'], total=totalin1usd)
            bnb_symbol = '1 BNB = {total} {symbol}'.format(
                symbol=filterValues[0]['symbol'], total=totalin1bnb)

            strOut = '{namesymbol} \n{priceusd} \n{pricebnb} \n \n{total1usd} \n{total1bnb} \n \n{pancake} \n{poo}'.format(
                namesymbol=token_symbol, priceusd=symbol_usd, pricebnb=symbol_bnb, symbol=filterValues[0]['symbol'], pancake=pancakeLink, poo=pooChart, total1usd=usd_symbol, total1bnb=bnb_symbol)

            return strOut
        elif typeCm == 2:
            return contractToken

    else:
        return "Token không tồn tại"
