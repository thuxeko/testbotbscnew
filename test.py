import dbrun
import checkToken

# symbol = 'shib'
# chain = 'eth'

# token = checkToken.getTokenWithSymbol(symbol, 1, 1, 1, chain)
# print(token)


obj = dbrun.getUserGroup(-533854846)
if obj['active']:
    print('Ok')
else:
    print('Không làm mà đòi có ăn chỉ có ăn đầu buồi ăn cứt')