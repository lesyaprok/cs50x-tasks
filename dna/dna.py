import csv
import sys


def main():

    # TODO: Check for command-line usage
    if len(sys.argv) != 3:
        sys.exit("Usage: python dna.py data.csv sequence.txt")
    data = sys.argv[1]
    sequence = sys.argv[2]

    # TODO: Read database file into a variable
    database = []
    try:
        with open(data, "r") as data_file:
            reader = csv.DictReader(data_file)
            STRS = reader.fieldnames[1:]
            for row in reader:
                database.append(row)
    except FileNotFoundError:
        sys.exit("Usage: python dna.py data.csv sequence.txt")

    # TODO: Read DNA sequence file into a variable
    try:
        with open(sequence, "r") as sequence_file:
            DNA_sequence = sequence_file.read()
    except FileNotFoundError:
        sys.exit("Usage: python dna.py data.csv sequence.txt")

    # TODO: Find longest match of each STR in DNA sequence
    counts = {}
    for str in STRS:
        longest = longest_match(DNA_sequence, str)
        counts[str] = longest

    # TODO: Check database for matching profiles
    is_found = False
    for i in database:
        for key in counts:
            if int(i[key]) != counts[key]:
                is_found = False
                break
            else:
                is_found = True
        if is_found:
            print(i["name"])
            return
    print("No match")
    return


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
