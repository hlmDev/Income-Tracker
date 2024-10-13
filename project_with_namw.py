import json ##########*****
import tkinter as tk
from tkinter import messagebox


class Transaction:
    def __init__(self, name, date, category, amount):
        self.name = name
        self.date = date
        self.category = category
        self.amount = amount

    def __repr__(self):
        return f"Transaction(name={self.name}, date={self.date}, category={self.category}, amount={self.amount})"

    def to_dict(self):
        return {
            "name": self.name,
            "date": self.date,
            "category": self.category,
            "amount": self.amount
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data["name"], data["date"], data["category"], data["amount"])

class TransactionManager:
    def __init__(self):
        self.transactions = []

    def add_transaction(self, transaction):
        self.transactions.append(transaction)

    def save_transactions_to_json(self, filename):
        filepath = "C:/Users/96659/OneDrive/Desktop/" + filename  # Adjust the file path here
        with open(filepath, "w") as file:
            json.dump([transaction.to_dict() for transaction in self.transactions], file, indent=4)

    def load_transactions_from_json(self, filename):
        with open(filename, "r") as file:
            data = json.load(file)
            self.transactions = [Transaction.from_dict(item) for item in data]

    def view_transactions_sorted_by_date(self):
        return sorted(self.transactions, key=lambda x: x.date)

    def update_transaction(self, index, new_amount):
        if 0 <= index < len(self.transactions):
            self.transactions[index].amount = new_amount
            return True
        return False

    def delete_transaction(self, index):
        if 0 <= index < len(self.transactions):
            del self.transactions[index]
            return True
        return False

    def calculate_spending_by_category(self):
        spending_by_category = {}
        for transaction in self.transactions:
            if transaction.category in spending_by_category:
                spending_by_category[transaction.category] += transaction.amount
            else:
                spending_by_category[transaction.category] = transaction.amount
        return spending_by_category

    '''def find_name(self):
        f_name={}
        for transaction in self.transactions:
            if transaction.name in f_name:
                f_name[transaction.name].append(transaction)#check
            else:
                f_name[transaction.name]=[transaction]
        return f_name'''

    def find_name(self):
        name_category_transactions = {}

        for transaction in self.transactions:
            name = transaction.name
            category = transaction.category

            if name not in name_category_transactions:
                name_category_transactions[name] = {}

            if category not in name_category_transactions[name]:
                name_category_transactions[name][category] = []

            name_category_transactions[name][category].append(transaction)

        return name_category_transactions


    def transactions_by_category(self):
        transactions_by_category = {}
        for transaction in self.transactions:
            if transaction.category in transactions_by_category:
                transactions_by_category[transaction.category].append(transaction)
            else:
                transactions_by_category[transaction.category] = [transaction]
        return transactions_by_category

    def calculate_average_transaction_by_category(self):
        transactions_by_category = self.transactions_by_category()
        average_by_category = {}
        for category, transactions in transactions_by_category.items():
            total_amount = sum(transaction.amount for transaction in transactions)
            average_amount = total_amount / len(transactions)
            average_by_category[category] = average_amount
        return average_by_category

class TransactionApp:
    def __init__(self, master):
        self.master = master
        self.transaction_manager = TransactionManager()

        self.create_widgets()
        self.load_transactions()

    def create_widgets(self):
        self.master.title("Transaction Manager")

        self.income_label = tk.Label(self.master, text="Enter Income:")
        self.income_label.pack()
        self.income_entry = tk.Entry(self.master)
        self.income_entry.pack()

        self.expenses_label = tk.Label(self.master, text="Enter Expenses:")
        self.expenses_label.pack()
        self.expenses_entry = tk.Entry(self.master)
        self.expenses_entry.pack()

        # Button to calculate savings
        self.calculate_savings_button = tk.Button(self.master, text="Calculate Savings", command=self.calculate_savings)
        self.calculate_savings_button.pack()

        self.add_button = tk.Button(self.master, text="Add Transaction", command=self.add_transaction,width=20, height=2)
        self.add_button.pack()

        self.view_button = tk.Button(self.master, text="View Transactions", command=self.view_transactions,width=20, height=2)
        self.view_button.pack()

        self.update_button = tk.Button(self.master, text="Update Transaction", command=self.update_transaction,width=20, height=2)
        self.update_button.pack()

        self.delete_button = tk.Button(self.master, text="Delete Transaction", command=self.delete_transaction,width=20, height=2)
        self.delete_button.pack()

        self.reports_button = tk.Button(self.master, text="Generate Reports", command=self.generate_basic_reports,width=20, height=2)
        self.reports_button.pack()

        self.transactions_listbox = tk.Listbox(self.master,width=80)
        self.transactions_listbox.pack()

    def calculate_savings(self):
        try:
            income = float(self.income_entry.get())
            expenses = float(self.expenses_entry.get())
            savings = income - expenses
            messagebox.showinfo("Savings", f"Your saving is: {savings} SR")
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numeric values for income and expenses.")

    def add_transaction(self):
        # Create a new window for adding transaction
        add_window = tk.Toplevel(self.master)
        add_window.title("Add Transaction")

        # Create entry fields for name, date, category, and amount
        tk.Label(add_window, text="Name:").grid(row=0, column=0)
        name_entry = tk.Entry(add_window)
        name_entry.grid(row=0, column=1)

        tk.Label(add_window, text="Date (YYYY-MM-DD):").grid(row=1, column=0)
        date_entry = tk.Entry(add_window)
        date_entry.grid(row=1, column=1)

        tk.Label(add_window, text="Category:").grid(row=2, column=0)
        category_entry = tk.Entry(add_window)
        category_entry.grid(row=2, column=1)

        tk.Label(add_window, text="Amount:").grid(row=3, column=0)
        amount_entry = tk.Entry(add_window)
        amount_entry.grid(row=3, column=1)


        def add():
            name = name_entry.get()
            date = date_entry.get()
            category = category_entry.get()
            amount = float(amount_entry.get())
            transaction = Transaction(name, date, category, amount)
            self.transaction_manager.add_transaction(transaction)
            self.save_transactions()
            messagebox.showinfo("Success", "Transaction added successfully.")
            add_window.destroy()
            self.view_transactions()  # Update the view after adding

        # Create button to add transaction
        add_button = tk.Button(add_window, text="Add", command=add)
        add_button.grid(row=4, columnspan=2)

    def view_transactions(self):
        sorted_transactions = self.transaction_manager.view_transactions_sorted_by_date()
        self.transactions_listbox.delete(0, tk.END)
        for transaction in sorted_transactions:
            self.transactions_listbox.insert(tk.END, transaction)

    def update_transaction(self):
        index = self.transactions_listbox.curselection()  # Get selected index
        if index:
            index = int(index[0])  # Convert to int
            new_amount = float(input("Enter new amount: "))
            if self.transaction_manager.update_transaction(index, new_amount):
                self.save_transactions()
                messagebox.showinfo("Success", "Transaction updated successfully.")
                self.view_transactions()  # Update the view after updating
            else:
                messagebox.showerror("Error", "Invalid index. Transaction not updated.")
        else:
            messagebox.showerror("Error", "Please select a transaction to update.")

    def delete_transaction(self):
        index = self.transactions_listbox.curselection()  # Get selected index
        if index:
            index = int(index[0])  # Convert to int
            if self.transaction_manager.delete_transaction(index):
                self.save_transactions()
                messagebox.showinfo("Success", "Transaction deleted successfully.")
                self.view_transactions()  # Update the view after deleting
            else:
                messagebox.showerror("Error", "Invalid index. Transaction not deleted.")
        else:
            messagebox.showerror("Error", "Please select a transaction to delete.")

    def generate_basic_reports(self):
        total_income = float(self.income_entry.get())
        total_expenses = float(self.expenses_entry.get())

        # Calculate savings
        savings = total_income - total_expenses

        spending_by_category = self.transaction_manager.calculate_spending_by_category()
        transactions_by_category = self.transaction_manager.transactions_by_category()
        average_by_category = self.transaction_manager.calculate_average_transaction_by_category()
        fin_name=self.transaction_manager.find_name()


        report_window = tk.Toplevel(self.master)
        report_window.title("Basic Reports")

        total_income_label = tk.Label(report_window, text=f"Total Income: {total_income}")
        total_income_label.pack()

        total_expenses_label = tk.Label(report_window, text=f"Total Expenses: {total_expenses}")
        total_expenses_label.pack()

        spending_label = tk.Label(report_window, text="Spending by Category:")
        spending_label.pack()
        for category, amount in spending_by_category.items():
            category_label = tk.Label(report_window, text=f"{category}: {amount}")
            category_label.pack()


        transactions_label = tk.Label(report_window, text="Transactions in Each Category:")
        transactions_label.pack()
        for category, transactions in transactions_by_category.items():
            category_label = tk.Label(report_window, text=f"{category}:")
            category_label.pack()
            for transaction in transactions:
                transaction_label = tk.Label(report_window, text=f"\t{transaction}")
                transaction_label.pack()

#here we work
        name_category_label = tk.Label(report_window, text="Transactions by Name and Category:")
        name_category_label.pack()
        for name, categories in fin_name.items():
            name_label = tk.Label(report_window, text=f"\n{name}:")
            name_label.pack()
            for category, transactions in categories.items():
                category_label = tk.Label(report_window, text=f"\t{category}:")
                category_label.pack()
                for transaction in transactions:
                    transaction_label = tk.Label(report_window, text=f"\t\t{transaction}")
                    transaction_label.pack()


        average_label = tk.Label(report_window, text="Average Transaction Value by Category:")
        average_label.pack()
        for category, average in average_by_category.items():
            average_category_label = tk.Label(report_window, text=f"{category}: {average}")
            average_category_label.pack()

    def load_transactions(self):
        try:
            self.transaction_manager.load_transactions_from_json(
                r"C:\Users\96659\OneDrive\Desktop\transactionsLNAME.json")
        except FileNotFoundError:
            messagebox.showwarning("Warning", "No transactions found.")

    def save_transactions(self):
        self.transaction_manager.save_transactions_to_json("transactionsLNAME.json")

def main():
    root = tk.Tk()
    app = TransactionApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
