import dbrun
import utils
import models
import requests
from lxml import etree
from bs4 import BeautifulSoup
import json
import re


def getTokenWithSymbol(symbol: str, typeCm, username, userid, chain):
    tokenRes = dbrun.findTokenWithSymbol(symbol, chain)
    urlChart = urlBuy = ''
    try:
        if tokenRes is not None:
            if typeCm == 1:
                getDetailsToken = utils.checkToken(tokenRes['contract'], chain)

                if getDetailsToken:
                    # String Link swap & Chart
                    if chain == 'bsc':
                        urlChart = '<a href="{link}">💩_PooChart_💩</a>'.format(
                            link='https://poocoin.app/tokens/{contract}'.format(contract=tokenRes['contract']))
                        urlBuy = '<a href="{linkPc}">🥞_PancakeSwap_🥞</a>'.format(
                            linkPc='https://exchange.pancakeswap.finance/#/swap?inputCurrency={contract}'.format(contract=tokenRes['contract']))
                    elif chain == 'eth':
                        urlChart = '<a href="{link}">📈_DexGuru_📈</a>'.format(
                            link='https://dex.guru/token/{contract}-eth'.format(contract=tokenRes['contract']))
                        urlBuy = '<a href="{linkPc}">🦄_UniSwap_🦄</a>'.format(
                            linkPc='https://app.uniswap.org/#/swap?outputCurrency={contract}'.format(contract=tokenRes['contract']))

                    # String Text
                    token_symbol = 'Token: ' + \
                        tokenRes['name'] + ' - ' + tokenRes['symbol']

                    symbol_usd = '1 {symbol} = {priceusd} USD'.format(
                        symbol=tokenRes['symbol'], priceusd=str(format(getDetailsToken['priceUSD'], '.14f')))

                    symbol_bnb = '1 {symbol} = {pricebnb} BNB/ETH'.format(
                        symbol=tokenRes['symbol'], pricebnb=str(format(getDetailsToken['priceETH'], '.14f')))

                    totalin1usd = str(1 / getDetailsToken['priceUSD'])
                    totalin1bnb = str(1 / getDetailsToken['priceETH'])
                    usd_symbol = '1 USD = {total} {symbol}'.format(
                        symbol=tokenRes['symbol'], total=totalin1usd)
                    bnb_symbol = '1 BNB/ETH = {total} {symbol}'.format(
                        symbol=tokenRes['symbol'], total=totalin1bnb)

                    donate = 'Ủng hộ cha làm bot ly ☕\nBNB-Bep20|ETH: 0x441949e9F37A84A0E080Cc6E58247dEE9668D160'

                    strOut = '<a href="tg://user?id={id_user}">Gửi sếp {user}</a> \n{namesymbol} \n{priceusd} \n{pricebnb} \n \n{total1usd} \n{total1bnb} \n \n{buyl} \n{chart} \n{dnt}'.format(
                        namesymbol=token_symbol, priceusd=symbol_usd, pricebnb=symbol_bnb, symbol=tokenRes['symbol'], buyl=urlBuy, chart=urlChart, total1usd=usd_symbol, total1bnb=bnb_symbol, user=username, id_user=userid, dnt=donate)

                    return strOut
                else:
                    return "Không thể truy vấn được Token"
            elif typeCm == 2:
                return tokenRes['contract']
        else:
            return "Token không tồn tại"
    except Exception as e:
        print(str(e))
        dbrun.writeLog('getTokenWithSymbol', str(e))


def crawlWithContract(contract: str):
    try:
        data = []
        # Check contract
        reqCheck = requests.get(
            'https://api.bscscan.com/api?module=contract&action=getabi&address={ct}&apikey=APK1BUUFYPH8ECC5EIJVCD6F464WFN3Y2S'.format(ct=contract))
        stt = json.loads(reqCheck.text)

        if stt['status'] == '0':
            print('Check lai contract')
            return 'Có lỗi xảy ra. Liên hệ dev'
        else:
            req = requests.get(
                'https://bscscan.com/token/{ct}#balances'.format(ct=contract))
            soup = BeautifulSoup(req.content, "html.parser")
            dom = etree.HTML(str(soup))

            tokenName = dom.xpath(
                '/html/body/div[1]/main/div[4]/div[1]/div[1]/div/div[2]/div[2]/div[2]/b')[0].text
            totalSup = dom.xpath(
                '//*[@id="ContentPlaceHolder1_divSummary"]/div[1]/div[1]/div/div[2]/div[2]/div[2]/span[1]')[0].text
            totalHolder = dom.xpath(
                '//*[@id="ContentPlaceHolder1_tr_tokenHolders"]/div/div[2]/div/div')[0].text

            # Get Total Supply
            reqTs = requests.get(
                'https://api.bscscan.com/api?module=stats&action=tokensupply&contractaddress={ct}&apikey=APK1BUUFYPH8ECC5EIJVCD6F464WFN3Y2S'.format(ct=contract))
            ttSupply = json.loads(reqTs.text)
            if ttSupply['status'] == '0':
                print('API BSC co van de')
                return 'Có lỗi xảy ra. Liên hệ dev'
            else:
                req = requests.get(
                    'https://bscscan.com/token/generic-tokenholders2?m=normal&a={ct}&s={sup}&p=1'.format(ct=contract, sup=ttSupply['result']))
                soup = BeautifulSoup(req.text, "html.parser")
                tbFind = soup.find(
                    "table", attrs={'class': 'table table-md-text-normal table-hover'})
                table_body = tbFind.find('tbody')
                rows = table_body.find_all('tr')

                getTop = [l for l in rows[:20]] if len(rows) > 20 else rows
                for row in getTop:
                    holder = models.Holder()
                    cols = row.find_all('td')
                    # Check Lock
                    checkLock = cols[1].find(
                        'i', attrs={'class': 'far fa-file-alt text-secondary'})
                    holder.lock = False if not checkLock else True

                    # Other
                    holder.name = cols[1].text.strip()
                    holder.linkaddress = 'https://bscscan.com' + \
                        cols[1].find("a")["href"]
                    holder.quantity = cols[2].text.strip()
                    holder.percentage = cols[3].text.strip()

                    data.append(holder)

                # Check Burn
                findBurn = [x for x in data if x.name == 'Burn Address']
                burnQuantity = f'{findBurn[0].quantity} ({findBurn[0].percentage})' if findBurn else '0 (0%)'

                # Find top holder without other wallet
                walletFind = [x for x in data if re.search('0x', x.name)][:5]
                topHolder = ''
                for wl in walletFind:
                    checkLock = '🔒' if wl.lock else ''
                    text_out = f'\n<a href="{wl.linkaddress}">Address</a> | {wl.quantity} | {wl.percentage} {checkLock}'
                    topHolder += text_out

                return 'Token Symbol: {symbol}\nHolder: {ttHolder}\nTổng Burn: {burnTotal}\nTotal Supply: {ttSup}\nTop 5 Holder:\n{holder}'.format(
                    symbol=tokenName, ttHolder=str(totalHolder).replace("addresses", "").strip(), ttSup=totalSup, burnTotal=burnQuantity, holder=topHolder)
    except Exception as e:
        print(str(e))
        dbrun.writeLog('crawlWithContract', str(e))