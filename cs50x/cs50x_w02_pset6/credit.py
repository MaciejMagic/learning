from cs50 import get_int


def main():
    # prompt the user for card number
    nm = get_int("Card number: ")

    # check for length
    i = len(str(nm))

    # check for legit card length and starting digits
    if i != 13 and i != 15 and i != 16:
        print("INVALID")
        return 0

    # checksum:
    # storing the sums for addition
    sum1 = 0
    sum2 = 0
    # dummy cc number for extraction
    chk = int(nm)

    # loop - extracting the digits and adding to the sum
    while True:
        # last digit
        ld = chk % 10
        # adding to sum1
        sum1 += ld
        # second to last digit
        chk = int(chk / 10)
        stld = chk % 10
        # multiply second to last digit by 2
        stld *= 2
        # extracting digits from the previous one multiplied by 2
        stld1 = int(stld / 10)
        stld2 = stld % 10
        # adding to sum2
        sum2 = sum2 + stld1 + stld2
        # to the next numbers
        chk = int(chk / 10)
        if chk <= 0:
            break

    # both sum1 and sum2
    sums = int(sum1 + sum2)

    # checking for the last digit of the total sums to be zero
    if sums % 10 != 0:
        print("INVALID")
        return 0

    # extracting first two digits of cc number
    ftdc = nm

    while True:
        ftdc = int(ftdc / 10)
        if ftdc < 100:
            break

    # checking for card type from the first two digits
    if (int(ftdc / 10) == 3) and (ftdc % 10 == 4 or ftdc % 10 == 7):
        print("AMEX")
    elif (int(ftdc / 10) == 5) and (ftdc % 10 < 6 and ftdc % 10 > 0):
        print("MASTERCARD")
    elif int(ftdc / 10) == 4:
        print("VISA")
    else:
        print("INVALID")
        return 0


main()
