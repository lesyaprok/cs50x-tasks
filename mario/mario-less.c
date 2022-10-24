#include <cs50.h>
#include <stdio.h>

int get_height(void);

int main(void)
{
    int height = get_height();
    int spaces = height - 1;

    //print pyramid
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < spaces; j++)
        {
            //print spaces
            printf(" ");
        }
        for (int k = 0; k < height - spaces; k++)
        {
            //print hashes
            printf("#");
        }
        printf("\n");
        spaces -= 1;
    }
}

int get_height(void)
{
    //get height from user, if 0 < height <= 8 return height, else prompt again.
    int height;
    do
    {
        height = get_int("Height: ");
    }
    while (height < 1 || height > 8);

    return height;
}