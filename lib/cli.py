from helpers import (
    add_income, add_expense, view_transactions, delete_transaction,
    view_balance, manage_categories, search_transactions, generate_reports,
    create_default_categories
)

def main_menu():
    print("\n========================================")
    print("PERSONAL BUDGET TRACKER")
    print("========================================")
    print("1. Add Income")
    print("2. Add Expense")
    print("3. View Transactions")
    print("4. Delete Transaction")
    print("5. View Balance")
    print("6. Manage Categories")
    print("7. Search Transactions")
    print("8. Generate Reports")
    print("0. Exit")

if __name__ == "__main__":
    print("Welcome to the Budget Tracker CLI!")
    
    # Create default categories on first run
    create_default_categories()
    
    while True:
        main_menu()
        choice = input("\nEnter choice: ")
        
        if choice == '1':
            add_income()
        elif choice == '2':
            add_expense()
        elif choice == '3':
            view_transactions()
        elif choice == '4':
            delete_transaction()
        elif choice == '5':
            view_balance()
        elif choice == '6':
            manage_categories()
        elif choice == '7':
            search_transactions()
        elif choice == '8':
            generate_reports()
        elif choice == '0':
            print("Thanks for using my CLI")
            break
        else:
            print("Invalid choice. Please try again.")