# Personal Budget Tracker CLI

A comprehensive command-line personal budget tracking application built with Python, SQLAlchemy, and Alembic. This application allows users to manage their personal finances by tracking income and expenses, categorizing transactions, and generating detailed financial reports.

## Overview

The Personal Budget Tracker CLI is designed to help individuals monitor their financial health through a simple yet powerful command-line interface. The application provides complete CRUD operations for financial transactions, advanced search capabilities, and comprehensive reporting features.

## Core Features

### Transaction Management
- Add income transactions with amount, category, and optional description
- Add expense transactions with detailed categorization
- View all transactions in a formatted list with complete details
- Delete transactions by ID to remove errors or outdated entries
- Automatic timestamp tracking for all transactions

### Financial Analysis
- Real-time balance calculation (total income minus total expenses)
- Category-based transaction filtering and analysis
- Date-based transaction search and filtering
- Weekly financial reports covering the last 7 days
- Monthly financial reports covering the last 30 days
- Category breakdown showing income and expense distribution

### Category Management
- Create custom transaction categories
- View all available categories
- Delete unused categories
- Default categories automatically created on first run
- One-to-many relationship between categories and transactions

## Technical Architecture

### Project Structure

```
personal-budget-tracker/
├── lib/                    # Main application directory
│   ├── cli.py             # Command-line interface and main entry point
│   ├── helpers.py         # Business logic and helper functions
│   ├── models/            # Database models package
│   │   ├── __init__.py    # Package initialization with imports
│   │   └── models.py      # SQLAlchemy ORM models and database logic
│   ├── db/                # Database-related files
│   │   └── seed.py        # Sample data generation script
│   ├── migrations/        # Alembic database migrations
│   │   ├── versions/      # Migration version files
│   │   ├── env.py         # Alembic environment configuration
│   │   ├── README         # Migration documentation
│   │   └── script.py.mako # Migration template
│   └── alembic.ini        # Alembic configuration file
├── budget.db              # SQLite database file (created automatically)
├── Pipfile                # Python dependencies specification
├── Pipfile.lock          # Locked dependency versions
└── README.md             # Project documentation
```

### Database Models

#### Category Model
The Category model represents transaction categories with the following attributes:
- **id**: Primary key (Integer, auto-increment)
- **name**: Category name (String, unique, required)
- **transactions**: One-to-many relationship with Transaction model

**Available Methods:**
- `create(name)`: Creates a new category
- `get_all()`: Retrieves all categories
- `find_by_id(id)`: Finds category by ID
- `delete(id)`: Deletes category by ID

#### Transaction Model
The Transaction model represents individual financial transactions:
- **id**: Primary key (Integer, auto-increment)
- **amount**: Transaction amount (Float, required)
- **type**: Transaction type - 'income' or 'expense' (String, required)
- **description**: Optional transaction description (String, nullable)
- **date**: Transaction timestamp (DateTime, auto-generated)
- **category_id**: Foreign key to Category (Integer, required)
- **category**: Many-to-one relationship with Category model

**Available Methods:**
- `create(amount, type, category_id, description)`: Creates new transaction
- `get_all()`: Retrieves all transactions
- `find_by_id(id)`: Finds transaction by ID
- `find_by_category(category_id)`: Finds transactions by category
- `find_by_date(date)`: Finds transactions by date
- `get_balance()`: Calculates current balance (income - expenses)
- `delete(id)`: Deletes transaction by ID

### Database Configuration

#### SQLAlchemy Setup
- **Database Engine**: SQLite with file-based storage
- **ORM**: SQLAlchemy declarative base for model definitions
- **Session Management**: Scoped sessions with automatic cleanup
- **Connection String**: `sqlite:///budget.db`

#### Alembic Migration System
- **Migration Directory**: `lib/migrations/`
- **Configuration File**: `lib/alembic.ini`
- **Environment Setup**: Configured to import models automatically
- **Version Control**: Tracks all database schema changes

## Installation and Setup

### Prerequisites
- Python 3.8 or higher
- pipenv (Python package manager)

### Installation Steps

1. **Clone or download the project**
```bash
cd personal-budget-tracker
```

2. **Install dependencies using pipenv**
```bash
pipenv install
```

3. **Activate the virtual environment**
```bash
pipenv shell
```

4. **Run the application**
```bash
pipenv run python lib/cli.py
```

### Optional Setup

**Generate sample data for testing:**
```bash
pipenv run python lib/db/seed.py
```

This creates sample categories and 20 random transactions for testing purposes.

## Application Usage

### Main Menu Navigation

The application presents an interactive menu system:

```
========================================
PERSONAL BUDGET TRACKER
========================================
1. Add Income
2. Add Expense
3. View Transactions
4. Delete Transaction
5. View Balance
6. Manage Categories
7. Search Transactions
8. Generate Reports
0. Exit
```

### Detailed Feature Descriptions

#### 1. Add Income
- Displays available categories
- Prompts for income amount in dollars
- Allows category selection by number
- Optional description field
- Validates numeric input
- Confirms successful addition

#### 2. Add Expense
- Similar to Add Income but for expenses
- Tracks money going out of the budget
- Same validation and confirmation process

#### 3. View Transactions
- Lists all transactions in chronological order
- Shows transaction ID, type, amount, category, date, and description
- Formatted display with clear separators
- Handles empty transaction list gracefully

#### 4. Delete Transaction
- Shows current transactions for reference
- Prompts for transaction ID to delete
- Validates transaction existence
- Confirms successful deletion

#### 5. View Balance
- Calculates real-time balance
- Shows current financial status
- Formula: Total Income - Total Expenses

#### 6. Manage Categories
Submenu with options:
- **View Categories**: Lists all available categories
- **Add Category**: Creates new custom categories
- **Delete Category**: Removes unused categories
- Input validation and error handling

#### 7. Search Transactions
Two search options:
- **Search by Category**: Filter transactions by specific category
- **Search by Date**: Find transactions from specific date (YYYY-MM-DD format)
- Results displayed in same format as View Transactions

#### 8. Generate Reports
Two report types:
- **Weekly Report**: Last 7 days financial summary
- **Monthly Report**: Last 30 days financial summary

Each report includes:
- Date range covered
- Total income and expenses
- Net amount (income - expenses)
- Category breakdown with income/expense totals

## Default Categories

The application automatically creates these categories on first run:
- **Food**: Restaurant meals, groceries, snacks
- **Rent**: Housing payments, utilities
- **Transport**: Gas, public transit, car maintenance
- **Entertainment**: Movies, games, subscriptions
- **Utilities**: Electricity, water, internet
- **Other**: Miscellaneous transactions

## Data Persistence

### Database Storage
- All data stored in SQLite database file (`budget.db`)
- Automatic table creation on first application run
- ACID compliance ensures data integrity
- No data loss between application sessions

### Session Management
- Proper SQLAlchemy session handling
- Automatic session cleanup after operations
- Prevention of detached instance errors
- Thread-safe database operations

## Error Handling

### Input Validation
- Numeric validation for amounts and IDs
- Date format validation (YYYY-MM-DD)
- Empty input handling
- Category existence verification

### Database Error Handling
- Graceful handling of database connection issues
- Duplicate category name prevention
- Foreign key constraint enforcement
- Transaction rollback on errors

### User Experience
- Clear error messages for invalid input
- Confirmation messages for successful operations
- Helpful prompts and instructions
- Graceful handling of edge cases

## Sample Usage Scenarios

### Adding Your First Income
```
Enter choice: 1
Categories:
1. Food
2. Rent
3. Transport
4. Entertainment
5. Utilities
6. Other
Income amount: $2500
Category number: 6
Description (optional): Monthly salary
Income of $2500.00 added successfully!
```

### Recording an Expense
```
Enter choice: 2
Categories:
1. Food
2. Rent
3. Transport
4. Entertainment
5. Utilities
6. Other
Expense amount: $45.50
Category number: 1
Description (optional): Grocery shopping
Expense of $45.50 added successfully!
```

### Checking Your Balance
```
Enter choice: 5

Current Balance: $2454.50
```

### Generating a Weekly Report
```
Enter choice: 8

--- Generate Reports ---
1. Weekly Report
2. Monthly Report

Enter choice: 1

Weekly Report (2024-01-15 to 2024-01-22):
Total Income: $2500.00
Total Expenses: $245.50
Net: $2254.50

Category Breakdown:
Food: Income $0.00, Expenses $45.50
Other: Income $2500.00, Expenses $0.00
Rent: Income $0.00, Expenses $200.00
```

## Dependencies and Technologies

### Core Dependencies
- **SQLAlchemy**: Object-Relational Mapping (ORM) toolkit
  - Database abstraction layer
  - Query building and execution
  - Relationship management
  - Session handling

- **Alembic**: Database migration tool
  - Schema version control
  - Automatic migration generation
  - Database upgrade/downgrade capabilities
  - Migration history tracking

- **Faker**: Test data generation library
  - Random transaction generation
  - Realistic sample data creation
  - Development and testing support

### Python Standard Library
- **datetime**: Date and time handling
- **sys/os**: System and file operations
- **random**: Random data generation

## Development and Testing

### Code Organization
- **Separation of Concerns**: CLI, business logic, and data models separated
- **Single Responsibility**: Each function has one clear purpose
- **DRY Principle**: No code duplication
- **Error Handling**: Comprehensive exception management

### Testing with Sample Data
The seed script creates realistic test data:
- Multiple transaction categories
- Random income and expense amounts
- Varied transaction dates
- Descriptive transaction details
- Balanced financial scenarios

### Database Schema Evolution
Alembic migrations allow for:
- Adding new columns to existing tables
- Creating new tables for additional features
- Modifying existing column constraints
- Maintaining data integrity during changes

## Future Enhancement Possibilities

### Potential Features
- Budget limits and alerts
- Recurring transaction support
- Data export to CSV/Excel
- Graphical reporting
- Multi-currency support
- Bank account integration
- Mobile companion app

### Technical Improvements
- PostgreSQL database option
- REST API development
- Web interface creation
- Docker containerization
- Automated testing suite
- Performance optimization

This Personal Budget Tracker CLI provides a solid foundation for personal financial management with room for future enhancements and customizations based on user needs.