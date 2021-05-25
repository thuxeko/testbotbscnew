import dbrun
import utils


def getTokenWithSymbol(symbol: str, typeCm, username, userid, chain):
    tokenRes = dbrun.findTokenWithSymbol(symbol, chain)
    try:
        if tokenRes is not None:
            if typeCm == 1:
                getDetailsToken = utils.checkToken(tokenRes['contract'], chain)

                if getDetailsToken:
                    # String Link PancakeSwap & Poocoin Chart
                    pooChart = '<a href="{link}">💩_PooChart_💩</a>'.format(
                        link='https://poocoin.app/tokens/{contract}'.format(contract=tokenRes['contract']))
                    pancakeLink = '<a href="{linkPc}">🥞_Buy Token_🥞</a>'.format(
                        linkPc='https://exchange.pancakeswap.finance/#/swap?inputCurrency={contract}'.format(contract=tokenRes['contract']))

                    # String Text
                    token_symbol = 'Token: ' + \
                        tokenRes['name'] + ' - ' + tokenRes['symbol']

                    symbol_usd = '1 {symbol} = {priceusd} USD'.format(
                        symbol=tokenRes['symbol'], priceusd=str(format(getDetailsToken['priceUSD'], '.14f')))

                    symbol_bnb = '1 {symbol} = {pricebnb} BNB'.format(
                        symbol=tokenRes['symbol'], pricebnb=str(format(getDetailsToken['priceETH'], '.14f')))

                    totalin1usd = str(
                        1/format(getDetailsToken['priceUSD'], '.14f'))
                    totalin1bnb = str(
                        1/format(getDetailsToken['priceETH'], '.14f'))
                    usd_symbol = '1 USD = {total} {symbol}'.format(
                        symbol=tokenRes['symbol'], total=totalin1usd)
                    bnb_symbol = '1 BNB = {total} {symbol}'.format(
                        symbol=tokenRes['symbol'], total=totalin1bnb)

                    donate = 'Ủng hộ cha làm bot ly ☕\nBNB-Bep20|ETH: 0x441949e9F37A84A0E080Cc6E58247dEE9668D160'

                    strOut = '<a href="tg://user?id={id_user}">Gửi sếp {user}</a> \n{namesymbol} \n{priceusd} \n{pricebnb} \n \n{total1usd} \n{total1bnb} \n \n{pancake} \n{poo} \n{dnt}'.format(
                        namesymbol=token_symbol, priceusd=symbol_usd, pricebnb=symbol_bnb, symbol=tokenRes['symbol'], pancake=pancakeLink, poo=pooChart, total1usd=usd_symbol, total1bnb=bnb_symbol, user=username, id_user=userid, dnt=donate)

                    return strOut
                else:
                    return "Không thể truy vấn được Token"
            elif typeCm == 2:
                return tokenRes['contract']
        else:
            return "Token không tồn tại"
    except Exception as e:
        dbrun.writeLog('getTokenWithSymbol', e)