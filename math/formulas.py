def ema(prices): #Расчет экспоненциальной скользящей средней (EMA)
    N = len(prices)
    weight = 2 / (N + 1)
    ema = prices[0]
    for price in prices[1:]:
        ema = (price * weight) + (ema * (1 - weight))
    return ema

def rsi(prices): #Индекс относительной силы (14) RSI
    N = len(prices)
    grows = [0] * N
    falls = [0] * N
    for i in range(N-1):
        if prices[i] < prices[i+1]:
            falls[i] = 0
            grows[i] = (prices[i+1] - prices[i])
        else:
            grows[i] = 0
            falls[i] = (prices[i] - prices[i+1])
    ema_grow = ema(grows)
    ema_fall = ema(falls)
    rs = ema_grow / ema_fall
    rsi = 100 - (100 / (1 + rs))
    return rsi

# prices = [15, 11, 10]
# print(f"Экспоненциальная скользящая средняя (EMA): {ema(prices):.2f} ₽")

# prices = [1000, 1010, 950]
# print(f"Индекс относительной силы (14) RSI: {rsi(prices):.2f}")