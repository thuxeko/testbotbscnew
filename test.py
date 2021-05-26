import dbrun
import checkToken

symbol = 'nst'
chain = 'bsc'

token = checkToken.getTokenWithSymbol(symbol, 1, 1, 1, chain)
print(token)
