#include "helpers.h"
#include "math.h"

// Convert image to grayscale

void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for(int i = 0; i < height; i++)
    {
        for(int j = 0; j < width; j++)
        {
            float grey = (image[i][j].rgbtBlue + image[i][j].rgbtGreen + image[i][j].rgbtRed) / 3.00;

            int average = round(grey);
            if (grey >255)
            {
                grey = 255;
            }
            image[i][j].rgbtBlue = average;
            image[i][j].rgbtGreen = average;
            image[i][j].rgbtRed = average;
        }

    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    for(int i = 0; i < height; i++)
    {
        for(int j = 0; j < width; j++)
        {
            int sepiaRed = round(.393 *image[i][j].rgbtRed  + .769 * image[i][j].rgbtGreen + .189 * image[i][j].rgbtBlue);
            int sepiaGreen = round(.349 *image[i][j].rgbtRed  + .686 * image[i][j].rgbtGreen + .168 * image[i][j].rgbtBlue);
            int sepiaBlue = round(.272 *image[i][j].rgbtRed  + .534 * image[i][j].rgbtGreen + .131 * image[i][j].rgbtBlue);
            if (sepiaRed >255)
            {
                sepiaRed = 255;
            }
             if (sepiaGreen >255)
            {
                sepiaGreen=255;
            }
             if (sepiaBlue >255)
            {
                sepiaBlue = 255;
            }
            image[i][j].rgbtBlue = sepiaBlue;
            image[i][j].rgbtGreen = sepiaGreen;
            image[i][j].rgbtRed = sepiaRed;
        }

    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    //use of a temporary array to swap values

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < round(width / 2.00); j++)
        {
            RGBTRIPLE temp[height][width];
            temp[i][j] = image[i][j];


            // swap pixels with the ones on the opposite side of the picture and viceversa
            image[i][j] = image[i][width - j - 1];

            image[i][width - j - 1] = temp[i][j];

        }
    }
    return;
}


// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width]){

    //create a temporary image to calculate blured pixels


    RGBTRIPLE temp[height][width];


    for(int i = 0; i < height; i++)
    {
        for(int j = 0; j < width; j++)
        {
            int sumBlue = 0;
            int sumGreen = 0;
            int sumRed = 0;
            float counter = 0.00;
            // sum pixels around i,j and itself (a total of 4-9), exclude if out of height, width
            for (int k = 0; k < 2; k++)
            {
                if ((i + k) < 0 || (i + k) >= height)
                {
                    continue;
                }


                for (int h = -1; h < 2; h++)
                {
                    if ((j + h) < 0 || (j + h) >= width )
                    {
                        continue;
                    }

                    sumBlue += image[i + k][j + h].rgbtBlue;
                    sumGreen += image[i + k][j + h].rgbtGreen;
                    sumRed += image[i + k][j + h].rgbtRed;
                    counter = counter + 1.00;
                }
            }
            //averaged pixel is saved to the original image
            temp[i][j].rgbtBlue = round(sumBlue / counter);
            temp[i][j].rgbtGreen = round(sumGreen / counter);
            temp[i][j].rgbtRed = round(sumRed / counter);

        }
    }
    //copies temp pixels to original image
    for (int i = 0; i < width; i++)
    {
        for (int j = 0; j < height; j++)
        {
            image[i][j].rgbtBlue = temp[i][j].rgbtBlue;
            image[i][j].rgbtGreen = temp[i][j].rgbtGreen;
            image[i][j].rgbtRed = temp[i][j].rgbtRed;
        }
    }
    return;
}
