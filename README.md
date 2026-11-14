# 📂 Python Files & Errors Assessment

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python&logoColor=white)
![Level](https://img.shields.io/badge/Level-Beginner-green)
![Topics](https://img.shields.io/badge/Topics-file%20handling%20%7C%20exceptions%20%7C%20sets%20%7C%20comprehensions-orange)

## 📌 Project Overview

This repository contains two small console-based management tools for a **training institute**, built with Python's **file handling**, **exception handling**, **sets** and **comprehensions**.

| # | Application | File | Purpose | Main Topics |
|---|-------------|------|---------|-------------|
| 1 | Institute Expense Tracker | `expense_tracker.py` | Records daily operational expenses (stationery, internet bills, refreshments, transport) and keeps them saved in a CSV file | `csv` file handling, `FileNotFoundError`, `ValueError`, sets |
| 2 | Student Attendance Cleaner | `attendance_cleaner.py` | Cleans a messy attendance list, removes duplicate students and produces a clean, sorted list | Text/CSV files, list comprehension, sets, `sorted()` |

## 📁 Project Structure

```
python-files-errors-assessment/
│
├── expense_tracker.py
├── attendance_cleaner.py
├── attendance.txt
└── README.md
```

**Files created automatically when the programs run:**

| File | Created by | When |
|------|------------|------|
| `expenses.csv` | `expense_tracker.py` | The first time an expense is added |
| `attendance_clean.csv` | `attendance_cleaner.py` | Every time the cleaner runs successfully |

---

## 💰 Task 1: Institute Expense Tracker

### Description
A menu-driven program that lets the administration add expenses, view them, and see how much was spent in each category. Every new expense is written to `expenses.csv` immediately, so the data is still there the next time the program starts.

### Menu

```
====================================
INSTITUTE EXPENSE TRACKER
====================================

1. Add New Expense
2. Show All Expenses
3. Calculate Total Expenses by Category
4. Exit

Enter your choice:
```

### CSV Format (`expenses.csv`)

```
date,item,category,amount
2026-11-10,A4 Paper Rim,Stationery,1850.00
2026-11-11,Internet Bill,Internet,4500.00
```

### Features
- **Loads saved expenses on startup.** If the file does not exist, the program starts with an empty list.
- **Add New Expense:** asks for date, item name, category and amount, then saves it to the CSV file.
- **Show All Expenses:** aligned table with a record count and grand total.
- **Totals by Category:** shows the **set of unique categories**, then the total spent in each one.
- Press **Enter** at the date prompt to use today's date.
- Categories are converted with `.title()`, so `transport` and `Transport` count as the same category.
- Amounts such as `4,500` (with a comma) are accepted.

### ▶️ How to Run
```bash
python expense_tracker.py
```
On some systems use `python3` instead of `python`.

---

## 🧹 Task 2: Student Attendance Cleaner

### Description
Reads student names from `attendance.txt` (one name per line). The file contains repeated names, inconsistent capitalization and extra spaces, so the program cleans every name, removes duplicates, sorts the names alphabetically and saves the final list to `attendance_clean.csv`.

### What the Program Does
1. Reads `attendance.txt`.
2. Cleans every name using `strip()` and `title()` inside a **list comprehension**.
3. Uses a **set** to find the unique students and count them.
4. Sorts the unique names alphabetically with `sorted()`.
5. Saves the final list to `attendance_clean.csv`.
6. Displays the original record count, unique student count and the cleaned list.

### Output Format (`attendance_clean.csv`)

```
student_name
Ali Khan
Ayesha Noor
Bilal Hussain
```

### ▶️ How to Run
```bash
python attendance_cleaner.py
```
Keep `attendance.txt` in the same folder as the program. The sample file included in this repository is deliberately messy (mixed capitalization, extra spaces, repeated names) so the cleaning can be seen working.

---

## 🛡️ Errors Handled and Why

### Expense Tracker

| Error | Where | Why it is handled | What the program does |
|-------|-------|-------------------|-----------------------|
| `FileNotFoundError` | Loading `expenses.csv` at startup | On the very first run the file does not exist yet. This is normal, not a failure. | Prints a message and starts with an empty expense list. |
| `ValueError` (amount) | `get_amount()` / `parse_amount()` | `float()` fails when the user types text such as `abc`. The program also raises it for zero, negative, `nan` and `inf` values, which are not real expenses. | Shows an error and asks for the amount **again**. |
| `ValueError` (date) | `get_date()` | `datetime.strptime()` fails for wrong formats or impossible dates such as `2026-13-45`. | Shows an error and asks for the date again. |
| `KeyError`, `TypeError`, `AttributeError`, `ValueError` | Reading each CSV row | A saved file can be edited by hand or damaged, leaving a row with a missing column or a bad amount. One bad row should not stop the program. | Skips the bad row and prints how many were skipped. |
| `OSError` | Reading the file (other than missing) | The file may be unreadable, for example because of permissions. | Prints a warning and starts with an empty list instead of crashing. |
| `OSError` | Saving an expense | The disk may be full or the file may be locked by another program. | Tells the user the expense was not saved, and does **not** add it to the in-memory list, so the screen and the file never disagree. |
| `KeyboardInterrupt`, `EOFError` | Whole program | The user may press `Ctrl + C` or close the input. | Exits with a polite message instead of a traceback. |

### Attendance Cleaner

| Error / Situation | Where | Why it is handled | What the program does |
|-------------------|-------|-------------------|-----------------------|
| `FileNotFoundError` | Reading `attendance.txt` | The input file may be missing or in a different folder. | Shows a clear message explaining where to put the file, then stops. |
| `OSError` | Saving `attendance_clean.csv` | The output file may be open in another program (for example Excel) or the disk may be full. | Shows an error message instead of crashing. |
| Empty file or blank lines | After reading | Blank lines are not student records, and an empty file has nothing to clean. | Blank lines are skipped and reported; an empty file shows a "nothing to clean" message. |

---

## 🧩 How Sets and List Comprehensions Are Used

### Sets: removing repeats

A **set** stores each value only once, which makes it ideal for finding unique items.

**Expense Tracker:** a *set comprehension* collects the unique categories.
```python
def get_unique_categories(expenses):
    return {expense["category"] for expense in expenses}
```
If five expenses use the categories `Stationery`, `Stationery`, `Internet`, `Transport`, `Internet`, the set holds only `Stationery`, `Internet` and `Transport`. Sets have no fixed order, so `sorted()` is used when the categories are displayed.

**Attendance Cleaner:** a set removes duplicate students.
```python
unique_names = set(cleaned_names)      # duplicates disappear
final_names = sorted(unique_names)     # sets are unordered, so sort them
```
`len(unique_names)` gives the unique student count.

### List comprehensions: building a list in one line

**Attendance Cleaner:** cleans every line of the file.
```python
[" ".join(line.strip().split()).title() for line in raw_lines if line.strip()]
```

| Part | What it does |
|------|--------------|
| `line.strip()` | Removes extra spaces at the start and end |
| `.split()` and `" ".join(...)` | Shrinks repeated spaces inside a name to one space |
| `.title()` | Fixes capitalization (`aLI kHAN` becomes `Ali Khan`) |
| `if line.strip()` | Skips lines that are empty or contain only spaces |

**Expense Tracker:** collects the amounts of one category so they can be added up.
```python
category_total = sum([e["amount"] for e in expenses if e["category"] == category])
```

**Attendance Cleaner:** turns each name into a one-column CSV row.
```python
writer.writerows([[name] for name in names])
```

---

## 🖥️ Sample Run: Expense Data Is Saved and Loaded Again

The menu is shown again before every `Enter your choice:` prompt. It is left out of the transcripts below to keep them short.

### ▶️ Run 1: first time (no `expenses.csv` yet)

```
$ python expense_tracker.py
No saved expense file found (expenses.csv). Starting with an empty expense list.

Enter your choice: 2

--- ALL EXPENSES ---
  No expenses recorded yet.

Enter your choice: 1

--- ADD NEW EXPENSE ---
Enter date (YYYY-MM-DD) [press Enter for today]: 2026-11-10
Enter item name: A4 Paper Rim
Enter category: stationery
Enter amount: abc
  Error: 'abc' is not a valid amount. Enter a number greater than zero (e.g. 1500 or 99.50).
Enter amount: 1850
  Success: expense saved to expenses.csv.

Enter your choice: 1

--- ADD NEW EXPENSE ---
Enter date (YYYY-MM-DD) [press Enter for today]: 2026-11-11
Enter item name: Internet Bill
Enter category: internet
Enter amount: -500
  Error: '-500' is not a valid amount. Enter a number greater than zero (e.g. 1500 or 99.50).
Enter amount: 4,500
  Success: expense saved to expenses.csv.

Enter your choice: 1

--- ADD NEW EXPENSE ---
Enter date (YYYY-MM-DD) [press Enter for today]: 2026-13-45
  Error: invalid date. Use the format YYYY-MM-DD (e.g. 2026-11-10).
Enter date (YYYY-MM-DD) [press Enter for today]: 2026-11-12
Enter item name: Tea & Biscuits
Enter category: REFRESHMENTS
Enter amount: 650.50
  Success: expense saved to expenses.csv.

Enter your choice: 1

--- ADD NEW EXPENSE ---
Enter date (YYYY-MM-DD) [press Enter for today]: 2026-11-12
Enter item name: Van Fuel
Enter category: Transport
Enter amount: 3200
  Success: expense saved to expenses.csv.

Enter your choice: 2

--- ALL EXPENSES ---
No.  Date        Item            Category            Amount
-----------------------------------------------------------
1    2026-11-10  A4 Paper Rim    Stationery        1,850.00
2    2026-11-11  Internet Bill   Internet          4,500.00
3    2026-11-12  Tea & Biscuits  Refreshments        650.50
4    2026-11-12  Van Fuel        Transport         3,200.00
-----------------------------------------------------------
Total records: 4 | Grand total: Rs. 10,200.50

Enter your choice: 4

Thank you for using the Expense Tracker. Goodbye!
```

### 📄 Contents of `expenses.csv` after Run 1

```
date,item,category,amount
2026-11-10,A4 Paper Rim,Stationery,1850.00
2026-11-11,Internet Bill,Internet,4500.00
2026-11-12,Tea & Biscuits,Refreshments,650.50
2026-11-12,Van Fuel,Transport,3200.00
```

### ▶️ Run 2: program started again (the saved data is loaded)

```
$ python expense_tracker.py
Loaded 4 saved expense(s) from expenses.csv.

Enter your choice: 2

--- ALL EXPENSES ---
No.  Date        Item            Category            Amount
-----------------------------------------------------------
1    2026-11-10  A4 Paper Rim    Stationery        1,850.00
2    2026-11-11  Internet Bill   Internet          4,500.00
3    2026-11-12  Tea & Biscuits  Refreshments        650.50
4    2026-11-12  Van Fuel        Transport         3,200.00
-----------------------------------------------------------
Total records: 4 | Grand total: Rs. 10,200.50

Enter your choice: 1

--- ADD NEW EXPENSE ---
Enter date (YYYY-MM-DD) [press Enter for today]: 2026-11-13
Enter item name: Printer Ink, Black
Enter category: stationery
Enter amount: 2,250
  Success: expense saved to expenses.csv.

Enter your choice: 3

--- TOTAL EXPENSES BY CATEGORY ---
Unique categories (4): Internet, Refreshments, Stationery, Transport

Category          Total Amount
------------------------------
Internet              4,500.00
Refreshments            650.50
Stationery            4,100.00
Transport             3,200.00
------------------------------
Grand Total          12,450.50

Enter your choice: 4

Thank you for using the Expense Tracker. Goodbye!
```

The four expenses from Run 1 were loaded successfully, and the new expense was added to them. Because the item `Printer Ink, Black` contains a comma, the `csv` module wraps it in quotes automatically:

```
date,item,category,amount
2026-11-10,A4 Paper Rim,Stationery,1850.00
2026-11-11,Internet Bill,Internet,4500.00
2026-11-12,Tea & Biscuits,Refreshments,650.50
2026-11-12,Van Fuel,Transport,3200.00
2026-11-13,"Printer Ink, Black",Stationery,2250.00
```

### ⚠️ Damaged rows in `expenses.csv`

If the CSV file contains bad rows (for example a text amount or a missing column), they are skipped and the rest of the data still loads:

```
$ python expense_tracker.py
Loaded 2 saved expense(s) from expenses.csv.
Warning: 3 damaged row(s) in expenses.csv were skipped.
```

---

## 🖥️ Sample Run: Student Attendance Cleaner

### 📄 Input: `attendance.txt` (16 lines, messy on purpose)

```
ali khan
  SARA AHMED  
Usman Tariq
ALI KHAN
hina malik
bilal   hussain
Sara Ahmed
   ayesha noor
usman tariq   
Hina Malik  
zain ul abideen
BILAL HUSSAIN
fatima zahra
Ayesha Noor
ali khan
  Zain Ul Abideen
```

### ▶️ Run

```
$ python attendance_cleaner.py
===== STUDENT ATTENDANCE CLEANER =====

Original number of records : 16
Unique student count       : 8
Duplicates removed         : 8

Cleaned attendance list (alphabetical):
   1. Ali Khan
   2. Ayesha Noor
   3. Bilal Hussain
   4. Fatima Zahra
   5. Hina Malik
   6. Sara Ahmed
   7. Usman Tariq
   8. Zain Ul Abideen

Saved to attendance_clean.csv
```

### 📄 Output: `attendance_clean.csv`

```
student_name
Ali Khan
Ayesha Noor
Bilal Hussain
Fatima Zahra
Hina Malik
Sara Ahmed
Usman Tariq
Zain Ul Abideen
```

### ❌ Missing input file

```
$ python attendance_cleaner.py
===== STUDENT ATTENDANCE CLEANER =====

Error: 'attendance.txt' was not found.
Create it in the same folder as this program (one student name per line) and run the program again.
```

### ⚠️ Blank lines in the input

```
===== STUDENT ATTENDANCE CLEANER =====

Original number of records : 3
Unique student count       : 2
Duplicates removed         : 1
Blank lines skipped        : 2

Cleaned attendance list (alphabetical):
   1. Ali Khan
   2. Sara

Saved to attendance_clean.csv
```

---

## 🧪 Testing Summary

| Program | Scenario Tested | Result |
|---------|-----------------|--------|
| Expense Tracker | No `expenses.csv` on first run (`FileNotFoundError`), starts empty | ✅ |
| Expense Tracker | Expenses saved to CSV and loaded again on the next run | ✅ |
| Expense Tracker | Non-numeric amount (`abc`) asks again (`ValueError`) | ✅ |
| Expense Tracker | Zero, negative and `nan` amounts rejected | ✅ |
| Expense Tracker | Invalid date format / impossible date rejected | ✅ |
| Expense Tracker | Amount with comma (`4,500`) accepted | ✅ |
| Expense Tracker | Item containing a comma saved and quoted correctly | ✅ |
| Expense Tracker | Unique categories shown using a set | ✅ |
| Expense Tracker | Totals by category and grand total correct | ✅ |
| Expense Tracker | Damaged CSV rows skipped with a warning | ✅ |
| Expense Tracker | Empty CSV file handled; header written on first save | ✅ |
| Expense Tracker | Unreadable or unwritable file does not crash the program | ✅ |
| Expense Tracker | Invalid menu choice handled | ✅ |
| Attendance Cleaner | Names cleaned with `strip()` and `title()` | ✅ |
| Attendance Cleaner | Duplicates removed using a set; unique count correct | ✅ |
| Attendance Cleaner | Names sorted alphabetically and saved to CSV | ✅ |
| Attendance Cleaner | Missing `attendance.txt` (`FileNotFoundError`) | ✅ |
| Attendance Cleaner | Empty file and blank lines handled | ✅ |
| Attendance Cleaner | File saved with a BOM (Windows Notepad) handled | ✅ |

## 🛠️ Requirements

- Python 3.x (3.6 or higher)
- Any terminal and a code editor (VS Code, PyCharm, etc.)
- No external libraries needed (only the built-in `csv`, `os`, `math` and `datetime` modules)

## 👤 Author

**Usama Malik** — Python Files & Errors Assessment
