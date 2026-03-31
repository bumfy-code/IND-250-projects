import pandas as pd
import os
from datetime import datetime
import matplotlib.pyplot as plt

# Configuration
FILE_NAME = "expenses.csv"

def save_df_sorted(df):
    """Saves dataframe to CSV, sorted by Amount in descending order."""
    df_sorted = df.sort_values(by="Amount", ascending=False, ignore_index=True)
    df_sorted.to_csv(FILE_NAME, index=False)

def initialize_df():
    """Ensures a CSV exists with the correct columns."""
    if os.path.exists(FILE_NAME):
        return pd.read_csv(FILE_NAME)
    else:
        # Define the structure of our tracker
        columns = ["Date", "Category", "Description", "Amount"]
        df = pd.DataFrame(columns=columns)
        df.to_csv(FILE_NAME, index=False)
        return df

def add_expense(category, description, amount):
    """Appends a new expense to the CSV."""
    df = pd.read_csv(FILE_NAME)

    new_entry = {
        "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Category": category,
        "Description": description,
        "Amount": float(amount)
    }

    # Append the new row and save sorted
    df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
    save_df_sorted(df)
    print("\n✅ Expense added successfully!")

def view_summary():
    """Displays data and basic stats using Pandas."""
    df = pd.read_csv(FILE_NAME)

    if df.empty:
        print("\n📭 No expenses recorded yet.")
        return

    print("\n--- Current Expenses ---")
    print(df)

    # Use Pandas magic for a quick summary
    total = df["Amount"].sum()
    average = df["Amount"].mean()
    print(f"\n💰 Total Spent: ${total:.2f}")
    print(f"📊 Average Expense: ${average:.2f}")

    print("\n--- Spending by Category ---")
    print(df.groupby("Category")["Amount"].sum())

def delete_expense():
    """Deletes an expense by index."""
    df = pd.read_csv(FILE_NAME)
    
    if df.empty:
        print("\n📭 No expenses to delete.")
        return
    
    print("\n--- Current Expenses ---")
    print(df)
    
    try:
        loc = int(input("Enter the index of the expense to delete: "))
        if loc not in df.index:
            print("\n❌ Invalid index!")
            return
        df = df.drop(index=loc)
        save_df_sorted(df)
        print("\n✅ Expense deleted successfully!")
        view_summary()
    except ValueError:
        print("\n❌ Please enter a valid number!")

def edit_expense():
    """Edits an existing expense and updates the timestamp."""
    df = pd.read_csv(FILE_NAME)
    
    if df.empty:
        print("\n📭 No expenses to edit.")
        return
    
    print("\n--- Current Expenses ---")
    print(df)
    
    try:
        idx = int(input("Enter the index of the expense to edit: "))
        if idx not in df.index:
            print("\n❌ Invalid index!")
            return
        
        print("\nLeave any field blank to keep the current value.")
        print(f"Current expense: {df.loc[idx].to_dict()}")
        
        cat = input("Enter new Category (or press Enter to skip): ").strip()
        if cat:
            df.at[idx, "Category"] = cat
        
        desc = input("Enter new Description (or press Enter to skip): ").strip()
        if desc:
            df.at[idx, "Description"] = desc
        
        amt = input("Enter new Amount (or press Enter to skip): ").strip()
        if amt:
            df.at[idx, "Amount"] = float(amt)
        
        # Auto-update the timestamp
        df.at[idx, "Date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        save_df_sorted(df)
        print("\n✅ Expense edited successfully!")
        view_summary()
    except ValueError:
        print("\n❌ Please enter valid values!")

def plot_expenses():
    """Generates a pie chart of all expenses by category."""
    df = pd.read_csv(FILE_NAME)
    
    if df.empty:
        print("\n📭 No expenses to plot.")
        return
    
    category_totals = df.groupby("Category")["Amount"].sum()
    plt.figure(figsize=(8, 8))
    plt.pie(category_totals, labels=category_totals.index, autopct="%1.1f%%")
    plt.title("Total Expenses by Category")
    plt.axis('equal')
    plt.show()
    

def main():
    initialize_df()

    while True:
        print("\n--- 📈 Expense Tracker CLI ---")
        print("1. Add Expense")
        print("2. View Summary")
        print("3. Delete Expense")
        print("4. Edit Expense")
        print("5. Plot")
        print("6. Exit")

        choice = input("Select an option: ")

        if choice == "1":
            cat = input("Enter Category (e.g., Food, Rent, Fun): ")
            desc = input("Short Description: ")
            amt = input("Amount: ")
            add_expense(cat, desc, amt)
        elif choice == "2":
            view_summary()
        elif choice == "3":
            delete_expense()
        elif choice == "4":
            edit_expense()
        elif choice == "5":
            plot_expenses()
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid choice, try again.")


if __name__ == "__main__":
    main()