#include <cs50.h>
#include <stdio.h>

int get_height(void);

int main(void)
{
    //print pyramide
    int height = get_height();
    int spaces = height - 1;

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < spaces; j++)
        {
            //print spaces
            printf(" ");
        }
        int count = 2;
        while (count)
        {
            //print hashes 2 times with spaces separator
            for (int k = 0; k < height - spaces; k++)
            {
                //print hashes on row
                printf("#");
            }
            if (count == 2)
            {
                printf("  ");
            }
            count--;
        }
        printf("\n");
        spaces--;
    }
}

int get_height(void)
{
    //get height from user
    int height;
    do
    {
        height = get_int("Height: ");
    }
    while (height < 1 || height > 8);
    return height;
}
