#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    int fcolor;
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            fcolor = ((image[i][j].rgbtBlue + image[i][j].rgbtGreen + image[i][j].rgbtRed) / 3);
            image[i][j].rgbtBlue = fcolor;
            image[i][j].rgbtGreen = fcolor;
            image[i][j].rgbtRed = fcolor;
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE oimage[height][width];

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
           oimage[i][j] = image[i][j];
        }
   }
   int sepiaRed, sepiaBlue, sepiaGreen;
   for (int i = 0; i < height; i++)
   {
       for (int j = 0; j < width; j++)
       {
           sepiaRed = round(.393 * oimage[i][j].rgbtRed + .769 * oimage[i][j].rgbtGreen + .189 * oimage[i][j].rgbtBlue);
           sepiaBlue = round(.272 * oimage[i][j].rgbtRed + .534 * oimage[i][j].rgbtGreen + .131 * oimage[i][j].rgbtBlue);
           sepiaGreen = round(.349 * oimage[i][j].rgbtRed + .686 * oimage[i][j].rgbtGreen + .168 * oimage[i][j].rgbtBlue);
           image[i][j].rgbtRed = sepiaRed > 255 ? 255 : sepiaRed;
           image[i][j].rgbtGreen = sepiaGreen > 255 ? 255 : sepiaGreen;
           image[i][j].rgbtBlue = sepiaBlue > 255 ? 255 : sepiaBlue;
       }
   }
   return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    int start, end;
    RGBTRIPLE temp;
    for (int i = 0; i < height; i++)
    {
       start = 0, end = width - 1;
        while (start < end)
        {
            temp = image[i][start];
            image[i][start] = image[i][end];
            image[i][end] = temp;
            start++;
            end--;
        }
    }
    return;
}

// Blur image
/*void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE oimage[height][width];
 for (int i = 0; i < height; i++)
 {
 for (int j = 0; j < width; j++)
 {
 oimage[i][j] = image[i][j];
 }
 }
 for (int i = 0; i < height; i++)
 {
 for (int j = 0; j < width; j++)
 {
 if (i == 0 && j == 0)
 {
 image[i][j].rgbtRed = round((oimage[i][j].rgbtRed + oimage[i + 1][j].rgbtRed
 + oimage[i][j + 1].rgbtRed + oimage[i + 1][j + 1].rgbtRed) / 4.0);
 image[i][j].rgbtGreen = round((oimage[i][j].rgbtGreen + oimage[i + 1][j].rgbtGreen
 + oimage[i][j + 1].rgbtGreen + oimage[i + 1][j + 1].rgbtGreen) / 4.0);
 }
 }}
    return;
}*/
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE ogImage[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            ogImage[i][j] = image[i][j];
        }
    }

    for (int i = 0, red, green, blue, counter; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            red = green = blue = counter = 0;

            if (i >= 0 && j >= 0)
            {
                red += ogImage[i][j].rgbtRed;
                green += ogImage[i][j].rgbtGreen;
                blue += ogImage[i][j].rgbtBlue;
                counter++;
            }
            if (i >= 0 && j - 1 >= 0)
            {
                red += ogImage[i][j - 1].rgbtRed;
                green += ogImage[i][j - 1].rgbtGreen;
                blue += ogImage[i][j - 1].rgbtBlue;
                counter++;
            }
            if ((i >= 0 && j + 1 >= 0) && (i >= 0 && j + 1 < width))
            {
                red += ogImage[i][j + 1].rgbtRed;
                green += ogImage[i][j + 1].rgbtGreen;
                blue += ogImage[i][j + 1].rgbtBlue;
                counter++;
            }
            if (i - 1 >= 0 && j >= 0)
            {
                red += ogImage[i-1][j].rgbtRed;
                green += ogImage[i-1][j].rgbtGreen;
                blue += ogImage[i-1][j].rgbtBlue;
                counter++;
            }
            if (i - 1 >= 0 && j - 1 >= 0)
            {
                red += ogImage[i - 1][j - 1].rgbtRed;
                green += ogImage[i - 1][j - 1].rgbtGreen;
                blue += ogImage[i - 1][j - 1].rgbtBlue;
                counter++;
            }
            if ((i - 1 >= 0 && j + 1 >= 0) && (i - 1 >= 0 && j + 1 < width))
            {
                red += ogImage[i - 1][j + 1].rgbtRed;
                green += ogImage[i - 1][j + 1].rgbtGreen;
                blue += ogImage[i - 1][j + 1].rgbtBlue;
                counter++;
            }
            if ((i + 1 >= 0 && j >= 0) && (i + 1 < height && j >= 0))
            {
                red += ogImage[i + 1][j].rgbtRed;
                green += ogImage[i + 1][j].rgbtGreen;
                blue += ogImage[i + 1][j].rgbtBlue;
                counter++;
            }
            if ((i + 1 >= 0 && j - 1 >= 0) && (i + 1 < height && j - 1 >= 0))
            {
                red += ogImage[i + 1][j - 1].rgbtRed;
                green += ogImage[i + 1][j - 1].rgbtGreen;
                blue += ogImage[i + 1][j - 1].rgbtBlue;
                counter++;
            }
            if ((i + 1 >= 0 && j + 1 >= 0) && (i + 1 < height && j + 1 < width))
            {
                red += ogImage[i + 1][j + 1].rgbtRed;
                green += ogImage[i + 1][j + 1].rgbtGreen;
                blue += ogImage[i + 1][j + 1].rgbtBlue;
                counter++;
            }

            image[i][j].rgbtRed = round(red / (counter * 1.0));
            image[i][j].rgbtGreen = round(green / (counter * 1.0));
            image[i][j].rgbtBlue = round(blue / (counter * 1.0));
        }
    }

    return;
}