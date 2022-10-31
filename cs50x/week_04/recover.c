#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

typedef uint8_t BYTE;

int main(int argc, char *argv[])
{
    // argument count check
    if (argc != 2)
    {
        printf("Usage: ./recover IMAGE\n");
        return 1;
    }
  
    // open memory card file
    FILE *card = fopen(argv[1], "r");
  
    // file opening error check
    if (card == NULL)
    {
        printf("File cannot be opened.");
        return 2;
    }
  
    // define a block of size 512 bytes
    BYTE buffer[512];
  
    // how many jpgs have we recovered
    int counter = 0;
  
    // file dummy
    FILE *output = NULL;
  
    // memory for filename
    char *name = malloc(8 * sizeof(char));
  
    // iterate through the card file
    while (fread(buffer, sizeof(char), 512, card) == sizeof(buffer))
    {
        // if we detect jpg signature first four bytes
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff)
        {
            // close previous opened file (or not - if its the first one)
            if (counter != 0)
            {
                fclose(output);
            }
          
            // create a filename
            sprintf(name, "%03i.jpg", counter);
          
            // open a new jpg file
            output = fopen(name, "w");
          
            // increase number od detected jpgs
            counter++;
        }

        // write to file if jpg was detected
        if (output != NULL)
        {
            // copy data to a new jpg file
            fwrite(buffer, sizeof(char), 512, output);
        }
    }
  
    // free all memory things
    fclose(output);
    free(name);
    fclose(card);
  
    return 0;
}
