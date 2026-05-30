# Expense Tracker Application

A simple desktop-based Expense Tracker Application built using Python, Tkinter, and SQLite. This application helps users manage daily expenses by allowing them to add, update, delete, and view expense records with date tracking and total expense calculation.

## Features

- Add new expenses
- Update existing expenses
- Delete expenses by ID
- View all recorded expenses
- Automatic total expense calculation
- Date validation (YYYY-MM-DD format)
- SQLite database integration
- User-friendly Tkinter GUI

## Technologies Used

- Python 3
- Tkinter
- SQLite3
- Datetime Module

## Project Structure

```
Expense_Tracker_Application/
│
├── expense.py          # Main application source code
├── EXPENSES.db         # SQLite database file
├── README.md           # Project documentation
```

## Installation

### Clone the Repository

```bash
git clone https://github.com/karthik-dl/Expense_Tracker_Application.git
cd Expense_Tracker_Application
```

### Run the Application

```bash
python expense.py
```

## Database Schema

The application creates the following table automatically:

```sql
CREATE TABLE expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    description TEXT NOT NULL,
    category TEXT NOT NULL,
    amount REAL NOT NULL,
    date TEXT NOT NULL
);
```

## Application Modules

### Add Expense
- Enter Description
- Enter Category
- Enter Amount
- Enter Date
- Save expense into SQLite database

### View Expenses
- Display all expense records
- Refresh list anytime

### Update Expense
- Modify existing expense details using Expense ID

### Delete Expense
- Remove expense records using Expense ID

### Total Expense Calculation
- Automatically calculates total expenses stored in the database

## Screenshots

You can add screenshots here after uploading them.

```
screenshots/
├── home.png
├── add_expense.png
├── update_expense.png
```

## Future Enhancements

- Expense filtering by category
- Monthly expense reports
- Data export to Excel/CSV
- Expense charts and visualizations
- Search functionality
- User authentication

## Author

**Karthik D L**

GitHub: https://github.com/karthik-dl

## License

This project is open-source and available under the MIT License.