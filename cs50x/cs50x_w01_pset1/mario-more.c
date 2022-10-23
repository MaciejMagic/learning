#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int n;
  
    do
    {
        // Prompt user for size
        n = get_int("How tall should the towers be?: ");
    }
    while (n < 1 || n > 8);

    // For each row
    for (int i = 0; i < n; i++)
    {
        // For each column
        for (int j = 1; j < n; j++)
        {
            // fork here
            if (i + j >= n)
            {
                // Print a brick
                printf("#");
            }
            else
            {
                // Print a blank space
                printf(" ");
            }
        }
        printf("#");
        printf(" ");
        printf(" ");
        printf("#");
      
        for (int k = 0; k < n; k++)
        {
            if (i > k)
            {
                // Print a brick
                printf("#");
            }
        }
        printf("\n");
    }
}
