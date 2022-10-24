#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <math.h>

int count_letters(string text);
int count_words(string text);
int count_sentences(string text);

int main(void)
{
    // print as output "Grade X" where X is the grade level computed by the Coleman-Liau formula
    // if the resulting index number is 16 or higher, should output "Grade 16+"
    // if the index number is less than 1, should output "Before Grade 1"
    
    string text = get_string("Text: ");

    int sentences = count_sentences(text);
    int words = count_words(text);
    int letters = count_letters(text);

    // L is the average number of letters per 100 words in the text,
    // S is the average number of sentences per 100 words in the text.
    const float L = (float) letters / words * 100;
    const float S = (float) sentences / words * 100;
    int index = round(0.0588 * L - 0.296 * S - 15.8);

    if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (index >= 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %i\n", index);
    }
}

int count_letters(string text)
{
    //count letters in text
    int letters = 0;
    for (int i = 0; i < strlen(text); i++)
    {
        if (isalnum(text[i]))
        {
            letters += 1;
        }
    }
    return letters;
}

int count_words(string text)
{
    //count words in text
    if (strlen(text) == 0)
    {
        return 0;
    }
    int words = 1;
    for (int i = 0; i < strlen(text); i++)
    {
        if (isspace(text[i]))
        {
            words += 1;
        }
    }
    return words;
}

int count_sentences(string text)
{
    //count sentences
    int sentences = 0;
    for (int i = 0; i < strlen(text); i++)
    {
        if (text[i] == '.' || text[i] == '!' || text[i] == '?')
        {
            sentences += 1;
        }
    }
    return sentences;
}
