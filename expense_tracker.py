"""
Institute Expense Tracker
-------------------------
A menu-driven program that records the daily operational expenses of a
training institute (stationery, internet bills, refreshments, transport...).

Expenses are stored in a CSV file named expenses.csv with the columns:
    date,item,category,amount

Concepts used: file handling (csv module), exception handling
(FileNotFoundError, ValueError, OSError), a set of unique categories,
and list / set comprehensions.
"""

import csv
import math
import os
from datetime import date, datetime

# The CSV file is stored next to this script, so the program works no matter
# which folder it is started from.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_NAME = "expenses.csv"
CSV_PATH = os.path.join(BASE_DIR, CSV_NAME)
FIELDNAMES = ["date", "item", "category", "amount"]
CURRENCY = "Rs."


# ---------------------------------------------------------------------------
# Input helper functions (validation)
# ---------------------------------------------------------------------------

def parse_amount(text):
    """Convert text to a positive number. Raises ValueError if it is invalid."""
    cleaned_text = str(text).strip().replace(",", "")   # allow "1,500"
    amount = float(cleaned_text)                        # ValueError if not a number

    # float() accepts 'nan' and 'inf', and we also reject zero / negative values
    if not math.isfinite(amount) or amount <= 0:
        raise ValueError("amount must be a number greater than zero")
    return amount


def get_text(prompt):
    """Keep asking until the user enters non-empty text."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("  Error: input cannot be empty. Please try again.")


def get_date():
    """Ask for a date in YYYY-MM-DD format (Enter = today's date)."""
    while True:
        text = input("Enter date (YYYY-MM-DD) [press Enter for today]: ").strip()
        if text == "":
            return date.today().isoformat()
        try:
            # strptime raises ValueError for impossible dates such as 2026-13-45
            return datetime.strptime(text, "%Y-%m-%d").date().isoformat()
        except ValueError:
            print("  Error: invalid date. Use the format YYYY-MM-DD (e.g. 2026-11-10).")


def get_amount():
    """Keep asking until the user enters a valid amount."""
    while True:
        text = input("Enter amount: ").strip()
        try:
            return parse_amount(text)
        except ValueError:
            # Not a number (or not positive): ask the user to enter it again
            print(f"  Error: '{text}' is not a valid amount. "
                  "Enter a number greater than zero (e.g. 1500 or 99.50).")


# ---------------------------------------------------------------------------
# File handling functions
# ---------------------------------------------------------------------------

def load_expenses():
    """Load saved expenses from expenses.csv and return them as a list of dictionaries."""
    expenses = []
    skipped_rows = 0

    try:
        with open(CSV_PATH, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    expenses.append({
                        "date": row["date"].strip(),
                        "item": row["item"].strip(),
                        "category": row["category"].strip().title(),
                        "amount": parse_amount(row["amount"]),
                    })
                except (KeyError, TypeError, AttributeError, ValueError):
                    # A damaged row (missing column or bad amount) is skipped
                    # so one bad line does not stop the whole program.
                    skipped_rows += 1
    except FileNotFoundError:
        # First run: there is no saved file yet, so start with an empty list
        print(f"No saved expense file found ({CSV_NAME}). "
              "Starting with an empty expense list.")
        return []
    except OSError as error:
        # Any other problem reading the file (e.g. permission denied)
        print(f"Warning: {CSV_NAME} could not be read ({error}). "
              "Starting with an empty expense list.")
        return []

    print(f"Loaded {len(expenses)} saved expense(s) from {CSV_NAME}.")
    if skipped_rows:
        print(f"Warning: {skipped_rows} damaged row(s) in {CSV_NAME} were skipped.")
    return expenses


def save_expense(expense):
    """Append one expense to expenses.csv (the header is written for a new file)."""
    needs_header = not os.path.isfile(CSV_PATH) or os.path.getsize(CSV_PATH) == 0

    # "a" (append) mode adds the new row without touching the old ones
    with open(CSV_PATH, "a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        if needs_header:
            writer.writeheader()
        writer.writerow({
            "date": expense["date"],
            "item": expense["item"],
            "category": expense["category"],
            "amount": f"{expense['amount']:.2f}",
        })


# ---------------------------------------------------------------------------
# Menu feature functions
# ---------------------------------------------------------------------------

def get_unique_categories(expenses):
    """Return a SET of all unique categories (set comprehension removes repeats)."""
    return {expense["category"] for expense in expenses}


def add_expense(expenses):
    """Option 1: collect a new expense, save it to the CSV file, keep it in memory."""
    print("\n--- ADD NEW EXPENSE ---")
    expense_date = get_date()
    item = get_text("Enter item name: ")
    # title() makes "transport" and "Transport" the same category
    category = get_text("Enter category: ").title()
    amount = get_amount()

    new_expense = {
        "date": expense_date,
        "item": item,
        "category": category,
        "amount": amount,
    }

    try:
        save_expense(new_expense)
    except OSError as error:
        # Disk full, file open in another program, no permission, etc.
        print(f"  Error: the expense could not be saved ({error}).")
        return

    expenses.append(new_expense)
    print(f"  Success: expense saved to {CSV_NAME}.")


def show_all_expenses(expenses):
    """Option 2: display every expense in an aligned table."""
    print("\n--- ALL EXPENSES ---")
    if not expenses:
        print("  No expenses recorded yet.")
        return

    # Size the text columns to fit the longest item / category
    item_width = max(len("Item"), max(len(e["item"]) for e in expenses))
    category_width = max(len("Category"), max(len(e["category"]) for e in expenses))

    header = (f"{'No.':<5}{'Date':<12}{'Item':<{item_width + 2}}"
              f"{'Category':<{category_width + 2}}{'Amount':>12}")
    print(header)
    print("-" * len(header))

    grand_total = 0
    for number, expense in enumerate(expenses, start=1):
        print(f"{number:<5}{expense['date']:<12}{expense['item']:<{item_width + 2}}"
              f"{expense['category']:<{category_width + 2}}{expense['amount']:>12,.2f}")
        grand_total += expense["amount"]

    print("-" * len(header))
    print(f"Total records: {len(expenses)} | Grand total: {CURRENCY} {grand_total:,.2f}")


def show_totals_by_category(expenses):
    """Option 3: list the unique categories (a set) and the total spent in each."""
    print("\n--- TOTAL EXPENSES BY CATEGORY ---")
    if not expenses:
        print("  No expenses recorded yet.")
        return

    unique_categories = get_unique_categories(expenses)
    # Sets have no order, so sorted() gives a neat alphabetical display
    print(f"Unique categories ({len(unique_categories)}): "
          f"{', '.join(sorted(unique_categories))}\n")

    category_width = max(len("Category"), max(len(c) for c in unique_categories))
    print(f"{'Category':<{category_width + 2}}{'Total Amount':>16}")
    print("-" * (category_width + 18))

    grand_total = 0
    for category in sorted(unique_categories):
        # List comprehension: collect the amounts that belong to this category
        category_total = sum([e["amount"] for e in expenses if e["category"] == category])
        grand_total += category_total
        print(f"{category:<{category_width + 2}}{category_total:>16,.2f}")

    print("-" * (category_width + 18))
    print(f"{'Grand Total':<{category_width + 2}}{grand_total:>16,.2f}")


# ---------------------------------------------------------------------------
# Main program
# ---------------------------------------------------------------------------

def show_menu():
    """Print the main menu."""
    print("\n====================================")
    print("INSTITUTE EXPENSE TRACKER")
    print("====================================\n")
    print("1. Add New Expense")
    print("2. Show All Expenses")
    print("3. Calculate Total Expenses by Category")
    print("4. Exit\n")


def main():
    """Load saved data, then run the menu loop until the user exits."""
    expenses = load_expenses()

    while True:
        show_menu()
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_expense(expenses)
        elif choice == "2":
            show_all_expenses(expenses)
        elif choice == "3":
            show_totals_by_category(expenses)
        elif choice == "4":
            print("\nThank you for using the Expense Tracker. Goodbye!")
            break
        else:
            print("  Invalid choice. Please enter a number from 1 to 4.")


# Run the program only when this file is executed directly
if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n\nProgram closed. Goodbye!")
