#include <cs50.h>
#include <stdio.h>
#include <math.h>
// minimize numbers of coins

int main(void)
{
    // If the user fails to provide a non-negative value,
    //re-prompt the user for a valid amount again and again until the user complies.
    float n;
    int p = 0;
    int q = 0;
    int r = 0;
    int s = 0;
    int Sum = 0;

    do
    {
        n = get_float("Change owed: ");
    }
    while (n < 0);

//to round your cents to the nearest penny
    int cents = round(n * 100);

//repeat counting coins till all cents were taken account.
//To minimize a number of coins, starts with quarters followed by dimes, nickels and pennies.
    while (cents > 0)
    {
//First, counts quarters (25¢)
        if ((cents - 25) >= 0)
        {
            for (int i = 1; cents > 24; i++)
            {
                (cents = cents - 25);
                p = i;
            }
        }
//Second, counts dimes (10¢)
        else if ((cents - 10) >= 0)
        {
            for (int j = 1; cents > 9; j++)
            {
                (cents = cents - 10);
                q = j;
            }
        }
//Third, counts nickels (5¢)
        else if ((cents - 5) >= 0)
        {
            for (int k = 1; cents > 4; k++)
            {
                (cents = cents - 5);
                r = k;
            }
        }
//Forth, counts pennies (1¢).
        else
        {
            for (int l = 1; cents > 0; l++)
            {
                (cents = cents - 1);
                s = l;
            }
        }
    }
//Sum up all coins
    Sum = (p + q + r + s);
    printf("%i\n", Sum);

}