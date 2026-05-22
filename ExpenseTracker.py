import argparse
import csv
from datetime import datetime
import os

File_path = "expense.csv"

def create_csv():
    """Creates the CSV file with headers if it doesn't exist."""
    if not os.path.isfile(File_path):
        with open(File_path, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Item Name", "Price"])
        
        print(f"--> SUCCESS: Created a brand new file at: {os.path.abspath(File_path)}")

def add_expense(args):
    """Appends a new expense to the CSV file."""
    create_csv()

    date_str = args.date if args.date else datetime.today().strftime("%d-%m-%Y")

    if args.date:
        try:
            datetime.strptime(args.date, "%d-%m-%Y")
        except ValueError:
            print("Error: Date must be in DD-MM-YYYY format.")
            return

    with open(File_path, "a", newline="", encoding="utf-8") as file:
        
          writer = csv.writer(file)
          writer.writerow([date_str, args.item, args.price])
          print(f"Added expense: {args.item} for ${args.price:.2f} on {date_str}")


def view_expenses(args):
    """Reads and displays expenses, calculating the total."""
    if not os.path.isfile(File_path):
        print("No expenses recorded yet! Use 'add' to log your first expense.")
        return

    total = 0.0
    print("-" * 56)
    print(f"|{'Date':<12} | {'Item Name':<25} | {'Price':<10} |")
    print("-" * 56)

    with open(File_path, "r", newline="", encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader)  
        
        for row in reader:
            if not row:
                continue
            date, item, price_str = row
            price = float(price_str)
            total += price
            
            print(f"|{date:<12} | {item:<25} | ${price:<9.2f} |")

    print("-" * 56)
    print(f"|{'TOTAL EXPENSES':<40} | ${total:<9.2f} |")
    print("-" * 56)

def main():
    parser = argparse.ArgumentParser(description="Advanced Expense Tracker CLI")
    subparsers = parser.add_subparsers(dest="command", required=True, help="Available subcommands")
    
    add_parser = subparsers.add_parser("add", help="Log a new expense")
    add_parser.add_argument("item", type=str, help="Name of the item purchased")
    add_parser.add_argument("price", type=float, help="Price of the item")
    add_parser.add_argument("-d", "--date", type=str, help="Date of expense (DD-MM-YYYY). Defaults to today.")
    add_parser.set_defaults(func=add_expense)

    view_parser = subparsers.add_parser("view", help="View summary of all expenses")
    view_parser.set_defaults(func=view_expenses)
                                                                        
    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()