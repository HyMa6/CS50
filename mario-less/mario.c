#include <cs50.h>
#include <stdio.h>
// Creating right-aligned pyramid of blocks based on the user input.
// User input determins high of the pyramid which must be between 1 and 8, inclusive.

int main(void)
{
    int n;
    do
    {
        n = get_int("Width: ");
    }
    while (n > 8 || n < 1);

    for (int i = 1; i <= n; i++)
    {
        for (int k = (n - i - 1); k >= 0; k--)
        {
            printf(" ");
        }
        for (int k = 1; k <= i; k++)
        {
            printf("#");
        }

        printf("\n");
    }
}