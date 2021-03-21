#prints a list of students for a given house in alphabetical order.
from sys import argv
import csv
import sqlite3


def main():

    # checking input

    if len(argv) != 2:
        print("Error")
        return


    # Opening db file
    db = sqlite3.connect("./students.db")

    #finding matches from db

    for row in db.execute(f"SELECT DISTINCT first, middle, last, birth FROM students WHERE house = '{argv[1]}' ORDER BY last, first;"):
        # checking for middle name
        if row[1] == None:
            name = row[0] + " " + row[2]
        else:
            name = row[0] + " " + row[1] + " " + row[2]
        print (f"{name}, born, {row[3]}")


    # Close db
    db.close()

main()