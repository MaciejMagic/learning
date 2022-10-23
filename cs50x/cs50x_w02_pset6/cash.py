from cs50 import get_float


def main():
    # Ask how many cents the customer is owed in dollars x.xx
    change = get_change()
    change *= 100

    # Calculate the number of quarters to give the customer
    quarters = calculate_quarters(change)
    change = change - quarters * 25

    # Calculate the number of dimes to give the customer
    dimes = calculate_dimes(change)
    change = change - dimes * 10

    # Calculate the number of nickels to give the customer
    nickels = calculate_nickels(change)
    change = change - nickels * 5

    # Calculate the number of pennies to give the customer
    pennies = calculate_pennies(change)
    change = change - pennies * 1

    # Sum coins
    coins = quarters + dimes + nickels + pennies
    coins = int(coins)

    # Print total number of coins to give the customer
    print("{}".format(coins))


def get_change():
    while True:
        c = get_float("How much change?: ")
        if c > 0:
            break
    return c


def calculate_quarters(change):
    q = change / 25
    q = int(q)
    return q


def calculate_dimes(change):
    d = change / 10
    d = int(d)
    return d


def calculate_nickels(change):
    n = change / 5
    n = int(n)
    return n


def calculate_pennies(change):
    p = change / 1
    p = int(p)
    return p


main()
