import requests
import json

import checkbsc

x = input('Symbol: ')
y = input('Type: ')

strOut = checkbsc.getTokenWithSymbol(x, int(y))

print(strOut)