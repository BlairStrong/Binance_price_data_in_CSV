from funcs import get_price_history

#Get list of prices information
#add items to get price history for to the list below. Make sure you follow the exact same format.
symbol_list = ["BTCUSDT", "ETHUSDT", "SOLUSDT"]
for symbol in symbol_list:
    get_price_history(symbol,"1h")