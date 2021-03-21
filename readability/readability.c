#include <stdio.h>
#include <ctype.h>
#include <cs50.h>
#include <math.h>
#include <string.h>

int count_letters(string s);
int count_words(string s);
int count_sentences(string s);


int main(void)
{
    int index;
    float L, S;
    L = S = index = 0;
    string text = get_string("Text: ");
    //printf ("%i letters(s)\n", count_letters(text));
    //printf ("%i words(s)\n", count_words(text));
    //printf ("%i sentences(s)\n", count_sentences(text));
    L = (float)count_letters(text) / count_words(text) * 100;
    S = (float)count_sentences(text) / count_words(text) * 100;
    //printf ("%f\n", L);
    //printf ("%f\n", S);
    //printf ("%f\n", 0.0588 * L - 0.296 * S - 15.8);
    //printf ("%f\n", round(0.0588 * L - 0.296 * S - 15.8));
    index = (int)round(0.0588 * L - 0.296 * S - 15.8);
    //printf ("%i\n", index);
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


int count_letters(string s)
{
    int l = 0;

    while (*s)                  //while not the nul-character
        if (isalpha(*s++))     // check if current is letter
        {
            l++;
        }
    return l;
}

int count_words(string s)
{
    int w = 1;                  // words is one more than a number of space

    while (*s)                  //while not the nul-character
    {
        if (isspace(*s++))     // check if current is space
        {
            w++;
        }
    }
    return w;
}

int count_sentences(string s)
{
    int sen = 0;
    for (int i = 0; i < strlen(s); i++)
    {
       if (s[i] == '.' || s[i] == '!' || s[i] == '?')
       {
           sen++;
       }
    }
    return sen;
}
