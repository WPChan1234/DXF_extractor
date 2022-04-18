import math

def round_half_up(n, decimals=0):
    multiplier = 10 ** decimals
    return math.floor(n*multiplier + 0.5) / multiplier

print(round_half_up(3.25,1))

print(round_half_up(3.245,1))