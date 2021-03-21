from cs50 import get_int

# Mario less
# recreastes the ahlf pyramid using hashes for blocks
# prompt for input, get_int for the half-pyramid's height,
#positive integer between 1 and 8

# if the user fails to provide a positive integer no greater than 8, reprompt for the same again
# reject characters as input
# reject no input

def main():
    a = get_int("Height: ")
    while not (1 < a < 8):
        a = get_int("Height: ")

# using print and lops, generate the desired half pyramid
# align the bottom-left corner of the half-pyramid
# no extra space after each line of the pyramid
    if  (1 < a < 8):
        for i in range (1, a+1):
            print(" "*(a-i) + "#"*i, end="\n")


main ()

