import sqlite3

# Function to create the database table if it doesn't exist
def create_table():
    conn = sqlite3.connect('budget.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS transactions
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, type TEXT, category TEXT, amount REAL)''')
    conn.commit()
    conn.close()

# Function to record income
def record_income(conn, cursor):
    amount = float(input("Enter income amount: "))
    cursor.execute("INSERT INTO transactions (type, amount) VALUES (?, ?)", ('income', amount))
    conn.commit()
    print("Income recorded successfully.")

# Function to record expense
def record_expense(conn, cursor):
    category = input("Enter expense category: ")
    amount = float(input("Enter expense amount: "))
    cursor.execute("INSERT INTO transactions (type, category, amount) VALUES (?, ?, ?)", ('expense', category, amount))
    conn.commit()
    print("Expense recorded successfully.")

# Function to calculate remaining budget
def calculate_remaining_budget(cursor):
    cursor.execute("SELECT SUM(amount) FROM transactions WHERE type='income'")
    income = cursor.fetchone()[0]
    cursor.execute("SELECT SUM(amount) FROM transactions WHERE type='expense'")
    expenses = cursor.fetchone()[0] or 0
    remaining_budget = income - expenses
    return remaining_budget

# Function to analyze expenses
def analyze_expenses(cursor):
    cursor.execute("SELECT category, SUM(amount) FROM transactions WHERE type='expense' GROUP BY category")
    expense_analysis = cursor.fetchall()
    
    print("Expense Analysis:")
    for category, amount in expense_analysis:
        print(f"{category}: ${amount}")

# Main function
def main():
    create_table()
    conn = sqlite3.connect('budget.db')
    cursor = conn.cursor()

    while True:
        print("\n===== Budget Tracker Menu =====")
        print("1. Record Income")
        print("2. Record Expense")
        print("3. Calculate Remaining Budget")
        print("4. Analyze Expenses")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            record_income(conn, cursor)
        elif choice == "2":
            record_expense(conn, cursor)
        elif choice == "3":
            remaining_budget = calculate_remaining_budget(cursor)
            print(f"Remaining Budget: ${remaining_budget}")
        elif choice == "4":
            analyze_expenses(cursor)
        elif choice == "5":
            print("Exiting Budget Tracker. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")

    conn.close()

if __name__ == "__main__":
    main()
