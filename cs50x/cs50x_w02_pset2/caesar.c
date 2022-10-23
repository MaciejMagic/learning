#include <cs50.h>
#include <stdio.h>
#include <ctype.h>
#include <string.h>
#include <stdlib.h>

bool only_digits(string s);
char cipher(char ch, int ik);
char cipheru(char chu, int iku);

int key;

int main(int argc, string argv[])
{
    if (argc > 2)
    {
        // error message in case of wrong command-line argument - too many arguments
        printf("Usage: ./caesar key\n");
        return 1;
    }
    else if (argc < 2)
    {
        // error message in case of wrong command-line argument - too few arguments
        printf("Usage: ./caesar key\n");
        return 1;
    }
  
    // check if key provided is made of digits
    bool dc = only_digits(argv[1]);
  
    if (dc == false)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }
  
    // convert string provided by user to integer
    key = atoi(argv[1]);
  
    // ask user for message to encrypt
    string pt = get_string("plaintext:  ");
  
    // encrypting
    int tl = strlen(pt);
  
    for (int l = 0; l < tl; l++)
    {
        if (islower(pt[l]))
        {
            // if its a lowercase letter then its a ciphered lowercase letter now
            pt[l] = cipheru(pt[l], key);
        }
        else if (isupper(pt[l]))
        {
            // if its a uppercase letter then its a ciphered uppercase letter now
            pt[l] = cipher(pt[l], key);
        }
        // if ist not a letter then do nothing to the char
    }
    // show user the encrypted message
    printf("ciphertext: %s\n", pt);
  
    return 0;
}

bool only_digits(string s)
{
    int kl = strlen(s);
  
    for (int i = 0; i < kl; i++)
    {
        if (isdigit(s[i]) == 0)
        {
            // error message in case of wrong command-line argument - non-digit
            printf("Usage: ./caesar key\n");
            return false;
        }
    }
  
    return true;
}

char cipher(char ch, int ik)
{
    // ascii char 'A' is 65
    char ch1 = ch - 65;
    char ch2 = (ch1 + ik) % 26;
    char ch3 = ch2 + 65;
  
    return ch3;
}

char cipheru(char chu, int iku)
{
    // ascii char 'a' is 97
    char chu1 = chu - 97;
    char chu2 = (chu1 + iku) % 26;
    char chu3 = chu2 + 97;
  
    return chu3;
}
