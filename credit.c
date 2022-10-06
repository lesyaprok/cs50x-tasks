#include <cs50.h>
#include <stdio.h>
#include <string.h>

int validate_card(long);
string check_card(long);

int main(void)
{
    //get card number from user, validate it and print result
    long card_number = get_long("Card number: ");
    string card_name = check_card(card_number);

    if (strcmp(card_name, "INVALID\n") == 0)
    {
        printf("%s", card_name);
    }
    else if (validate_card(card_number) == 1)
    {
        printf("%s", card_name);
    }
    else
    {
        printf("INVALID\n");
    }
}

string check_card(long card_number)
{
    //is it visa (number starts with 4; 13 or 16 digits)
    int check_13_digits_visa = card_number / 1000000000000;
    int check_16_digits_visa = card_number / 1000000000000000;
    int check_15_digits_amex = card_number / 10000000000000;
    int check_16_digits_master = card_number / 100000000000000;

    if (check_13_digits_visa == 4 || check_16_digits_visa == 4)
    {
        return "VISA\n";
    }
    //is it american express (starts with 34 or 37; 15 digits)
    if (check_15_digits_amex == 34 || check_15_digits_amex == 37)
    {
        return "AMEX\n";
    }
    //is it master card (starts with 51, 52, 53, 54, 55; 16 digits)
    else if (check_16_digits_master >= 51 && check_16_digits_master <= 55)
    {
        return "MASTERCARD\n";
    }
    else
    {
        return "INVALID\n";
    }
}

int validate_card(long card_number)
{
    //validate card
    int sum_of_digits = 0;
    int i = 0;

    while (card_number)
    {
        if (i % 2 == 0)
        {
            //digits that weren’t multiplied by 2
            sum_of_digits += card_number % 10;
        }
        else
        {
            //multiply every other digit by 2, starting with the number’s second-to-last digit
            //then add those products’ digits together.
            int product = card_number % 10 * 2;
            while (product)
            {
                sum_of_digits += product % 10;
                product /= 10;
            }
        }
        card_number /= 10;
        i++;
    }
    //if the total’s last digit is 0, the number is valid
    return sum_of_digits % 10 == 0 ? 1 : 0;
}
