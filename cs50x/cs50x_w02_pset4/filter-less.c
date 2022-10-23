#include <math.h>

#include "helpers.h"

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    // for every row and every column
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // avarage the values from 3 channels
            float avg = (image[i][j].rgbtBlue + image[i][j].rgbtGreen + image[i][j].rgbtRed) / 3.0;
          
            // round it to an integer
            int avgr = round(avg);
          
            // assign the new value to all channels
            image[i][j].rgbtBlue = avgr;
            image[i][j].rgbtGreen = avgr;
            image[i][j].rgbtRed = avgr;
        }
    }
  
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    // for every row and every column
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // calculate sepia formula on each channel
            float sepiaB = (image[i][j].rgbtRed * 0.272) + (image[i][j].rgbtGreen * 0.534) + (image[i][j].rgbtBlue * 0.131);
            float sepiaG = (image[i][j].rgbtRed * 0.349) + (image[i][j].rgbtGreen * 0.686) + (image[i][j].rgbtBlue * 0.168);
            float sepiaR = (image[i][j].rgbtRed * 0.393) + (image[i][j].rgbtGreen * 0.769) + (image[i][j].rgbtBlue * 0.189);
          
            // rounding the floats
            int sepiaBlue = round(sepiaB);
            int sepiaGreen = round(sepiaG);
            int sepiaRed = round(sepiaR);
          
            // cap values at 255
            if (sepiaBlue > 255)
            {
                sepiaBlue = 255;
            }
            if (sepiaGreen > 255)
            {
                sepiaGreen = 255;
            }
            if (sepiaRed > 255)
            {
                sepiaRed = 255;
            }
          
            // assign the new value to all channels
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

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < (width / 2); j++)
        {
            // store temporary values
            int b = image[i][j].rgbtBlue;
            int g = image[i][j].rgbtGreen;
            int r = image[i][j].rgbtRed;
          
            // assign values to pixels (from left side of row) with those of pixels from right side of row
            image[i][j].rgbtBlue = image[i][width - (j + 1)].rgbtBlue;
            image[i][j].rgbtGreen = image[i][width - (j + 1)].rgbtGreen;
            image[i][j].rgbtRed = image[i][width - (j + 1)].rgbtRed;
          
            // assign values to the pixels (from right side of row) with temporary ones
            image[i][width - (j + 1)].rgbtBlue = b;
            image[i][width - (j + 1)].rgbtGreen = g;
            image[i][width - (j + 1)].rgbtRed = r;
        }
    }
  
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    // declare a copy of the image array
    RGBTRIPLE copy[height][width];
  
    // copy contents of image array to copy array
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // each copy pixel has values from the argument pixel array
            copy[i][j].rgbtBlue = image[i][j].rgbtBlue;
            copy[i][j].rgbtGreen = image[i][j].rgbtGreen;
            copy[i][j].rgbtRed = image[i][j].rgbtRed;
        }
    }
  
    // for every pixel in input image apply blurring formula
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // store the sums of all 9 r/g/b values
            int tR = 0;
            int tG = 0;
            int tB = 0;
          
            // number of valid neighbours
            float nei = 0.00;
          
            // for every pixel (in a 9-pixel square) around the current pixel
            for (int k = -1; k < 2; k++)
            {
                for (int l = -1; l < 2; l++)
                {
                    int x = i + k;
                    int y = j + l;
                  
                    // check for corners
                    if (x < 0 || x > (height - 1) || y < 0 || y > (width - 1))
                    {
                        // skip it
                        continue;
                    }
                  
                    // update totals
                    tR += image[x][y].rgbtRed;
                    tG += image[x][y].rgbtGreen;
                    tB += image[x][y].rgbtBlue;
                  
                    // update neighbour counter
                    nei++;
                }
                // assign new valid-pixel values
                copy[i][j].rgbtBlue = round(tB / nei);
                copy[i][j].rgbtGreen = round(tG / nei);
                copy[i][j].rgbtRed = round(tR / nei);
            }
        }
    }
  
    // assigning new pixel values
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j].rgbtBlue = copy[i][j].rgbtBlue;
            image[i][j].rgbtGreen = copy[i][j].rgbtGreen;
            image[i][j].rgbtRed = copy[i][j].rgbtRed;
        }
    }
  
    return;
}
