#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>

bool is_valid_key(string key);
char transform_char(char c, string key);
void cipher_text(string text, string key);

int main(int argc, string argv[])
{
    // if a user provides too many/ no command-line argument at all, program should remind the user how to use the program
    // if a user doesn’t provide a valid key, the program should explain with an error message

    if (argc != 2)
    {
        printf("Usage: ./substitution key\n");
        return 1;
    }
    else if (!is_valid_key(argv[1]))
    {
        printf("Key must contain 26 unique characters.\n");
        return 1;
    }

    string key = argv[1];
    //get user's input
    string text = get_string("plaintext: ");
    
    //cipher input and print it
    cipher_text(text, key);
}

bool is_valid_key(string key)
{
    //if not valid key, return false, else true. The valid key consists of 26 unique alpha-characters.

    if (strlen(key) != 26)
    {
        return false;
    }
    // make hash for checking unique characters
    int hash[26] = {0};

    for (int i = 0; i < strlen(key); i++)
    {
        if (!isalpha(key[i]))
        {
            return false;
        }
        //if character is already in hash return false
        else if (hash[((int) toupper(key[i])) - 65] >= 1)
        {
            return false;
        }
        //add character to hash
        hash[((int) toupper(key[i])) - 65] = 1;
    }
    return true;
}

char transform_char(char c, string key)
{
    //cipher character with key and return transformed character

    if (isalpha(c) && islower(c))
    {
        return tolower(key[c - 97]);
    }
    else if (isalpha(c) && isupper(c))
    {
        return toupper(key[c - 65]);
    }
    else
    {
        return c;
    }
}

void cipher_text(string text, string key)
{
    printf("ciphertext: ");
    for (int i = 0; i < strlen(text); i++)
    {
        printf("%c", transform_char(text[i], key));
    }
    printf("\n");
}
