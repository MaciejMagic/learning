#include <cs50.h>
#include <stdio.h>
#include <ctype.h>
#include <string.h>
#include <stdlib.h>

int main(int argc, string argv[])
{
    // error message in case of too many arguments
    if (argc > 2)
    {
        printf("Usage: ./substitution key\n");
        return 1;
    }
  
    // error message in case of too few arguments
    if (argc < 2)
    {
        printf("Usage: ./substitution key\n");
        return 1;
    }
  
    // check if key is 26 chars
    if (strlen(argv[1]) != 26)
    {
        printf("Key must contain 26 characters.\n");
        return 1;
    }
  
    // check if each char of argument is case-insensitive alphabetical char
    for (int i = 0; i < 26; i++)
    {
        if (isalpha(argv[1][i]) == 0)
        {
            printf("Key must only contain alphabetic characters.\n");
            return 1;
        }
    }
  
    // check if key is containing each letter exactly once
    char lcheck1[26];
    bool lcheck2[26];
  
    // populate bool array with false values
    for (int m = 0; m < 26; m++)
    {
        // assigning
        lcheck2[m] = false;
    }
  
    // checking if each letter shows only once (uppercase and lowercase)
    for (int n = 0; n < 26; n++)
    {
        // uppercase tracking
        if (isupper(argv[1][n]))
        {
            if (lcheck2[argv[1][n] - 'A'] == true)
            {
                // message for invalid key
                printf("Key must only contain one of each alphabetic characters.\n");
                return 1;
            }
            else
            {
                // if it was false then assign true and populate char array
                lcheck2[argv[1][n] - 'A'] = true;
                lcheck1[n] = argv[1][n] - 'A';
            }
        }
        // lowercase tracking
        else
        {
            if (lcheck2[argv[1][n] - 'a'] == true)
            {
                // message for invalid key
                printf("Key must only contain one of each alphabetic characters.\n");
                return 1;
            }
            else
            {
                // if it was false then assign true and populate char array
                lcheck2[argv[1][n] - 'a'] = true;
                lcheck1[n] = argv[1][n] - 'a';
            }
        }
    }

    // ask user for message to encrypt
    string pt = get_string("plaintext:  ");

    // encrypting
    // length of the string provided by user
    int tl = strlen(pt);
  
    // for every char of that string
    for (int l = 0; l < tl; l++)
    {
        // if its a letter
        if (isalpha(pt[l]))
        {
            // if its an uppercase letter
            if (isupper(pt[l]))
            {
                // assign value from lcheck1 array
                pt[l] = (lcheck1[pt[l] - 'A'] + 'A');
            }
            // is its a lowercase letter
            else
            {
                // assign value from lcheck1 array
                pt[l] = (lcheck1[pt[l] - 'a'] + 'a');
            }
        }
        // if ist not a letter then do nothing to the char
    }
    // show user the encrypted message
    printf("ciphertext: %s\n", pt);
    return 0;
}
