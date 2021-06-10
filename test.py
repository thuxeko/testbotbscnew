import dbrun
import checkToken
import utils
import json
import cloudscraper

symbol = '0x0E8D5504bF54D9E44260f8d153EcD5412130CaBb'
chain = 'bsc'

# token = checkToken.getTokenWithSymbol(symbol, 1, 1, 1, chain)
# print(token)

# token = utils.checkToken(symbol, chain)
# print(token)
url = "https://api.dex.guru/v1/tokens/{contract}?network={network}"
scraper = cloudscraper.create_scraper()
for x in range(5):
    print(x)
#   res = scraper.get(url.format(
#         contract=symbol.lower(), network=chain))
#   if res.status_code == 200:
#         print(json.loads(res.text))
#         break
