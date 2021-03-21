#a program that first asks the user to type in some text, and then outputs the grade level for the text, according to the Coleman-Liau formula

#the Coleman-Liau index is computed as 0.0588 * L - 0.296 * S - 15.8, where L is the average number of letters per 100 words in the text, and S is the average number of sentences per 100 words in the text.


def main():
    # input as text
    text = input ("Type the text: ")


  # initialising the values
    words = 1
    letters = 0
    sentences = 0

    # Checking
    for i in text:
        if i == " ":
            words += 1
        elif i == "." or i == "!" or i == "?":
            sentences += 1
        elif i.isalpha():
            letters += 1

    L = letters / words * 100
    S = sentences / words * 100
    index = round (0.0588 * L - 0.296 * S - 15.8)

    if index < 1:
        print("Before Grade 1")

    elif index > 16:
        print("Grade 16+")

    else:
        print("Grade", index)


main()

