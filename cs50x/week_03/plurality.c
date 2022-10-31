#include <cs50.h>
#include <stdio.h>
#include <string.h>

// Max number of candidates
#define MAX 9

// Candidates have name and vote count
typedef struct
{
    string name;
    int votes;
}
candidate;

// Array of candidates
candidate candidates[MAX];

// Number of candidates
int candidate_count;

// Function prototypes
bool vote(string name);
void print_winner(void);

int main(int argc, string argv[])
{
    // Check for invalid usage
    if (argc < 2)
    {
        printf("Usage: plurality [candidate ...]\n");
        return 1;
    }

    // Populate array of candidates
    candidate_count = argc - 1;
  
    if (candidate_count > MAX)
    {
        printf("Maximum number of candidates is %i\n", MAX);
        return 2;
    }

    for (int i = 0; i < candidate_count; i++)
    {
        candidates[i].name = argv[i + 1];
        candidates[i].votes = 0;
    }

    int voter_count = get_int("Number of voters: ");

    // Loop over all voters
    for (int i = 0; i < voter_count; i++)
    {
        string name = get_string("Vote: ");

        // Check for invalid vote or add vote to the total of each candidate
        if (!vote(name))
        {
            printf("Invalid vote.\n");
        }
    }

    // Display winner of election
    print_winner();
}

// Update vote totals given a new vote
bool vote(string name)
{
    // if its correct then add 1 vote to the candidate array and return true
    for (int j = 0; j < candidate_count; j++)
    {
        if (strcmp(candidates[j].name, name) == 0)
        {
            // add 1 to vote count for that candidate
            candidates[j].votes += 1;
            return true;
        }
    }
  
    return false;
}

// Print the winner (or winners) of the election
void print_winner(void)
{
    // searching for highest value
    int win = 0;
  
    // for every candidate assign new value to win, if higher
    for (int l = 0; l < candidate_count; l++)
    {
        if (candidates[l].votes > win)
        {
            win = candidates[l].votes;
        }
    }
  
    // iterate for every candidate again. if equal to highest then print
    for (int m = 0; m < candidate_count; m++)
    {
        if (candidates[m].votes == win)
        {
            printf("%s\n", candidates[m].name);
        }
    }
  
    return;
}
