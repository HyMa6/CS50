# first asks the user how much change is owed and then spits out the minimum number of coins with which said change can be made

from cs50 import get_float

def main():

    dollor = get_float("What is change? ")

#If the user fails to provide a non-negative value, your program should re-prompt the user for a valid amount again and again until the user complies.
    while (dollor < 0):
        dollor = get_float("What is change? ")

    cents = int (dollor * 100)
#program’s last line of output be only the minimum number of coins possible: an integer followed by a newline.

    total = 0

    div = [25, 10, 5, 1]
    for i in div:
        total += cents //i
        cents %= i
    print (total)



main()