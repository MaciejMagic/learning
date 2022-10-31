#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <math.h>

int grade_text(string t);
int letters(string tl);
int words(string tw);
int sentences(string ts);

int main(void)
{
    // prompt user for text
    string text = get_string("Text: ");
  
    // calc number of letters
    int l = letters(text);
  
    // calc number of words
    int w = words(text);
  
    // calc number of sentences
    int s = sentences(text);
  
    // calculate text with Coleman-Liau formula
    float lf = l;
    float wf = w;
    float sf = s;
    float la = lf / wf * 100;
    float sa = sf / wf * 100;
    float cl = (0.0588 * la) - (0.296 * sa) - 15.8;
  
    // round the calculated float value to the nearest integer
    int grade = round(cl);
  
    // show calculated grade
    if (grade > 15)
    {
        printf("Grade 16+\n");
    }
    else if (grade < 1)
    {
        printf("Before Grade 1\n");
    }
    else
    {
        printf("Grade %i\n", grade);
    }
}

int letters(string tl)
{
    // counting the number of alphabet chars in the input string
    int x = 0;
    int jl = strlen(tl);
  
    for (int il = 0; il < jl; il++)
    {
        // if char is a letter then add 1
        if (isalpha(tl[il]))
        {
            x++;
        }
    }
    return x;
}

int words(string tw)
{
    // counting the number of words from 0
    int y = 0;
    int jw = strlen(tw);
  
    // each space char is a word before it
    for (int iw = 0; iw < jw; iw++)
    {
        if (isspace(tw[iw]))
        {
            y++;
        }
    }
  
    // add 1 word at end of text (no spaces there)
    y++;
    return y;
}

int sentences(string ts)
{
    // counting the number of sentences
    int z = 0;
    int js = strlen(ts);
  
    for (int is = 0; is < js; is++)
    {
        // every string before a dot, exclamation mark or a question mark is a sentence
        if (ts[is] == '.')
        {
            z++;
        }
        else if (ts[is] == '!')
        {
            z++;
        }
        else if (ts[is] == '?')
        {
            z++;
        }
    }
    return z;
}
