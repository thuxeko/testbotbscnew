import dbrun
import checkToken

symbol = 'shib'
chain = 'eth'

token = checkToken.getTokenWithSymbol(symbol, 1, 1, 1, chain)
print(token)
