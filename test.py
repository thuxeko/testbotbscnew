import requests
from lxml import etree
from bs4 import BeautifulSoup
import json


class Holder:
    def __init__(self, name='', linkaddress='', quantity='', percentage='', lock=False, burn=False):
        self.name = name
        self.linkaddress = linkaddress
        self.quantity = quantity
        self.percentage = percentage
        self.lock = lock
        self.burn = burn


data = []

contract = '0xa6537a67f1ac1f58022c3ac3b1facf3469b268db'
# Check contract
reqCheck = requests.get(
    'https://api.bscscan.com/api?module=contract&action=getabi&address={ct}&apikey=APK1BUUFYPH8ECC5EIJVCD6F464WFN3Y2S'.format(ct=contract))
stt = json.loads(reqCheck.text)

if stt['status'] == '0':
    print('Check lại contract')
else:
    req = requests.get(
        'https://bscscan.com/token/{ct}#balances'.format(ct=contract))
    soup = BeautifulSoup(req.content, "html.parser")
    dom = etree.HTML(str(soup))

    tokenName = dom.xpath(
        '/html/body/div[1]/main/div[4]/div[1]/div[1]/div/div[2]/div[2]/div[2]/b')[0].text
    totalSup = dom.xpath(
        '//*[@id="ContentPlaceHolder1_divSummary"]/div[1]/div[1]/div/div[2]/div[2]/div[2]/span[1]')[0].text

    # Get Total Supply
    reqTs = requests.get(
        'https://api.bscscan.com/api?module=stats&action=tokensupply&contractaddress={ct}&apikey=APK1BUUFYPH8ECC5EIJVCD6F464WFN3Y2S'.format(ct=contract))
    ttSupply = json.loads(reqTs.text)
    if ttSupply['status'] == '0':
        print('API BSC có vấn đề')
    else:
        req = requests.get(
            'https://bscscan.com/token/generic-tokenholders2?m=normal&a={ct}&s={sup}&p=1'.format(ct=contract, sup=ttSupply['result']))
        soup = BeautifulSoup(req.text, "html.parser")
        tbFind = soup.find(
            "table", attrs={'class': 'table table-md-text-normal table-hover'})
        table_body = tbFind.find('tbody')
        rows = table_body.find_all('tr')
        getTop5 = [l for l in rows[:5]]
        for row in getTop5:
            holder = Holder()
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
            # data.append(json.dumps(holder.__dict__))

        # print(json.dumps(data))

        for hd in data:
            print(hd.name)