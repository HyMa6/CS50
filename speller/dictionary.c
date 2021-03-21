// Implements a dictionary's functionality

#include <stdbool.h>
#include <stdlib.h>
#include <math.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <strings.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Number of buckets in hash table
const unsigned int N = 2999;
// from testing, over 3000 does not change time. Each list has about 143000/3000 = 48 nodes

// Hash table
node *table[N];
int NumberofWords=0;


// Returns true if word is in dictionary else false
bool check(const char *word)
{
    // TODO
    node *tmp= table [hash(word)];
    while (tmp != NULL)
    {
        if (strcasecmp(word, tmp -> word) == 0)
        {
            return true;
        }
        tmp = tmp ->next;

    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // TODO
    //input character or apostrophes
    //output numerical index between 0- N-1
    //determiinistic

    // the Rabin-Karp rolling hash function from web

    int a = 99;
    // random number from testing

    long HashValue = 0;

    // The hash function loop each letter within a word
    for (int i = 0, j = strlen(word); i < j; i++)
    {
        //converting each letter to lowercase
        HashValue += (tolower(word[i]) * pow(a, j - i));
    }

    //return HashValue;
    //unknown reason, final ind can be negative, so return it to absolute value
    return labs(HashValue % N);

}


// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    // TODO
    // Opening the raw file
    FILE *dict = fopen(dictionary, "r");

    // Checking if the file is empty
    if (dict == NULL)
    {
        return false;
    }

    //read strings from file one at a time

    node *currentNode, *tmp;

    int hashedNumber, i;
    char tmpword[(LENGTH + 1)];

    for (i = fscanf(dict, "%s", tmpword); i != EOF; i = fscanf(dict, "%s", tmpword))
    {
        NumberofWords ++;

    // hash function, fuction takes string and returns an index

        hashedNumber = hash(tmpword);
    //create a new node for each word
        tmp = malloc(sizeof(node));

        strcpy(tmp -> word, tmpword);
        tmp-> next = NULL ;



    //insert node into hash table at that location

        if (table[hashedNumber] == NULL)
        {
            table[hashedNumber] = tmp;
        }

        else
        {

            currentNode = table [hashedNumber];
            while (currentNode -> next != NULL)
            {
                currentNode = currentNode -> next;
            }
            currentNode -> next = tmp;
        }
    }

    //  closing the dict file
    fclose(dict);

    if (i == EOF)
    {
        return true;
    }
    return false;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    // TODO

    return NumberofWords;

}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    // TODO
    // go through buckets in the hash table
    for (int i = 0;  i < N; i++)
    {
        if (table[i] != NULL)
        {

            node *cursor= table [i];
            node *tmp = table [i];

            // use two nodes in order to free all memories
            while (cursor != NULL)
            {
                cursor = cursor -> next;
                free(tmp);
                tmp = cursor;
            }
        }
    }
    return true;
}

