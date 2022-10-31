#include <cs50.h>
#include <stdio.h>
#include <string.h>

// Max voters and candidates
#define MAX_VOTERS 100
#define MAX_CANDIDATES 9

// preferences[i][j] is jth preference for voter i
int preferences[MAX_VOTERS][MAX_CANDIDATES];

// Candidates have name, vote count, eliminated status
typedef struct
{
    string name;
    int votes;
    bool eliminated;
}
candidate;

// Array of candidates
candidate candidates[MAX_CANDIDATES];

// Numbers of voters and candidates
int voter_count;
int candidate_count;

// Function prototypes
bool vote(int voter, int rank, string name);
void tabulate(void);
bool print_winner(void);
int find_min(void);
bool is_tie(int min);
void eliminate(int min);

int main(int argc, string argv[])
{
    // Check for invalid usage
    if (argc < 2)
    {
        printf("Usage: runoff [candidate ...]\n");
        return 1;
    }

    // Populate array of candidates
    candidate_count = argc - 1;
  
    if (candidate_count > MAX_CANDIDATES)
    {
        printf("Maximum number of candidates is %i\n", MAX_CANDIDATES);
        return 2;
    }
  
    for (int i = 0; i < candidate_count; i++)
    {
        candidates[i].name = argv[i + 1];
        candidates[i].votes = 0;
        candidates[i].eliminated = false;
    }

    voter_count = get_int("Number of voters: ");
    if (voter_count > MAX_VOTERS)
    {
        printf("Maximum number of voters is %i\n", MAX_VOTERS);
        return 3;
    }

    // Keep querying for votes
    for (int i = 0; i < voter_count; i++)
    {

        // Query for each rank
        for (int j = 0; j < candidate_count; j++)
        {
            string name = get_string("Rank %i: ", j + 1);

            // Record vote, unless it's invalid
            if (!vote(i, j, name))
            {
                printf("Invalid vote.\n");
                return 4;
            }
        }

        printf("\n");
    }

    // Keep holding runoffs until winner exists
    while (true)
    {
        // Calculate votes given remaining candidates
        tabulate();

        // Check if election has been won
        bool won = print_winner();
        if (won)
        {
            break;
        }

        // Eliminate last-place candidates
        int min = find_min();
        bool tie = is_tie(min);

        // If tie, everyone wins
        if (tie)
        {
            for (int i = 0; i < candidate_count; i++)
            {
                if (!candidates[i].eliminated)
                {
                    printf("%s\n", candidates[i].name);
                }
            }
            break;
        }

        // Eliminate anyone with minimum number of votes
        eliminate(min);

        // Reset vote counts back to zero
        for (int i = 0; i < candidate_count; i++)
        {
            candidates[i].votes = 0;
        }
    }
  
    return 0;
}

// Record preference if vote is valid
bool vote(int voter, int rank, string name)
{
    for (int i = 0; i < candidate_count; i++)
    {
        if (strcmp(candidates[i].name, name) == 0)
        {
            // if name check passes, then update this field in preferences array with voted name (represented as a number)
            preferences[voter][rank] = i;
            return true;
        }
    }
  
    return false;
}

// Tabulate votes for non-eliminated candidates
void tabulate(void)
{
    // update the number of votes each candidate has at this stage in the runoff
    // every voter votes for their top non-eliminated candidate
  
    // for every voter
    for (int i = 0; i < voter_count; i++)
    {
        // and for every rank
        for (int j = 0; j < candidate_count; j++)
        {
            // if that candidate has not been eliminated
            int c = preferences[i][j];
            if (candidates[c].eliminated == false)
            {
                // add 1 vote
                candidates[c].votes++;
                break;
            }
        }
    }
  
    return;
}

// Print the winner of the election, if there is one
bool print_winner(void)
{
    // temporary coverting voter_count int into a float (for division calc)
    float tmp = voter_count;

    // for every candidate check if his vote count is higher then half of voters
    for (int i = 0; i < candidate_count; i++)
    {
        if (candidates[i].votes > (tmp / 2))
        {
            // if yes then the winner is chosen and printed
            printf("%s\n", candidates[i].name);
            return true;
        }
    }
  
    return false;
}

// Return the minimum number of votes any remaining candidate has
int find_min(void)
{
    // keeping track of the smallest vote
    int x = voter_count + 1;
  
    // for every candidate
    for (int i = 0; i < candidate_count; i++)
    {
        // if he is still in the election
        if (!candidates[i].eliminated)
        {
            // if it has the lowest nr of votes
            if (candidates[i].votes < x)
            {
                // record it
                x = candidates[i].votes;
            }
        }
    }
  
    // return the value recorded
    if (x > 0)
    {
        return x;
    }
    else
    {
        return 0;
    }
}

// Return true if the election is tied between all candidates, false otherwise
bool is_tie(int min)
{
    // keeping track
    int x = 0;
    int y = 0;
  
    // how many current candidates have minimum votes
    for (int i = 0; i < candidate_count; i++)
    {
        // if he is still in the election
        if (!candidates[i].eliminated && candidates[i].votes == min)
        {
            x++;
        }
    }
  
    // how many candidates are still running
    for (int j = 0; j < candidate_count; j++)
    {
        // if he is still in the election
        if (!candidates[j].eliminated)
        {
            y++;
        }
    }
  
    // if its the same amount then its a tie
    if (x == y)
    {
        return true;
    }
    else
    {
        return false;
    }
}

// Eliminate the candidate (or candidates) in last place
void eliminate(int min)
{
    // for every candidate
    for (int i = 0; i < candidate_count; i++)
    {
        // if he is still in the election and his vote total is lowest
        if (!candidates[i].eliminated && candidates[i].votes == min)
        {
            candidates[i].eliminated = true;
        }
    }
  
    return;
}
