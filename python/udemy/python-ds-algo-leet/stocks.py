def get_top_stocks(stocks, prices):
    averages = []
    map = {} 
    for i in range(len(stocks)):
        total = 0
        for j in range(len(prices)):
            total += prices[j][i] 
        average = total / len(prices)
        averages.append(average)
        map[average] = stocks[i]
    
    averages.sort(reverse=True)
    return [map[averages[0]], map[averages[1]], map[averages[2]]]


stocks = ['TESLA', 'PEPSI', 'GOOGLE', 'APPLE', 'NVIDIA', 'MICROSOFT']
prices = [[18.34, 11.10, 15.11, 10.93, 9.83, 16.14], [18.21, 10.35, 15.52, 10.36, 8.14, 16.21]]

print(get_top_stocks(stocks, prices))
