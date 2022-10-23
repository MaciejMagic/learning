#include <ctype.h>
#include <cs50.h>
#include <stdio.h>
#include <string.h>

// Points assigned to each letter of the alphabet
int POINTS[] = {1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10};

int compute_score(string word);

int main(void)
{
    // Get input words from both players
    string word1 = get_string("Player 1: ");
    string word2 = get_string("Player 2: ");

    // Score both words
    int score1 = compute_score(word1);
    int score2 = compute_score(word2);

    // Print the winner
    if (score1 > score2)
    {
        printf("Player 1 wins!\n");
    }
    else if (score1 < score2)
    {
        printf("Player 2 wins!\n");
    }
    else
    {
        printf("Tie!\n");
    }
}

int compute_score(string word)
{
    // compute and return score for string
    int result = 0;
  
    // do this check for every char of the string user provided
    for (int i = 0, n = strlen(word); i < n; i++)
    {
        // check if each char of the string provided is a lowercase or uppercase letter
        if (isupper(word[i]))
        {
            // add point value of the letter to the sum of all letters
            result += POINTS[word[i] - 'A'];
        }
        else if (islower(word[i]))
        {
            // add point value of the letter to the sum of all letters
            result += POINTS[word[i] - 'a'];
        }
    }
  
    // add all points from letters
    return result;
}
