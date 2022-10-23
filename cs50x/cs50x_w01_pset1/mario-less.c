#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int n;
  
    // checking for valid input
    do
    {
        // Prompt user for size of the pyramid
        n = get_int("How many steps should the pyramid have?: ");
    }
    while (n < 1 || n > 8);
  
    // For each row
    for (int i = 1; i < n + 1; i++)
    {
        // inverse pyramid of spaces
        for (int j = n; j > i; j--)
        {
            // show blank space
            printf(" ");
        }
      
        // pyramid of hashes
        for (int k = 0; k < i; k++)
        {
            // show hash
            printf("#");
        }
      
        // Move to next row
        printf("\n");
    }
}
