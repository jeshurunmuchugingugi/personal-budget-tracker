from models.models import Category, Transaction
from datetime import datetime, timedelta

def add_income():
    categories = Category.get_all()
    if not categories:
        print("No categories found. Please create a category first.")
        return
    
    print("Categories:")
    for cat in categories:
        print(f"{cat['id']}. {cat['name']}")
    
    try:
        amount = float(input("Income amount: $"))
        category_id = int(input("Category number: "))
        description = input("Description (optional): ").strip() or None
        
        Transaction.create(amount, 'income', category_id, description)
        print(f"Income of ${amount:.2f} added successfully!")
    except ValueError:
        print("Invalid input. Please enter valid numbers.")
    except Exception as e:
        print(f"Error: {e}")

def add_expense():
    categories = Category.get_all()
    if not categories:
        print("No categories found. Please create a category first.")
        return
    
    print("Categories:")
    for cat in categories:
        print(f"{cat['id']}. {cat['name']}")
    
    try:
        amount = float(input("Expense amount: $"))
        category_id = int(input("Category number: "))
        description = input("Description (optional): ").strip() or None
        
        Transaction.create(amount, 'expense', category_id, description)
        print(f"Expense of ${amount:.2f} added successfully!")
    except ValueError:
        print("Invalid input. Please enter valid numbers.")
    except Exception as e:
        print(f"Error: {e}")

def view_transactions():
    transactions = Transaction.get_all()
    categories = {cat['id']: cat['name'] for cat in Category.get_all()}
    
    if not transactions:
        print("No transactions found.")
        return
    
    print("\nAll Transactions:")
    print("-" * 80)
    for t in transactions:
        cat_name = categories.get(t['category_id'], 'Unknown')
        print(f"ID: {t['id']} | {t['type'].title()}: ${t['amount']:.2f} | Category: {cat_name}")
        print(f"Date: {t['date']} | Description: {t['description'] or 'N/A'}")
        print("-" * 80)

def delete_transaction():
    transactions = Transaction.get_all()
    if not transactions:
        print("No transactions to delete.")
        return
    
    view_transactions()
    try:
        transaction_id = int(input("Enter transaction ID to delete: "))
        if Transaction.delete(transaction_id):
            print("Transaction deleted successfully!")
        else:
            print("Transaction not found.")
    except ValueError:
        print("Invalid input. Please enter a valid ID.")

def view_balance():
    balance = Transaction.get_balance()
    print(f"\nCurrent Balance: ${balance:.2f}")

def manage_categories():
    while True:
        print("\n--- Category Management ---")
        print("1. View Categories")
        print("2. Add Category")
        print("3. Delete Category")
        print("0. Back to Main Menu")
        
        choice = input("Enter choice: ")
        
        if choice == '1':
            categories = Category.get_all()
            if categories:
                print("\nCategories:")
                for cat in categories:
                    print(f"{cat['id']}. {cat['name']}")
            else:
                print("No categories found.")
        
        elif choice == '2':
            name = input("Category name: ").strip()
            if name:
                try:
                    Category.create(name)
                    print(f"Category '{name}' created successfully!")
                except Exception as e:
                    print(f"Error: {e}")
            else:
                print("Category name cannot be empty.")
        
        elif choice == '3':
            categories = Category.get_all()
            if categories:
                print("\nCategories:")
                for cat in categories:
                    print(f"{cat['id']}. {cat['name']}")
                try:
                    cat_id = int(input("Enter category ID to delete: "))
                    if Category.delete(cat_id):
                        print("Category deleted successfully!")
                    else:
                        print("Category not found.")
                except ValueError:
                    print("Invalid input. Please enter a valid ID.")
            else:
                print("No categories to delete.")
        
        elif choice == '0':
            break
        else:
            print("Invalid choice. Please try again.")

def search_transactions():
    print("\n--- Search Transactions ---")
    print("1. Search by Category")
    print("2. Search by Date")
    
    choice = input("Enter choice: ")
    categories = {cat['id']: cat['name'] for cat in Category.get_all()}
    
    if choice == '1':
        cats = Category.get_all()
        if not cats:
            print("No categories found.")
            return
        
        print("Categories:")
        for cat in cats:
            print(f"{cat['id']}. {cat['name']}")
        
        try:
            cat_id = int(input("Enter category ID: "))
            transactions = Transaction.find_by_category(cat_id)
            
            if transactions:
                print(f"\nTransactions in category:")
                print("-" * 80)
                for t in transactions:
                    cat_name = categories.get(t['category_id'], 'Unknown')
                    print(f"ID: {t['id']} | {t['type'].title()}: ${t['amount']:.2f} | Category: {cat_name}")
                    print(f"Date: {t['date']} | Description: {t['description'] or 'N/A'}")
                    print("-" * 80)
            else:
                print("No transactions found for this category.")
        except ValueError:
            print("Invalid input. Please enter a valid ID.")
    
    elif choice == '2':
        date = input("Enter date (YYYY-MM-DD): ")
        transactions = Transaction.find_by_date(date)
        
        if transactions:
            print(f"\nTransactions on {date}:")
            print("-" * 80)
            for t in transactions:
                cat_name = categories.get(t['category_id'], 'Unknown')
                print(f"ID: {t['id']} | {t['type'].title()}: ${t['amount']:.2f} | Category: {cat_name}")
                print(f"Date: {t['date']} | Description: {t['description'] or 'N/A'}")
                print("-" * 80)
        else:
            print("No transactions found for this date.")
    else:
        print("Invalid choice.")

def generate_reports():
    print("\n--- Generate Reports ---")
    print("1. Weekly Report")
    print("2. Monthly Report")
    
    choice = input("Enter choice: ")
    
    if choice == '1':
        # Last 7 days
        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)
        print(f"\nWeekly Report ({start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}):")
        
    elif choice == '2':
        # Last 30 days
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
        print(f"\nMonthly Report ({start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}):")
    else:
        print("Invalid choice.")
        return
    
    transactions = Transaction.get_all()
    categories = {cat['id']: cat['name'] for cat in Category.get_all()}
    
    # Filter transactions by date range
    filtered_transactions = []
    for t in transactions:
        t_date = datetime.strptime(str(t['date']).split()[0], '%Y-%m-%d')
        if start_date <= t_date <= end_date:
            filtered_transactions.append(t)
    
    if not filtered_transactions:
        print("No transactions found in this period.")
        return
    
    total_income = sum(t['amount'] for t in filtered_transactions if t['type'] == 'income')
    total_expenses = sum(t['amount'] for t in filtered_transactions if t['type'] == 'expense')
    
    print(f"Total Income: ${total_income:.2f}")
    print(f"Total Expenses: ${total_expenses:.2f}")
    print(f"Net: ${total_income - total_expenses:.2f}")
    
    # Category breakdown
    category_totals = {}
    for t in filtered_transactions:
        cat_name = categories.get(t['category_id'], 'Unknown')
        if cat_name not in category_totals:
            category_totals[cat_name] = {'income': 0, 'expense': 0}
        category_totals[cat_name][t['type']] += t['amount']
    
    print("\nCategory Breakdown:")
    for cat, totals in category_totals.items():
        print(f"{cat}: Income ${totals['income']:.2f}, Expenses ${totals['expense']:.2f}")

def create_default_categories():
    default_categories = ['Food', 'Rent', 'Transport', 'Entertainment', 'Utilities', 'Other']
    existing_categories = [cat['name'] for cat in Category.get_all()]
    
    for cat_name in default_categories:
        if cat_name not in existing_categories:
            Category.create(cat_name)
    
    print("Default categories created!")