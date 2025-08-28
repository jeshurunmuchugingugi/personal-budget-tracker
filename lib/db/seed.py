import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from faker import Faker
from models.models import Category, Transaction
import random
from datetime import datetime, timedelta

fake = Faker()

def seed_data():
    print("Seeding database with sample data...")
    
    # Create categories
    categories = ['Food', 'Rent', 'Transport', 'Entertainment', 'Utilities', 'Salary', 'Freelance']
    category_ids = []
    
    for cat_name in categories:
        try:
            cat = Category.create(cat_name)
            category_ids.append(cat['id'])
            print(f"Created category: {cat_name}")
        except:
            # Category might already exist
            existing_cats = Category.get_all()
            for existing_cat in existing_cats:
                if existing_cat['name'] == cat_name:
                    category_ids.append(existing_cat['id'])
                    break
    
    # Create sample transactions
    for _ in range(20):
        amount = round(random.uniform(10, 1000), 2)
        transaction_type = random.choice(['income', 'expense'])
        category_id = random.choice(category_ids)
        description = fake.sentence(nb_words=4)
        
        Transaction.create(amount, transaction_type, category_id, description)
    
    print("Sample data created successfully!")
    print(f"Current balance: ${Transaction.get_balance():.2f}")

if __name__ == "__main__":
    seed_data()