def main():
    text = input("Text: ")
    sentences = count_sentences(text)
    words = count_words(text)
    letters = count_letters(text)

    L = letters / words * 100
    S = sentences / words * 100
    index = round(0.0588 * L - 0.296 * S - 15.8)

    if (index < 1):
        print("Before Grade 1")
    elif (index >= 16):
        print("Grade 16+")
    else:
        print(f"Grade {index}")


# count letters in text
def count_letters(text):
    letters = 0
    for i in text:
        if (i.isalnum()):
            letters += 1
    return letters


# count words in text
def count_words(text):
    return len(text.split(" "))


# count sentences
def count_sentences(text):
    signs = (".", "!", "?")
    sentences = 0

    for i in text:
        if i in signs:
            sentences += 1
    return sentences


if __name__ == "__main__":
    main()
