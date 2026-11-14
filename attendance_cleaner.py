"""
Student Attendance Cleaner
--------------------------
Reads student names from attendance.txt (one name per line), cleans them,
removes duplicates, sorts them alphabetically and saves the final list to
attendance_clean.csv.

Concepts used: file handling (text + csv), exception handling
(FileNotFoundError, OSError), a list comprehension for cleaning, and a set
for finding unique students.
"""

import csv
import os

# Files are located next to this script, so the program works no matter
# which folder it is started from.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_NAME = "attendance.txt"
OUTPUT_NAME = "attendance_clean.csv"
INPUT_PATH = os.path.join(BASE_DIR, INPUT_NAME)
OUTPUT_PATH = os.path.join(BASE_DIR, OUTPUT_NAME)


def read_lines():
    """Read every line of attendance.txt. Returns None if the file is missing."""
    try:
        # utf-8-sig also handles files saved with a BOM (e.g. by Windows Notepad)
        with open(INPUT_PATH, "r", encoding="utf-8-sig") as file:
            return file.read().splitlines()
    except FileNotFoundError:
        print(f"Error: '{INPUT_NAME}' was not found.")
        print(f"Create it in the same folder as this program "
              f"(one student name per line) and run the program again.")
        return None


def clean_names(raw_lines):
    """Clean the names with a list comprehension.

    strip()  -> removes extra spaces at the start and end
    split()/join() -> shrinks spaces inside a name to a single space
    title()  -> fixes capitalization ("aLI kHAN" -> "Ali Khan")
    The 'if line.strip()' part skips lines that are empty or only spaces.
    """
    return [" ".join(line.strip().split()).title() for line in raw_lines if line.strip()]


def save_clean_list(names):
    """Save the final cleaned and sorted names to attendance_clean.csv."""
    with open(OUTPUT_PATH, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["student_name"])                   # header row
        writer.writerows([[name] for name in names])        # one name per row


def main():
    """Read, clean, de-duplicate, sort, save and display the attendance list."""
    print("===== STUDENT ATTENDANCE CLEANER =====\n")

    raw_lines = read_lines()
    if raw_lines is None:
        return

    # 1. Clean every name with a list comprehension
    cleaned_names = clean_names(raw_lines)
    original_count = len(cleaned_names)
    blank_lines = len(raw_lines) - original_count

    if original_count == 0:
        print(f"'{INPUT_NAME}' has no student names. Nothing to clean.")
        return

    # 2. A set keeps only one copy of each name (duplicates disappear)
    unique_names = set(cleaned_names)

    # 3. Sets have no order, so sort the unique names alphabetically
    final_names = sorted(unique_names)

    # 4. Save the final list to the CSV file
    try:
        save_clean_list(final_names)
    except OSError as error:
        print(f"Error: the cleaned list could not be saved ({error}).")
        return

    # 5. Display the results
    print(f"Original number of records : {original_count}")
    print(f"Unique student count       : {len(unique_names)}")
    print(f"Duplicates removed         : {original_count - len(unique_names)}")
    if blank_lines:
        print(f"Blank lines skipped        : {blank_lines}")

    print("\nCleaned attendance list (alphabetical):")
    for number, name in enumerate(final_names, start=1):
        print(f"  {number:>2}. {name}")

    print(f"\nSaved to {OUTPUT_NAME}")


if __name__ == "__main__":
    main()
