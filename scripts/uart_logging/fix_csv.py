# Remove non-printable characters from a CSV file.

import csv
import string
import sys
import shutil
import os
from pathlib import Path


def remove_non_printable(input_str):
    printable_chars = set(string.printable)
    return "".join(char for char in input_str if char in printable_chars)


def clean_csv(input_file):
    temp_csv_file = input_file + "_temp"

    with open(input_file, "r", newline="", encoding="utf-8") as infile, open(
        temp_csv_file, "w", newline="", encoding="utf-8"
    ) as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        for row in reader:
            cleaned_row = [remove_non_printable(cell) for cell in row]
            writer.writerow(cleaned_row)

    if not input_file.lower().endswith(".csv"):
        input_file = Path(input_file).stem + ".csv"

    shutil.move(temp_csv_file, input_file)
    return input_file


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py input.csv")
        sys.exit(1)

    input_csv_file = sys.argv[1]

    if not os.path.isfile(input_csv_file):
        print(f"Error: File '{input_csv_file}' not found.")
        sys.exit(1)

    result_filename = clean_csv(input_csv_file)

    print(
        f"Non-printable characters removed. Cleaned data saved to '{result_filename}'."
    )
