def triangular(x, a, b, c):
    if x <= a or x >= c:
        return 0
    elif x == b:
        return 1
    elif x < b:
        return (x - a) / (b - a)
    else:
        return (c - x) / (c - b)


# temperature = 78

# high = triangular(temperature,60,80,100)
# print(high);

for temperature in [60, 65, 70, 75, 80, 85, 90, 95, 100]:
    high = triangular(temperature, 60, 80, 100)
    print(temperature, "->", high)