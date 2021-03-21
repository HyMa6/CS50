#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <stdint.h>

int main(int argc, char *argv[])
{
    //checking if there are two arguments
    if (argc != 2)
    {
        printf("Enter 2 arg\n");
        return 1;
    }

    // Opening the raw file
    FILE *file = fopen(argv[1], "r");

    // Checking if the file can be opened
    if (file == NULL)
    {
        printf("File could not be opened %s.\n", argv[1]);
        return 1;
    }

    // read, write and close
    uint8_t buffer[512];
    FILE *img = NULL;
    char title[8];
    int count = 0;


    while (true)
    {
        // reading a block of the memory card image
        size_t Block_Read = fread(buffer, sizeof(uint8_t), 512, file);

        // breaking out of the loop when reaching the end of the card
        if (Block_Read == 0 && feof(file))
        {
            break;
        }

        // Checking if the header of the buffer has jpg the first three bytes
        bool JpgHeader = buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0;

        // Closing the jpg file since a new jpg file starts
        if (JpgHeader && img != NULL)
        {
            fclose(img);
            count++;
        }

        // Opening a new jpg file
        if (JpgHeader)
        {

            sprintf(title, "%03i.jpg", count);
            img = fopen(title, "w");
        }

        if (img != NULL)
        {
            // Writing on the img file
            fwrite(buffer, sizeof(uint8_t), 512, img);
        }

    }

    // Closing files
    fclose(img);
    fclose(file);
}