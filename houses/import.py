from sys import argv
import csv
import sqlite3


def main():

    # checking input

    if len(argv) != 2:
        print("Usage: import.py characters.csv")
        return


    # Opening db file
    db = sqlite3.connect("./students.db")


    #open and read csv
    with open(argv[1]) as titles:
        reader = csv.DictReader(titles)

    # Iterate over CSV file
        for row in reader:
            name = row["name"].split()
            house = row["house"]
            birth = row["birth"]

        # checking number of names, insert into db
            if len(name) == 2:
             # Deciding whether the person has middle name or not
                values = [name[0], name[1], house, birth]
                db.execute("INSERT INTO students (first, last, house, birth) VALUES(?, ?, ?, ?)", values)

            elif len(name) == 3:
                values = [name[0], name[1], name[2], house, birth]
                db.execute("INSERT INTO students (first, middle, last, house, birth) VALUES(?, ?, ?, ?, ?)", values)

    # Save db
    db.commit()

    # Close db
    db.close()

main()