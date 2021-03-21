# open the csv file and DNA sequence, read contents into memory

import csv
import sys

# CSV file: NAME and STR number

def main():

    File = open (sys.argv[1], "r")
    database = csv.reader(File)
    data = []
    People = {}

    for rows in database:
        data.append(rows)
    #print(data)

    # STRs list for matching to sequence
    STRs = data[0][1:]
    #print(STRs)

    # Storing the  person's dna as key and name as value
    for i in data[1:]:
        uniqueN = ",".join(i[1:])
        People[uniqueN] = i[0]

    #print(People)


    file = open(sys.argv[2], "r")
    sequence = file.read()
    sequence_list = [sequence]
    # print(sequence)

# for each STR, compute the longest run of consecutive repeats in the DNA sequence
    n = []
    NofSTRinSequence = []
    STR_no_in_Sequence = {}
    l = 1

    #looping for each STR in csv file
    for i in STRs:
        NoLetters= len(i)
        #print(NoLetters)
        #print (i)

        for j in range(len(sequence) - NoLetters):
            Units = sequence[j : j + NoLetters]
            #print (Units)
            #finding STR
            if Units == i:
                n.insert (j, 1)

                #looping for consecutitive STRs
                for k in range (1, len(sequence) - j - NoLetters):
                    units = sequence [j + k * NoLetters : j + (k + 1) * NoLetters]
                    #print (units)
                    if units == i:
                        l += 1
                        #print (l)
                        n.insert (j, l)

                    else:
                        l = 1 # import default l before looping for next j
                        break


            else:
                n.insert (j, 0)


            #print(n)
        #print (n)
        STR_no_in_Sequence [i] = max (n)

        #import to empty the list before next STR
        n = []
    #print (STR_no_in_Sequence)

    print


# compare the STR counts againt each row in the CSV file
# if key of people dictionary is same with value of STR_no_in_Sequence, print value of people dictionary
    NomatchingPerson = 0
    final = list (STR_no_in_Sequence.values())
    final_str  =  list (map(str, final)) # convert int values in dictionary to str values
    #print (final_str)
    for key in People:
        key_list = key.split(",") # convert string to list
        #key_list_int  =  list (map(int, key_list))
        #print(key_list)
        if key_list == final_str:
            print (People[key])
            NomatchingPerson += 1

    if NomatchingPerson == 0:
        print ("No match")







main()