from cs50 import get_string


def main():
    # prompt user for text
    text = get_string("Text: ")
    # calc number of letters
    l = letters(text)
    # calc number of words
    w = words(text)
    # calc number of sentences
    s = sentences(text)
    # calculate text with Coleman-Liau formula
    lf = float(l)
    wf = float(w)
    sf = float(s)
    la = lf / wf * 100
    sa = sf / wf * 100
    cl = (0.0588 * la) - (0.296 * sa) - 15.8
    # round the calculated float value to the nearest integer
    grade = int(round(cl))

    # show calculated grade
    if grade > 15:
        print("Grade 16+")
    elif grade < 1:
        print("Before Grade 1")
    else:
        print("Grade {}".format(grade))


def letters(tl: str) -> int:
    # counting the number of alphabet characters in the input string
    x = 0
    for i in tl:
        # if char is a letter then add 1
        if i.isalpha():
            x += 1
    return x


def words(tw: str) -> int:
    # counting the number of words from 0
    y = 0
    # each space char is a word before it
    for i in tw:
        if i.isspace():
            y += 1
    # add 1 word at end of text (no spaces there)
    y += 1
    return y


def sentences(ts: str) -> int:
    # counting the number of sentences
    z = 0
    for i in ts:
        # every string before a dot, exclamation mark or a question mark is a sentence
        if i == '.' or i == '!' or i == '?':
            z += 1
    return z


main()
