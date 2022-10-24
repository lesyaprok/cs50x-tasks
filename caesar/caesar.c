#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>

bool is_numeric(string arg);
char transform_char(char c, int key);
void cipher_text(string text, int key);

int main(int argc, string argv[])
{
    // program must accept a single command-line argument, a non-negative integer
    if (argc != 2 || !is_numeric(argv[1]))
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }

    int key = atoi(argv[1]) % 26;
    
    // get user input, transform and print it
    string text = get_string("plaintext: ");
    cipher_text(text, key);

}

bool is_numeric(string arg)
{
    //check is the argument consists of only digits
    for (int i = 0; i < strlen(arg); i++)
    {
        if (!isdigit(arg[i]))
        {
            return false;
        }
    }
    return true;
}

char transform_char(char c, int key)
{
    //transform character to the specified number of positions (key)

    if (isalpha(c) && islower(c))
    {
        //if alpha && lowercase
        if ((c + key) > 122)
        {
            return (char)(97 + (c + key) % 123);
        }
        else
        {
            return (char)(c + key);
        }
    }
    else if (isalpha(c) && isupper(c))
    {
        //if alpha && uppercase
        if ((c + key) > 90)
        {
            return (char)(65 + (c + key) % 91);
        }
        else
        {
            return (char)(c + key);
        }
    }
    else
    {
        //if non-alpha, return character
        return c;
    }
}

void cipher_text(string text, int key)
{
    //cipher text and print it
    printf("ciphertext: ");
    for (int i = 0; i < strlen(text); i++)
    {
        printf("%c", transform_char(text[i], key));
    }
    printf("\n");
}
