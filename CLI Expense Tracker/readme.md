CLI Expense Tracker

A lightweight, zero-dependency Command Line Interface (CLI) tool to log and track your daily expenses. Data is saved locally in a clean CSV format.

How to Run

Prerequisites
Make sure you have [Python 3](https://www.python.org/) installed on your system.

1. Clone the repository
   
git clone [https://github.com/parthsantoki963/Internship-Weekly-Mini-Projects](https://github.com/parthsantoki963/Internship-Weekly-Mini-Projects)

cd Internship-Weekly-Mini-Projects/CLI Expense Tracker

2. Log a new expense
   
To add an item, pass the item name and the price. The script will automatically log it with today's date in DD-MM-YYYY format.

Command:-

-python script_name.py add "Coffee" 4.50


3. Log a backdated expense (Optional)
   
If you want to log an expense for a past date, use the -d date

Command:-

python script_name.py add "Groceries" 42.15 -d 15-05-2026


4. View your total summary
   
To see an aligned table of all your logged expenses and your grand total:

Command:-

python script_name.py view
