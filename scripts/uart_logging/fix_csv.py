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

        # Process header
        header = next(reader)
        writer.writerow(header)
        # Get the number of columns in the header
        num_columns = len(header)

        for row in reader:
            if len(row) == num_columns:
                cleaned_row = [remove_non_printable(cell) for cell in row]
                writer.writerow(cleaned_row)
            else:
                if len(row) < 2:    # Skip empty lines
                    print(".", end="")
                    if len(row) == 1:   
                        writer.writerow("")
                else:
                    print(f"\nWarning: Skipping row with len: {len(row)} data: {row}")


    if not input_file.lower().endswith(".csv"):
        input_file = Path(input_file).stem + ".csv"

    shutil.move(temp_csv_file, input_file)
    return input_file

def remove_invalid_bytes(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # If decoding succeeds without errors, return the content as is
            return content
    except UnicodeDecodeError:
        with open(file_path, 'rb') as f:
            content = f.read()
        # Remove bytes that cause UnicodeDecodeError
        cleaned_content = content.decode('utf-8', errors='ignore')
        # Write the cleaned content back to the file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(cleaned_content)
        return cleaned_content

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py input.csv")
        sys.exit(1)

    input_csv_file = sys.argv[1]

    if not os.path.isfile(input_csv_file):
        print(f"Error: File '{input_csv_file}' not found.")
        sys.exit(1)

    remove_invalid_bytes(input_csv_file)
    # Remove invalid bytes from the file
    result_filename = clean_csv(input_csv_file)

    print(
        f"\nNon-printable characters removed. Cleaned data saved to '{result_filename}'."
    )
