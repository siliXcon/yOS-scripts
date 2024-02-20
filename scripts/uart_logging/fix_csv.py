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

        try:
            # Process header
            header = next(reader)
            writer.writerow(header)
            # Get the number of columns in the header
            num_columns = len(header)

            for row in reader:
                try:
                    if len(row) == num_columns:
                        cleaned_row = [remove_non_printable(cell) for cell in row]
                        writer.writerow(cleaned_row)
                    else:
                        print(f"Warning: Skipping row with {len(row)} columns: {row}")
                except UnicodeDecodeError as e:
                    print(f"Error: {e}")
                    print(f"Row: {row}")

        except UnicodeDecodeError as e:
            print(f"UnicodeDecodeError: {e}. Skipping the problematic line.")

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
