from cs50 import get_float


# asks the user how much change is owed and then spits out the minimum number of coins with which said change can be made.
def main():
    owed = get_input()
    print(get_number_of_coins(owed))


# get user input, if the user fails to provide a non-negative value, should re-prompt the user for a valid amount
def get_input():
    while True:
        owed = get_float("Change owed: ")
        if (owed < 0):
            continue
        return owed


# calculates the minimum number of coins required to give a user change
def get_number_of_coins(owed):
    coins = [0.25, 0.10, 0.05, 0.01]
    number_of_coins = 0
    index = 0

    while (owed):
        count = round(owed - coins[index], 2)
        if (count >= 0):
            number_of_coins += 1
            owed = count
        else:
            index += 1
    return number_of_coins


if __name__ == "__main__":
    main()
