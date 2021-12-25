import csv
import re


def get_numbers(incsv):
    with open(incsv, "r") as csvfile:
        csvdata = csv.reader(csvfile)

        for row in tuple(csvdata)[1:]:
            if row[34].strip() != "":
                yield (row[0], row[34])


def dump_numbers(incsv, output):
    with open(output, "w") as outfile:
        for contact in get_numbers(incsv):
            numbers = contact[1].split(":::")
            numbers = [re.sub(r"[-()\s]|(?:\+1)", "", _) for _ in numbers]
            dumped = []

            for number in numbers:
                if number in dumped:
                    continue

                dumped.append(number)
                outfile.write(contact[0] + ", " + number + "\n")


if __name__ == "__main__":
    dump_numbers("contacts.csv", "numbers.txt")