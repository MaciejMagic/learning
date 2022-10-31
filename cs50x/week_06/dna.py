import csv
import sys


def main():

    # Check for command-line usage
    if len(sys.argv) != 3:
        # Invalid number of command-line arguments
        print("Usage: python dna.py data.csv sequence.txt")
        return 1

    # Read database file into a variable
    # create a list of dictionaries
    suspects = []
    # open file
    with open(sys.argv[1], "r") as file:
        # read csv data
        reader = csv.DictReader(file)
        # cast into an int type
        for name in reader:
            # add to list
            suspects.append(name)

    # Read DNA sequence file into a variable
    with open(sys.argv[2], "r") as file:
        # store string from file into a variable
        seq = str(file.read())

    # Find longest match of each STR in DNA sequence
    # create a list with dna subsequences / extract from suspects list, butt from second
    strs = list(suspects[0].keys())[1:]
    # create empty dict to store read values from txt file
    counts = {}
    # count longest runs
    for ss in strs:
        sslm = longest_match(seq, ss)
        counts[ss] = sslm

    # Check database for matching profiles
    # iterate over list of dicts
    for g in suspects:
        matching = 0
        # count matching substrings
        for gg in strs:
            if int(g[gg]) == int(counts[gg]):
                matching += 1
        # print suspects name
        if matching == len(strs):
            print("{}".format(g["name"]))
            return
    print("No match")


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()
