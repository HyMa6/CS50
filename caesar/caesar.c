#include <stdlib.h>
#include <cs50.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>
#include <stdio.h>
#include <math.h>

int main(int argc, string argv[])
{
    //to check if two arg
    if (argc != 2)
    {
        printf("Did you remember to type argv?\n");
        return 1;
    }


    string key = argv[1];

    //to check if key is number. If not, return 1
    for (int i = 0, n = strlen(key); i < n; i++)
    {
        if (!(isalnum(key[i]) && !isalpha(key[i])))
        {
            return 1;
        }
    }

    // put key into an int k
    int k = atoi(argv[1]);


    string plaintext = get_string("plain text: ");

    printf("ciphertext: ");
    for (int i = 0, n = strlen(plaintext); i < n; i++)
    {
        //check is input is lower case, then convert to lowercase ifmmp
        if (islower(plaintext[i]))
        {
            //consider number of alpha 26
            int j = k % 26;
            //z is 122
            if (((int)(plaintext[i]) + j) <= 122)
            {
                printf("%c", plaintext[i] + j);
            }
            else
            {

                printf("%c", plaintext[i] + j - 26);
            }
        }
        //check if input is uppercase, then convert to uppercase ciphertext
        else if (isupper(plaintext[i]))
        {
            int j = k % 26;
            //consider Z is 90
            if (((int)(plaintext[i]) + j) <= 90)
            {
                printf("%c", plaintext[i] + j);
            }
            else
            {

                printf("%c", plaintext[i] + j - 26);
            }
        }
        //if input char is other than alpha, then do not convert to ciphertext
        else
        {
            printf("%c", plaintext[i]);
        }
    }
    printf("\n");
}