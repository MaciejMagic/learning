#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // prompt the user for card number
    long nm = get_long("Card number: ");

    // check for length
    int i = 0;
    long nmc = nm;
    while (nmc > 0)
    {
        nmc = nmc / 10;
        i++;
    }


    // check for legit card length and starting digits
    if (i != 13 && i != 15 && i != 16)
    {
        printf("INVALID\n");
        return 0;
    }

    // checksum:
    // storing the sums for addition
    int sum1 = 0;
    int sum2 = 0;
    // creditcard number copy for digit extraction
    long chk = nm;
    // last digit
    int ld;
    // second to last digit
    int stld;
    // and its two digits..
    int stld1;
    int stld2;
    // loop - extracting the digits and adding to the sum
    do
    {
        // last digit
        ld = chk % 10;
        // adding to sum1
        sum1 += ld;
        // second to last digit
        chk /= 10;
        stld = chk % 10;
        // multiply second to last digit by 2
        stld *= 2;
        // extracting digits from the previous one multiplied by 2
        stld1 = stld / 10;
        stld2 = stld % 10;
        // adding to sum2
        sum2 = sum2 + stld1 + stld2;
        // to the next numbers
        chk /= 10;
    }
    while (chk > 0);

    // both sum1 and sum2
    int sums = sum1 + sum2;

    // checking for the last digit of the total sums to be zero
    if (sums % 10 != 0)
    {
        printf("INVALID\n");
        return 0;
    }

    // extracting first two digits of cc number
    long ftdc = nm;
    do
    {
        ftdc /= 10;
    }
    while (ftdc > 100);

    // checking for card type from the first two digits
    if ((ftdc / 10 == 3) && (ftdc % 10 == 4 || ftdc % 10 == 7))
    {
        printf("AMEX\n");
    }
    else if ((ftdc / 10 == 5) && (ftdc % 10 < 6 && ftdc % 10 > 0))
    {
        printf("MASTERCARD\n");
    }
    else if (ftdc / 10 == 4)
    {
        printf("VISA\n");
    }
    else
    {
        printf("INVALID\n");
        return 0;
    }
}
