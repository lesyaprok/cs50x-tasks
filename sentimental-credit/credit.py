def main():
    card_number = input("Card number: ")
    card_name = check_card(card_number)

    if (card_name == "INVALID"):
        print(card_name)
    elif (validate_card(card_number)):
        print(card_name)
    else:
        print("INVALID")


def check_card(card_number):
    length = len(card_number)
    first_digits = int(card_number[0] + card_number[1])

    # is it visa (number starts with 4; 13 or 16 digits)
    if card_number[0] == "4" and (length == 13 or length == 16):
        return "VISA"

    # is it american express (starts with 34 or 37; 15 digits)
    elif length == 15 and (first_digits == 34 or first_digits == 37):
        return "AMEX"

    # is it master card (starts with 51, 52, 53, 54, 55; 16 digits)
    elif length == 16 and 51 <= first_digits <= 55:
        return "MASTERCARD"
    else:
        return "INVALID"


# validate card
def validate_card(card_number):
    card_number = int(card_number)
    sum_of_digits = 0
    i = 0

    while (card_number):
        if (i % 2 == 0):
            # digits that weren’t multiplied by 2
            sum_of_digits += card_number % 10
        else:
            # multiply every other digit by 2, starting with the number’s second-to-last digit
            # then add those products’ digits together.
            product = card_number % 10 * 2
            while (product):
                sum_of_digits += product % 10
                product //= 10
        card_number //= 10
        i += 1

    # if the total’s last digit is 0, the number is valid
    return sum_of_digits % 10 == 0


if __name__ == "__main__":
    main()
